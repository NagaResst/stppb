import tkinter
import ttkbootstrap

window = tkinter.Tk()
window.geometry('900x600')
# to rename the title of the window
window.title("猴面雀 - FF14市场查询小工具")


# pack is used to show the object in the window

def output_user_input(text):
    return text


text = tkinter.Text(window, width=50, height=3, undo=True, autoseparators=False).pack()
b = tkinter.Button(window, text="点击执行回调函数", command=output_user_input).pack()
tkinter.mainloop()
