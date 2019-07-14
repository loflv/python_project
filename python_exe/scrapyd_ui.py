import json
import tkinter
from tkinter import Listbox

import requests

curselection = None
spiderSelect = None


def changeButton(*args):
    global curselection
    current = listbox1.curselection()
    if current:
        curselection = current
        params = {
            'project': listbox1.get(curselection)
        }
        response = requests.get("http://127.0.0.1:6800/listspiders.json", params=params)
        jsonSipder = json.loads(response.content, encoding='ascii')['spiders']
        listSipder.set(list(jsonSipder))
        print(response)


def chooseSipder(*args):
    global spiderSelect
    current = listbox2.curselection()
    if current:
        spiderSelect = current


jobid = None


def doSipder():
    global curselection
    global spiderSelect
    global jobid
    params = {
        'project': listbox1.get(curselection),
        'spider': listbox2.get(spiderSelect)
    }
    response = requests.post("http://127.0.0.1:6800/schedule.json", params=params)
    jobid = json.loads(response.content, encoding='ascii')['jobid']
    showResulttext.delete('1.0', 'end')
    showResulttext.insert("insert", "开始爬虫,jobid is "+ jobid)


def stopSider():
    global jobid
    params = {
        'project': listbox1.get(curselection),
        'job': jobid
    }
    response = requests.post("http://127.0.0.1:6800/cancel.json", params=params)
    showResulttext.delete('1.0', 'end')
    showResulttext.insert("insert","停止任务:"+json.loads(response.content)['status'])

def querySider():
    global jobid
    if curselection:
        params = {
            'project': listbox1.get(curselection)
        }

    #response = requests.get("http://127.0.0.1:6800/listjobs.json", params=params)
    response = requests.get("http://127.0.0.1:6800/daemonstatus.json")
    showResulttext.delete('1.0', 'end')
    showResulttext.insert("insert",response.content)

#### 初始化一个窗口
window = tkinter.Tk()
window.title("scrapy")
window.geometry('400x600')

tkinter.Label(window, text="projects").place(x=40, y=10)
listProject = tkinter.StringVar()
listbox1: Listbox = tkinter.Listbox(window, listvariable=listProject)
listbox1.place(x=20, y=30)
listbox1.bind("<<ListboxSelect>>", changeButton)
response = requests.get("http://127.0.0.1:6800/listprojects.json")
jsonProject = json.loads(response.content, encoding='ascii')['projects']
listProject.set(list(jsonProject))

tkinter.Label(window, text="spiders").place(x=240, y=10)
listSipder = tkinter.StringVar()
listbox2: Listbox = tkinter.Listbox(window, listvariable=listSipder)
listbox2.bind("<<ListboxSelect>>", chooseSipder)
listbox2.place(x=200, y=30)

buttonVar = tkinter.StringVar()
buttonVar.set("开始爬虫")
button = tkinter.Button(window, textvariable=buttonVar, command=doSipder)
button.place(x=40, y=290)

buttonVar2 = tkinter.StringVar()
buttonVar2.set("停止爬虫")
button2 = tkinter.Button(window, textvariable=buttonVar2, command=stopSider)
button2.place(x=120, y=290)

buttonVar3 = tkinter.StringVar()
buttonVar3.set("获取状态")
button3 = tkinter.Button(window, textvariable=buttonVar3, command=querySider)
button3.place(x=200, y=290)


showResulttext = tkinter.Text(window,width=50,height=10)
showResulttext.place(x = 20,y = 330)

window.mainloop()
