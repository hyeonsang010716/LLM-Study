# LLM_Sharing
#### 해당 프로젝트는 2024 여름방학 LangChain 및 LLM 스터디를 진행하며, 최종 목표인 DACON 재정정보 AI 검색 알고리즘 경진대회에 출전을 목표로 진행했습니다.
![ai](https://github.com/user-attachments/assets/8d97a652-9023-457c-b4cb-8ee566ba0eab)

## 1. 프로젝트 인원 및 맡은 역
- LangChain : 조현상
- Fine-tuning : 차민수
- Hugging Face : 정의현

## 2. 사용한 모델
- Embedding - intfloat/multilingual-e5-base
- DB - FAISS
- Tokenizer - rtzr/ko-gemma-2-9b-it

## 3. 시나리오
중소벤처기업부_혁신창업사업화자금(융자) , ./test_source/중소벤처기업부_혁신창업사업화자금(융자).pdf , 2022년 혁신창업사업화자금(융자)의 예산은 얼마인가요?

위와 같은 쿼리가 주어졌을 때 리트리버를 통해 쿼리에 대한 답변 생성

-> 2022년 혁신창업사업화자금(융자)의 예산은 2조 78억원입니다.

## 4. 알고리즘 단계
1. PDF 텍스트 추출
2. 텍스트를 chunk로 분할
3. Document 객체 리스트 생성
4. Document 임베딩
5. DB 저장 및 리트리버 생성
6. LLM 모델 세팅
7. RAG 체인 진

## 5. 최종 결과
![image](https://github.com/user-attachments/assets/aeba2579-b893-4b67-b6ca-59daf713ede9)

## 6. 개선 해야 할 사항
- GPU 한계로 무거운 모델 사용 불가
- 자원의 한계가 있기 때문에 가벼운 모델이라도 여러 번 테스트 불가
