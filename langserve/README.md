## 소개

이 글은 Langserve를 활용하여 LLM 기반 채팅 웹사이트를 구현하는 방법을 설명합니다.

## 목차

1. [환경 세팅](#환경-세팅)
2. [Langserve 구현](#langserve-구현)
3. [Ngrok을 통한 테스트](#ngrok을-통한-테스트)
4. [Koyeb 배포](#koyeb-배포)
5. [문제 해결](#문제-해결)

## 환경 세팅

### Python 버전

- Python 3.11.9 사용
- pyenv virtualenv 사용

### 필수 패키지 설치

- requirements.txt

  > langchain-upstage
  > langchain-core
  > langserve
  > fastapi
  > python-dotenv
  > uvicorn
  > sse_starlette

- pip를 이용하여 requirements.txt 내의 패키지 다운로드
  ```terminal
  pip install -r requirements.txt
  ```

### 환경변수 설정

- LLM을 사용할 때에는 api key가 필요합니다.
- Upstage
  - https://console.upstage.ai/login?redirect=/docs/getting-started/quick-start 에서 회원가입을 합니다
  - 로그인 후 api key를 위 사이트에서 받아옵니다.
- python-dotenv를 사용하여 env 관리하는 방법
  - .env 파일을 root 디렉토리에 생성합니다
  - .env 파일 안에 아래와 같이 작성합니다 (your_api_key에는 위에서 받아온 키를 입력합니다)
  ```
  UPSTAGE_API_KEY="YOUR_API_KEY"
  ```
- 위 설정을 마쳤으면 환경변수를 가져와야하는 경우 dotenv의 load_dotenv 함수를 사용하면 됩니다.

## Langserve 구현

### Chain 구성하기

- Chain
  - 기본적인 Chain은 Prompt | LLM | Output parser로 구성됩니다.
- Prompt
  - ChatPromptTemplate는 System에 전달할 프롬프트, 그리고 유저의 입력을 담을 부분을 지정하게 됩니다.
  - MessagePlaceHolder는 메시지의 기록을 담게 되며 chatting 형식의 Chain을 구성하도록 도와줍니다.

```python
    prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful, smart, kind, and efficient AI assistant. You always fulfill the user's requests to the best of your ability. You always answer succinctly. You must answer in Korean."),
    ("user", "{user_input}"),
    MessagesPlaceholder(variable_name="messages")
])
```

- LLM
  - LLM은 자신이 사용하고 싶은 어떤 모델을 가져와도 됩니다.

```python
llm = ChatUpstage()
```

- Output Parser는 langchain_core의 StrOutputParser를 사용합니다.

```python
chain = prompt | llm | StrOutputParser()
```

### 로컬 서버 실행

- main.py 구성 방법
  - langserve는 Fast api 기반으로 만들어졌습니다.
  - prompt 형태로 해서 사용할 수 있고 Chatting 형식으로도 사용할 수 있습니다.
  - 기본적인 형태는 app으로 FastAPI 클래스를 호출합니다.
    `app = FastAPI()`
  - CORS를 통해 외부 HTTP 요청을 허용하도록 작성합니다.
  - CORS는 외부의 cross-origin 요청을 확인 하도록 해줍니다.
  - CORS는 사이트가 사용자의 공격에 대비할 수 있게 해주고 다른 사이트가 모방하는 것을 막습니다.
    ```python
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    ```
- Prompt 형식 구현
  ```python
  @app.get("/") # root를 호출하였을때
  async def redirect_root_to_chat(): # root 대신 chat 화면으로 보내기
    return RedirectResponse("/prompt/playground")
  add_routes(app, chain, path="/prompt")
  ```
- Chat 형식 구현

  ```python
    class InputChat(BaseModel):
        """Input for the chat endpoint."""

        messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ...,
        description="The chat messages representing the current conversation.",
    )

    add_routes(
        app,
        chain.with_types(input_type=InputChat),
        path="/chat",
        enable_feedback_endpoint=True, # 피드백 기능 활성화
        enable_public_trace_link_endpoint=True,
        playground_type="chat", # 채팅 형태로 정리
    )
  ```

  > 위 두 코드는 둘 중 하나만 선택해서 작성하면 됩니다.

- 실행 명령어
  - python을 이용한 실행
  ```
  python main.py
  ```
  - Terminal을 사용한 실행
  ```terminal
  uvicorn main:app --host 0.0.0.0 --port 8080
  ```

## Ngrok을 통한 테스트

### Ngrok 설정

- 설치 방법
  - https://ngrok.com/docs/getting-started/?os=windows에 접속하여 운영체제에 맞는 방법을 선택하여 다운로드
- 기본 사용법

  - 위에서 적은 코드를 로컬에서 실행 중이어야 합니다.
  - 포트 번호가 같을 때 아래 명령어를 사용합니다.

  ```terminal
        Ngrok http http://localhost:8000
  ```

- 실행시 나온 URL을 사용하면 다른 PC에서 원격으로 접속이 가능합니다.

## Koyeb 배포

### 배포 준비

- Github 업로드
  - 현재까지의 코드들을 Github에 업로드 합니다.
- Koyeb 세팅
  - https://www.koyeb.com/에서 회원가입을 합니다.
  - Overview로 가서 Web Service를 생성합니다.
- 프로젝트 구성
  - Setting에 Builder/Run command에 아래 명령어를 입력합니다
  ```terminal
  Ngrok http http://127.0.0.1:8000
  ```
  - Exposed ports의 포트 번호 설정이 명령어 포트와 동일한지 확인합니다.
  - Enbironments variables에 LLM API Key를 추가합니다.

### 주의사항

- API 키 관리
  - api key는 악용될 가능성이 높기 때문에 Github에 올리지 말고 로컬에서 관리합니다.
  - Koyeb에서도 Secret으로 설정해서 악용되지 않게 사용합니다.
- 패키지 호환성
  - pywin32와 같이 특정 운영체제에서만 사용되는 모듈이 requirements.txt에 포함되지 않게 관리합니다.
  - pydantic.v1처럼 각 모듈의 버전을 확인하고 충돌이 나지 않게 관리 합니다.
- 이미지 크기 최적화
  - Koyeb은 자동으로 github 코드를 Docker img로 바꾸어 줍니다. 이때 img의 크기가 너무 크면 호스팅이 안되므로 이를 확인해 주어야 합니다.

## 참조한 사이트

- Upstage : https://console.upstage.ai/docs/getting-started/quick-start
- langserve Documents : https://python.langchain.com/docs/langserve/
- Teddy-note Youtube: https://www.youtube.com/watch?app=desktop&v=mdzMBF56HOM
- 블로그 글: https://velog.io/@uniuj130/%EB%82%98%EB%A7%8C%EC%9D%98-LLM-%ED%98%B8%EC%8A%A4%ED%8C%85-%EB%94%B0%EB%9D%BC%ED%95%98%EA%B8%B0-2
  https://velog.io/@eogh773/Koyeb%EC%9D%84-%ED%86%B5%ED%95%9C-%EB%AC%B4%EB%A3%8C-%EB%B0%B0%ED%8F%AC
