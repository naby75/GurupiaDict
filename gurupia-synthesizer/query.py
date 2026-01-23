#!/usr/bin/env python3
"""
GurupiaDict Query Tool - Interactive knowledge graph explorer

Features:
- Search articles by title (FTS5 prefix search)
- View article content with HTML formatting
- Show backlinks (articles that reference this article)
- Browse the knowledge graph interactively
"""

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import Dict, List, Optional


class GurupiaQuery:
    """Query interface for GurupiaDict knowledge graph"""
    
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
        if not Path(self.db_path).exists():
            raise FileNotFoundError(f"Database not found: {self.db_path}")
        
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    
    def search_titles(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Prefix search on titles using FTS5
        
        Example:
            search_titles("컴퓨") -> ["컴퓨터", "컴퓨터 과학", ...]
        """
        self.cursor.execute("""
            SELECT n.id, n.title
            FROM NodesFTS
            JOIN Nodes n ON NodesFTS.rowid = n.id
            WHERE NodesFTS.title MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (f"{query}*", limit))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_article(self, title: str) -> Optional[Dict]:
        """Get article by exact title match"""
        self.cursor.execute("""
            SELECT id, title, raw_content, html_content, created_at
            FROM Nodes
            WHERE title = ?
        """, (title,))
        
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_outgoing_links(self, title: str) -> List[str]:
        """Get articles that THIS article references"""
        self.cursor.execute("""
            SELECT DISTINCT e.target_title
            FROM Nodes n
            JOIN Edges e ON n.id = e.source_id
            WHERE n.title = ?
            ORDER BY e.target_title
        """, (title,))
        
        return [row['target_title'] for row in self.cursor.fetchall()]
    
    def get_backlinks(self, title: str, limit: int = 50) -> List[str]:
        """
        Get articles that reference THIS article (backlinks)
        
        This is the core "expert option" feature!
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
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        stats = {}
        
        # Total nodes
        self.cursor.execute("SELECT COUNT(*) as count FROM Nodes")
        stats['total_nodes'] = self.cursor.fetchone()['count']
        
        # Total edges
        self.cursor.execute("SELECT COUNT(*) as count FROM Edges")
        stats['total_edges'] = self.cursor.fetchone()['count']
        
        # Most referenced articles (top 10)
        self.cursor.execute("""
            SELECT target_title, COUNT(*) as ref_count
            FROM Edges
            GROUP BY target_title
            ORDER BY ref_count DESC
            LIMIT 10
        """)
        stats['most_referenced'] = [dict(row) for row in self.cursor.fetchall()]
        
        # Articles with most outgoing links
        self.cursor.execute("""
            SELECT n.title, COUNT(*) as link_count
            FROM Nodes n
            JOIN Edges e ON n.id = e.source_id
            GROUP BY n.id
            ORDER BY link_count DESC
            LIMIT 10
        """)
        stats['most_links'] = [dict(row) for row in self.cursor.fetchall()]
        
        return stats
    
    def full_text_search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search both title and content"""
        self.cursor.execute("""
            SELECT 
                n.id, 
                n.title,
                snippet(NodesFTS, 1, '<mark>', '</mark>', '...', 50) as snippet
            FROM NodesFTS
            JOIN Nodes n ON NodesFTS.rowid = n.id
            WHERE NodesFTS MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (query, limit))
        
        return [dict(row) for row in self.cursor.fetchall()]


def print_article(article: Dict, query_tool: GurupiaQuery):
    """Pretty print an article with metadata"""
    print("\n" + "="*80)
    print(f"📖 {article['title']}")
    print("="*80)
    
    # HTML content
    print("\n【 Content 】")
    print(article['html_content'])
    
    # Outgoing links
    outgoing = query_tool.get_outgoing_links(article['title'])
    if outgoing:
        print(f"\n【 References ({len(outgoing)}) 】")
        for link in outgoing[:10]:
            print(f"  → {link}")
        if len(outgoing) > 10:
            print(f"  ... and {len(outgoing) - 10} more")
    
    # Backlinks
    backlinks = query_tool.get_backlinks(article['title'])
    if backlinks:
        print(f"\n【 Referenced By ({len(backlinks)}) 】")
        for link in backlinks[:10]:
            print(f"  ← {link}")
        if len(backlinks) > 10:
            print(f"  ... and {len(backlinks) - 10} more")
    
    print("\n" + "="*80)


def interactive_mode(query_tool: GurupiaQuery):
    """Interactive REPL for exploring the knowledge graph"""
    print("\n🔍 GurupiaDict Interactive Mode")
    print("Commands:")
    print("  search <query>  - Search for articles")
    print("  view <title>    - View article details")
    print("  stats           - Show database statistics")
    print("  quit/exit       - Exit")
    print()
    
    while True:
        try:
            cmd = input("gurupia> ").strip()
            
            if not cmd:
                continue
            
            if cmd in ('quit', 'exit', 'q'):
                break
            
            parts = cmd.split(maxsplit=1)
            command = parts[0].lower()
            
            if command == 'search' and len(parts) == 2:
                query = parts[1]
                results = query_tool.search_titles(query)
                
                if results:
                    print(f"\n🔎 Found {len(results)} results:")
                    for i, result in enumerate(results, 1):
                        print(f"  {i}. {result['title']}")
                else:
                    print("❌ No results found")
            
            elif command == 'view' and len(parts) == 2:
                title = parts[1]
                article = query_tool.get_article(title)
                
                if article:
                    print_article(article, query_tool)
                else:
                    print(f"❌ Article not found: {title}")
                    # Try searching
                    results = query_tool.search_titles(title)
                    if results:
                        print(f"\n💡 Did you mean:")
                        for i, result in enumerate(results[:5], 1):
                            print(f"  {i}. {result['title']}")
            
            elif command == 'stats':
                stats = query_tool.get_statistics()
                print(f"\n📊 Database Statistics:")
                print(f"   Total Articles: {stats['total_nodes']}")
                print(f"   Total Links: {stats['total_edges']}")
                
                print(f"\n🔗 Most Referenced Articles:")
                for item in stats['most_referenced']:
                    print(f"   {item['target_title']:30s} ({item['ref_count']} refs)")
                
                print(f"\n📝 Articles with Most Links:")
                for item in stats['most_links']:
                    print(f"   {item['title']:30s} ({item['link_count']} links)")
            
            else:
                print("❌ Unknown command. Available: search, view, stats, quit")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='GurupiaDict Query Tool - Explore your knowledge graph'
    )
    parser.add_argument('database', help='Path to GurupiaDict SQLite database')
    parser.add_argument('--search', '-s', help='Search for articles')
    parser.add_argument('--view', '-v', help='View specific article')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    try:
        with GurupiaQuery(args.database) as query_tool:
            if args.stats:
                stats = query_tool.get_statistics()
                print(f"📊 Database Statistics:")
                print(f"   Total Articles: {stats['total_nodes']}")
                print(f"   Total Links: {stats['total_edges']}")
                
                print(f"\n🔗 Most Referenced Articles:")
                for item in stats['most_referenced']:
                    print(f"   {item['target_title']:30s} ({item['ref_count']} references)")
            
            elif args.search:
                results = query_tool.search_titles(args.search)
                print(f"🔎 Search results for '{args.search}':")
                for i, result in enumerate(results, 1):
                    print(f"  {i}. {result['title']}")
            
            elif args.view:
                article = query_tool.get_article(args.view)
                if article:
                    print_article(article, query_tool)
                else:
                    print(f"❌ Article not found: {args.view}")
            
            elif args.interactive:
                interactive_mode(query_tool)
            
            else:
                # Default to interactive if no specific command
                interactive_mode(query_tool)
    
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
