import re

with open('filename.txt', 'r') as file:
    text = file.read()

url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

# найти все ссылки в тексте
urls = re.findall(url_pattern, text)

for url in urls:
    print(url)