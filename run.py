from nlp import *
from line import *

# ? settings---------
trigger = "สวัสดี"
terminate = "เลิกทำ"
script = f"พูด {trigger} เพื่อเลือกโหมด พูด {terminate} เพื่อปิดโปรแกรม"
# ? -----------------

def main():
    speak_print(script)
    while True:
        text = recog_Thai()
        if terminate in text:
            print("End")
            return
        elif trigger in text:
            mode_selection_Thai()
        print("result:", text)

main()