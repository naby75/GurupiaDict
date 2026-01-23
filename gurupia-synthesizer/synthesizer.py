#!/usr/bin/env python3
"""
GurupiaDict Synthesizer v0.1.0
Converts JSONL output from Gurupia-Parser into a searchable SQLite knowledge graph.

Features:
- Extracts [[WikiLink]] patterns to build node relationships
- Creates bidirectional edge table for backlink support
- Converts wiki markup to HTML with dict:// internal links
- Builds FTS5 full-text search index
"""

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


class WikiLink:
    """Represents a wiki link extracted from text"""
    
    def __init__(self, target: str, display: str = None):
        self.target = target.strip()
        self.display = display.strip() if display else self.target
    
    def __repr__(self):
        return f"WikiLink({self.target!r}, {self.display!r})"


class GurupiaSynthesizer:
    """Main synthesizer class for building the knowledge graph"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn: sqlite3.Connection = None
        self.cursor: sqlite3.Cursor = None
        
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
    
    def connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
    def create_schema(self):
        """Create database schema with FTS5 search support"""
        print("📐 Creating database schema...")
        
        # Main nodes table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Nodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                raw_content TEXT NOT NULL,
                html_content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Edges table for knowledge graph (bidirectional)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Edges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER NOT NULL,
                target_title TEXT NOT NULL,
                edge_type TEXT DEFAULT 'reference',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_id) REFERENCES Nodes(id) ON DELETE CASCADE
            )
        """)
        
        # FTS5 virtual table for full-text search
        self.cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS NodesFTS USING fts5(
                title, 
                content,
                content='Nodes',
                content_rowid='id',
                tokenize='unicode61'
            )
        """)
        
        # Triggers to keep FTS in sync
        self.cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS nodes_ai AFTER INSERT ON Nodes BEGIN
                INSERT INTO NodesFTS(rowid, title, content)
                VALUES (new.id, new.title, new.raw_content);
            END
        """)
        
        self.cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS nodes_ad AFTER DELETE ON Nodes BEGIN
                DELETE FROM NodesFTS WHERE rowid = old.id;
            END
        """)
        
        self.cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS nodes_au AFTER UPDATE ON Nodes BEGIN
                UPDATE NodesFTS SET title = new.title, content = new.raw_content
                WHERE rowid = new.id;
            END
        """)
        
        # Indexes for performance
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_nodes_title ON Nodes(title)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_edges_source ON Edges(source_id)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_edges_target ON Edges(target_title)
        """)
        
        self.conn.commit()
        print("✅ Schema created successfully")
    
    def extract_wiki_links(self, text: str) -> List[WikiLink]:
        """
        Extract [[WikiLink]] and [[Target|Display]] patterns from text
        
        Examples:
            [[컴퓨터]] -> WikiLink("컴퓨터")
            [[CPU|중앙처리장치]] -> WikiLink("CPU", "중앙처리장치")
        """
        # Pattern: [[target]] or [[target|display]]
        pattern = r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'
        
        links = []
        for match in re.finditer(pattern, text):
            target = match.group(1)
            display = match.group(2)
            
            # Skip File/Image links (should be already cleaned by Rust parser)
            if target.startswith(('File:', 'Image:', '파일:', '그림:')):
                continue
            
            # Normalize target (capitalize first letter)
            target = target.strip()
            if target:
                target = target[0].upper() + target[1:]
                links.append(WikiLink(target, display))
        
        return links
    
    def convert_to_html(self, text: str, title: str) -> str:
        """
        Convert wiki markup to HTML with dict:// protocol links
        
        - [[Link]] -> <a href="dict://Link">Link</a>
        - [[Target|Display]] -> <a href="dict://Target">Display</a>
        - '''Bold''' -> <strong>Bold</strong>
        - ''Italic'' -> <em>Italic</em>
        """
        html = text
        
        # Convert [[Target|Display]] first (before simple [[Target]])
        def replace_piped_link(match):
            target = match.group(1).strip()
            display = match.group(2).strip()
            target = target[0].upper() + target[1:] if target else target
            return f'<a href="dict://{target}" class="dict-link">{display}</a>'
        
        html = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', replace_piped_link, html)
        
        # Convert [[Target]]
        def replace_simple_link(match):
            target = match.group(1).strip()
            target = target[0].upper() + target[1:] if target else target
            return f'<a href="dict://{target}" class="dict-link">{target}</a>'
        
        html = re.sub(r'\[\[([^\]]+)\]\]', replace_simple_link, html)
        
        # Bold: '''text''' -> <strong>text</strong>
        html = re.sub(r"'''([^']+)'''", r'<strong>\1</strong>', html)
        
        # Italic: ''text'' -> <em>text</em>
        html = re.sub(r"''([^']+)''", r'<em>\1</em>', html)
        
        # Convert newlines to <br> and paragraphs
        html = html.replace('\r\n', '\n').replace('\r', '\n')
        paragraphs = html.split('\n\n')
        html = '<p>' + '</p>\n<p>'.join(p.replace('\n', '<br>') for p in paragraphs if p.strip()) + '</p>'
        
        return html
    
    def process_jsonl(self, jsonl_path: str) -> Tuple[int, int]:
        """
        Process JSONL file and insert nodes into database
        
        Returns: (nodes_count, edges_count)
        """
        print(f"📖 Reading JSONL from: {jsonl_path}")
        
        nodes_count = 0
        edges_count = 0
        
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    data = json.loads(line)
                    title = data['title']
                    raw_content = data['content']
                    
                    # Convert to HTML
                    html_content = self.convert_to_html(raw_content, title)
                    
                    # Extract links for edge creation
                    links = self.extract_wiki_links(raw_content)
                    
                    # Insert node
                    try:
                        self.cursor.execute(
                            "INSERT INTO Nodes (title, raw_content, html_content) VALUES (?, ?, ?)",
                            (title, raw_content, html_content)
                        )
                        node_id = self.cursor.lastrowid
                        nodes_count += 1
                        
                        # Insert edges
                        for link in links:
                            self.cursor.execute(
                                "INSERT INTO Edges (source_id, target_title) VALUES (?, ?)",
                                (node_id, link.target)
                            )
                            edges_count += 1
                        
                        if nodes_count % 100 == 0:
                            print(f"\r📊 Processed: {nodes_count} nodes, {edges_count} edges", end='', flush=True)
                    
                    except sqlite3.IntegrityError as e:
                        print(f"\n⚠️  Duplicate title at line {line_num}: {title}")
                        continue
                
                except json.JSONDecodeError as e:
                    print(f"\n❌ JSON error at line {line_num}: {e}")
                    continue
        
        self.conn.commit()
        print(f"\n✅ Imported {nodes_count} nodes and {edges_count} edges")
        
        return nodes_count, edges_count
    
    def get_backlinks(self, title: str, limit: int = 10) -> List[str]:
        """
        Get articles that reference this title (backlinks)
        
        This is the "expert option" mentioned in the design doc!
        """
        self.cursor.execute("""
            SELECT DISTINCT n.title
            FROM Edges e
            JOIN Nodes n ON e.source_id = n.id
            WHERE e.target_title = ?
            ORDER BY n.title
            LIMIT ?
        """, (title, limit))
        
        return [row['title'] for row in self.cursor.fetchall()]
    
    def search_titles(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Prefix search on titles using FTS5
        """
        self.cursor.execute("""
            SELECT n.id, n.title, snippet(NodesFTS, 1, '<mark>', '</mark>', '...', 30) as snippet
            FROM NodesFTS
            JOIN Nodes n ON NodesFTS.rowid = n.id
            WHERE NodesFTS MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (f"{query}*", limit))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        stats = {}
        
        # Total nodes
        self.cursor.execute("SELECT COUNT(*) as count FROM Nodes")
        stats['total_nodes'] = self.cursor.fetchone()['count']
        
        # Total edges
        self.cursor.execute("SELECT COUNT(*) as count FROM Edges")
        stats['total_edges'] = self.cursor.fetchone()['count']
        
        # Most referenced articles
        self.cursor.execute("""
            SELECT target_title, COUNT(*) as ref_count
            FROM Edges
            GROUP BY target_title
            ORDER BY ref_count DESC
            LIMIT 10
        """)
        stats['most_referenced'] = [dict(row) for row in self.cursor.fetchall()]
        
        return stats


def main():
    parser = argparse.ArgumentParser(
        description='GurupiaDict Synthesizer - Build knowledge graph from parsed Wikipedia data'
    )
    parser.add_argument('input', help='Input JSONL file from gurupia-parser')
    parser.add_argument('output', help='Output SQLite database path')
    parser.add_argument('--reset', action='store_true', help='Reset database (delete if exists)')
    parser.add_argument('--stats', action='store_true', help='Show statistics after import')
    
    args = parser.parse_args()
    
    # Check input file
    if not Path(args.input).exists():
        print(f"❌ Input file not found: {args.input}")
        sys.exit(1)
    
    # Handle reset
    if args.reset and Path(args.output).exists():
        print(f"🗑️  Deleting existing database: {args.output}")
        Path(args.output).unlink()
    
    # Process
    print("🐍 GurupiaDict Synthesizer v0.1.0")
    print(f"📥 Input:  {args.input}")
    print(f"💾 Output: {args.output}")
    print()
    
    with GurupiaSynthesizer(args.output) as synth:
        synth.create_schema()
        nodes_count, edges_count = synth.process_jsonl(args.input)
        
        if args.stats:
            print("\n📊 Database Statistics:")
            stats = synth.get_statistics()
            print(f"   Total Nodes: {stats['total_nodes']}")
            print(f"   Total Edges: {stats['total_edges']}")
            print(f"\n🔗 Most Referenced Articles:")
            for item in stats['most_referenced']:
                print(f"   {item['target_title']:30s} ({item['ref_count']} references)")
    
    print("\n✅ Synthesis completed successfully!")
    print(f"🎯 Knowledge graph ready at: {args.output}")


if __name__ == '__main__':
    main()
