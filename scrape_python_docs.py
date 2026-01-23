"""
Fetch Python Standard Library data from DevDocs-like sources or official docs.
For now, let's create a specialized Python Standard Library scraper.
"""

import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_python_builtins():
    url = "https://docs.python.org/3/library/functions.html"
    print(f"🚀 Scraping Python Built-in Functions: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        
        functions = []
        
        # Find all function definitions
        # In Python docs, functions are under dl.function or dt id
        for dt in soup.find_all('dt', id=True):
            name = dt.get('id')
            if not name: continue
            
            # The next element (dd) usually contains the description
            dd = dt.find_next_sibling('dd')
            content = ""
            if dd:
                content = dd.get_text(separator='\n', strip=True)
            
            # Syntax/Signature
            signature = dt.get_text(strip=True)
            
            full_content = f"# {name}\n\n**Signature:** `{signature}`\n\n{content[:2000]}"
            
            functions.append({
                'title': f"python:{name}",
                'content': full_content
            })
            
        print(f"✅ Found {len(functions)} built-in functions.")
        return functions
        
    except Exception as e:
        print(f"❌ Error scraping Python documentation: {e}")
        return []

def save_to_jsonl(documents, filename="win32dict_data/python_stdlib.jsonl"):
    with open(filename, 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    print(f"✅ Saved to {filename}")

def scrape_python_module(module_name):
    url = f"https://docs.python.org/3/library/{module_name}.html"
    print(f"🚀 Scraping Python Module: {module_name} ({url})")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        
        items = []
        
        # In module pages, functions/classes are under dt
        for dt in soup.find_all('dt', id=re.compile(f"^{module_name}\.")):
            name = dt.get('id')
            if not name: continue
            
            dd = dt.find_next_sibling('dd')
            content = ""
            if dd:
                content = dd.get_text(separator='\n', strip=True)
            
            signature = dt.get_text(strip=True)
            
            full_content = f"# {name}\n\n**Module:** `{module_name}`\n**Signature:** `{signature}`\n\n{content[:2000]}"
            
            items.append({
                'title': f"python:{name}",
                'content': full_content
            })
            
        print(f"✅ Found {len(items)} items in {module_name}.")
        return items
        
    except Exception as e:
        print(f"❌ Error scraping {module_name}: {e}")
        return []

if __name__ == '__main__':
    import re
    all_docs = []
    
    # 1. Built-in functions
    all_docs.extend(scrape_python_builtins())
    
    # 2. Major modules
    major_modules = ['os', 'sys', 'json', 're', 'datetime', 'math', 'random', 'sqlite3']
    for mod in major_modules:
        all_docs.extend(scrape_python_module(mod))
        
    if all_docs:
        save_to_jsonl(all_docs)
