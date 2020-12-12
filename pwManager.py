#!/usr/bin/env python3
# Password manager v1.1.3 Stable for Linux (SFL)
# by CISCer
import os
import csv
import base64
import random
import datetime
import time


# Colours
yellow, blue, green, mc, red = "\033[33m", "\033[34m", "\033[32m", "\033[0m", "\033[31m"  # mc - clean colours

try:    # Запуск стороннийх библиотек
    import emoji
    import stdiomask
except ModuleNotFoundError:     # Установка сторонних библиотек
    print(yellow + "... Wait ..." + mc)
    os.system("pip3 install emoji")
    os.system("pip3 install stdiomask")
    os.system("clear")
    print(green + "-- Success! --" + mc)
    time.sleep(1)
    os.system("clear")

# Emoji
shit = emoji.emojize(":poop:", use_aliases=True)
sleep = emoji.emojize(":sleeping:", use_aliases=True)
moon = emoji.emojize(":crescent_moon:", use_aliases=True)
coffee = emoji.emojize(":coffee:", use_aliases=True)
donut = emoji.emojize(":doughnut:", use_aliases=True)
smile = emoji.emojize(":stuck_out_tongue_winking_eye:", use_aliases=True)
relax = emoji.emojize(":relaxed:", use_aliases=True)
krokodil = emoji.emojize(":crocodile:", use_aliases=True)

main_lyster = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-='  # List of all symbols
lyster_for_pas = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def DateTime():
    """ Фунция вывода приветствия в зависимости от времени суток """
    self_name_file = "files/.self_name.dat"     # Файл с именем (никнеймом)
    if os.path.exists(self_name_file) == False:     # Создание файла с именем
        with open(self_name_file, "w") as self_name:
            name = input(yellow + '- Your name or nickname: ' + mc)
            self_name.write(name)
            self_name.close()
            DateTime()

    elif os.path.exists(self_name_file) == True:    # Чтение из файла с именем и вывод в консоль
        with open(self_name_file, "r") as self_name:
            for name in self_name.readlines():
                hms = datetime.datetime.today()     # Дата и время
                hour = int(hms.hour)                # Формат часов
                minute = int(hms.minute)            # Формат минут
                secunde = int(hms.second)           # Формат секунд
                # Для корректоного вывода
                if hour < 10:
                    hour = str(0) + str(hour)
                if minute < 10:
                    minute = str(0) + str(minute)
                if secunde < 10:
                    secunde = str(0) + str(secunde)
                time_format = (str(hour), str(minute), str(secunde))
                time_now = ":".join(time_format)    # Форматирование в формат времени

                if '04:00:00' <= time_now < '12:00:00':
                    seq = (green, coffee, 'Good morning,', name, coffee, donut*3, mc)
                    print(" ".join(seq))

                elif '12:00:00' <= time_now < '17:00:00':
                    seq = (green, 'Good afternoon,', name, smile*3, relax*2, mc)
                    print(" ".join(seq))

                elif '17:00:00' <= time_now <= '23:59:59':
                    seq = (green, relax, 'Good evening,', name, sleep*2, mc)
                    print(" ".join(seq))

                elif '00:00:00' <= time_now < '04:00:00':
                    seq = (green, 'Good night,', name, moon*3, mc)
                    print(" ".join(seq))


def text2bits(text, encoding='utf-8', errors='surrogatepass'):
    """ Перевод в двоичный вид """
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def bits2text(bits, encoding='utf-8', errors='surrogatepass'):
    """ Перевод из двоичного вида """
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def CryptoBase64(message, key):
    """ Шифрование на основе библиотеки base64 """
    enc = []
    for i in range(len(message)):
        key_c = key[i % len(key)]
        enc.append(chr((ord(message[i]) + ord(key_c)) % 256))
    encryption = base64.urlsafe_b64encode("".join(enc).encode()).decode()
    return encryption


def DecryptoBase64(encryption, key):
    """ Дешифрование на основе библиотеки base64 """
    dec = []
    message = base64.urlsafe_b64decode(encryption).decode()
    for i in range(len(message)):
        key_c = key[i % len(key)]
        dec.append(chr((256 + ord(message[i]) - ord(key_c)) % 256))
    return "".join(dec)


def ClearTerminal():
    """ Очистка консоли """
    os.system("clear")


def fuckingMakingFiles():
    """ Запись перемешанных символов в файл """
    print('Wait a few moment... You will only see it once')
    os.mkdir('files')
    qty = 10000  # qty of dictionaries
    for i in range(qty):
        symb = []
        for j in main_lyster:
            symb.append(j)
        random.shuffle(symb)
        string = ''.join(symb)  # Добавление символов в строку
        # Recording data to file
        with open("files/.listers.dat", "a") as listers:  # Opening a file as "file"
            listers.write(string)  # Recording an encrypted message
            listers.write('\n')  # Line break
            listers.close()  # Closing the file to save data
    print(green, '-- All right, program will restarted --', '\n' * 100, mc)
    time.sleep(1)
    ClearTerminal()


