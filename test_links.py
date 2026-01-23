import requests
from bs4 import BeautifulSoup

url = "https://learn.microsoft.com/en-us/windows/win32/api/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')

print("All links containing '/api/':")
count = 0
for link in soup.find_all('a', href=True):
    href = link['href']
    if '/api/' in href:
        print(f"  {href}")
        count += 1
        if count >= 20:
            break

print(f"\nTotal links with '/api/': {count}")
