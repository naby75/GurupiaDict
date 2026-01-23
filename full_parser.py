#!/usr/bin/env python3
"""
GurupiaDict Full Parser (Python)
Complete Wikipedia XML parser - stores FULL articles
"""

import sys
import json
import re
from pathlib import Path
from lxml import etree

def clean_wiki_markup(text):
    """Remove wiki markup noise while preserving structure"""
    # Remove File/Image references
    text = re.sub(r'\[\[(?:File|파일|Image|그림):[^\]]*\]\]', '', text)
    
    # Remove <ref>...</ref> tags
    text = re.sub(r'<ref[^>]*>.*?</ref>', '', text, flags=re.DOTALL)
    
    # Remove HTML comments
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove infoboxes (but keep other templates for now)
    text = re.sub(r'\{\{정보상자[^}]*\}\}', '', text, flags=re.DOTALL)
    
    # Clean up multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Clean up multiple spaces
    text = re.sub(r' {2,}', ' ', text)
    
    return text.strip()

def parse_wikipedia_xml(input_path, output_path):
    """Parse Wikipedia XML dump - FULL CONTENT"""
    print(f"🐍 GurupiaDict Full Parser (Python)")
    print(f"📖 Reading: {input_path}")
    print(f"📝 Writing: {output_path}")
    print(f"💾 Mode: FULL CONTENT (complete articles)")
    print()
    
    # XML namespace
    ns = {'mw': 'http://www.mediawiki.org/xml/export-0.11/'}
    
    page_count = 0
    processed_count = 0
    
    with open(output_path, 'w', encoding='utf-8') as out_file:
        # Use iterparse for memory efficiency
        context = etree.iterparse(input_path, events=('end',), tag='{http://www.mediawiki.org/xml/export-0.11/}page')
        
        for event, page in context:
            page_count += 1
            
            try:
                # Extract title
                title_elem = page.find('mw:title', ns)
                if title_elem is None or not title_elem.text:
                    page.clear()
                    continue
                
                title = title_elem.text.strip()
                
                # Extract namespace
                ns_elem = page.find('mw:ns', ns)
                if ns_elem is None or ns_elem.text != '0':
                    page.clear()
                    continue
                
                # Extract text
                text_elem = page.find('.//mw:text', ns)
                if text_elem is None or not text_elem.text:
                    page.clear()
                    continue
                
                text = text_elem.text
                
                # Skip redirects
                if text.strip().startswith(('#REDIRECT', '#redirect')):
                    page.clear()
                    continue
                
                # Skip disambiguation pages
                if '(동음이의)' in title or '{{동음이의}}' in text:
                    page.clear()
                    continue
                
                # Clean wiki markup (but keep FULL content!)
                cleaned = clean_wiki_markup(text)
                
                # Minimum length check (at least 100 chars)
                if len(cleaned) < 100:
                    page.clear()
                    continue
                
                # Write to JSONL - FULL CONTENT!
                node = {
                    'title': title,
                    'content': cleaned  # Complete article!
                }
                
                out_file.write(json.dumps(node, ensure_ascii=False) + '\n')
                processed_count += 1
                
                if processed_count % 1000 == 0:
                    print(f"\r📊 Processed: {processed_count:,} articles (Total pages: {page_count:,})", end='', flush=True)
                
            except Exception as e:
                print(f"\n⚠️  Error processing page {page_count}: {e}")
            
            # Clear element to free memory
            page.clear()
            while page.getprevious() is not None:
                del page.getparent()[0]
    
    print(f"\n📈 Final Stats:")
    print(f"   Total pages scanned: {page_count:,}")
    print(f"   Full articles extracted: {processed_count:,}")
    print(f"\n✅ Parsing completed successfully!")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python full_parser.py <input.xml> <output.jsonl>")
        print("\nExample:")
        print("  python full_parser.py kowiki-latest-pages-articles.xml kowiki_complete.jsonl")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not Path(input_path).exists():
        print(f"❌ Input file not found: {input_path}")
        sys.exit(1)
    
    parse_wikipedia_xml(input_path, output_path)