if os.path.exists("files/.listers.dat") == False:      # Создание файла с уникальными строками
    fuckingMakingFiles()


def AppendInLister(oper_key):
    """ Добавление символов из файла в список """
    lyster_shuffle = []  # Пустой список
    with open("files/.listers.dat") as file:  # Файл с рандомными
        s = 0  # Счетчик (по умолчанию 0)
        for row in file:  # Перебор по строкам файла
            s += 1  # Счетчик увеличивается на 1
            if s == oper_key:  # Если значение счетчика равно опер-ключу
                for syb in row:  # Перебор строки посимвольно
                    lyster_shuffle.append(syb)  # Добавление символов в ранее пустой список
    return lyster_shuffle


def CryptoCaesar(password, key_caesar, lister):
    """ Encryption based Caesar """
    first_message = ''
    second_message = ''
    third_message = ''
    for a in password:  # First pass
        first_message += lister[
            (lister.index(a) - key_caesar) % len(lister)]  # Permutation to n-amount of first pass
    for b in first_message:  # Second pass
        second_message += lister[
            (lister.index(b) - key_caesar) % len(lister)]  # Permutation to n-amount of second pass
    for c in second_message:  # Third pass
        third_message += lister[
            (lister.index(c) - key_caesar) % len(lister)]  # Permutation to n-amount of third pass
    return third_message


def DecryptoCaesar(password, key_caesar, lister):
    """ Decryption based Caesar """
    first_message = ''
    second_message = ''
    third_message = ''
    for a in password:  # First pass
        first_message += lister[
            (lister.index(a) + key_caesar) % len(lister)]  # Permutation to n-amount of first pass
    for b in first_message:  # Second pass
        second_message += lister[
            (lister.index(b) + key_caesar) % len(lister)]  # Permutation to n-amount of second pass
    for c in second_message:  # Third pass
        third_message += lister[
            (lister.index(c) + key_caesar) % len(lister)]  # Permutation to n-amount of third pass
    return third_message


file_date_base = "files/.data.dat"
check_file_date_base = os.path.exists(file_date_base)    # Главный файл, где хранятся пароли


def SaveDataToFile(resource, login, password, key, lister, key_word):
    """ Шифрование логина и пароля. Сохранение в csv-файл (если этого файла нет)"""
    with open(file_date_base, mode="a", encoding='utf-8') as data:
        fieldnames = ['resource', 'login', 'password']
        writer = csv.DictWriter(data, fieldnames=fieldnames)
        if check_file_date_base == False:
            writer.writeheader()

        crypto_base_log = CryptoBase64(login, key_word)
        crypto_caesar_log = CryptoCaesar(crypto_base_log, key, lister)  # Next comes 3-pass encryption
        crypto_base_log = text2bits(crypto_caesar_log)  # To binary view

        crypto_base_pas = CryptoBase64(password, key_word)
        crypto_caesar_pas = CryptoCaesar(crypto_base_pas, key, lister)  # Next comes 3-pass encryption
        crypto_base_pas = text2bits(crypto_caesar_pas)  # To binary view

        writer.writerow({'resource': resource, 'login': crypto_base_log, 'password': crypto_base_pas})


def PasswordGeneraton():
    """ Генерирование нового случайного пароля """
    pas_gen = ''  # Password
    length = 21  # Amount
    for pas_elem in range(length):
        pas_gen += random.choice(lyster_for_pas)  # Password Adding random symbols from lister
    return pas_gen      # Возвращает пароль


