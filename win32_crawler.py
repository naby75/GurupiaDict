"""
Win32Dict Crawler
Crawl Microsoft Learn Win32 API documentation for offline reference
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

class Win32Crawler:
    def __init__(self, output_dir="win32dict_data"):
        self.base_url = "https://learn.microsoft.com"
        self.win32_root = "/en-us/windows/win32/"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.visited = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_all_headers(self):
        """Get list of all Win32 header files from sidebar"""
        print("📚 Getting list of all headers...")
        
        url = self.base_url + self.win32_root + "api/"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            
            headers = []
            seen_urls = set()
            
            # Find all links in the page
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # Look for header file links
                # Pattern: /en-us/windows/win32/api/HEADERNAME/
                if '/windows/win32/api/' in href:
                    # Extract header name from URL
                    parts = [p for p in href.split('/') if p]
                    
                    # Find 'api' in parts
                    try:
                        api_index = parts.index('api')
                        if api_index + 1 < len(parts):
                            header_name = parts[api_index + 1]
                            
                            # Skip if it's a function page (contains nf-, ns-, etc.)
                            if any(x in header_name for x in ['nf-', 'ns-', 'ne-', 'nn-', 'nc-']):
                                continue
                            
                            # Build full URL
                            full_url = urljoin(self.base_url, href)
                            
                            # Ensure URL ends with /
                            if not full_url.endswith('/'):
                                full_url += '/'
                            
                            if full_url not in seen_urls:
                                seen_urls.add(full_url)
                                headers.append({
                                    'name': header_name,
                                    'url': full_url
                                })
                    except (ValueError, IndexError):
                        continue
            
            print(f"✅ Found {len(headers)} headers")
            return headers
            
        except Exception as e:
            print(f"❌ Error getting headers: {e}")
            return []
    
    def get_apis_from_header(self, header_url, header_name):
        """Get all API functions from a header page"""
        print(f"  📄 Crawling header: {header_name}")
        
        try:
            response = self.session.get(header_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            
            apis = []
            
            # Find all API links (functions start with nf-, structures with ns-)
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Look for function/structure links
                if '/nf-' in href or '/ns-' in href or '/ne-' in href or '/nn-' in href:
                    full_url = urljoin(self.base_url, href)
                    title = link.get_text(strip=True)
                    if title and full_url not in [a['url'] for a in apis]:
                        apis.append({
                            'url': full_url,
                            'title': title,
                            'header': header_name
                        })
            
            print(f"    ✅ Found {len(apis)} APIs in {header_name}")
            return apis
            
        except Exception as e:
            print(f"    ❌ Error: {e}")
            return []
    
    def crawl_api_page(self, url, title, header=None):
        """Crawl individual API documentation page"""
        if url in self.visited:
            return None
        
        self.visited.add(url)
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract main content
            main_content = soup.find('main') or soup.find('article')
            if not main_content:
                return None
            
            # Extract sections
            content_parts = []
            
            # Get syntax
            syntax_section = main_content.find('h2', string=re.compile('Syntax', re.I))
            if syntax_section:
                code = syntax_section.find_next('pre') or syntax_section.find_next('code')
                if code:
                    content_parts.append(f"## Syntax\n```cpp\n{code.get_text(strip=True)}\n```\n")
            
            # Get parameters
            params_section = main_content.find('h2', string=re.compile('Parameters', re.I))
            if params_section:
                params_text = []
                next_elem = params_section.find_next_sibling()
                while next_elem and next_elem.name != 'h2':
                    params_text.append(next_elem.get_text(strip=True))
                    next_elem = next_elem.find_next_sibling()
                if params_text:
                    content_parts.append(f"## Parameters\n{' '.join(params_text[:500])}\n")
            
            # Get return value
            return_section = main_content.find('h2', string=re.compile('Return', re.I))
            if return_section:
                return_text = return_section.find_next_sibling()
                if return_text:
                    content_parts.append(f"## Return Value\n{return_text.get_text(strip=True)[:500]}\n")
            
            # Combine all content
            full_content = '\n'.join(content_parts)
            
            if not full_content:
                # Fallback to main content
                full_content = main_content.get_text(separator='\n', strip=True)[:3000]
            
            # Create document
            doc = {
                'title': title,
                'url': url,
                'content': full_content,
                'header': header,
                'timestamp': time.strftime('%Y-%m-%d')
            }
            
            return doc
            
        except Exception as e:
            return None
    
    def save_to_jsonl(self, documents, filename="win32_api.jsonl"):
        """Save documents to JSONL format"""
        output_file = self.output_dir / filename
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for doc in documents:
                if doc:
                    # Convert to GurupiaDict format
                    node = {
                        'title': doc['title'],
                        'content': doc['content']
                    }
                    f.write(json.dumps(node, ensure_ascii=False) + '\n')
        
        print(f"\n✅ Saved {len(documents)} documents to {output_file}")
    
    def crawl_win32_api(self, max_headers=None, max_apis_per_header=None):
        """Main crawling function - improved version"""
        print(f"🚀 Win32Dict Crawler (Improved)")
        print(f"📍 Target: Microsoft Learn Win32 API")
        print()
        
        # Step 1: Get all headers
        headers = self.get_all_headers()
        
        if max_headers:
            headers = headers[:max_headers]
            print(f"📊 Limiting to {max_headers} headers")
        
        # Step 2: For each header, get APIs
        all_apis = []
        for i, header in enumerate(headers, 1):
            print(f"[{i}/{len(headers)}] ", end='')
            apis = self.get_apis_from_header(header['url'], header['name'])
            
            if max_apis_per_header:
                apis = apis[:max_apis_per_header]
            
            all_apis.extend(apis)
            time.sleep(1)  # Be polite
        
        print(f"\n✅ Total APIs found: {len(all_apis)}")
        print()
        
        # Step 3: Crawl each API page
        documents = []
        for i, api in enumerate(all_apis, 1):
            print(f"[{i}/{len(all_apis)}] {api['title'][:50]}")
            doc = self.crawl_api_page(api['url'], api['title'], api.get('header'))
            if doc:
                documents.append(doc)
            
            time.sleep(0.5)  # Be polite
        
        # Save results
        self.save_to_jsonl(documents)
        
        print(f"\n📈 Summary:")
        print(f"   Headers crawled: {len(headers)}")
        print(f"   APIs found: {len(all_apis)}")
        print(f"   Documents saved: {len(documents)}")
        print(f"   Output: {self.output_dir}")
        print(f"\n✅ Crawling completed!")
        
        return documents

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Crawl Microsoft Win32 API documentation')
    parser.add_argument('--max-headers', type=int, default=5, help='Maximum headers to crawl (default: 5)')
    parser.add_argument('--max-apis', type=int, help='Maximum APIs per header (optional)')
    parser.add_argument('--output', default='win32dict_data', help='Output directory')
    
    args = parser.parse_args()
    
    crawler = Win32Crawler(output_dir=args.output)
    crawler.crawl_win32_api(max_headers=args.max_headers, max_apis_per_header=args.max_apis)

if __name__ == '__main__':
    main()
