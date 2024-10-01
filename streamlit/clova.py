import requests


class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }

        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                            headers=headers, json=completion_request, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    print(line.decode("utf-8"))
            return line.decode("utf-8")



if __name__ == '__main__':
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiYwLhxUCPwl7nI1gMUryuUJLEWQvya9qkipzyjPLOJC7j',
        api_key_primary_val='F5VsxkgU5FncyQ3kz4tsVc3HyqNpDimmr2DVyGdq',
        request_id='370a7184-f79a-4768-893a-0146968e9f52'
    )

    preset_text = [{"role":"system","content":"- MBTI에 대한 지식을 기반으로, MBTI 질문에 답해보세요.\n\n질문: ESFJ는 문제에 봉착했을때 어떻게 대응하는가?"}]

    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 512,
        'temperature': 0.5,
        'repeatPenalty': 5.0,
        'stopBefore': [],
        'includeAiFilters': True,
        'seed': 0
    }
    result = completion_executor.execute(request_data)

    print("-----------------------------------------------------------------------------------------------------")
    print(result)