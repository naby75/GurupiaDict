#!/usr/bin/env python3
"""
GurupiaDict Fast Parser (Python)
High-performance Wikipedia XML parser using lxml
"""

import sys
import json
import re
from pathlib import Path
from lxml import etree

def clean_wiki_markup(text):
    """Remove wiki markup noise"""
    # Remove File/Image references
    text = re.sub(r'\[\[(?:File|파일|Image|그림):[^\]]*\]\]', '', text)
    
    # Remove <ref>...</ref> tags
    text = re.sub(r'<ref[^>]*>.*?</ref>', '', text, flags=re.DOTALL)
    
    # Remove HTML comments
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove infoboxes and templates
    text = re.sub(r'\{\{[^}]*\}\}', '', text, flags=re.DOTALL)
    
    # Clean up multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Clean up multiple spaces
    text = re.sub(r' {2,}', ' ', text)
    
    return text.strip()

def extract_first_paragraph(text):
    """Extract first paragraph before section headers"""
    # Find content before first section header (==)
    parts = text.split('\n==')
    intro = parts[0]
    
    # Get meaningful paragraphs
    paragraphs = [p.strip() for p in intro.split('\n\n') 
                  if p.strip() and not p.strip().startswith(('{|', '|'))]
    
    return '\n\n'.join(paragraphs)

def smart_truncate(text, min_chars=500, max_chars=1500):
    """Smart truncation at sentence boundary"""
    if len(text) <= max_chars:
        return text
    
    # Find sentence ending between min and max
    search_range = text[min_chars:min(max_chars, len(text))]
    
    # Look for Korean or English sentence endings
    sentence_ends = ['. ', '.\n', '다.', '다!', '다?', '요.', '음.', '임.']
    
    for ending in sentence_ends:
        pos = search_range.rfind(ending)
        if pos != -1:
            cut_point = min_chars + pos + len(ending)
            return text[:cut_point].strip()
    
    # If no sentence boundary found, cut at max_chars
    return text[:max_chars].strip()

def parse_wikipedia_xml(input_path, output_path):
    """Parse Wikipedia XML dump"""
    print(f"🐍 GurupiaDict Fast Parser (Python)")
    print(f"📖 Reading: {input_path}")
    print(f"📝 Writing: {output_path}")
    print()
    
    # XML namespace - Updated to 0.11
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
                
                # Extract first paragraph
                first_para = extract_first_paragraph(text)
                
                if not first_para:
                    page.clear()
                    continue
                
                # Clean wiki markup
                cleaned = clean_wiki_markup(first_para)
                
                # Smart truncate
                truncated = smart_truncate(cleaned, 500, 1500)
                
                if len(truncated) < 100:
                    page.clear()
                    continue
                
                # Write to JSONL
                node = {
                    'title': title,
                    'content': truncated
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
    print(f"   Main namespace articles extracted: {processed_count:,}")
    print(f"\n✅ Parsing completed successfully!")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python fast_parser.py <input.xml> <output.jsonl>")
        print("\nExample:")
        print("  python fast_parser.py kowiki-latest-pages-articles.xml kowiki_full.jsonl")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not Path(input_path).exists():
        print(f"❌ Input file not found: {input_path}")
        sys.exit(1)
    
    parse_wikipedia_xml(input_path, output_path)
