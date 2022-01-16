import requests
url = ''
strhtml = requests.get(url)
print(strhtml.text)