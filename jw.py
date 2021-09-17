import os
from selenium import webdriver
import datetime
import pandas as pd
from selenium.webdriver.chrome.webdriver import WebDriver

def myexit():
    print("---------------------프로그램을 종료합니다.---------------------")
    exit()
    
def makedirs(path): 
    try: 
        os.makedirs(path) 
    except OSError: 
        if not os.path.isdir(path): 
            raise

def ln(num=100): #라인 그리기 프린트함수
    print('='*num)

def savefile(num, lst, file_name):
    
    file_ext = ["txt","csv","xlsx"] #파일 확장자
    
    dir_path = input("저장할 폴더를 지정해주세요 > ")
    if dir_path[-1]!= '\\': dir_path=dir_path+'\\'
    
    if not os.path.exists(dir_path): #디렉토리가 존재하지 않을경우
        makedirs(dir_path)
    
    current_time = datetime.datetime.now()
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    minute = current_time.minute
    filename = f"{year}-{month}-{day}-{hour}-{minute}-{file_name}.{file_ext[num-1]}"
    file_full_path = dir_path+filename
    
    if num == 1: #txt
        f = open(file_full_path, 'a', encoding='utf-8')
        for i in range(len(lst[0])):
                f.write("번호: "+str(lst[0][i])+'\n')
                f.write("제목: "+lst[1][i]+'\n')
                f.write("내용: "+lst[2][i]+'\n')
                f.write('\n')
        f.close()        
    else:   #txt가 아닐때
        result = pd.DataFrame()
        result['번호'] = lst[0]
        result['작성자'] = lst[1]
        result['날짜'] = lst[2]
        result['제목'] = lst[3]
        result['내용'] = lst[4]
        result = result.set_index("번호")
        if num == 2: #csv
            result.to_csv(file_full_path, encoding='utf-8-sig')
        else: #xlsx
            result.to_excel(file_full_path)
    ln()
    print(file_full_path+"로 저장하였습니다.")
    ln()
    
    
def view(query_txt): #네이버 검색에서 View 섹션 출력 함수
    no2 = []  #번호들을 담을 리스트
    writers = [] #작성자들을 담을 리스트
    dates = [] #날짜들을 담을 리스트
    titles = []  #제목들을 담을 리스트
    contents = [] #내용들을 담을 리스트
    
    d_path = 'C:\python_temp\chromedriver.exe'
    driver = webdriver.Chrome(d_path)
    driver.get("https://search.naver.com/search.naver?sm=tab_hty.top&where=blog&query="+query_txt)  #네이버 VIEW - 블로그 주소
    # driver.find_element_by_id("query").send_keys(query_txt+'\n')
    no = 1
    
    print(f'VIEW-블로그 섹션의 {query_txt}으로 수집된 데이터를 추출합니다.')
    elements = driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div/div[1]/section/html-persist/div/more-contents/div/ul/li')

    for element in elements:
        title = element.find_element_by_css_selector('div > div.total_area > a').text #블로그 제목
        content = element.find_element_by_css_selector('div > div > div.total_group > div > a > div').text  # 블로그 요약 내용
        writer = element.find_element_by_css_selector('div > div > div.total_info > div.total_sub > span > span > span.elss.etc_dsc_inner > a').text #작성자
        date = element.find_element_by_css_selector('div > div > div.total_info > div.total_sub > span > span > span.etc_dsc_area > span').text #날짜

        print(f'번호: {no}')
        no2.append(no)
        no+=1
        print("작성자: ",writer.strip())
        writers.append(writer)
        print("날짜:",date)
        dates.append(date)
        print("제목:",title)
        titles.append(title)
        print("내용:",content)
        contents.append(content)
        print('\n')
            
    result =[no2,writers,dates,titles,contents]
    
    issave = input('추출된 데이터를 파일로 저장하시겠습니까?(Y/N) > ')
    if issave.upper() == 'Y': #y,Y를 입력했을 경우
    #저장하기
        print("[메뉴] 1.txt 2.csv 3.xls (종료: 0)")
        select_num = int(input("메뉴를 선택해주세요 > "))    
    
        if not select_num in (1,2,3): #선택한게 1,2,3이 아니면
            myexit()
        else: 
            filename=query_txt+'-'+'view'
            savefile(select_num, result, filename) #파일 저장
    else: #파일 저장을 안할경우
        myexit()

