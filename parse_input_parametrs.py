from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from bs4 import BeautifulSoup
import time


class InputParametrs():

    def __init__(self, root, get_record_rate, load_rate):
        self.lst_reult_currence = []
        self._listbox = []
        self._load_rate = load_rate
        self.button_run = Button()
        self._root = root
        self._get_record_rate = get_record_rate
        self._root.geometry('300x400')
        self._root.title('Курсы валют ЦБ РФ')

        self.start: DateEntry()
        self.stop: DateEntry()
        self._init_label = [('Выгрузка курсов валют ЦБ РФ', 'green', 16),
                            ('в csv (EXCEL) файл', 'green', 12),
                            ('Интервал дат', 'blue', 12)
                           ]


# Создание меток формы
    def create_label(self, text, color, font_size):
        ttk.Label(font=('Roboto Condensed', font_size),
                  foreground=color, text=text).pack(expand=TRUE)


# Обработка нажатия кнопки "Далее"
    def click_button_next(self):
        self.button_next['state'] = 'disable'
        self._root.update()
        self._listbox = Listbox(selectmode=MULTIPLE,
                          font = ('courier new', 11), width=30)
        for cur in self._get_record_rate(str(self.start.get_date())):
            self._listbox.insert(END, cur[1] + '  ->  ' + cur[3])
        self._listbox.pack(expand=TRUE)
        self.button_run = ttk.Button(text='Приступить к выгрузке', command=self.click_button_run)
        self.button_run.pack(expand=TRUE)



# Обработка нажатия кнопки "Приступить к выгрузке"
    def click_button_run(self):
        self.button_run['state'] = 'disable'
        self._root.update()
        list_currency = self._listbox.curselection()
        for currence in list_currency:
            cur = self._listbox.get(currence).split()
            self.lst_reult_currence.append(cur[0])
        self._load_rate(self.start.get_date(), self.stop.get_date(), self.lst_reult_currence)

        
        
    def get_parametrs(self):
        return(self.start, self.stop, self.lst_reult_currence)


    def run(self):
        self.create_label(*self._init_label[0])
        self.create_label(*self._init_label[1])
        self.create_label(*self._init_label[2])
        self._root.update()
        self.start = DateEntry(self._root, selectmode='day', locale='ru')
        self.start.pack(expand=TRUE)
        self.stop  = DateEntry(self._root, selectmode='day', locale='ru')
        self.stop.pack(expand=TRUE)
        self.button_next = ttk.Button(text='Далее', command=self.click_button_next)
        self.button_next.pack(expand=TRUE)

        self._root.mainloop()
