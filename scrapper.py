import requests
from bs4 import BeautifulSoup

# 인크루트
def search_incruit(keyword, page=1):
    jobs = []

    startno = (page - 1) * 30

    url = f'https://search.incruit.com/list/search.asp?col=job&kw={keyword}&startno={startno}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    lis = soup.find_all('li', class_='c_col')

    for li in lis:
        company = li.find('a', class_='cpname').text
        title = li.find('div', class_='cell_mid').find('div', class_='cl_top').find('a').text
        location = li.find('div', class_='cl_md').find_all('span')[0].text
        link = li.find('div', class_='cell_mid').find('div', class_='cl_top').find('a').get('href')

        job_data = {
            'company': company,
            'title': title,
            'location': location,
            'link': link,
        }
        jobs.append(job_data)
    return jobs

# 잡코리아
def search_jobkorea(keyword, page=1):
    jobs = []

    url = f'https://www.jobkorea.co.kr/Search/?stext={keyword}&tabType=recruit&Page_No={page}'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.select('[data-sentry-component="CardJob"]')

    for card in cards:
        title_tag = None

        for a in card.select('a[href*="/Recruit/GI_Read/"]'):
            if a.get_text(strip=True):
                title_tag = a
                break

        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        link = title_tag.get('href')

        company = ''

        for a in card.find_all('a'):
            text = a.get_text(strip=True)

            if text and text != title and '로고' not in text:
                company = text
                break

        location = ''

        for item in card.select('[data-sentry-component="GrayChip"]'):
            if item.select_one('.emoji--basicemoji-place2'):
                location = item.get_text(strip=True)
                break

        jobs.append({
            'company': company,
            'title': title,
            'location': location,
            'link': link
        })
    return jobs


# 사람인
def search_saramin(keyword, page=1):
    jobs = []

    url = f'https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=search&searchword={keyword}&recruitPage={page}'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.select('.item_recruit')

    for item in items:
        title_tag = item.select_one('.job_tit a')
        title = title_tag.get_text(strip=True)

        link = title_tag.get('href')

        if link.startswith('/'):
            link = 'https://www.saramin.co.kr' + link

        company_tag = item.select_one('.corp_name a')
        company = company_tag.get_text(strip=True)

        location_tag = item.select_one('.job_condition > span')
        location = location_tag.get_text(' ', strip=True)

        jobs.append({
            'company': company,
            'title': title,
            'location': location,
            'link': link,
        })
    return jobs
