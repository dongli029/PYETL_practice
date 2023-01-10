import requests  # 用get or post來爬取資料
from bs4 import BeautifulSoup
import pandas as pd
url = 'https://www.104.com.tw/jobs/search/?keyword=Python&order=1&jobsource=2018indexpoc&ro=0'

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'

headers = {'User-Agent': useragent}

# 列出想查詢的關鍵字
my_params = {'role': '1',  # 限定全職的工作，如果不限定則輸入0
             'keyword': 'python',  # 想要查詢的關鍵字
             'isnew': '30'}  # 只要最近一個月有更新的過的

res = requests.get(url, my_params,  headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')

# print(soup)

job_list = soup.findAll('article', {'class': 'b-block--top-bord'})  # job_list = soup.find_all('article', {'class': 'b-block--top-bord'})也可
job_num = len(job_list)-1
print('共抓到' + str(job_num) + ' 筆資料')

JobList = pd.DataFrame()
for i in range(job_num):
    job_name = job_list[i].find('a', {'class': 'js-job-link'}).text # 工作職稱
    work_content = job_list[i].find('p', {'class': "job-list-item__info b-clearfix b-content"}).text # 工作內容
    company_name = job_list[i].find('ul', {'class': 'b-list-inline b-clearfix'}).a.text     # 公司名
    company_division = list(job_list[i].find('ul', {'class': 'b-list-inline b-clearfix'}).findAll('li'))[-1].text  # 公司行業別
    work_place = job_list[i].find('ul', {'class': "b-list-inline b-clearfix job-list-intro b-content"}).find('li').text # 公司位置
    Salary = list(job_list[i].find('div', {'class': 'job-list-tag b-content'}))[1].text   # 薪水
    # print(company_name, company_division, job_name, work_content, work_place, Salary, sep="\n", end="\n------------------\n")

    df = pd.DataFrame(
        data=[{
            '公司名稱': company_name,
            '工作職稱': job_name,
            '工作內容': work_content,
            '工作待遇': Salary,
            '公司行業別': company_division,
            '公司位置': work_place
            }],
        columns=['公司名稱', '工作職稱', '工作內容', '工作待遇', '公司行業別', '公司位置'
                 ])
    JobList = JobList.append(df, ignore_index=True)

JobList.to_excel(r'your url\JobList_use_request.xlsx')