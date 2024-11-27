from functions import get_video_details, search_video
from summary import summarize_text_korean

if __name__ == "__main__":
    keyword = input()
    ytube_id = search_video(keyword)
    text = get_video_details(ytube_id)
    summary = summarize_text_korean(text)
    print(f"원문: {text}")
    print("--"*20)
    print(f"요약: {summary}")
    