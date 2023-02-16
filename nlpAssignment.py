import azure.cognitiveservices.speech as speechsdk
from func import *

script = open("script.txt","w")

Speech_key = "3b66785c9d73403b99708544933c45a2"
Region = "southeastasia"
Endpoint = "https://southeastasia.api.cognitive.microsoft.com/sts/v1.0/issuetoken"

speech_config = speechsdk.SpeechConfig(subscription=Speech_key, region = Region)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
start()

while True:
    f_result = repeat()
    if type(f_result) == str:
        if "2 + 2" in f_result.lower():
            print("2 + 2 equals to 4")
        elif "quit" in f_result.lower():
            print("QUIT")
            break
        else:
            print(f_result)
            script.write(f_result+"\n")