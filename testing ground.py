from func import check, transform

text = "hello \nworld hi ui รน \nรยบ\n king oi n\nน นย  สย po op บล "

def joinlist(l,start,stop):
    return " ".join(l[start+1:stop+1])

def sep(text):
    phrase = text.split()

    out = []
    temp = []
    for i in range(0,len(phrase)-1,1):
        if check(phrase[i]) != check(phrase[i+1]):
            temp.append(i)

    order = [-1] + temp + [len(phrase)-1]
    t = round((len(order)+1)/2)+1

    for i in range(len(order)-1):
        obj = joinlist(phrase,order[i],order[i+1])
        out.append(obj)
        
    return out

print(transform("""ฉันชอบตัวเองเวลาที่อยู่กับเธอ
ชอบที่ฉันเป็นตอนอยู่กับเธอ
เหมือนฉันได้กลายมาเป็นอีกคนที่ดีกว่าเดิม"""))
