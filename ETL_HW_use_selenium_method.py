import time, requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'

headers = {'User-Agent': useragent}

# 列出想查詢的關鍵字
my_params = {'role': '1',  # 限定全職的工作，如果不限定則輸入0
             'keyword': 'python',  # 想要查詢的關鍵字
             'isnew': '30'}  # 只要最近一個月有更新的過的
url = requests.get('https://www.104.com.tw/jobs/search/?', my_params, headers=headers).url
driver = webdriver.Chrome(r'C:\Users\Tibame_T14\Desktop\Tibame\PyETL\pyetl_HW\chromedriver.exe')
driver.get(url)

# 滑動到下方時，會自動加載新資料，透過程式送出Java語法幫我們執行「滑到下方」的動作
for i in range(15):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(0.6)

# 自動加載15次，超過之後必須要點選「手動載入」的按鈕才能繼續載入新資料（可能是防止爬蟲）
k = 1
while k != 0:
    try:
        # 手動載入新資料之後會出現新的more page，舊的就無法再使用，所以要使用最後一個物件
        driver.find_elements_by_class_name("js-more-page")[-1].click()
        # driver.find_element_by_xpath("//*[contains(text(),'手動載入')]").click()
        print('Click 手動載入，' + '載入第' + str(15 + k) + '頁')
        k = k + 1
        time.sleep(1)  # 時間設定太短的話，來不及載入新資料就會跳錯誤
    except:
        k = 0
        print('No more Job')

# 透過BeautifulSoup解析資料
soup = BeautifulSoup(driver.page_source, 'html.parser')

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
    # Salary = list(job_list[i].find('div', {'class': 'job-list-tag b-content'}))[1].text   # 薪水

    # print(company_name, company_division, job_name, work_content, work_place, Salary, sep="\n", end="\n------------------\n")

    df = pd.DataFrame(
        data=[{
            '公司名稱': company_name,
            '工作職稱': job_name,
            '工作內容': work_content,
            #'工作待遇': Salary,
            '公司行業別': company_division,
            '公司位置': work_place
            }],
        columns=['公司名稱', '工作職稱', '工作內容', '公司行業別', '公司位置'
                 ])
    JobList = JobList.append(df, ignore_index=True)

JobList.to_excel(r'your url\JobList_use_Selenium.xlsx')