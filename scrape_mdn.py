import requests
import json
import os
import time
from pathlib import Path

def fetch_mdn_article(path, category):
    """
    Fetch MDN article as JSON and convert to Gurupia format.
    Example path: 'Web/JavaScript/Reference/Global_Objects/Array'
    """
    url = f"https://developer.mozilla.org/en-US/docs/{path}/index.json"
    print(f"🚀 Fetching MDN ({category}): {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        doc = data['doc']
        title = doc['title']
        summary = doc['summary']
        
        # Construct content
        # We'll use the summary and potentially the first few sections
        content = f"# {title}\n\n{summary}\n\n"
        
        # Add a bit more detail from body sections if available
        if 'body' in doc:
            for section in doc['body'][:3]:  # Take first 3 sections for brevity
                if section.get('title'):
                    content += f"## {section['title']}\n"
                if section.get('value'):
                    # Basic cleanup of some MDN specific macros if any
                    text = section['value']
                    content += f"{text}\n\n"

        return {
            'title': f"{category}:{title}",
            'content': content
        }
    except Exception as e:
        print(f"❌ Error fetching {path}: {e}")
        return None

def main():
    targets = {
        'js': [
            'Web/JavaScript/Reference/Global_Objects/Array',
            'Web/JavaScript/Reference/Global_Objects/String',
            'Web/JavaScript/Reference/Global_Objects/Object',
            'Web/JavaScript/Reference/Global_Objects/Promise',
            'Web/JavaScript/Reference/Global_Objects/Function',
            'Web/JavaScript/Reference/Global_Objects/JSON',
            'Web/JavaScript/Reference/Global_Objects/Map',
            'Web/JavaScript/Reference/Global_Objects/Set',
            'Web/JavaScript/Reference/Global_Objects/Math',
            'Web/JavaScript/Reference/Global_Objects/Date',
        ],
        'html': [
            'Web/HTML/Element/div',
            'Web/HTML/Element/span',
            'Web/HTML/Element/a',
            'Web/HTML/Element/img',
            'Web/HTML/Element/button',
            'Web/HTML/Element/input',
            'Web/HTML/Element/form',
            'Web/HTML/Element/video',
            'Web/HTML/Element/canvas',
        ],
        'css': [
            'Web/CSS/CSS_Flexible_Box_Layout/Basic_Concepts_of_Flexbox',
            'Web/CSS/CSS_Grid_Layout/Basic_Concepts_of_Grid_Layout',
            'Web/CSS/box-model',
            'Web/CSS/color',
            'Web/CSS/background',
            'Web/CSS/font',
            'Web/CSS/position',
        ]
    }
    
    output_dir = Path("mdn_data")
    output_dir.mkdir(exist_ok=True)
    
    all_docs = []
    
    for category, paths in targets.items():
        for path in paths:
            doc = fetch_mdn_article(path, category)
            if doc:
                all_docs.append(doc)
            time.sleep(0.5)  # Respectful delay
            
    output_file = output_dir / "mdn_reference.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for doc in all_docs:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
            
    print(f"\n✅ Successfully collected {len(all_docs)} MDN articles.")
    print(f"📁 Data saved to: {output_file}")

if __name__ == "__main__":
    main()
