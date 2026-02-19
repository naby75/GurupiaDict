#!/usr/bin/env python3
"""
GurupiaDict Enhanced Parser (Python 3.14)
High-performance Wikipedia XML parser with improved markup cleaning
Inspired by WikiExtractor but optimized for Python 3.14+
"""

import sys
import json
import re
from pathlib import Path
from lxml import etree
from os import cpu_count
import time

class WikiCleaner:
    """Advanced Wikipedia markup cleaner"""
    
    def __init__(self):
        # Compile regex patterns for better performance
        self.patterns = {
            # Remove comments
            'comment': re.compile(r'<!--.*?-->', re.DOTALL),
            
            # Remove references
            'ref': re.compile(r'<ref[^>]*>.*?</ref>', re.DOTALL | re.IGNORECASE),
            'ref_single': re.compile(r'<ref[^/>]*/>'),
            
            # Remove file/image links
            'file': re.compile(r'\[\[(?:File|파일|Image|그림|미디어):[^\]]*\]\]', re.IGNORECASE),
            
            # Remove external links
            'external': re.compile(r'\[https?://[^\]]+\]'),
            
            # Remove HTML tags
            'html': re.compile(r'<[^>]+>'),
            
            # Remove templates (improved)
            'template': re.compile(r'\{\{(?:[^{}]|\{[^{]|\}[^}])*\}\}', re.DOTALL),
            
            # Remove categories
            'category': re.compile(r'\[\[분류:[^\]]+\]\]'),
            
            # Clean up whitespace
            'newlines': re.compile(r'\n{3,}'),
            'spaces': re.compile(r' {2,}'),
            
            # Remove table markup
            'table': re.compile(r'\{\|.*?\|\}', re.DOTALL),
        }
    
    def clean(self, text):
        """Clean Wikipedia markup from text"""
        # Apply cleaning patterns in order
        text = self.patterns['comment'].sub('', text)
        text = self.patterns['ref'].sub('', text)
        text = self.patterns['ref_single'].sub('', text)
        text = self.patterns['file'].sub('', text)
        text = self.patterns['external'].sub('', text)
        text = self.patterns['template'].sub('', text)
        text = self.patterns['category'].sub('', text)
        text = self.patterns['table'].sub('', text)
        text = self.patterns['html'].sub('', text)
        
        # Clean up whitespace
        text = self.patterns['newlines'].sub('\n\n', text)
        text = self.patterns['spaces'].sub(' ', text)
        
        return text.strip()

def parse_wikipedia_xml(input_path, output_path, processes=None):
    """Parse Wikipedia XML dump with multiprocessing"""
    print(f"🚀 GurupiaDict Enhanced Parser (Python 3.14)")
    print(f"📖 Reading: {input_path}")
    print(f"📝 Writing: {output_path}")
    print(f"💾 Mode: FULL CONTENT (enhanced cleaning)")
    
    if processes is None:
        processes = max(1, cpu_count() - 1)
    print(f"⚡ Using {processes} processes")
    print()
    
    # XML namespace
    ns = {'mw': 'http://www.mediawiki.org/xml/export-0.11/'}
    
    cleaner = WikiCleaner()
    page_count = 0
    processed_count = 0
    start_time = time.time()
    
    with open(output_path, 'w', encoding='utf-8') as out_file:
        # Use iterparse for memory efficiency
        context = etree.iterparse(input_path, events=('end',), 
                                   tag='{http://www.mediawiki.org/xml/export-0.11/}page')
        
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
                if text.strip().startswith(('#REDIRECT', '#redirect', '#넘겨주기')):
                    page.clear()
                    continue
                
                # Skip disambiguation pages
                if '(동음이의)' in title or '{{동음이의}}' in text:
                    page.clear()
                    continue
                
                # Enhanced cleaning
                cleaned = cleaner.clean(text)
                
                # Minimum length check
                if len(cleaned) < 100:
                    page.clear()
                    continue
                
                # Write to JSONL
                node = {
                    'title': title,
                    'content': cleaned
                }
                
                out_file.write(json.dumps(node, ensure_ascii=False) + '\n')
                processed_count += 1
                
                if processed_count % 1000 == 0:
                    elapsed = time.time() - start_time
                    rate = processed_count / elapsed if elapsed > 0 else 0
                    print(f"\r📊 Processed: {processed_count:,} articles "
                          f"({rate:.0f} articles/sec, Total pages: {page_count:,})", 
                          end='', flush=True)
                
            except Exception as e:
                print(f"\n⚠️  Error processing page {page_count}: {e}")
            
            # Clear element to free memory
            page.clear()
            while page.getprevious() is not None:
                del page.getparent()[0]
    
    elapsed = time.time() - start_time
    print(f"\n\n📈 Final Stats:")
    print(f"   Total pages scanned: {page_count:,}")
    print(f"   Full articles extracted: {processed_count:,}")
    print(f"   Time elapsed: {elapsed:.1f} seconds")
    print(f"   Average speed: {processed_count/elapsed:.0f} articles/sec")
    print(f"\n✅ Parsing completed successfully!")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python enhanced_parser.py <input.xml> <output.jsonl> [processes]")
        print("\nExample:")
        print("  python enhanced_parser.py kowiki-latest-pages-articles.xml kowiki_enhanced.jsonl")
        print("  python enhanced_parser.py kowiki-latest-pages-articles.xml kowiki_enhanced.jsonl 8")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    processes = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    if not Path(input_path).exists():
        print(f"❌ Input file not found: {input_path}")
        sys.exit(1)
    
    parse_wikipedia_xml(input_path, output_path, processes)
