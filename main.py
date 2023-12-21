import sys
import os
import shutil
from pathlib import Path
import subprocess
import ctypes
import tkinter as tk

root = tk.Tk()
root.geometry("300x200")
root.title("Сleaner")

Info = tk.Label()
Info.pack()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

home_path = Path.home()

def CleanTemp():
    temp_folder = home_path / "AppData" / "Local" / "Temp"
    if not is_admin():
        Info.config(text="Запустите программу с правами администратора")
        #ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:
        try:
            file_list = os.listdir(temp_folder)
            for file_name in file_list:
                file_path = os.path.join(temp_folder, file_name)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        os.rmdir(file_path)
                except Exception as ex:
                    print(ex)
            Info.config(text="Очистка временных файлов выполнена успешно")
        except Exception as ex:
            print(ex)

def LogClear():
    if not is_admin():
        Info.config(text="Запустите программу с правами администратора")
        #ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:
        try:
            command = 'wevtutil cl System && wevtutil cl Application && wevtutil cl Security'
            subprocess.call(command, shell=True)
            Info.config(text="Очистка журнала выполнена успешно")
        except Exception as ex:
            print(ex)

CleanTempButton = tk.Button(command=CleanTemp, text="Очистить временные файлы")
CleanTempButton.pack()

CleanLogsButton = tk.Button(command=LogClear, text="Очистить журнал windows")
CleanLogsButton.pack()

root.mainloop()