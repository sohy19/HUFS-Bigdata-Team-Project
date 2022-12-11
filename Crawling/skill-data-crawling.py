from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

driver_path = "./chromedriver"   # chromedriver 위치
url = "https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=company.response_rate_order&years=-1&selected=873&selected=669&selected=872&locations=all"   # 크롤링할 주소

browser = webdriver.Chrome(executable_path=driver_path)
browser.get(url)

# 스크롤 내리기
for i in range(10):
  scroll_location = browser.execute_script("return document.body.scrollHeight")   #스크롤 내리기 이동 전 위치
  browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")   #현재 스크롤의 가장 아래로 내림
  time.sleep(2)   #전체 스크롤이 늘어날 때까지 대기
  scroll_height = browser.execute_script("return document.body.scrollHeight")   #늘어난 스크롤 높이
  scroll_location = browser.execute_script("return document.body.scrollHeight")   #늘어난 스크롤 높이

page = browser.page_source
soup = bs(page, "html.parser")
more_links = soup.find_all('div', class_ = 'Card_className__u5rsb')

skill = []
for more_link in more_links:
  each_more_link = "https://www.wanted.co.kr/wd/" + more_link.a['data-position-id']
  browser.get(each_more_link)
  info_page = browser.page_source
  info_soup = bs(info_page, "html.parser")

  # 기술 크롤링
  skills = info_soup.find_all('div', class_ = "SkillItem_SkillItem__E2WtM")
  for s in skills:
    skill.append(s.string)

skill_df = pd.DataFrame(skill, columns=['웹 개발자'])
# print(skill_df)
save_frame = './web-skill-data.csv'
skill_df.to_csv(save_frame, encoding='utf-8-sig')    # save the DataFrame to csv file
