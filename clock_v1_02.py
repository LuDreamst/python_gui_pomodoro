import time
import tkinter
from ttkbootstrap import Style
import sys
# from winsound import Beep

style = Style(theme='journal')

# root = tkinter.Tk()
root = style.master
# root.title("Pomodoro")
width_gui = 300
height_gui = 120
width_screen = root.winfo_screenwidth()
height_screen = root.winfo_screenheight()
root.geometry('{}x{}+{}+{}'.format(width_gui, height_gui, int((width_screen - width_gui) / 2),
                                   int((height_screen - height_gui) / 2)))
# root.iconbitmap('python_logo.ico')
root.overrideredirect(True)

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


def MouseDown(event):  # 不要忘记写参数event
    global mousX  # 全局变量，鼠标在窗体内的x坐标
    global mousY  # 全局变量，鼠标在窗体内的y坐标

    mousX = event.x  # 获取鼠标相对于窗体左上角的X坐标
    mousY = event.y  # 获取鼠标相对于窗左上角体的Y坐标


def MouseMove(event):
    root.geometry(f'+{event.x_root - mousX}+{event.y_root - mousY}')  # 窗体移动代码
    # event.x_root 为窗体相对于屏幕左上角的X坐标
    # event.y_root 为窗体相对于屏幕左上角的Y坐标


frame2 = tkinter.Frame(root)
frame2.pack(anchor='center')
labal_title = tkinter.Label(frame2, text="Pomodoro by LuDreamst")
label_work = tkinter.Label(frame2, text="工作:")
label_rest = tkinter.Label(frame2, text="休息:")
entry_work = tkinter.Entry(frame2, width=7)
entry_rest = tkinter.Entry(frame2, width=7)
settime = tkinter.Button(frame2, text="设定", command=GetText)

labal_title.pack()
label_work.pack(side='left', fill='both', expand=True)
entry_work.pack(side='left', fill='both', expand=True)
label_rest.pack(side='left', fill='both', expand=True)
entry_rest.pack(side='left', fill='both', expand=True)
settime.pack(side='left', fill='both', expand=True, padx=3)
frame1 = tkinter.Frame(root)
frame1.pack()

frame3 = tkinter.Frame(root)
frame3.pack()

tkinter.Label(frame1, textvariable=time_display, font=('Times', 20)).pack(fill='both', expand=True)  # 文本变量
tkinter.Button(frame3, text='开始', command=Start).pack(side=tkinter.LEFT, fill='both', expand=True, padx=6)
tkinter.Button(frame3, text='停止', command=Stop).pack(side=tkinter.LEFT, fill='both', expand=True, padx=6)
tkinter.Button(frame3, text='重置', command=Reset).pack(side=tkinter.LEFT, fill='both', expand=True, padx=6)
tkinter.Button(frame3, text='退出', command=sys.exit).pack(side=tkinter.LEFT, fill='both', expand=True, padx=6)


root.bind("<Button-1>", MouseDown)  # 按下鼠标左键绑定MouseDown函数
root.bind("<B1-Motion>", MouseMove)  # 鼠标左键按住拖曳事件,3个函数都不要忘记函数写参数

root.mainloop()
