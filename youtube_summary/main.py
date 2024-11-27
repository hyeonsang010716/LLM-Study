import summary_okt
import summary_llm

if __name__ == "__main__":
    keyword = input()

    # 형태소 분석기를 이용한 요약
    print(f"형태소 분석기 요약: {summary_okt.summary_news_with_keyword(keyword)}")
    print("---"*20)
    print(f"LLM 요약: {summary_llm.search_news_keyword(keyword)}")
    