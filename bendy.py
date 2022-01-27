from string import punctuation
from tkinter import *
import keyboard
import time


class Bendy:

    def __init__(self):
        self.Tk = Tk()
        self.Tk.resizable(width=False, height=False)
        self.Tk.title("Bendy the binder")

        self.Tk.line = Label(text="─" * 35)
        self.Tk.line.place(x=-10, y=40)
        self.Tk.open_chat_text = Label(text="Opening a chat: ")
        self.Tk.open_chat_text.place(x=10, y=16)
        self.Tk.chat = Entry(width=10)
        self.Tk.chat.place(x=100, y=18)

        self.Tk.bind_all("<Key>", self.button_chat)

        self.Tk.start = Button(text="Start", command=self.start_bendy)
        self.Tk.start.place(x=180, y=14)
        self.Tk.reset = Button(text="Reset", command=self.reset_bendy)
        self.Tk.reset.place(x=220, y=14)

        self.Tk.add = Button(text="+", command=self.create_bendy)
        self.Tk.add.place(x=275, y=14)
        self.Tk.dell = Button(text="-", command=self.delete_bendy)
        self.Tk.dell.place(x=300, y=14)

        self.create_bendy()

        self.Tk.configure(bg="gray17")
        self.Tk.line.configure(bg="gray17", fg="orange")
        self.Tk.open_chat_text.configure(bg="gray17", fg="orange")
        self.Tk.chat.configure(bg="gray16", fg="orange")
        self.Tk.start.configure(bg="gray16", fg="orange", activebackground="#DEBA55", activeforeground="orange")
        self.Tk.reset.configure(bg="gray16", fg="orange", activebackground="#DEBA55", activeforeground="orange")
        self.Tk.add.configure(bg="gray16", fg="orange", activebackground="#DEBA55", activeforeground="orange")
        self.Tk.dell.configure(bg="gray16", fg="orange", activebackground="#DEBA55", activeforeground="orange")

        try:
            self.Tk.iconbitmap("icon.ico")
        except:
            pass

        self._rus_chars = u"ё!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
        self._eng_chars = u"~!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
        self._trans_table = dict(zip(self._rus_chars, self._eng_chars))

        self.Tk.mainloop()

    def create_bendy(self):
        new_bendy = round(15 + 30 * len(self.Tk.winfo_children()) / 4)
        self.Tk.commandtext = Label(text="Command:")
        self.Tk.commandtext.place(x=10, y=new_bendy)
        self.Tk.command = Entry(width=20)
        self.Tk.command.place(x=75, y=new_bendy + 2)

        self.Tk.hotkeytext = Label(text="Hotkey:")
        self.Tk.hotkeytext.place(x=205, y=new_bendy)
        self.Tk.hotkey = Entry(width=10)
        self.Tk.hotkey.place(x=253, y=new_bendy + 2)

        self.Tk.commandtext.configure(bg="gray17", fg="orange")
        self.Tk.command.configure(bg="gray16", fg="orange")
        self.Tk.hotkeytext.configure(bg="gray17", fg="orange")
        self.Tk.hotkey.configure(bg="gray16", fg="orange")

        self.Tk.geometry(f"330x{round(15 + 30 * len(self.Tk.winfo_children()) / 4)}")

    def delete_bendy(self):
        if len(self.Tk.winfo_children()) > 7:
            for num, widget in enumerate(self.Tk.winfo_children()[::-1]):
                if num > 3:
                    break
                widget.destroy()

            self.Tk.geometry(f"330x{round(15 + 30 * len(self.Tk.winfo_children()) / 4)}")

    def reset_bendy(self):
        for widget in self.Tk.winfo_children():
            if isinstance(widget, Entry):
                widget.delete(0, "end")

    def start_bendy(self):
        self.Tk.start["state"] = "disabled"

        i = 0
        button_to_open_chat = ""
        command_and_hotkey = []

        for widget in self.Tk.winfo_children():
            if isinstance(widget, Entry):
                if i == 0:
                    button_to_open_chat = widget.get()
                else:
                    command_and_hotkey.append(widget.get())
                i += 1

        if [""] * len(command_and_hotkey) == command_and_hotkey:
            self.Tk.start["state"] = "normal"
            return

        if not self.Tk.focus_get():
            for i in range(0, len(command_and_hotkey), 2):
                try:
                    if keyboard.is_pressed(command_and_hotkey[i + 1]):
                        if button_to_open_chat != "":
                            keyboard.send(button_to_open_chat)
                            time.sleep(0.1)
                        keyboard.write(command_and_hotkey[i])
                        time.sleep(0.2)
                        keyboard.send("Enter")
                        time.sleep(0.1)
                except:
                    continue
        self.Tk.after(50, self.start_bendy)

    def button_chat(self, event):
        send_button = None
        i = 0

        for widget in self.Tk.winfo_children():
            if isinstance(widget, Entry):
                if self.Tk.focus_get() == widget:
                    if i == 0 or i % 2 == 0:
                        send_button = widget
                        break
                i += 1

        if send_button:
            print(send_button.get(), event.keysym)
            if send_button.get() != "" and event.keysym[0].lower() == event.keysym[0]:
                if send_button.get()[-1] != event.keysym and send_button.get()[-1] in punctuation:
                    event.keysym = send_button.get()[-1]
                elif send_button.get()[-1] in self._rus_chars:
                    event.keysym = self._trans_table.get(send_button.get()[-1])
            event.keysym = event.keysym.replace("_L", "").replace("_R",
                                                                  "") if "Lock" not in event.keysym else event.keysym
            send_button.delete(0, len(send_button.get()))
            send_button.insert(1, event.keysym)


def run():
    Bendy()


if __name__ == '__main__':
    run()
