"""
TTS语音工具： pip install pyttsx3 -i https://pypi.tuna.tsinghua.edu.cn/simple/ -U
"""
import pyttsx3


def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


if __name__ == '__main__':
    text_to_speech('你好，我是中国人')
