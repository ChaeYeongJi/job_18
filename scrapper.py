import requests
from bs4 import BeautifulSoup

keyword = '파이썬'
url = f'https://search.incruit.com/list/search.asp?col=job&kw={keyword}&startno=0'
response = requests.get(url)
# print(response.status_code)
# print(response.text)

soup = BeautifulSoup(response.text, 'html.parser')

lis = soup.find_all('li', class_='c_col')

for li in lis:
    company = li.find('a', class_='cpname').text
    title = li.find('div', class_='cell_mid').find('div', class_='cl_top').find('a').text
    location = li.find('div', class_='cl_md').find_all('span')[0].text
    link = li.find('div', class_='cell_mid').find('div', class_='cl_top').find('a').get('href')