import json
import time
from ctypes import windll
from string import punctuation
from tkinter import *

import keyboard

from tools.utils import *
from tools.visual import *


class Bendy:

    def __init__(self):
        # Создание экземпляра класса.
        self.Tk = Tk()

        # Предупреждение пользователя о запуске программы не от имени администратора.
        if not is_admin():
            self.Tk.withdraw()
            messagebox.showwarning('Bendy the binder', 'Предупреждение!\n'
                                                       'Программа запущена не от имени администратора.\n'
                                                       'Программа может функционировать некорректно.')

        # Создание словаря для смены русских символов для горячих клавиш.
        self._rus_chars = u"ё!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
        self._eng_chars = u"~!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
        self._trans_table = dict(zip(self._rus_chars, self._eng_chars))
        del self._eng_chars

        # Создание переменных для работы чек-боксов.
        self.checkEnterVar = None
        self.checkOpenChatVar = None

        # Получение конфиг-файла для преднастройки.
        self.config: dict = get_config(self.Tk)
        self.var_chat: bool = self.config["auto_chat"]
        self.var_send: bool = self.config["auto_send"]

        # Начальная настройка приложения.
        self.Tk.overrideredirect(True)
        self.Tk.config(bg="gray13")
        self.Tk.resizable(width=False, height=False)
        self.Tk.title("Bendy the binder")

        try:
            self.Tk.iconbitmap("icon.ico")
        except TclError:
            pass

        # Инициализация внутренних частей программы.
        self.top_menu()
        self.right_frame()
        self.left_frame()
        self.Tk.after(10, self.read_bendy())

        self.Tk.after(10, self.set_appwindow)
        self.Tk.mainloop()

    # Показ иконки приложения на панели задач. (Windows only)
    def set_appwindow(self):
        hwnd = windll.user32.GetParent(self.Tk.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, -20)
        style = style & ~0x00000080
        style = style | 0x00040000
        windll.user32.SetWindowLongW(hwnd, -20, style)

        self.Tk.wm_withdraw()
        self.Tk.after(10, lambda: self.Tk.wm_deiconify())

    # Изменение состояния чек-боксов.
    def change_var1(self):
        self.var_send = not self.var_send

    def change_var2(self):
        self.var_chat = not self.var_chat

    # Функции для перемещения окна.
    @staticmethod
    def start_move(event):
        global x, y
        x = event.x
        y = event.y

    @staticmethod
    def stop_move(event):
        del event
        global x, y
        x = None
        y = None

    def moving(self, event):
        global x, y
        x_ = (event.x_root - x)
        y_ = (event.y_root - y)
        self.Tk.geometry("+%s+%s" % (x_, y_))

    def frame_mapped(self, e):
        del e
        self.Tk.update_idletasks()
        self.Tk.overrideredirect(True)
        self.Tk.state('normal')

    # Верхняя панель программы.
    def top_menu(self):
        self.Tk.menuFrame = Frame(width=450, height=20, bg="gray20")
        self.Tk.menuFrame.pack_propagate(False)
        self.Tk.menuFrame.pack(side=TOP)

        self.Tk.helloText = Label(self.Tk.menuFrame, text="BENDY THE BINDER",
                                  bg="gray20", fg="orange")
        self.Tk.helloText.pack(side=LEFT)

        self.Tk.exitButton = Button(self.Tk.menuFrame, text="  X  ", command=self.exit,
                                    bd=0, bg="gray20", fg="orange")
        self.Tk.exitButton.pack(side=RIGHT)
        self.Tk.exitButton.bind("<Enter>", on_enter_exit)
        self.Tk.exitButton.bind("<Leave>", on_leave_exit)

        for frame in [self.Tk.menuFrame, self.Tk.helloText]:
            frame.bind("<Button-1>", self.start_move)
            frame.bind("<ButtonRelease-1>", self.stop_move)
            frame.bind("<B1-Motion>", self.moving)
            frame.bind("<Map>", self.frame_mapped)

    # Левая панель программы с функциональными инструментами.
    def left_frame(self):
        self.Tk.leftFrame = Frame(width=100, height=270, bg="gray10")
        self.Tk.leftFrame.pack_propagate(False)
        self.Tk.leftFrame.pack(side=LEFT)

        self.Tk.add = Button(self.Tk.leftFrame, text="ADD BIND",
                             bd=0, bg="gray10", fg="orange", height=2, width=20, command=self.create_bendy)
        self.Tk.add.pack(side=TOP)
        self.Tk.add.bind("<Enter>", on_enter_left)
        self.Tk.add.bind("<Leave>", on_leave_left)

        self.Tk.dell = Button(self.Tk.leftFrame, text="DELETE BIND",
                              bd=0, bg="gray10", fg="orange", height=2, width=20, command=self.delete_bendy)
        self.Tk.dell.pack(side=TOP)
        self.Tk.dell.bind("<Enter>", on_enter_left)
        self.Tk.dell.bind("<Leave>", on_leave_left)

        self.checkEnterVar = BooleanVar()
        self.checkEnterVar.set(self.config.get("auto_send"))
        self.Tk.checkEnter = Checkbutton(self.Tk.leftFrame, text="AUTO SEND", variable=self.checkEnterVar,
                                         onvalue=1, offvalue=0, command=self.change_var1,
                                         bg="gray10", fg="orange", selectcolor="gray10", height=2, width=20)
        self.Tk.checkEnter.pack(side=TOP)
        self.Tk.checkEnter.bind("<Enter>", on_enter_left)
        self.Tk.checkEnter.bind("<Leave>", on_leave_left)

        self.Tk.EnterBind = Entry(self.Tk.leftFrame, width=20, bg="gray10", fg="orange", bd=1)
        self.Tk.EnterBind.insert(0, self.config.get("auto_send_button"))
        self.Tk.EnterBind.pack(side=TOP, pady=7, padx=10)

        self.checkOpenChatVar = BooleanVar()
        self.checkOpenChatVar.set(self.config.get("auto_chat"))
        self.Tk.checkOpenChat = Checkbutton(self.Tk.leftFrame, text="AUTO CHAT",
                                            variable=self.checkOpenChatVar,
                                            onvalue=1, offvalue=0, command=self.change_var2,
                                            bg="gray10", fg="orange", selectcolor="gray10", height=2, width=20)
        self.Tk.checkOpenChat.pack(side=TOP)
        self.Tk.checkOpenChat.bind("<Enter>", on_enter_left)
        self.Tk.checkOpenChat.bind("<Leave>", on_leave_left)

        self.Tk.OpenChatBind = Entry(self.Tk.leftFrame, width=20, bg="gray10", fg="orange", bd=1)
        self.Tk.OpenChatBind.insert(0, self.config.get("auto_chat_button"))
        self.Tk.OpenChatBind.pack(side=TOP, pady=8, padx=10)

        self.Tk.save = Button(self.Tk.leftFrame, text="SAVE",
                              bd=0, bg="gray10", fg="orange", height=2, width=20, command=self.save)
        self.Tk.save.pack(side=TOP)
        self.Tk.save.bind("<Enter>", on_enter_left)
        self.Tk.save.bind("<Leave>", on_leave_left)

        for conf in self.config.get("command_and_hotkey"):
            self.create_bendy(conf)

        self.Tk.bind_all("<Key>", self.button_chat)

    # Часть с биндами. Изначально пустая. Добавление проводится через create_bendy.
    def right_frame(self):
        self.Tk.rightFrame = Frame(width=350, height=270, bg="gray13")
        self.Tk.rightFrame.pack_propagate(False)
        self.Tk.rightFrame.pack(side=RIGHT)

    # Добавление новых биндов.
    def create_bendy(self, conf: dict = None):
        if conf is None:
            conf = ["", ""]

        self.Tk.bendy = Frame(self.Tk.rightFrame, width=10, bg=f"gray13")
        self.Tk.bendy.pack(side=TOP)

        self.Tk.bendy.commandtext = Label(self.Tk.bendy, text="COMMAND:", height=1)
        self.Tk.bendy.commandtext.pack(side=LEFT, pady=6)
        self.Tk.bendy.command = Entry(self.Tk.bendy)
        self.Tk.bendy.command.pack(side=LEFT, pady=6, padx=7.5)
        self.Tk.bendy.command.insert(0, conf[0])

        self.Tk.bendy.hotkeytext = Label(self.Tk.bendy, text="HOTKEY:")
        self.Tk.bendy.hotkeytext.pack(side=LEFT)
        self.Tk.bendy.hotkey = Entry(self.Tk.bendy, width=12)
        self.Tk.bendy.hotkey.pack(side=LEFT, padx=7.5)
        self.Tk.bendy.hotkey.insert(0, conf[1])

        self.Tk.bendy.commandtext.configure(bg="gray13", fg="orange")
        self.Tk.bendy.command.configure(bg="gray13", fg="orange")
        self.Tk.bendy.hotkeytext.configure(bg="gray13", fg="orange")
        self.Tk.bendy.hotkey.configure(bg="gray13", fg="orange")

        if len(self.Tk.rightFrame.winfo_children()) > 8:
            self.Tk.rightFrame.config(height=round(33.75 * (len(self.Tk.rightFrame.winfo_children()))))
            self.Tk.leftFrame.config(height=round(33.75 * (len(self.Tk.rightFrame.winfo_children()))))

    # Удаление последнего бинда.
    def delete_bendy(self):
        if len(self.Tk.rightFrame.winfo_children()) > 8:
            self.Tk.rightFrame.winfo_children()[::-1][0].destroy()
            self.Tk.rightFrame.config(height=round(33.75 * (len(self.Tk.rightFrame.winfo_children()))))
            self.Tk.leftFrame.config(height=round(33.75 * (len(self.Tk.rightFrame.winfo_children()))))

    # Запись горячей клавиши.
    def button_chat(self, event):
        send_button = None

        for widget in self.Tk.leftFrame.winfo_children():
            if isinstance(widget, Entry):
                if self.Tk.focus_get() == widget:
                    send_button = widget
                    break

        i = 0
        for bendy_widget in self.Tk.rightFrame.winfo_children():
            for widget in bendy_widget.winfo_children():
                if isinstance(widget, Entry):
                    if self.Tk.focus_get() == widget:
                        if i % 2 != 0:
                            send_button = widget
                            break
                    i += 1

        if send_button:
            if send_button.get() != "" and event.keysym[0].lower() == event.keysym[0]:
                if send_button.get()[-1] != event.keysym and send_button.get()[-1] in punctuation:
                    event.keysym = send_button.get()[-1]
                elif send_button.get()[-1] in self._rus_chars:
                    event.keysym = self._trans_table.get(send_button.get()[-1])
            for s in ["_L", "_R"]:
                event.keysym = event.keysym[:-2] if event.keysym[-2:] == s else event.keysym
            event.keysym = event.keysym.replace("Return", "Enter")
            send_button.delete(0, len(send_button.get()))
            if event.keysym != "BackSpace":
                send_button.insert(1, event.keysym)

    # Сохранение настроек пользователя в конфиг.
    def save(self):
        output = {"auto_send": self.var_send,
                  "auto_chat": self.var_chat,
                  "auto_send_button": "Enter",
                  "auto_chat_button": "t",
                  "command_and_hotkey": []
                  }
        auto_send = False
        for widget in self.Tk.leftFrame.winfo_children():
            if isinstance(widget, Entry):
                if not auto_send:
                    output["auto_send_button"] = widget.get()
                    auto_send = True
                else:
                    output["auto_chat_button"] = widget.get()

        widgets = []
        for bendy_widget in self.Tk.rightFrame.winfo_children():
            for widget in bendy_widget.winfo_children():
                if isinstance(widget, Entry):
                    widgets.append(widget.get())

        for i in range(0, len(widgets), 2):
            output["command_and_hotkey"].append([widgets[i], widgets[i + 1]])

        try:
            with open("bendy_config.json", "w") as file:
                json.dump(output, file, indent=4)
        except PermissionError:
            self.Tk.withdraw()
            messagebox.showerror('Bendy the binder', 'Ошибка! Недостаточно прав для сохранения конфига.')

    # Закрытие программы.
    def exit(self):
        self.Tk.destroy()

    # Запуск постоянного цикла для чтения биндов и последующего выполнения.
    def read_bendy(self):
        output = {"auto_send": self.var_send,
                  "auto_chat": self.var_chat,
                  "auto_send_button": "Enter",
                  "auto_chat_button": "t",
                  "command_and_hotkey": []
                  }

        auto_send = 0
        for widget in self.Tk.leftFrame.winfo_children():
            if isinstance(widget, Entry):
                if not auto_send:
                    output["auto_send_button"] = widget.get()
                    auto_send = 1
                else:
                    output["auto_chat_button"] = widget.get()
                    auto_send = 2

        widgets = []
        for bendy_widget in self.Tk.rightFrame.winfo_children():
            for widget in bendy_widget.winfo_children():
                if isinstance(widget, Entry):
                    widgets.append(widget.get())

        if not self.Tk.focus_get():
            for i in range(0, len(widgets), 2):
                try:
                    if keyboard.is_pressed(widgets[i + 1]):
                        if self.var_chat:
                            keyboard.send(output.get("auto_chat_button"))
                            time.sleep(0.1)
                        keyboard.write(widgets[i])
                        time.sleep(0.2)
                        if self.var_send:
                            keyboard.send(output.get("auto_send_button"))
                            time.sleep(0.1)
                except ValueError:
                    continue
        self.Tk.after(10, self.read_bendy)


if __name__ == '__main__':
    Bendy()
