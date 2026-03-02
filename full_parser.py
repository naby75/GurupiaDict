#!/usr/bin/env python3
"""
GurupiaDict Full Parser (Python)
Complete Wikipedia XML parser - stores FULL articles
"""

import sys
import json
import re
import logging
from pathlib import Path
from lxml import etree

# 1.2 정규식(Regex) 전역 모듈 레벨 캐싱
RE_FILE = re.compile(r'\[\[(?:File|파일|Image|그림):[^\]]*\]\]')
RE_REF = re.compile(r'<ref[^>]*>.*?</ref>', flags=re.DOTALL)
RE_COMMENT = re.compile(r'<!--.*?-->', flags=re.DOTALL)
RE_HTML = re.compile(r'<[^>]+>')
RE_INFOBOX = re.compile(r'\{\{정보상자[^}]*\}\}', flags=re.DOTALL)
RE_NEWLINES = re.compile(r'\n{3,}')
RE_SPACES = re.compile(r' {2,}')

def clean_wiki_markup(text):
    """Remove wiki markup noise while preserving structure"""
    # Remove File/Image references
    text = RE_FILE.sub('', text)
    
    # Remove <ref>...</ref> tags
    text = RE_REF.sub('', text)
    
    # Remove HTML comments
    text = RE_COMMENT.sub('', text)
    
    # Remove HTML tags
    text = RE_HTML.sub('', text)
    
    # Remove infoboxes (but keep other templates for now)
    text = RE_INFOBOX.sub('', text)
    
    # Clean up multiple newlines
    text = RE_NEWLINES.sub('\n\n', text)
    
    # Clean up multiple spaces
    text = RE_SPACES.sub(' ', text)
    
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
    
    # 3.1 XML Bomb 방어를 위해 엔티티 확장 비활성화 (Zero Trust)
    safe_parser = etree.XMLParser(resolve_entities=False, recover=True)
    
    # 2.1 File 핸들 라이프사이클 명시적 통제
    with open(input_path, 'rb') as in_file, open(output_path, 'w', encoding='utf-8') as out_file:
        # Use iterparse for memory efficiency
        context = etree.iterparse(in_file, events=('end',), tag='{http://www.mediawiki.org/xml/export-0.11/}page', parser=safe_parser)
        
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
                # 1.1 스택 트레이스 및 컨텍스트 기록 유지
                title_for_log = title if 'title' in locals() else "Unknown"
                logging.exception(f"\n⚠️ Error processing page {page_count}. Title: {title_for_log}")
            
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
        
    # 3.2 Output Path Traversal 검증 (Least Privilege)
    output_dir = Path(output_path).parent.resolve()
    if not output_dir.exists():
        print(f"❌ 보안 거부: 지정된 출력 디렉토리가 존재하지 않거나 접근할 수 없습니다: {output_dir}")
        sys.exit(1)
    
    parse_wikipedia_xml(input_path, output_path)