def MainFun():
    """ The main function responsible for the operation of the program """
    if check_file_date_base == False:   # Если файла нет, идет создание файла с ресурсами

        print('\n', 'No resources saved. Add them:')
        resource = input('Resource: ')
        login = input('Login: ')

        pin = stdiomask.getpass('Key (6 numbers): ', mask='*')  # Encryption key
        key_word = stdiomask.getpass('Secure word: ', mask='*')
        pin = int(pin)
        key = pin // 10000
        oper_key = pin % 10000
        lister = AppendInLister(oper_key)

        print(green + '1' + yellow + ' - Generation new pas; ' + green + '2' + yellow + ' - save your pas: ' + mc)

        change = int(input('Change: '))
        if change == 1:  # Generation new password
            password = PasswordGeneraton()
            SaveDataToFile(resource, login, password, key, lister, key_word)
            print('Your new password - ' + green + password + mc + ' - success saved' + krokodil * 3 + mc)
            time.sleep(2)
            ClearTerminal()
            MainFun()
        elif change == 2:  # Save user password
            password = stdiomask.getpass('Password: ')
            SaveDataToFile(resource, login, password, key, lister, key_word)
            ClearTerminal()
            print(green + '- Your password ' +
                  password[0] +
                  password[1] + '*******' +
                  password[-1] + ' success saved -' + krokodil * 3 + mc)
            time.sleep(2)
            ClearTerminal()
            MainFun()
        else:
            print(red + '-- Error of change, please, change again --' + mc)
            time.sleep(1)
            ClearTerminal()
            MainFun()

    # Reader
    elif check_file_date_base == True:
        # Если файл уже создан, выводтся содержимое и дальнейшее взаимодействие с программой происходит тут
        with open(file_date_base, encoding='utf-8') as data:
            s = 0
            reader = csv.DictReader(data, delimiter=',')
            print('\n' + yellow + '--- Saved resources ---' + mc)
            for line in reader:
                s += 1
                print(str(s) + '.', line["resource"])

            print('\n' + blue + 'Enter "-r" to restart, "-x" to exit')  # A text prompting you to restart the program
            print('Enter "-a", to add new resource')
            print(yellow, 'Select resource by number', mc)

            def ShowResources():
                resource_number = input('\n''Change: ')
                if resource_number == '-a':
                    print('\n' + green + krokodil + ' -- Add new resource -- ' + krokodil + mc)
                    resource = input('Resource: ')
                    login = input('Login: ')

                    pin = stdiomask.getpass('Key (6 numbers): ', mask='*')  # Encryption key
                    key_word = stdiomask.getpass('Secure word: ', mask='*')
                    pin = int(pin)
                    key = pin // 10000
                    oper_key = pin % 10000
                    lister = AppendInLister(oper_key)

                    print(green + '1' + yellow + ' - Generation new pas ' +
                          green + '2' + yellow + ' - save your pas ' + mc)

                    change = int(input('Change: '))
                    if change == 1:  # Generation new password
                        password = PasswordGeneraton()
                        SaveDataToFile(resource, login, password, key, lister, key_word)
                        print('Your new password - ' + green + password + mc + ' - success saved' + krokodil * 3 + mc)
                        time.sleep(2)
                        ClearTerminal()
                        MainFun()
                    elif change == 2:  # Save user password
                        password = stdiomask.getpass('Password: ')
                        SaveDataToFile(resource, login, password, key, lister, key_word)
                        ClearTerminal()
                        print(green + '- Your password ' +
                              password[0] +
                              password[1] + '*******' +
                              password[-1] + ' success saved -' + krokodil * 3 + mc)
                        time.sleep(2)
                        ClearTerminal()
                        MainFun()
                    else:
                        print(red + '-- Error, please, change again --' + mc)
                        time.sleep(1)
                        ClearTerminal()
                        MainFun()

                elif resource_number == '-x':  # Condition exit
                    ClearTerminal()  # Clearing terminal
                    DateTime()
                    print(blue, '--- Program is closet ---' + '\n', mc)
                    quit()  # Exit
                elif resource_number == '-r':  # Condition restart
                    ClearTerminal()  # Clearing terminal
                    print('\n', green, '-- Restart --', mc)  # Show message of restart
                    time.sleep(1)
                    ClearTerminal()
                    MainFun()  # Start main function

                with open(file_date_base, encoding='utf-8') as profiles:
                    reader = csv.DictReader(profiles, delimiter=',')
                    count = 0
                    for line in reader:
                        count += 1
                        if count == int(resource_number):
                            resource = line["resource"]
                            login = line["login"]
                            password = line["password"]
                            print('Selected resource:', green + resource + mc)

                            pin = stdiomask.getpass('\n''Key (6 numbers): ', mask='*')  # Encryption key
                            master_password = stdiomask.getpass('Secure word: ', mask='*')  # Encryption word
                            pin = int(pin)
                            key = pin // 10000
                            oper_key = pin % 10000
                            lister = AppendInLister(oper_key)

                            # Decoding login and password
                            decryption_bin_log = bits2text(login)
                            decryption_caesar_log = DecryptoCaesar(decryption_bin_log, key, lister)
                            decryption_base_log = DecryptoBase64(decryption_caesar_log, master_password)

                            decryption_bin_pas = bits2text(password)  # To binary view
                            decryption_caesar_pas = DecryptoCaesar(decryption_bin_pas, key, lister)  # Next comes 3-pass encryption
                            decryption_base_pas = DecryptoBase64(decryption_caesar_pas, master_password)

                            print('\n' +
                                  resource + ' --> ' +
                                  green + decryption_base_log + ' --> ' +
                                  decryption_base_pas + mc)
                ShowResources()
            ShowResources()


if __name__ == '__main__':
    try:  # Running a program through an exception
        ClearTerminal()
        print(blue, '\n' 'Password manager v1.1.3 Stable for Linux (BFL)' '\n' 'by CISCer' '\n', mc)  # Start text
        time.sleep(2)
        ClearTerminal()
        DateTime()
        print('\n' * 5)
        MainFun()
    except ValueError:  # With this error (not entered value), the program is restarted
        print(red, '\n' + shit + ' --- ValueError, program is restarted --- ' + shit, mc)
        time.sleep(1.5)
        ClearTerminal()
        MainFun()
