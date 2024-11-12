from pytube import YouTube
from pytubefix import YouTube
from pytubefix.cli import on_progress
import moviepy.editor
import re
from IPython.display import Audio
from dotenv import load_dotenv
from openai import OpenAI

# 토큰 정보로드
load_dotenv()

client = OpenAI()

# 유튜브 링크

def download_audio(url):
    yt = YouTube(url, on_progress_callback = on_progress)
    ys = yt.streams.get_highest_resolution()
    audio_file = ys.download(filename="audio.mp4")
    renamed_file = audio_file[:-4] + ".mp3"
    video = moviepy.editor.VideoFileClip(audio_file)
    video.audio.write_audiofile(renamed_file)
    return renamed_file

def transcribe_audio(audio_path):
    audio_file = open(audio_path, "rb")
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        language="ko",
        response_format="text",
        temperature=0.0,
    )

    return transcript

def extract_dates(text):
    # 날짜 패턴 검색
    dates = re.findall(r'\d{4}년|\d{2}년|\d+월|\d+일', text)

    return dates

def extract_keywords_with_llm(text):
    messages = [
        {"role": "system", "content": "You are an assistant that extracts keywords related to economics."},
        {"role": "user", "content": f"다음 텍스트에서 가장 중요한 키워드를 한가지만 추출해 주세요: {text}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.3
    )
    keyword = response.choices[0].message.content.strip()
    return keyword

def summarize_text_with_llm(text):
    messages = [
        {"role": "system", "content": "You are an assistant that summarizes texts related to economics."},
        {"role": "user", "content": f"다음 텍스트를 한글로 요약해 주세요: {text}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.3
    )
    summary = response.choices[0].message.content.strip()
    return summary

def retrieve_related_info(summary_text):
    messages = [
        {"role": "system", "content": "You are an assistant that provides additional information on summarized economic topics."},
        {"role": "user", "content": f"다음 요약 내용과 관련된 경제 정보를 제공해 주세요: {summary_text}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.3
    )
    related_info = response.choices[0].message.content.strip()
    return related_info

# Step 3: LLM을 통한 사실 검증

# (1) 전체 텍스트의 정확성 검증
def verify_with_llm_overall(transcribed_text):
    messages = [
        {"role": "system", "content": "You are an assistant that verifies factual accuracy of the provided text."},
        {"role": "user", "content": f"다음 텍스트의 내용이 사실인지 검토해주세요. 답변은 한글로 해주세요.: {transcribed_text}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.2
    )
    verification_result = response.choices[0].message.content.strip()
    return verification_result


def verify_with_llm_keywords(transcribed_text, keyword):
    messages = [
        {"role": "system", "content": "You are an assistant that verifies factual accuracy related to specific keywords."},
        {"role": "user", "content": f"이 텍스트에서 '{keyword}'와 관련된 정보가 사실인지 확인해 주세요. 답변은 한글로 해주세요.: {transcribed_text}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.2
    )
    result = response.choices[0].message.content.strip()
    
    return result


# (3) 과거와 현재 정보 비교
def verify_with_llm_temporal(transcribed_text, dates):
    results = {}
    for date in dates:
        messages = [
            {"role": "system", "content": "You are an assistant that verifies the factual accuracy of information based on specific dates."},
            {"role": "user", "content": f"이 텍스트에 있는 날짜 '{date}'에 해당하는 정보가 당시의 사실과 일치하는지 검토해 주세요. 답변은 한글로 해주세요.: {transcribed_text}"}
        ]
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.2
        )
        results[date] = response.choices[0].message.content.strip()
    return results

def assess_truthfulness(summary_text, related_info):
    # 요약된 내용과 관련 정보를 기반으로 LLM에게 검토를 요청
    messages = [
        {"role": "system", "content": "You are an assistant that assesses the truthfulness of economic statements by comparing summarized content with related information."},
        {"role": "user", "content": f"다음 요약 내용: {summary_text}"},
        {"role": "user", "content": f"추가 정보: {related_info}"},
        {"role": "user", "content": "위 요약 내용이 추가 정보와 일치하는지, 또는 왜곡된 부분이 있는지 판단해 주세요."}
    ]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.2
    )
    assessment_result = response.choices[0].message.content.strip()
    return assessment_result



if __name__ == "__main__":

    #video_url = "https://www.youtube.com/watch?v=bN8XdNQuRVU"
    #audio_path = download_audio(video_url)
    #transcribed_text = transcribe_audio(audio_path)
    transcribed_text = """ 이번엔 전세 얻을 분들에겐 안 좋은 소식입니다. 앞으로 전세대출이 더 까다로워질 것 같습니다. 가계부채 줄이라는 정책 때문이 아닙니다. 전세대출이 구조적인 문제 때문에 일명 외통수에 빠졌기 때문입니다.
    잠시 은행 입장에서 생각해 볼까요. 주택담보대출은 집을 담보로 잡고 큰 돈을 빌려주죠. 대충금을 안 갚더라도 집을 처분하면 되니까 은행은 안심입니다. 그런데 전세대출은 대체 뭘 보고 보증금 수억 원씩을 빌려줄까요.
    집주인에게서 보증금을 돌려받을 권리, 세입자의 그 권리가 일종의 담보인데 사실 집주인이 떼먹으면 그만이어서 매우 불안한 담보입니다. 그래서 보완장치가 필요합니다. 집주인이 보증금을 떼먹어도 우리가 대신 갚아준다.
    주택도시보증공사, 주택금융공사, 서울보증보험, 보증삼총사 이들을 믿고 은행이 전세보증금을 빌려주는 겁니다. 뒤집어서 보자면 보증에 문제가 생기면 전세대출 자체가 흔들리는데 그 문제가 지금 커지고 있습니다.전세 사기 때문입니다. 
    전세 사기꾼들이 떼먹은 막대한 보증금을 보증삼총사가 은행에 대신 갚아주고 있습니다. 나중이라도 사기꾼들에게 받아야겠지만 사기꾼들이 순수난리가 있겠습니까.폐수율 10%대입니다. 나머진 족족 보증기관의 손실입니다. 
    전세대출의 40%를 보증하는 주택도시보증공사가 가장 심각한데 대신 갚아준 보증금이 2018년엔 500원대였지만 지난해 3조 5천억 원을 넘겼고 올해는 최소 4조 원을 넘길 것으로 보입니다. 한마디로 회사가 망할 지경이 된 겁니다. 
    이 정도면 아무리 인심좋아도 보증에 인색해 줄 수밖에 없습니다. 앞으로는 전세보증금 전액이 아닌 일부만 대체로 80% 이하만 보증할 방침이고 보증 수수료도 더 비싸게 올릴 계획입니다. 집주인의 신용도 볼 계획입니다.
    집주인이 보증금을 돌려줄만 해야만 보증을 서준다는 방안을 검토 중입니다. 이게 실행되면 집주인 신용이안 좋은 경우에는 아무리 신용 좋은 세입자도 전세대출을 못 받을 수 있습니다. 지금까지 경제 아클립이었습니다.
    """
    #print("전사된 텍스트:", transcribed_text + "\n")

        # 키워드 및 날짜 추출
    #dates = extract_dates(transcribed_text)
    #keywords = extract_keywords_with_llm(transcribed_text)
    #print("추출된 키워드:", keywords)
    #print("추출된 날짜:", dates)

    # 전체 텍스트 검증
    #overall_verification = verify_with_llm_overall(transcribed_text)
    #print("전체 내용 사실 검증 결과:", overall_verification + "\n")

    # 키워드 중심 사실 검증
    #keyword_verification = verify_with_llm_keywords(transcribed_text, keywords)
    #print("키워드 중심 검증 결과:", keyword_verification + "\n")

    # 날짜별 사실 검증
    #temporal_verification = verify_with_llm_temporal(transcribed_text, dates)
    #print("날짜별 검증 결과:", temporal_verification)

    summary = summarize_text_with_llm(transcribed_text)
    print("요약된 텍스트:", summary  + "/n")

    # 요약된 내용 기반 관련 정보 탐색
    related_info = retrieve_related_info(summary)
    print("관련된 추가 정보:", related_info)

    # 진위 여부 판단
    truthfulness_assessment = assess_truthfulness(summary, related_info)
    print("진위 여부 판별 결과:", truthfulness_assessment)