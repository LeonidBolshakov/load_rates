from parse_input_parametrs import InputParametrs
from datetime import timedelta
import sys
import csv
from tkinter import *
from tkinter import ttk
import requests
from bs4 import BeautifulSoup

# URL адрес ЦБ РФ без даты, за которую запрашиваются курсы валют
URL_WITHOUT_DATE = 'https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To='

# Формирование "списка" кортежей курсов валют за конкретную дату. Источник - майт ЦБ РФ.
def get_record_rate(dat):
    url = URL_WITHOUT_DATE + dat
    try:
        resp = requests.get(url)
    except:
        Button(text='Не смогли добраться до сайта ЦБ РФ. '
                    '\nПроверьте доспуп к интернету,'
                    '\nповторите попытку позже.',
               command=lambda:sys.exit()).pack(expand=TRUE)
        root.mainloop()

# Разбор ответа ЦБ РФ
    soup = BeautifulSoup(resp.text, 'html.parser')
    rates = soup.find_all('tr')
    for rate in rates:
        rec = rate.find_all('td')

        if len(rec) > 1:
#                         date currency_symbol multiplicity currency_name rate
            record_out = (dat, rec[1].text, rec[2].text, rec[3].text, rec[4].text.replace(',', '.'))
            yield record_out


# Выгрузка курсов валют с сайта ЦБ РФ
def load_rate(start, stop, lst_reult_currence):
    date = start
    date_step = timedelta(days=1)
    value_var = IntVar()
    value_var.set(0)
    dif_days = (stop-start).days + 1
    ttk.Progressbar(variable=value_var, maximum=dif_days).pack(expand=TRUE)
    record_all = []
    while date <= stop:
        value_var.set(value_var.get() + 1)
        root.update()
        for record_day in get_record_rate(date.strftime('%d.%m.%Y')):
            if record_day[1] in lst_reult_currence:
                record_all.append(record_day)
        date += date_step
    write_rates_csv(record_all)
    Button(text='Выгрузка завершена!', command=lambda: root.destroy()).pack(expand=TRUE)


# запись "списка" кортежей валют в CSV файл
def write_rates_csv(rec_all):
    with open('rates.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';', lineterminator='\n')
        for record in rec_all:
            writer.writerow(record)


# Ввод начальной и конечной дат и выбор курсов валют
root = Tk()
input_parametrs = InputParametrs(root, get_record_rate, load_rate)
input_parametrs.run()



