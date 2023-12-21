import sys
import os
import shutil
from pathlib import Path
import subprocess
import ctypes
import tkinter

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def warning():
    print("Для выполнения программы нужны права администратора.")
    input("Для продолжения нажмите Enter")

home_path = Path.home()

def Clean(temp_folder):
    warning()
    if not is_admin():
        print("Запустите программу с правами администратора")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit(0)
    else:
        print("1 - очистить временные файлы\n2 - очистить журнал событий")
        sel = input("Выберите действие: ")
        match sel:
            case '1':
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
                    print("очистка выполнена успешно")
                except Exception as ex:
                    print(ex)
            case '2':
                try:
                    command = 'wevtutil cl System && wevtutil cl Application && wevtutil cl Security'
                    subprocess.call(command, shell=True)
                except Exception as ex:
                    print(ex)


temp_folder = home_path / "AppData" / "Local" / "Temp"

Clean(temp_folder)