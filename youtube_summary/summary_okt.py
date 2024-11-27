from konlpy.tag import Okt
from collections import Counter
import numpy as np
from get_news import get_news_context


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

def summary_news_with_keyword(keyword: str):
    text = get_news_context(keyword)
    summary = summarize_text_korean(text)
    return summary

if __name__ == "__main__":
    print(summary_news_with_keyword("폭설"))