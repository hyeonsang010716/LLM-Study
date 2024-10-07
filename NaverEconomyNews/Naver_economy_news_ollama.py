import requests
import bs4
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
import concurrent.futures
import pandas as pd
from tqdm import tqdm
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

def get_soup_from_url(url):
    """
    주어진 URL에서 HTML 페이지를 가져와 BeautifulSoup 객체로 반환하는 함수.
    페이지를 가져오는 데 실패하면 None을 반환.

    Args:
    - url (str): 가져올 웹 페이지의 URL

    Returns:
    - soup (BeautifulSoup): 성공 시 BeautifulSoup 객체, 실패 시 None
    """
    agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    response = requests.get(url, headers={'User-agent': agent})

    if response.status_code != 200:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return None
    
    # 성공적으로 페이지를 가져온 경우, BeautifulSoup 객체 생성 및 반환
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup





def extract_news_data(div_list, data, news_link):
    """
    주어진 HTML div 요소 리스트에서 뉴스 기사의 제목, 언론사를 추출하여 
    제공된 리스트에 추가하는 함수.

    Args:
    - div_list (list): 각 뉴스 기사가 포함된 HTML div 요소 리스트.
    - data (list): 기사 제목과 언론사 정보를 담을 리스트.
    - news_link (list): 기사 링크를 담을 리스트.

    Returns:
    - None: 함수는 입력된 리스트를 직접 수정하여 반환하지 않음.
    """
    
    # div_list 안의 각 뉴스 아이템을 순회
    for item in div_list:
        
        # 기사 링크 추출
        link = item.find('a')['href']
        # 기사 제목 추출
        title = item.find('strong', class_='sa_text_strong').text.strip()
        # 언론사 정보 추출
        agency = item.find('div', class_='sa_text_press').text.strip()

        article_data = {'agency': agency, 'title': title}
        data.append(article_data)
        news_link.append(link)





def summarize(text):
    """
    주어진 텍스트를 한국어로 최대 7문장으로 요약하는 함수.
    
    프롬프트 템플릿을 사용하여 주어진 텍스트를 한국어로 7문장 이내로 요약 요청.
    OpenAI의 llama3.1:latest 모델을 이용하여 텍스트 요약을 생성.
    생성된 요약문을 문자열로 반환.
    
    Args:
    - text (str): 요약할 텍스트.

    Returns:
    - str: 요약된 텍스트.
    
    """

    prompt_template = """ 
    
    "{text}"
    
    
    You are a professional summarizer. Please write a summary within 7 sentences of the this text in Korean Hanguel (한글): 
    
    """

    prompt = PromptTemplate.from_template(prompt_template)

    llm = ChatOllama(
        model="llama3.1:latest",
        temperature=0)

    output_parser = StrOutputParser()
    
    llm_chain = prompt | llm | output_parser

    response = llm_chain.invoke({"text": text})
    
    return response





def load_web_content(url):
    """
    주어진 URL에서 웹 콘텐츠를 로드하고 특정 부분을 파싱하여 요약된 본문 내용을 반환하는 함수.

    WebBaseLoader를 사용해 주어진 URL의 웹페이지에서 HTML 요소를 찾아 로드.
    가져온 웹페이지 콘텐츠를 summarize 함수를 사용해 요약.
    
    Args:
    - url (str): 웹페이지의 URL 주소.

    Returns:
    - str: 요약된 본문 내용.
    
    """
    loader = WebBaseLoader(
        web_paths=(url,),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                attrs={"class": ['go_trans _article_content']}
            )
        ),
    )

    docs = loader.load()  # 대기 시간 설정
    content = summarize(docs)

    return content



def get_naver_finance_news(date):
    news_links = []
    data = []
    categories = [258, 259, 260, 261, 262, 263, 771, 310]  # 세부 카테고리

    print("Fetching news articles...")

    # tqdm을 사용하여 카테고리별 진행률 표시
    for category in tqdm(categories, desc="Categories processed"):
        base_url = f'https://news.naver.com/breakingnews/section/101/{category}?date={date}'
        soup = get_soup_from_url(base_url)

        if soup is None:
            continue

        news_divs = soup.find_all('div', class_="sa_text")
        extract_news_data(news_divs, data, news_links)

    print(f"Total news articles found: {len(news_links)}")

    # 기사 내용을 병렬로 처리하면서 진행률 표시
    print("Loading web content...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        contents = list(tqdm(executor.map(load_web_content, news_links), total=len(news_links), desc="Articles processed"))

    # DataFrame 생성
    df = pd.DataFrame(data)
    df['summary'] = contents

    # 파일명에 날짜 포함
    file_name = f'Naver_economy_news_{date}.txt'
    df.to_csv(file_name, index=False)

    print(f"Saved data to {file_name}")



# 실행
if __name__ == "__main__":
    get_naver_finance_news("20240927")
