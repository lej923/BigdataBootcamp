

import requests    #get() / post()
from bs4 import BeautifulSoup
import pandas as pd

url = "https://news.daum.net"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
print(url)

def get_news_list():
    
    """
    
    daum 뉴스 목록 조회
    조회 결과는 pandas의 Dataframe(표)로 만들어서 반환 처리
    
    """
    #요청
    response = requests.get(url,headers={"User-Agent": user_agent})
     
    #상태코드가 200인지 확인
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        tag_list = soup.select("ul.list_newsissue > li strong > a")
        print(len(tag_list))
        link_list =[]
        title_list = []
    
        for tag in tag_list:
            link_list.append(tag.get("href"))
            title_list.append(tag.get_text().strip())
            
        return pd.DataFrame({
                "title" : title_list,
                "link" : link_list     #link 리스트를 column으로 가져온다
            })
    
    else:
        print("문제 발생 :", response.status_code)


def get_news(url):
        #news 상세기사 url을 받아서 뉴스내용을 반환
        #연결
    response = requests.get(url, headers={"User-Agent" : user_agent})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        p_list = soup.select( "div.article_view p")
            
        article = []   #리스트에 문단 (p)의 text들을 저장.
        for p in p_list:
            article.append(p.get_text())
                #리스트안의 문단들을 합쳐서 하나의 문자열로 만들기.
        return "\n\n".join(article)  #구분자문자열.join(리스트)
        
                
if __name__ == "__main__":
    #뉴스목록 저장
    from datetime import datetime
    import os
    d = datetime.now().strftime("%Y-%m-%d")    #strftime() : 날짜시간을 원하는 형태의 문자열로 변환
    file_path = f"daum_news_list_{d}.csv"
    print(file_path)
    result = get_news_list()
    ##csv 파일로 저장
    result.to_csv(file_path, index = False) #utf-8 형식으로 저장
    
    #개별 뉴스들의 가사를 저장
    #result: DataFrame(표)에서 링크 조회
    links = result["link"]  #표["컬럼이름"] => 컬러의 값들(행)을 반환
    result_news =[ get_news(link) for link in links]
    print(len(result_news))
    #    print(result_news)
    # print(result_news[0])
    #날짜 이름으로 news/ 디렉토리를 생성
    save_path = f"news/{d}"
    os.makedirs(save_path, exist_ok= True)  #상위 디렉토리까지 생성
    titles= result["title"]   #뉴스제목
    import re
    for title, news in zip(titles, result_news):
        title = re.sub('[^\w]', "", title)
        with open(f"{save_path}/{title}.txt", "wt") as fw:
        fw.write(news)
    
    print("완료")

