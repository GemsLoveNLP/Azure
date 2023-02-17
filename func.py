import azure.cognitiveservices.speech as speechsdk
 
Speech_key = "3b66785c9d73403b99708544933c45a2"
Region = "southeastasia"
Endpoint = "https://southeastasia.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
Thai_set = {'ก', 'ข', 'ฃ', 'ค', 'ฅ', 'ฆ', 'ง', 'จ', 'ฉ', 'ช', 'ซ', 'ฌ', 'ญ', 'ฎ', 'ฏ', 'ฐ', 'ฑ', 'ฒ', 'ณ', 'ด', 'ต', 'ถ', 'ท', 'ธ', 'น', 'บ', 'ป', 'ผ', 'ฝ', 'พ', 'ฟ', 'ภ', 'ม', 'ย', 'ร', 'ล', 'ว', 'ศ', 'ษ', 'ส', 'ห', 'ฬ', 'อ', 'ฮ'}
Thai = "th-TH-NiwatNeural"
# Thai = "th-TH-PremwadeeNeural"
Eng = "en-US-AIGenerate1Neural"
Ind = "en-IN-PrabhatNeural"

speech_config = speechsdk.SpeechConfig(subscription=Speech_key, region =Region)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

def check(text):
    if set(text).intersection(Thai_set) == set():
         return Eng
    return Thai
         
def speak(text):
    #just speak
    speech_config.speech_synthesis_voice_name = check(text)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    speech_synthesizer.speak_text_async(text).get()

def start():
    result = speech_recognizer.recognize_once()
    print(result.text)
    if "start" in result.text.lower():
        speak("The app is starting")
        return True
    return False
    
def joinlist(l,start,stop):
    #join the list pieces from start+1 to stop+1
    return " ".join(l[start+1:stop+1])

def sep(text):
    #split text into parts
    phrase = text.split()
    #output
    out = []
    #index container
    temp = []
    #list the breaking points
    for i in range(0,len(phrase)-1,1):
        if check(phrase[i]) != check(phrase[i+1]):
            temp.append(i)
    order = [-1] + temp + [len(phrase)-1]
    #form the pieces
    for i in range(len(order)-1):
        obj = joinlist(phrase,order[i],order[i+1])
        out.append(obj)    
    return out

def speak2(text):
     #speak but separate Thai and English
     phrase = sep(text)
     for part in phrase:
        speak(part)

def transform(text):
    return text.strip().replace("\n"," ")

def speech_loop():
    #loop for speak()
    while True:
        text = transform(input("Enter your text: "))
        if text == 'q': 
                return 
        speak(text)
    return

def speech_loop2():
    #loop for speak2()
    while True:
        text = transform(input("Enter your text: "))
        if text == 'q': 
                return 
        speak2(text)
    return

def indianvoice(text):
    speech_config.speech_synthesis_voice_name = Ind
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    speech_synthesizer.speak_text_async(text).get()
