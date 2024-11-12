유튜브 영상 다운로드 받기 위해서 pytube를 import 헤줘야한다.
이 떄, 제대로 실행이 되지 않는다면

from pytubefix import YouTube
from pytubefix.cli import on_progress 를 추가 해야한다.

def download_audio(url) 함수 설명

yt = YouTube(url, on_progress_callback = on_progress)

YouTube 클래스의 인스턴스를 생성하여 yt 변수에 할당합니다. url 매개변수를 사용해 YouTube 비디오를 가져오고, on_progress_callback을 통해 다운로드 진행 상황을 추적하는 콜백 함수를 설정합니다.

ys = yt.streams.get_highest_resolution()

yt 객체의 streams 속성에서 가장 높은 해상도의 스트림을 가져옵니다. 이는 ys 변수에 저장되며, 이후 다운로드할 비디오 스트림입니다.

audio_file = ys.download(filename="audio.mp4")

ys 스트림을 audio.mp4라는 파일 이름으로 다운로드합니다. 다운로드된 파일의 경로가 audio_file에 저장됩니다.

renamed_file = audio_file[:-4] + ".mp3"

.mp4 파일의 확장자를 .mp3로 바꾸기 위해 문자열 슬라이싱을 사용하여 새로운 파일 이름을 만듭니다.

video = moviepy.editor.VideoFileClip(audio_file)

moviepy 라이브러리를 사용하여 다운로드된 audio_file(.mp4 형식)을 비디오 클립 객체로 불러옵니다. 이를 통해 비디오 파일에서 오디오를 추출할 수 있습니다.

video.audio.write_audiofile(renamed_file)
video 객체의 audio 속성을 사용하여 오디오를 추출하고, renamed_file 경로로 저장합니다. 이때 오디오는 .mp3 형식으로 저장됩니다