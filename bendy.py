import ctypes
import json
import keyboard
import os
from string import punctuation
import time
from tkinter import *
from tkinter import messagebox
from ctypes import windll


class Bendy:

    def __init__(self):
        self.Tk = Tk()

        if not self.is_admin():
            self.Tk.withdraw()
            messagebox.showerror('Bendy the binder', 'Ошибка. Программа запущена не от имени администратора.')
            return

        self.GWL_EXSTYLE = -20
        self.WS_EX_APPWINDOW = 0x00040000
        self.WS_EX_TOOLWINDOW = 0x00000080

        self.var_send = False
        self.var_chat = False

        self.config = {"auto_send": True,
                       "auto_chat": False,
                       "auto_send_button": "Enter",
                       "auto_chat_button": "t",
                       "command_and_hotkey": [
                           [
                               "",
                               ""
                           ]
                       ]
                       }
        self.check = ["auto_send", "auto_chat", "auto_send_button", "auto_chat_button", "command_and_hotkey"]
        try:
            with open("bendy_config.json", "r") as file:
                config_info = json.load(file)
                for i in self.check:
                    if not config_info.get(i) and config_info.get(i) != False:
                        break
                    if i == self.check[-1]:
                        self.config = config_info
        except:
            pass

        self.Tk.overrideredirect(True)
        self.Tk.config(bg="gray13")
        self.Tk.resizable(width=False, height=False)
        self.Tk.title("Bendy the binder")

        try:
            self.Tk.iconbitmap("icon.ico")
        except:
            pass

        # ==== BORDER ====
        self.Tk.borderFrame = Frame(width=450, height=20, bg="gray20")
        self.Tk.borderFrame.pack_propagate(False)
        self.Tk.borderFrame.pack(side=TOP)

        self.Tk.helloText = Label(self.Tk.borderFrame, text="Bendy the binder",
                                  bg="gray20", fg="orange")
        self.Tk.helloText.pack(side=LEFT)

        self.Tk.exit_button = Button(self.Tk.borderFrame, text="  X  ", command=self.exit,
                                     bd=0, bg="gray20", fg="orange")
        self.Tk.exit_button.pack(side=RIGHT)
        self.Tk.exit_button.bind("<Enter>", self.on_enter_exit)
        self.Tk.exit_button.bind("<Leave>", self.on_leave_exit)

        self.Tk.borderFrame.bind("<Button-1>", self.start_move)
        self.Tk.borderFrame.bind("<ButtonRelease-1>", self.stop_move)
        self.Tk.borderFrame.bind("<B1-Motion>", self.moving)
        self.Tk.borderFrame.bind("<Map>", self.frame_mapped)

        # ==== RIGHT FRAME ====
        self.Tk.rightFrame = Frame(width=350, height=270, bg="gray13")
        self.Tk.rightFrame.pack_propagate(False)
        self.Tk.rightFrame.pack(side=RIGHT)

        # ==== LEFT FRAME ====
        self.Tk.leftFrame = Frame(width=100, height=270, bg="gray10")
        self.Tk.leftFrame.pack_propagate(False)
        self.Tk.leftFrame.pack(side=LEFT)

        self.Tk.add = Button(self.Tk.leftFrame, text="ADD BIND",
                             bd=0, bg="gray10", fg="orange", height=2, width=20, command=self.create_bendy)
        self.Tk.add.pack(side=TOP)
        self.Tk.add.bind("<Enter>", self.on_enter_left)
        self.Tk.add.bind("<Leave>", self.on_leave_left)

        self.Tk.dell = Button(self.Tk.leftFrame, text="DELETE BIND",
                              bd=0, bg="gray10", fg="orange", height=2, width=20, command=self.delete_bendy)
        self.Tk.dell.pack(side=TOP)
        self.Tk.dell.bind("<Enter>", self.on_enter_left)
        self.Tk.dell.bind("<Leave>", self.on_leave_left)

        self.checkEnterVar = BooleanVar()
        self.checkEnterVar.set(self.config.get("auto_send"))
        self.Tk.checkEnter = Checkbutton(self.Tk.leftFrame, text="Auto send".upper(), variable=self.checkEnterVar,
                                         onvalue=1, offvalue=0, command=self.change_var1,
                                         bg="gray10", fg="orange", selectcolor="gray10", height=2, width=20)
        self.Tk.checkEnter.pack(side=TOP)
        self.Tk.checkEnter.bind("<Enter>", self.on_enter_left)
        self.Tk.checkEnter.bind("<Leave>", self.on_leave_left)

        self.Tk.EnterBind = Entry(self.Tk.leftFrame, width=20, bg="gray10", fg="orange", bd=1)
        self.Tk.EnterBind.insert(0, self.config.get("auto_send_button"))
        self.Tk.EnterBind.pack(side=TOP, pady=7, padx=10)

        self.checkOpenChatVar = BooleanVar()
        self.checkOpenChatVar.set(self.config.get("auto_chat"))
        self.Tk.checkOpenChat = Checkbutton(self.Tk.leftFrame, text="Auto chat".upper(),
                                            variable=self.checkOpenChatVar,
                                            onvalue=1, offvalue=0, command=self.change_var2,
                                            bg="gray10", fg="orange", selectcolor="gray10", height=2, width=20)
        self.Tk.checkOpenChat.pack(side=TOP)
        self.Tk.checkOpenChat.bind("<Enter>", self.on_enter_left)
        self.Tk.checkOpenChat.bind("<Leave>", self.on_leave_left)

        self.Tk.OpenChatBind = Entry(self.Tk.leftFrame, width=20, bg="gray10", fg="orange", bd=1)
        self.Tk.OpenChatBind.insert(0, self.config.get("auto_chat_button"))
        self.Tk.OpenChatBind.pack(side=TOP, pady=8, padx=10)

        self.Tk.save = Button(self.Tk.leftFrame, text="SAVE",
                              bd=0, bg="gray10", fg="orange", height=2, width=20, command=self.save)
        self.Tk.save.pack(side=TOP)
        self.Tk.save.bind("<Enter>", self.on_enter_left)
        self.Tk.save.bind("<Leave>", self.on_leave_left)

        for conf in self.config.get("command_and_hotkey"):
            self.create_bendy(conf)

        self.Tk.bind_all("<Key>", self.button_chat)
        self._rus_chars = u"ё!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
        self._eng_chars = u"~!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
        self._trans_table = dict(zip(self._rus_chars, self._eng_chars))

        self.Tk.after(10, self.start_bendy())

        self.Tk.after(10, self.set_appwindow)
        self.Tk.mainloop()

    # Check before start
    def is_admin(self):
        try:
            return os.getuid() == 0
        except AttributeError:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0

    # Make Icon in taskbar
    def set_appwindow(self):
        hwnd = windll.user32.GetParent(self.Tk.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, self.GWL_EXSTYLE)
        style = style & ~self.WS_EX_TOOLWINDOW
        style = style | self.WS_EX_APPWINDOW
        windll.user32.SetWindowLongW(hwnd, self.GWL_EXSTYLE, style)

        self.Tk.wm_withdraw()
        self.Tk.after(10, lambda: self.Tk.wm_deiconify())

    # Checkbox changer
    def change_var1(self):
        if not self.var_send:
            self.var_send = True
        else:
            self.var_send = False

    def change_var2(self):
        if not self.var_chat:
            self.var_chat = True
        else:
            self.var_chat = False

    # Moving part
    def start_move(self, event):
        global x, y
        x = event.x
        y = event.y

    def stop_move(self, event):
        global x, y
        x = None
        y = None

    def moving(self, event):
        global x, y
        x_ = (event.x_root - x)
        y_ = (event.y_root - y)
        self.Tk.geometry("+%s+%s" % (x_, y_))

    def frame_mapped(self, e):
        self.Tk.update_idletasks()
        self.Tk.overrideredirect(True)
        self.Tk.state('normal')

    # Visual part
    def on_enter_left(self, e):
        e.widget['background'] = 'gray14'
        e.widget['foreground'] = 'white'
        e.widget['activebackground'] = 'gray14'
        e.widget['activeforeground'] = 'white'

    def on_leave_left(self, e):
        e.widget['background'] = 'gray10'
        e.widget['foreground'] = 'orange'

    def on_enter_exit(self, e):
        e.widget['background'] = 'red'
        e.widget['foreground'] = 'white'
        e.widget['activebackground'] = 'red'
        e.widget['activeforeground'] = 'white'

    def on_leave_exit(self, e):
        e.widget['background'] = 'gray20'
        e.widget['foreground'] = 'orange'

    # Buttons
    def create_bendy(self, conf=None):
        if conf is None:
            conf = ["", ""]

        self.Tk.bendy = Frame(self.Tk.rightFrame, width=10, bg=f"gray13")
        self.Tk.bendy.pack(side=TOP)

        self.Tk.bendy.commandtext = Label(self.Tk.bendy, text="Command:", height=1)
        self.Tk.bendy.commandtext.pack(side=LEFT, pady=6)
        self.Tk.bendy.command = Entry(self.Tk.bendy)
        self.Tk.bendy.command.pack(side=LEFT, pady=6, padx=7.5)
        self.Tk.bendy.command.insert(0, conf[0])

        self.Tk.bendy.hotkeytext = Label(self.Tk.bendy, text="Hotkey:")
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

    def delete_bendy(self):
        if len(self.Tk.rightFrame.winfo_children()) > 8:
            self.Tk.rightFrame.winfo_children()[::-1][0].destroy()
            self.Tk.rightFrame.config(height=round(33.75 * (len(self.Tk.rightFrame.winfo_children()))))
            self.Tk.leftFrame.config(height=round(33.75 * (len(self.Tk.rightFrame.winfo_children()))))

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
            event.keysym = event.keysym.replace("_L", "").replace("_R",
                                                                  "") if "Lock" not in event.keysym else event.keysym
            send_button.delete(0, len(send_button.get()))
            if event.keysym != "BackSpace":
                send_button.insert(1, event.keysym)

    def save(self):
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

        for i in range(0, len(widgets), 2):
            output["command_and_hotkey"].append([widgets[i], widgets[i + 1]])

        with open("bendy_config.json", "w") as file:
            json.dump(output, file, indent=4)

    def exit(self):
        self.Tk.destroy()

    # Start
    def start_bendy(self):
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
                except:
                    continue
        self.Tk.after(10, self.start_bendy)


def run():
    Bendy()


if __name__ == '__main__':
    run()
