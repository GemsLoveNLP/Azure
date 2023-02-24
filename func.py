import azure.cognitiveservices.speech as speechsdk
import requests, uuid, json

#Region
Region = "southeastasia"

#speech
Speech_key = "3b66785c9d73403b99708544933c45a2"
Endpoint = "https://southeastasia.api.cognitive.microsoft.com/sts/v1.0/issuetoken"

#translate
Translate_key = "ca0e0d8f2c774ba5abfeeb1a7d0b5397"
endpoint = "https://api.cognitive.microsofttranslator.com"

#utility
Thai_set = {'ก', 'ข', 'ฃ', 'ค', 'ฅ', 'ฆ', 'ง', 'จ', 'ฉ', 'ช', 'ซ', 'ฌ', 'ญ', 'ฎ', 'ฏ', 'ฐ', 'ฑ', 'ฒ', 'ณ', 'ด', 'ต', 'ถ', 'ท', 'ธ', 'น', 'บ', 'ป', 'ผ', 'ฝ', 'พ', 'ฟ', 'ภ', 'ม', 'ย', 'ร', 'ล', 'ว', 'ศ', 'ษ', 'ส', 'ห', 'ฬ', 'อ', 'ฮ'}
Thai = "th-TH-NiwatNeural"
# Thai = "th-TH-PremwadeeNeural"
Eng = "en-US-AIGenerate1Neural"
Ind = "en-IN-PrabhatNeural"

#config
speech_config = speechsdk.SpeechConfig(subscription=Speech_key, region =Region)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

#functions
# --------------------------------------------------------------------

# check if there are any Thai in the text
def check(text):
    if set(text).intersection(Thai_set) == set():
         return Eng
    return Thai

#  speak out the text  
def speak(text):
    #just speak
    speech_config.speech_synthesis_voice_name = check(text)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    speech_synthesizer.speak_text_async(text).get()

# listen to the user and return what they speak in all lower case
def recog():
    result = speech_recognizer.recognize_once()
    text = result.text.lower()
    return text

# speak and print out the text
def speak_print(text):
    speak(text)
    print(text)

# select the mode the user want to use
# NEEDED FOR ACTUAL PROJECT $
def mode_selection():
    speak_print("Select your mode")
    text = recog()
    print(f"Your respond: {text}")
    if "1" in text or "one" in text:
        speak_print("You want to use mode one reading right?")
        ans = recog()
        print(f"Your respond: {ans}")
        if "yes" in ans or "yeah" in ans or "exactly" in ans:
            print("Mode 1: reading has been selected")
            return 1
        else:
            mode_selection()
    elif "2" in text or "two" in text:
        speak_print("You want to use mode two translating right?")
        ans = recog()
        print(f"Your respond: {ans}")
        if "yes" in ans or "yeah" in ans or "exactly" in ans:
            speak_print("Mode 2: translating has been selected")
            return 2
        else:
            mode_selection()
    elif "3" in text or "three" in text:
        speak_print("You want to use mode three identifying right?")
        ans = recog()
        print(f"Your respond: {ans}")
        if "yes" in ans or "yeah" in ans or "exactly" in ans:
            speak_print("Mode 3: indentifying has been selected")
            return 3
        else:
            mode_selection()
    else:
        speak_print("No mode has been selected")

# join the list items together from start+1, stop+1
# list must only contains strings
def joinlist(l,start,stop):
    return " ".join(l[start+1:stop+1])

# separate long text into groups of Thai and English
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
        out.append((obj,check(obj)))    
    return out

# speak with better accent
def speak2(text):
     #speak but separate Thai and English
     phrase = sep(text)
     for part, lang in phrase:
        speak(part)

#  transform a long text into a more usable one
def transform(text):
    return text.strip().replace("\n"," ")

# loop for continuos speaking
def speech_loop():
    #loop for speak2()
    while True:
        text = transform(input("Enter text to read: "))
        if text == 'q': 
                return 
        speak2(text)

# speak in Inglish
def indianvoice(text):
    speech_config.speech_synthesis_voice_name = Ind
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    speech_synthesizer.speak_text_async(text).get()

# translate the given text
def translate(text):
    path = '/translate'
    constructed_url = endpoint + path

    params = { 'api-version': '3.0', 'from': 'en', 'to': ['th'] }

    headers = {'Ocp-Apim-Subscription-Key': Translate_key, 'Ocp-Apim-Subscription-Region': Region, 'Content-type': 'application/json', 'X-ClientTraceId': str(uuid.uuid4())}

    body = [{ 'text': text }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    translated_text = response[0]['translations'][0]['text']
    return translated_text

# transalte the given mixed language text
def translate2(text):
    phrase = sep(text)
    for part, lang in phrase:
        if lang == Eng:
            speak(translate(part))
        else:
            speak(part)

# translate loop
def translate_loop():
    #loop for speak2()
    while True:
        text = transform(input("Enter text to translate: "))
        if text == 'q': 
                return 
        translate2(text)