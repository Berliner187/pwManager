import datetime
import os
from enc_module import enc_data, dec_data


yellow, blue, purple, green, mc, red = "\033[33m", "\033[36m", "\033[35m", "\033[32m", "\033[0m", "\033[31m"
main_folder = 'data/'
file_self_name = main_folder + ".self_name.dat"  # Файл с именем (никнеймом)


def greeting(master_password):   # Greating Depending On Date Time
    """ Фунция вывода приветствия в зависимости от времени суток """
    def time(name):
        hms = datetime.datetime.today()  # Дата и время
        hour = int(hms.hour)  # Формат часов
        minute = int(hms.minute)  # Формат минут
        secunde = int(hms.second)  # Формат секунд
        # Для корректоного вывода
        if hour < 10:
            hour = str(0) + str(hour)
        if minute < 10:
            minute = str(0) + str(minute)
        if secunde < 10:
            secunde = str(0) + str(secunde)
        time_format = (str(hour), str(minute), str(secunde))
        time_now = ":".join(time_format)  # Форматирование в формат времени
        if '04:00:00' <= time_now < '12:00:00':  # Condition morning
            seq = (green, 'Good morning,', name, mc)
            total = " ".join(seq)
            return total
        elif '12:00:00' <= time_now < '17:00:00':  # Condition day
            seq = (green, 'Good afternoon,', name, mc)
            total = " ".join(seq)
            return total
        elif '17:00:00' <= time_now <= '23:59:59':  # Condition evening
            seq = (green, 'Good evening,', name, mc)
            total = " ".join(seq)
            return total
        elif '00:00:00' <= time_now < '04:00:00':  # Condition night
            seq = (green, 'Good night,', name, mc)
            total = " ".join(seq)
            print(total)
    if os.path.exists(file_self_name) == bool(False):  # Создание файла с именем
        with open(file_self_name, "w") as self_name:
            name = input(yellow + ' - Your name or nickname: ' + mc)
            enc_name = enc_data(name, master_password)
            self_name.write(enc_name)
            self_name.close()
            print(time(name))
    else:  # Чтение из файла с именем и вывод в консоль
        with open(file_self_name, "r") as self_name:
            dec_name = self_name.readline()
            name = dec_data(dec_name, master_password)
            print(time(name))
