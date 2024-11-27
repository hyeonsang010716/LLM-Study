from konlpy.tag import Okt
from langchain_text_splitters import RecursiveCharacterTextSplitter
from collections import Counter
import numpy as np
import re

def summarize_text_korean(text):
    # 형태소 분석기 초기화
    okt = Okt()

    nouns = okt.nouns(text)
    
    from collections import Counter
    word_freq = Counter(nouns)
    
    sentences = text.split('.')
    sentence_scores = []
    for sentence in sentences:
        score = sum(word_freq[noun] for noun in okt.nouns(sentence))
        sentence_scores.append((sentence, score))
    
    top_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:3]
    summary = ' '.join([sentence for sentence, score in top_sentences])
    return summary

if __name__ == "__main__":
    text = """
함박눈이 쏟아지는 새벽.

도로가 눈으로 뒤덮였습니다.

서울 전역에 내린 큰 눈에 시민들은 출근길에 불편을 겪기도 했습니다.

한 시민은 지하철역에 사람들이 빽빽하게 들어선 사진을 KBS에 제보했습니다.

제보자는 "출근길 9호선인데 깔려 죽을 뻔해서 압사사고가 날 뻔했다"면서 "회사는 재택근무를 지시해야 한다"고 했습니다. 

버스들도 눈이 쌓인 채 도로를 달립니다.

동이 튼 아침, 사람들이 빙판길로 변해버린 횡단보도를 조심스럽게 건넙니다.

뛰어가던 여성은 도로에 쌓인 눈 더미를 만나자, 속도를 늦춥니다.

어젯밤부터 내린 폭설에 서울 전역에 대설주의보가 내렸습니다.

서울에 대설경보가 내려진 건 2010년 이후 14년만입니다.

서울교통공사는 오늘(27일) 오전 폭설에 1~8호선 '러시아워(열차 집중 투입 시간대)' 운행을 9시 30분까지 긴급 연장했습니다.

기상청은 앞으로 내일까지 강원 산지에 최대 30cm 이상, 경기 내륙과 강원 내륙, 충북과 전북 동부에는 최대 15에서 20cm의 많은 눈이 더 내리겠다고 내다봤습니다.

KBS 뉴스 고해람입니다.

▣ KBS 기사 원문보기 : http://news.kbs.co.kr/news/view.do?ncd=8116418

▣ 제보 하기
◇ 카카오톡 : 'KBS제보' 검색
◇ 전화 : 02-781-1234
◇ 홈페이지 : https://goo.gl/4bWbkG
◇ 이메일 : kbs1234@kbs.co.kr

Copyright ⓒ KBS.
"""
    print(summarize_text_korean(text))
