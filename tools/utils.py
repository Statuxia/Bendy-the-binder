import ctypes
import json.decoder
import os
from json import load
from tkinter import messagebox


def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


def get_config(tk):
    config = {"auto_send": False,
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
    try:
        with open("bendy_config.json", "r") as file:
            try:
                config_info = load(file)
            except json.decoder.JSONDecodeError:
                tk.withdraw()
                messagebox.showerror('Bendy the binder', 'Ошибка! Конфиг не загружен.')
                return config  # Возврат стандартной конфигурации если файл поврежден.

            for arg in config:
                if config[arg] != config_info[arg]:
                    config[arg] = config_info[arg]
            return config  # Возврат конфигурации, которая может отличаться от стандартной.
    except FileNotFoundError:
        return config  # Возврат стандартной конфигурации если файла нет в текущей дериктории.
