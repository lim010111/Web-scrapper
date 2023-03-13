from bs4 import BeautifulSoup
from selenium import webdriver

def get_page_count(what):
    base_url = "https://www.jobkorea.co.kr/Search/?stext="

    final_url = f"{base_url}{what}"
    
    browser = webdriver.Chrome()
    browser.get(final_url)
    
    soup = BeautifulSoup(browser.page_source, "html.parser")
    
    job_count_string = soup.select_one('p strong').string
    
    job_count_list = []
    for string in job_count_string:
        if string.isdigit():
            job_count_list.append(string)
    job_count = int("".join(job_count_list))
    
    if job_count % 20 == 0:
        pages = job_count // 20
    else:
        pages = (job_count // 20) + 1
        
    return pages


def extract_jobkorea_jobs(what):
    base_url = "https://www.jobkorea.co.kr/Search/?stext="
    pages = get_page_count(what)
    print("Found", pages, "pages..")
    
    results = []
    
    for page in range(pages):
        final_url = f"{base_url}{what}&Page_No={page+1}"

        browser = webdriver.Chrome()
        browser.get(final_url)

        soup = BeautifulSoup(browser.page_source, "html.parser")

        jobs = soup.find('div', class_="list-default").select('ul li')

        for job in jobs:
            anchor = job.find('div').find('div', class_="post-list-corp").find('a') # link, company 추출
            title = job.find('div').find('div', class_="post-list-info").find('a')
            info = job.find('div').find('div', class_="post-list-info").find('p', class_="option")
            exp = info.find('span', class_="exp")
            edu = info.find('span', class_="edu")
            location = info.find('span', class_="loc long")
            
            job_data = {
                'link': "https://www.jobkorea.co.kr/"+anchor["href"],
                'company': anchor["title"],
                'title': title["title"].replace(",", " "),
                'exp': exp.string,
                'edu': edu.string,
                'location': location.string
            }             
            results.append(job_data)
            
    return results