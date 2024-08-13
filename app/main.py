import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By # 특정요소찾기
from io import StringIO
import os
browser = webdriver.Chrome()

# 1. 페이지 이동
url = 'https://finance.naver.com/sise/sise_market_sum.naver?page='
browser.get(url)

# 2. 조회 항목 초기화 (체크되어있는 항목 체크 해제)
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected(): # 체크박스가 체크된 상태라면
        checkbox.click() # 클릭(체크해제)

# 3. 조회 항목 설정
items_to_select = ['영업이익','자산총계','매출액'] # 항목 설정
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH,'..') # 부모element 찾음
    label = parent.find_element(By.TAG_NAME,'label')
    if label.text in items_to_select:
        checkbox.click()

# 4. 적용하기 클릭
btn_apply = browser.find_element(By.XPATH,'//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()

# 5. 데이터 추출 및 파일 저장
for idx in range(1, 100):  # 최대 99페이지만
    # 페이지이동
    # https://finance.naver.com/sise/sise_market_sum.naver?page=
    browser.get(url + str(idx))

    # 데이터 추출
    # StringIO는 문자열 데이터를 파일처럼 다룰 수 있게 해주는 객체로 html문자열을 안전하게 전달할 수 있다.
    df = pd.read_html(StringIO(browser.page_source))[1]
    # print(df)
    # df.dropna
    # axis = 'index'  row 기준 삭제, columns 행 기준 삭제
    # how ='all' 줄 전체에 데이터가 없을경우 how = 'any' 줄에 하나라도 데이터가 없을경우
    # inplace = True df에 반영 기본값 False
    df.dropna(axis='index', how='all', inplace=True)
    df.dropna(axis='columns', how='all', inplace=True)
    if len(df) == 0:  # 더이상 가져올 데이터가 없다면
        break

    # 파일 저장
    f_name = 'sise.csv'
    if os.path.exists(f_name):  # 파일이 있다면 헤더 제외
        # 데이터프레임을 csv로 변환
        # mode ='a' -> 파일이 존재하면 데이터 append
        # header=False 헤더 제외
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else:
        df.to_csv(f_name, encoding='utf-8-sig', index=False)

browser.quit()  # 브라우저 종료