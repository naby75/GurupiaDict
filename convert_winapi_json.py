"""
Convert WinAPI Categories JSON to GurupiaDict JSONL format
"""

import json
from pathlib import Path

def convert_winapi_to_jsonl(input_file, output_file, max_apis=1000):
    """Convert WinAPI JSON to JSONL format"""
    
    print(f"🚀 WinAPI JSON to JSONL Converter")
    print(f"📖 Reading: {input_file}")
    
    # Load JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ Total APIs in file: {len(data)}")
    
    # Convert to JSONL
    documents = []
    for api_name, api_info in list(data.items())[:max_apis]:
        # Build content
        content_parts = [f"# {api_name}\n"]
        
        # Category
        if 'category' in api_info:
            content_parts.append(f"**Category:** {api_info['category']}\n")
        
        # DLL
        if 'dll' in api_info:
            content_parts.append(f"**DLL:** {api_info['dll']}\n")
        
        # Header
        if 'header' in api_info:
            content_parts.append(f"**Header:** {api_info['header']}\n")
        
        # Return type
        if 'ret' in api_info:
            content_parts.append(f"**Return Type:** {api_info['ret']}\n")
        
        # Arguments
        if 'args' in api_info and api_info['args']:
            content_parts.append(f"\n## Arguments ({api_info.get('nargs', 0)})\n")
            for i, arg in enumerate(api_info['args'][:10], 1):  # Max 10 args
                arg_type = arg.get('type', 'unknown')
                arg_name = arg.get('name', f'arg{i}')
                arg_desc = arg.get('description', '')
                arg_io = arg.get('in_out', '')
                
                content_parts.append(f"\n**{i}. {arg_name}** ({arg_type})")
                if arg_io:
                    content_parts.append(f" [{arg_io}]")
                if arg_desc:
                    content_parts.append(f"\n{arg_desc}")
                content_parts.append("\n")
        
        # Create document
        doc = {
            'title': api_name,
            'content': ''.join(content_parts)
        }
        documents.append(doc)
    
    # Save to JSONL
    output_path = Path(output_file)
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    
    print(f"✅ Converted {len(documents)} APIs")
    print(f"📝 Output: {output_path}")
    print(f"\n📊 Sample APIs:")
    for doc in documents[:5]:
        print(f"   - {doc['title']}")
    
    print(f"\n🎯 Next step:")
    print(f"   python gurupia-synthesizer\\synthesizer.py {output_path} Win32Dict.db --reset")

if __name__ == '__main__':
    import sys
    
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'winapi_categories.json'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'win32dict_data/win32_api.jsonl'
    max_apis = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    
    convert_winapi_to_jsonl(input_file, output_file, max_apis)
