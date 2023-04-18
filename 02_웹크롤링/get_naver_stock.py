import requests  
from bs4 import BeautifulSoup
import pandas as pd
import os

def main():
    base_url = "https://finance.naver.com/sise/sise_market_sum.naver?&page={}"
    #페이지 이동 필요 41페이지
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"            
    
    #요청
    result_list = []  # 전체 결과를 담을 리스트
    for page in range(1,42):
        url = base_url.format(page)
        response = requests.get(url, headers={"User-Agent" : user_agent})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
        
        # print(len(tr_list))
        ##주의 : 전일비 : 화살표 이미지 값 
        #       화살표가 올라가는 화살표 인경우 🔺 -상승- alt속성의 값이 상승
        #       화살표가 내려가는 화살표인 경우 🔻 -하락- alt속성의 값이 하락
        #       변경이 없을 경우 image 가 없음
        #       ⬆️ ⬇️ 는 상한가 하한가로 alt속성이 없음 -> image명을 구분
            tr_list = soup.select("table.type_2 > tbody> tr")
            for tr in tr_list:
                td_list = tr.find_all("td")   
                if len(td_list) == 1 : #선울 그리는 용으로 사용된 tr (blank)
                    continue
                td_content_list = [] #한 행의 조회결과를 담을 (td들의 값) 리스트
                for idx, td in enumerate(td_list):  #위에 변수명에 인덱스 붙여줌
                    txt = td.text.strip()
                    if idx == 3: #전일비<td>
                        img_tag= td.find("img")
                        if img_tag != None : #앞에 이미지(상승, 하락)가 있는 경우
                            alt_attr = img_tag.get("alt")
                            if alt_attr == None: #<img>에 alt속성이 없는 경우 -> 상한가/하한가 이미지
                            #<img>의 src 속성값들을 조회
                                alt_attr = "상한" if img_tag.get("src").endswith("ico_up02.jpg") else "하한"
                            txt = alt_attr + txt
                    elif idx ==12:
                        continue
                    td_content_list.append(txt)    #한 행을 구성하는 컬럼값을 저장
                result_list.append(td_content_list)    #한 행을 저장
        else:
            print(f"{page}실패")
            continue
    return result_list
 
###한 페이지 끝 

if __name__ == "__main__":
    
    import time
    start = time.time()
    result = main()
    print(len(result))
    end = time.time()
    print("걸린시간 : end -start")

    save_path = "stocks"
    os. makedirs(save_path)
    file_name = datetime.now().strftime("%Y_%m_%d_코스피 종목별 시세 정보.csv")

    df = pd.DataFrame(result)
    df.to_csv(f"{save_path}/{file_name}")