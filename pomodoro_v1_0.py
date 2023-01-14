import time
import tkinter
from ttkbootstrap import Style
# from winsound import Beep

style = Style(theme='litera')

# root = tkinter.Tk()
root = style.master
root.title("番茄钟")
width_gui = 220
height_gui = 120
width_screen = root.winfo_screenwidth()
height_screen = root.winfo_screenheight()
root.geometry('{}x{}+{}+{}'.format(width_gui, height_gui, int((width_screen - width_gui) / 2),
                                   int((height_screen - height_gui) / 2)))
root.iconbitmap('python_logo.ico')
# root["background"] = "#FFFFFF"
root.minsize(width_gui, height_gui)
root.maxsize(220, 120)

label1 = tkinter.Label(root, text="工作:")
label2 = tkinter.Label(root, text="休息:")
label1.grid(row=0)
label2.grid(row=1)
# label1.pack(side='left')
# label2.pack(side='left')
entry_work = tkinter.Entry(root)
entry_rest = tkinter.Entry(root)
entry_work.grid(row=0, column=1)
entry_rest.grid(row=1, column=1)
# setbutton = tkinter.Button(root)
# setbutton.grid(row=1, column=2)
# entry1.pack(padx=20, pady=20)
# entry1.insert(0, 'xxxxxx')
# print(entry1.get())
frame1 = tkinter.Frame(root)
# frame1.pack()
frame1.grid(row=2, column=1)


settime_work = 0.0
settime_rest = 0.0
starttime = 0  # 定义开始时的时间，全局变量
timer = None
# timer_rest = None# 定义计时器，刷新
elapsedtime = 0.0  # 运行时长，初始为0
running = False  # 用以判断是否“开始”过
ifsettime = False
time_display = tkinter.StringVar()
# time_display.set('工作:?分，休息:?分'.format(settime_work/60, settime_rest/60))
time_display.set('工作:?分，休息:?分')  # 初始显示
ifrest = False


def GetText():
    global settime_work
    global settime_rest
    global ifsettime
    get_entry_work = entry_work.get()
    get_entry_rest = entry_rest.get()
    time_display.set('工作:{}分,休息:{}分'.format(get_entry_work, get_entry_rest))
    settime_work = float(get_entry_work) * 60
    settime_rest = float(get_entry_rest) * 60
    ifsettime = True
    pass


def Update():
    global elapsedtime
    global time_display
    global timer  # Stop()用得到，故global
    global countdown
    global ifrest
    global settime_work
    elapsedtime = time.time() - starttime
    countdown = settime_work - elapsedtime
    mins_work = int(countdown/60)
    secs_work = int(countdown - mins_work*60)
    # if mins_work == 0 and secs_work == 0 or secs_work < 0 or mins_work < 0:
    if countdown <= 0:
        # if secs_work <= 0:
        Rest()
        timer = root.after(50, Update)  # print(ifrest)
    else:
        time_display.set('工作倒计时 {}:{}'.format(mins_work, secs_work))
        timer = root.after(50, Update)
    # if mins_work == 0 and secs_work == 0 or mins_work < 0 and secs_work < 0:
    #     Rest()


def Rest():
    global ifrest
    global settime_rest
    ifrest = True
    final_display_rest = settime_rest + countdown  # 此时countdown为负数
    if final_display_rest >= 0:
        mins_rest = int(final_display_rest / 60)
        secs_rest = int(final_display_rest - mins_rest * 60)
        time_display.set('休息 {}:{}'.format(mins_rest, secs_rest))
    else:
        time_display.set('结束')
        # Stop()
    # timer_rest = root.after(50, Rest)


def Start():
    global ifsettime
    # global settime_work
    # global settime_rest
    if ifsettime:
        global running  # Stop()用得到
        global starttime  # Stop() and Update()
        # if not running:
        running = True
        starttime = time.time() - elapsedtime
        Update()
        pass


def Stop():
    global running
    global timer
    global elapsedtime
    running = False
    # global timer_rest
    # if running:
    root.after_cancel(timer)
    elapsedtime = time.time() - starttime
    stop_display = settime_work - elapsedtime
    stop_display_rest = settime_rest + stop_display
    mins_stop_rest = int(stop_display_rest/60)
    secs_stop_rest = int(stop_display_rest - mins_stop_rest*60)
    mins_stop = int(stop_display/60)
    secs_stop = int(stop_display - mins_stop*60)
    if ifrest:
        time_display.set('休息暂停 {}:{}'.format(mins_stop_rest, secs_stop_rest))
    else:
        time_display.set('工作暂停 {}:{}'.format(mins_stop, secs_stop))
        # running = False
    pass


def Reset():
    global running
    global starttime
    global elapsedtime
    global ifrest
    ifrest = False
    running = True
    elapsedtime = 0.0  # 运行时间归零
    starttime = time.time() - elapsedtime
    Update()
    pass


tkinter.Label(frame1, textvariable=time_display).pack()  # 文本变量
tkinter.Button(frame1, text='开始', command=Start).pack(side=tkinter.LEFT)
tkinter.Button(frame1, text='停止', command=Stop).pack(side=tkinter.LEFT)
tkinter.Button(frame1, text='重置', command=Reset).pack(side=tkinter.LEFT)
tkinter.Button(frame1, text='退出', command=quit).pack(side=tkinter.LEFT)
tkinter.Button(root, text='设定', command=GetText).grid(row=1, column=2)

root.mainloop()
