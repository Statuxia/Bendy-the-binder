from keyboard import write, send, is_pressed
from time import sleep
from tkinter import Tk, Label, Button, Entry


def clicked():
    commands = [command.get(), command2.get(), command3.get(), command4.get(), command5.get(), command6.get()]
    hotkeys = [hotkey.get(), hotkey2.get(), hotkey3.get(), hotkey4.get(), hotkey5.get(), hotkey6.get()]
    for key in range(len(hotkeys)):
        if hotkeys[key] == "":
            hotkeys[key] = "F11"
    if is_pressed(hotkeys[0]):
        send(chat.get())
        sleep(0.1)
        write(commands[0])
        sleep(0.1)
        send("Enter")
        sleep(0.1)
    elif is_pressed(hotkeys[1]):
        send(chat.get())
        sleep(0.1)
        write(commands[1])
        sleep(0.1)
        send("Enter")
        sleep(0.1)
    elif is_pressed(hotkeys[2]):
        send(chat.get())
        sleep(0.1)
        write(commands[2])
        sleep(0.1)
        send("Enter")
        sleep(0.1)
    elif is_pressed(hotkeys[3]):
        send(chat.get())
        sleep(0.1)
        write(commands[3])
        sleep(0.1)
        send("Enter")
        sleep(0.1)
    elif is_pressed(hotkeys[4]):
        send(chat.get())
        sleep(0.1)
        write(commands[4])
        sleep(0.1)
        send("Enter")
        sleep(0.1)
    elif is_pressed(hotkeys[5]):
        send(chat.get())
        sleep(0.1)
        write(commands[5])
        sleep(0.1)
        send("Enter")
        sleep(0.1)
    window.after(50, clicked)



window = Tk()
window.title("Command Binder")
window.geometry("410x240")
window.resizable(width=False, height=False)
try:
    window.iconbitmap("eraser.ico")
except:
    pass

line = Label(window, text="──────────────────────────────────────────────────────")
line.place(x=-10, y=40)
textchat = Label(window, text="Открытие чата: ")
textchat.place(x=10, y=20)
chat = Entry(window, width=10)
chat.place(x=110, y=21)
start = Button(window, text="Нажмите для запуска", command=clicked)
start.place(x=270, y=18)

commandtext = Label(window, text="Команда:")
commandtext.place(x=10, y=60)
command = Entry(window, width=20)
command.place(x=75, y=61)
commandtext2 = Label(window, text="Команда: ")
commandtext2.place(x=10, y=90)
command2 = Entry(window, width=20)
command2.place(x=75, y=91)
commandtext3 = Label(window, text="Команда:")
commandtext3.place(x=10, y=120)
command3 = Entry(window, width=20)
command3.place(x=75, y=121)
commandtext4 = Label(window, text="Команда: ")
commandtext4.place(x=10, y=150)
command4 = Entry(window, width=20)
command4.place(x=75, y=151)
commandtext5 = Label(window, text="Команда:")
commandtext5.place(x=10, y=180)
command5 = Entry(window, width=20)
command5.place(x=75, y=181)
commandtext6 = Label(window, text="Команда: ")
commandtext6.place(x=10, y=210)
command6 = Entry(window, width=20)
command6.place(x=75, y=211)



hotkeytext = Label(window, text="Горячая клавиша:")
hotkeytext.place(x=220, y=60)
hotkey = Entry(window, width=10)
hotkey.place(x=325, y=61)
hotkeytext2 = Label(window, text="Горячая клавиша: ")
hotkeytext2.place(x=220, y=90)
hotkey2 = Entry(window, width=10)
hotkey2.place(x=325, y=91)
hotkeytext3 = Label(window, text="Горячая клавиша:")
hotkeytext3.place(x=220, y=120)
hotkey3 = Entry(window, width=10)
hotkey3.place(x=325, y=121)
hotkeytext4 = Label(window, text="Горячая клавиша: ")
hotkeytext4.place(x=220, y=150)
hotkey4 = Entry(window, width=10)
hotkey4.place(x=325, y=151)
hotkeytext5 = Label(window, text="Горячая клавиша:")
hotkeytext5.place(x=220, y=180)
hotkey5 = Entry(window, width=10)
hotkey5.place(x=325, y=181)
hotkeytext6 = Label(window, text="Горячая клавиша: ")
hotkeytext6.place(x=220, y=210)
hotkey6 = Entry(window, width=10)
hotkey6.place(x=325, y=211)

window.mainloop()

#мне было лень делать нормальный, не блочный код, поэтому, если тебя что-то не нравится, то завались, так как ты
#пользуешься моей программой, которую я сделал за 2 часов поедая нагетсы и смотря аниме.