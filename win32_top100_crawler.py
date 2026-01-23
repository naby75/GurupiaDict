"""
Win32 Top 100 API Crawler
Crawl only the most frequently used Win32 APIs
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path

# Top 100 Win32 APIs
TOP_100_APIS = [
    # Window Management
    "CreateWindowEx", "DestroyWindow", "ShowWindow", "UpdateWindow",
    "SetWindowText", "GetWindowText", "MoveWindow", "SetWindowPos",
    "GetClientRect", "GetWindowRect",
    
    # Message Handling
    "GetMessage", "PeekMessage", "SendMessage", "PostMessage",
    "DispatchMessage", "TranslateMessage", "DefWindowProc",
    
    # GDI
    "BeginPaint", "EndPaint", "GetDC", "ReleaseDC",
    "TextOut", "DrawText", "Rectangle", "Ellipse", "LineTo", "BitBlt",
    
    # File I/O
    "CreateFile", "ReadFile", "WriteFile", "CloseHandle",
    "GetFileSize", "SetFilePointer", "DeleteFile", "CopyFile", "MoveFile",
    
    # Memory Management
    "VirtualAlloc", "VirtualFree", "HeapAlloc", "HeapFree",
    "GlobalAlloc", "GlobalFree",
    
    # Process/Thread
    "CreateProcess", "CreateThread", "ExitProcess", "ExitThread",
    "WaitForSingleObject", "Sleep", "GetCurrentProcess", "GetCurrentThread",
    
    # Registry
    "RegOpenKeyEx", "RegCloseKey", "RegQueryValueEx", "RegSetValueEx",
    "RegCreateKeyEx", "RegDeleteKey",
    
    # Common Controls
    "CreateStatusWindow", "CreateToolbarEx",
    "ListView_InsertItem", "TreeView_InsertItem",
    
    # Dialog
    "DialogBox", "CreateDialog", "EndDialog",
    "GetDlgItem", "SetDlgItemText",
    
    # System Info
    "GetSystemInfo", "GetVersionEx", "GetComputerName", "GetUserName",
    
    # Error Handling
    "GetLastError", "FormatMessage", "SetLastError",
    
    # Keyboard/Mouse
    "GetKeyState", "GetAsyncKeyState", "SetCursor",
    "GetCursorPos", "SetCursorPos",
    
    # Timer
    "SetTimer", "KillTimer", "GetTickCount",
    
    # String
    "lstrlen", "lstrcpy", "lstrcat", "lstrcmp",
    
    # Clipboard
    "OpenClipboard", "CloseClipboard",
    "SetClipboardData", "GetClipboardData",
]

def search_api_url(api_name):
    """Search for API documentation URL"""
    search_url = f"https://learn.microsoft.com/en-us/search/?terms={api_name}+function"
    
    try:
        response = requests.get(search_url, timeout=10)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Find first result link
        for link in soup.find_all('a', href=True):
            href = link['href']
            if api_name.lower() in href.lower() and '/windows/win32/' in href:
                if href.startswith('http'):
                    return href
                else:
                    return f"https://learn.microsoft.com{href}"
        
        # Fallback: construct URL
        return f"https://learn.microsoft.com/en-us/windows/win32/api/search?q={api_name}"
        
    except:
        return None

def crawl_api_page(url, api_name):
    """Crawl API documentation page"""
    try:
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.content, 'lxml')
        
        main_content = soup.find('main') or soup.find('article')
        if not main_content:
            return None
        
        # Extract content
        content_parts = [f"# {api_name}\n\n"]
        
        # Get syntax
        syntax = main_content.find('h2', string=lambda x: x and 'syntax' in x.lower())
        if syntax:
            code = syntax.find_next('pre') or syntax.find_next('code')
            if code:
                content_parts.append(f"## Syntax\n```cpp\n{code.get_text(strip=True)}\n```\n\n")
        
        # Get description
        desc = main_content.find('p')
        if desc:
            content_parts.append(f"## Description\n{desc.get_text(strip=True)}\n\n")
        
        # Get parameters
        params = main_content.find('h2', string=lambda x: x and 'parameter' in x.lower())
        if params:
            params_text = []
            elem = params.find_next_sibling()
            while elem and elem.name != 'h2' and len(params_text) < 10:
                params_text.append(elem.get_text(strip=True))
                elem = elem.find_next_sibling()
            if params_text:
                content_parts.append(f"## Parameters\n{' '.join(params_text)}\n\n")
        
        return {
            'title': api_name,
            'content': ''.join(content_parts)[:3000],
            'url': url
        }
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

def main():
    print("🚀 Win32 Top 100 API Crawler")
    print(f"📊 Total APIs: {len(TOP_100_APIS)}")
    print()
    
    output_dir = Path("win32dict_data")
    output_dir.mkdir(exist_ok=True)
    
    documents = []
    
    for i, api_name in enumerate(TOP_100_APIS, 1):
        print(f"[{i}/{len(TOP_100_APIS)}] {api_name}")
        
        # Search for URL
        url = search_api_url(api_name)
        if not url:
            print(f"  ⚠️  URL not found")
            continue
        
        # Crawl page
        doc = crawl_api_page(url, api_name)
        if doc:
            documents.append(doc)
            print(f"  ✅ Success")
        
        time.sleep(2)  # Be polite
    
    # Save to JSONL
    output_file = output_dir / "win32_top100.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for doc in documents:
            node = {
                'title': doc['title'],
                'content': doc['content']
            }
            f.write(json.dumps(node, ensure_ascii=False) + '\n')
    
    print(f"\n📈 Summary:")
    print(f"   APIs crawled: {len(documents)}/{len(TOP_100_APIS)}")
    print(f"   Output: {output_file}")
    print(f"\n✅ Completed!")
    print(f"\n📝 Next step:")
    print(f"   python gurupia-synthesizer\\synthesizer.py {output_file} Win32Dict.db --reset")

if __name__ == '__main__':
    main()
