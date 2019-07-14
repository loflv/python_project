import tkinter
from tkinter import messagebox, Listbox
import requests
from fake_useragent import UserAgent

curselection = None


def changeButton(*args):
    global curselection
    curselection = listbox.curselection()
    getContent = listbox.get(curselection)
    buttonVar.set(getContent + "签到")


def youdaoSign():
    headers = {
    "Accept":"*/*",
    "Cache-Control":"no-cache",
    "Postman-Token": "9be17e05-f83d-47d2-8ab8-db5560b57ae0,0dbb4a31-f172-45f3-87f2-bb18cf687a99",
    "Host":"note.youdao.com",
    "accept-encoding": "gzip, deflate",
    "content-length":" ",
    "Connection": "keep-alive",
    "cache-control":"no-cache",
    'Cookie': "YNOTE_FORCE=true; YNOTE_SESS=v2|RWWJrfXaScJyPMkAhHwS0PLh4UAhLJB0qBnLU5hMqFReFkMzAOf6FRTFkMkMhMgLReBO4qy64zM0Umh4wFk4pZ0gFkf6BnMgz0; YNOTE_LOGIN=1||1561884937384; JSESSIONID=aaadqlZSzNJi3dNYQ7KUw"
    }

    param = {
        'method': 'checkin'
    }
    response = requests.post("http://note.youdao.com/yws/mapi/user", params=param, headers=headers)
    print(response.status_code)


def doSign():
    if curselection[0] == 0:
        youdaoSign()


#### 初始化一个窗口
window = tkinter.Tk()
window.title("签到")
window.geometry('400x600')

listvar = tkinter.StringVar()
listvar.set(['有道云笔记'])

listbox: Listbox = tkinter.Listbox(window, listvariable=listvar)
listbox.place(x=20, y=20)
listbox.bind("<<ListboxSelect>>", changeButton)

buttonVar = tkinter.StringVar()
buttonVar.set("未定义")
button = tkinter.Button(window, textvariable=buttonVar, command=doSign)
button.place(x=40, y=290)

window.mainloop()
