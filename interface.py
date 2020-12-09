from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox as mb
from tkinter import filedialog
import infinity_suffer
import threading
import keyboard
import log_maker
import sikuli.TF
import sikuli.bat_maker
import logging
import os
import ctypes



class suicide_thred(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


formatter = logging.Formatter('%(asctime)s. %(message)s')
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


class tkinter_interface():
    def __init__(self):
        self.main_window = None
        self.logger_for_default = None
        self.logger_for_graphics = None
        self.path = None
        self.pathes = {'sikuli_path' : None,'sikuli_script' : None}



    def threds_killer(self,*threds):
        while True:
            if keyboard.is_pressed('esc'):
                for i in threds:
                    try:
                        i.kill()
                        print('poluchlos`')
                    except:
                        print('ebat')
                break


    def folder_path_changer(self, type, key = None):
        if type == 'var':
            self.path = filedialog.askdirectory()

        elif type == 'dict':
            self.pathes[key] = filedialog.askopenfilename()



    def default(self):
        if self.path:
            self.logger_for_default = setup_logger('default_stats', self.path + '/default_log.txt')
            A_L = infinity_suffer.action_logger(log = self.logger_for_default)
            U_P = infinity_suffer.user_press(log = self.logger_for_default,path = self.path)
            keyboard_th = suicide_thred(target=U_P.start_lis)
            mouse_th = suicide_thred(target=U_P.mouse)
            exe_and_spec = suicide_thred(target=infinity_suffer.loop, args=(A_L, U_P,))
            # threds_killer = suicide_thred(target=self.threds_killer, args=(keyboard_th, mouse_th,exe_and_spec,))
            keyboard_th.start()
            exe_and_spec.start()
            mouse_th.start()
            # threds_killer.start()


    def graphics(self):
        if self.path:
            self.logger_for_default = setup_logger('default_stats', self.path + '/default_log.txt')
            self.logger_for_graphics = setup_logger('graphics_stats', self.path + '/graphics_log.txt')
            A_L = infinity_suffer.action_logger(log=self.logger_for_default)
            U_P = infinity_suffer.user_press(log=self.logger_for_default, path=self.path)
            keyboard_th = suicide_thred(target=U_P.start_lis)
            mouse_th = suicide_thred(target=U_P.mouse)
            exe_and_spec = suicide_thred(target=infinity_suffer.loop, args=(A_L, U_P,))
            keyboard_th.start()
            exe_and_spec.start()
            mouse_th.start()
            T_F = sikuli.TF.Action_Logger(path = self.path,log = self.logger_for_graphics)
            keys = suicide_thred(target=T_F.key_loop)
            mouses = suicide_thred(target=sikuli.TF.mouse_loop, args=(T_F,))
            # threds_killer = suicide_thred(target=self.threds_killer, args=(keyboard_th, mouse_th, exe_and_spec,keys,mouses,))
            keys.start()
            mouses.start()
            # threds_killer.start()
        else:
            print()
            ctypes.windll.user32.MessageBoxW(0, u"Не все пути заполнены", u"Ошибка", 0)


    def make_action(self):
        if self.path and self.pathes['sikuli_path'] and self.pathes['sikuli_script']:
            if not os.path.exists(self.path + '/bats'):
                path = os.path.join(self.path, 'bats')
                os.mkdir(path)
            B_M = sikuli.bat_maker.bat_maker(path_to_bat = path,
                                             path_to_log = self.path + '/graphics_log.txt',
                                             path_to_repeater = self.pathes['sikuli_script'],
                                             path_to_studio = self.pathes['sikuli_path'])
            B_M.make_files()
            rs = mb.askyesno(title='sheduler',message='add bats to sheduler?')
            if rs == True:
                self.main_window.destroy()
                self.main_window = Tk()
                self.main_window.geometry('200x150')
                self.main_window.title('Модуль для мыла')
                sedule_type = Label(self.main_window, text="Тип планировщика").grid(row=0, column=0)
                sedule_t = StringVar()
                sedule_type_e = Entry(self.main_window, textvariable=sedule_t).grid(row=0, column=1)

                task_name = Label(self.main_window, text="Имя задачи").grid(row=1, column=0)
                task = StringVar()
                task_name_e = Entry(self.main_window, textvariable=task, show='*').grid(row=1, column=1)

                go_btn = Button(self.main_window, text="Зарегистрировать",
                                     command=lambda: self.B_M.make_shedule(sedule_type_e, task_name_e)).grid(
                    row=4, column=0)
                self.main_window.mainloop()


    def make_stats(self):
        self.path = filedialog.askdirectory()
        if not os.path.exists(self.path + '/stats'):
            path = os.path.join(self.path, 'stats')
            os.mkdir(path)

        L_M = log_maker.stats(i_p = self.path + '/default_log.txt',o_p = self.path + '/stats/log_stat.txt',
                        csv = self.path + '/stats/log_stat.xlsx')
        L_M.make_stats()


if __name__ == '__main__':
    T_I = tkinter_interface()
    T_I.main_window = Tk()
    T_I.main_window.geometry("350x500")
    label = Label(T_I.main_window, text="Выберите способ записи")
    label.pack(pady=10)
    mod_0 = Button(T_I.main_window,
                 text="Путь к папке хранения",
                 command= lambda: T_I.folder_path_changer(type = 'var'))
    mod_1 = Button(T_I.main_window,
                 text="Записывать только статистику",
                 command=T_I.default)
    mod_2 = Button(T_I.main_window,
                 text="Записывать статистику и графические элементы",
                 command=T_I.graphics)
    mod_3 = Button(T_I.main_window,
                 text="Создать файлы для воспроизведения действий",
                 command=T_I.make_action)
    mod_4 = Button(T_I.main_window,
                   text="Сформировать статистику",
                   command=T_I.make_stats)
    mod_5 = Button(T_I.main_window,
                   text="Добавить путь к sikuliX(ситуативно)",
                   command=lambda: T_I.folder_path_changer(key = 'sikuli_path',type = 'dict'))
    mod_6 = Button(T_I.main_window,
                   text="Добавить путь к срипту(ситуативно)",
                   command=lambda: T_I.folder_path_changer(key = 'sikuli_script',type = 'dict'))

    mod_0.pack(pady=10)
    mod_1.pack(pady=10)
    mod_2.pack(pady=10)
    mod_3.pack(pady=10)
    mod_4.pack(pady=10)
    mod_5.pack(pady=10)
    mod_6.pack(pady=10)
    T_I.main_window.mainloop()

