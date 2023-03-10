import time
import tkinter
from ttkbootstrap import Style
import sys

style = Style(theme='journal')

root = style.master
root.wm_attributes('-topmost', 1)  # 窗口置顶
width_gui = 300
height_gui = 120
width_screen = root.winfo_screenwidth()
height_screen = root.winfo_screenheight()
root.geometry('{}x{}+{}+{}'.format(width_gui, height_gui, int((width_screen - width_gui) / 2),
                                   int((height_screen - height_gui) / 2)))
root.overrideredirect(True)

settime_work = 0.0
settime_rest = 0.0
starttime = 0  # 定义开始时的时间，全局变量
timer = None
elapsedtime = 0.0  # 运行时长，初始为0
running = False  # 用以判断是否“开始”过
ifsettime = False
time_display = tkinter.StringVar()
time_display.set('工作 ?分，休息 ?分')  # 初始显示
ifrest = False


def Update():
    global elapsedtime
    global time_display
    global timer  # Stop()用得到，故global
    global countdown
    global settime_work
    elapsedtime = time.time() - starttime
    countdown = settime_work - elapsedtime
    mins_work = int(countdown/60)
    secs_work = int(countdown - mins_work*60)
    if countdown <= 0:
        Rest()
        timer = root.after(50, Update)  # print(ifrest)
    else:
        time_display.set('工作倒计时 {}:{}'.format(mins_work, secs_work))
        timer = root.after(50, Update)


def GetText_settime():
    global settime_work
    global settime_rest
    global ifsettime
    global running
    global elapsedtime
    global timer
    get_entry_work = entry_work.get()
    get_entry_rest = entry_rest.get()
    settime_work = float(get_entry_work) * 60
    settime_rest = float(get_entry_rest) * 60
    if ifsettime is False and timer is None:
        time_display.set('工作 {}分,休息 {}分'.format(get_entry_work, get_entry_rest))
    elif ifsettime is True and timer is None:
        time_display.set('工作 {}分,休息 {}分'.format(get_entry_work, get_entry_rest))
    elif ifsettime is True and timer is not None:
        root.after_cancel(timer)
        elapsedtime = 0.0
        time_display.set('工作 {}分,休息 {}分'.format(get_entry_work, get_entry_rest))
    ifsettime = True
    running = True
    pass


def Rest():
    global ifrest
    global settime_rest
    global timer
    ifrest = True
    final_display_rest = settime_rest + countdown  # 此时countdown为负数
    if final_display_rest >= 0:
        mins_rest = int(final_display_rest / 60)
        secs_rest = int(final_display_rest - mins_rest * 60)
        time_display.set('休息 {}:{}'.format(mins_rest, secs_rest))
    else:
        time_display.set('结束')
        root.after_cancel(timer)


def Start():
    global ifsettime
    if ifsettime:
        global running  # Stop()用得到
        global starttime  # Stop() and Update()
        if running:
            starttime = time.time() - elapsedtime
            Update()
            pass


def Stop():
    global timer
    global elapsedtime
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
    root.after_cancel(timer)
    pass


def Reset():
    global starttime
    global elapsedtime
    global ifrest
    ifrest = False
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
    root.geometry(f'+{event.x_root - mousX}+{event.y_root - mousY}')
    # root.geometry(f'+{event.x_root}+{event.y_root}')# 窗体移动代码
    # event.x_root 为窗体相对于屏幕左上角的X坐标
    # event.y_root 为窗体相对于屏幕左上角的Y坐标


root.bind("<Button-1>", MouseDown)  # 按下鼠标左键绑定MouseDown函数
root.bind("<B1-Motion>", MouseMove)  # 鼠标左键按住拖曳事件,3个函数都不要忘记函数写参数

frame1 = tkinter.Frame(root)
frame1.pack(anchor='center')
labal_title = tkinter.Label(frame1, text="Pomodoro by LuDreamst")
label_work = tkinter.Label(frame1, text="工作:")
label_rest = tkinter.Label(frame1, text="休息:")
entry_work = tkinter.Entry(frame1, width=7)
entry_rest = tkinter.Entry(frame1, width=7)
settime = tkinter.Button(frame1, text="设定", command=GetText_settime)

labal_title.pack()
label_work.pack(side='left', fill='both', expand=True)
entry_work.pack(side='left', fill='both', expand=True)
label_rest.pack(side='left', fill='both', expand=True)
entry_rest.pack(side='left', fill='both', expand=True)
settime.pack(side='left', fill='both', expand=True, padx=3)

frame2 = tkinter.Frame(root)
frame2.pack()
tkinter.Label(frame2, textvariable=time_display, font=('Times', 20)).pack(fill='both', expand=True)  # 文本变量

frame3 = tkinter.Frame(root)
frame3.pack()
tkinter.Button(frame3, text='开始', command=Start).pack(side=tkinter.LEFT, fill='both', expand=True, padx=6)
tkinter.Button(frame3, text='停止', command=Stop).pack(side=tkinter.LEFT, fill='both', expand=True, padx=6)
tkinter.Button(frame3, text='重置', command=Reset).pack(side=tkinter.LEFT, fill='both', expand=True, padx=6)
tkinter.Button(frame3, text='退出', command=sys.exit).pack(side=tkinter.LEFT, fill='both', expand=True, padx=6)

root.mainloop()
