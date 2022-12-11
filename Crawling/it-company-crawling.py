
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.webdriver.common.by import By
from time import sleep
from tqdm import tqdm
from selenium.webdriver.common.keys import Keys

driver_path = "./chromedriver"   # chromedriver 위치
url = "https://www.catch.co.kr/Member/Login?ReturnURL=%2FComp%2FCompMajor"   # 크롤링할 주소

browser = webdriver.Chrome(executable_path=driver_path)
browser.get(url)

# 로그인
browser.find_element(By.XPATH, '//*[@id="id_login"]').send_keys('ID')
browser.find_element(By.XPATH, '//*[@id="pw_login"]').send_keys('Password')
browser.find_element(By.XPATH, '//*[@id="wrapper"]/div/div[2]/div/p[1]').click()
sleep(0.5)

def go_main():
  while True:
    browser.get('https://www.catch.co.kr/Comp/CompMajor')
    try:
      # 필터 선택
      browser.find_element(By.XPATH, '//*[@id="Contents"]/div[3]/div[1]/div[1]/button').click()
      sleep(0.5)   # 로드 될  때까지  기다림
      browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div[1]/div[3]/div[1]/div[1]/ul/li[5]/button').click()
      sleep(0.5)
      browser.find_element(By.XPATH, '//*[@id="Contents"]/div[3]/div[1]/div[1]/ul/li[5]/div/span[6]/label').click()
      sleep(0.5)
      break
    except:
      # 팝업 제거
      browser.find_element(By.XPATH, '//*[@id="layerInterest4"]/div/button[2]').click()

go_main()

now = 1
company_list = []
name = []
address = []
salary = []
welfare = []

for i in tqdm(range(28)):
  cnt = 0
  page = browser.page_source
  soup = bs(page, "html.parser")
  links = soup.find_all('div', class_ = 'pic')

  for link in links:
    if cnt < 6:
      cnt += 1
      continue
    each_more_link = "https://www.catch.co.kr" + link.a['href']
    browser.get(each_more_link)
    info_page = browser.page_source
    info_soup = bs(info_page, "html.parser")

    # 사명
    n = info_soup.find('div', {'class': 'name'})
    name.append(n.h2.get_text().lstrip())

    # 주소
    address.append(info_soup.find('p', {'class': 'address'}).get_text())

    # 연봉
    s = info_soup.find_all('span', {'class': 'font17'})
    try:
      salary.append(s[1].get_text())
    except:
      salary.append('')
    
    # 복지
    ws = info_soup.find_all('a', {'class': 'bt'})
    temp = []
    for w in ws:
      temp.append(w.get_text())
    welfare.append(temp)

  go_main()
  for k in range(now):
    try:
      browser.find_element(By.XPATH, '//*[@id="Contents"]/p/a[12]').send_keys(Keys.ENTER)  # 페이지 넘기기
    except:
      continue
  now += 1

com_df = pd.DataFrame({'name': name, 'address': address, 'salary': salary, 'welfare': welfare})
print(com_df)
save_frame = './platform-company-data.csv'
com_df.to_csv(save_frame, encoding='utf-8-sig')    # save the DataFrame to csv file
