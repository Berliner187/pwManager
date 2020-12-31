#!/usr/bin/env python3
# Password manager v1.2.0 beta for Linux (SFL)
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
    print(green + "  -- Successfully installed! --  " + mc)
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


def RestartProgram():
    """ Restart Program """
    os.system("./pwManager-BFL.py")


def ClearTerminal():
    """ Clear terminal """
    os.system("clear")


# Уровни шифрования
def CryptoLevel1(text, encoding='utf-8', errors='surrogatepass'):
    """ Translation to binary view """
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def DecryptoLevel1(bits, encoding='utf-8', errors='surrogatepass'):
    """ Translation from binary """
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def CryptoLevel2(password, key_caesar, lister):
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


def DecryptoLevel2(password, key_caesar, lister):
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


def CryptoLevel3(message, key):
    """ Base64-based encryption """
    enc = []
    for i in range(len(message)):
        key_c = key[i % len(key)]
        enc.append(chr((ord(message[i]) + ord(key_c)) % 256))
    encryption = base64.urlsafe_b64encode("".join(enc).encode()).decode()
    return encryption


def DecryptoLevel3(encryption, key):
    """ Base64-based decryption """
    dec = []
    message = base64.urlsafe_b64decode(encryption).decode()
    for i in range(len(message)):
        key_c = key[i % len(key)]
        dec.append(chr((256 + ord(message[i]) - ord(key_c)) % 256))
    return "".join(dec)


file_date_base = "files/.test-data.dat"     # Файл, в котором лежат пароли
check_file_date_base = os.path.exists(file_date_base)    # Проверка этого файла на наличие

listers_file = "files/.listers.dat"     # Файл со строками в кол-ве 10000
check_listers_file = os.path.exists("files/.listers.dat")   # Проверка этого файла на наличие

if listers_file == bool(False):      # Файл рандомно заполняется символами
    """ Writing shuffled characters to a file """
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
        with open(listers_file, "a") as listers:  # Opening a file as "file"
            listers.write(string)  # Recording an encrypted message
            listers.write('\n')  # Line break
            listers.close()  # Closing the file to save data
    ClearTerminal()
    print(green, ' -- All right, program will restarted -- \n' * 100, mc)
    time.sleep(1)
    ClearTerminal()


def DateTime():
    """ Фунция вывода приветствия в зависимости от времени суток """
    self_name_file = "files/.self_name.dat"     # Файл с именем (никнеймом)
    if os.path.exists(self_name_file) == bool(False):     # Создание файла с именем
        with open(self_name_file, "w") as self_name:
            name = input(yellow + ' - Your name or nickname: ' + mc)
            self_name.write(name)
            self_name.close()
            DateTime()

    elif os.path.exists(self_name_file) == bool(True):    # Чтение из файла с именем и вывод в консоль
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

                if '04:00:00' <= time_now < '12:00:00':     # Condition morning
                    seq = (green, coffee, 'Good morning,', name, coffee, donut*3, mc)
                    print(" ".join(seq))
                elif '12:00:00' <= time_now < '17:00:00':   # Condition day
                    seq = (green, krokodil*3, 'Good afternoon,', name, smile*3, relax*2, mc)
                    print(" ".join(seq))
                elif '17:00:00' <= time_now <= '23:59:59':  # Condition evening
                    seq = (green, relax, 'Good evening,', name, sleep*2, mc)
                    print(" ".join(seq))
                elif '00:00:00' <= time_now < '04:00:00':   # Condition night
                    seq = (green, 'Good night,', name, moon*3, mc)
                    print(" ".join(seq))


def AppendInLister(additional_key):
    """ Добавление символов из файла в список для дальнейшего шифрования"""
    lister_shuffle = []  # Пустой список
    with open("files/.listers.dat") as file:  # Файл с рандомными
        s = 0  # Счетчик (по умолчанию 0)
        for row in file:  # Перебор по строкам файла
            s += 1  # Счетчик увеличивается на 1
            if s == additional_key:  # Если значение счетчика равно дополнительному ключу
                for syb in row:  # Перебор строки посимвольно
                    lister_shuffle.append(syb)  # Добавление символов в ранее пустой список
    return lister_shuffle


def SaveDataToFile(resource, login, password, key, lister, key_word):
    """ Шифрование логина и пароля. Сохранение в csv-файл """
    with open(file_date_base, mode="a", encoding='utf-8') as data:
        writer = csv.DictWriter(data, fieldnames=['resource', 'login', 'password'])
        if check_file_date_base == bool(False):
            writer.writeheader()
        # Encryption resource
        crypto_res_1 = CryptoLevel3(resource, key_word)
        crypto_res_2 = CryptoLevel2(crypto_res_1, key, lister)  # Next comes 3-pass encryption
        crypto_res_3 = CryptoLevel1(crypto_res_2)  # To binary view
        # Encryption login
        crypto_log_1 = CryptoLevel3(login, key_word)
        crypto_log_2 = CryptoLevel2(crypto_log_1, key, lister)  # Next comes 3-pass encryption
        crypto_log_3 = CryptoLevel1(crypto_log_2)  # To binary view
        # Encryption password
        crypto_pas_1 = CryptoLevel3(password, key_word)
        crypto_pas_2 = CryptoLevel2(crypto_pas_1, key, lister)  # Next comes 3-pass encryption
        crypto_pas_3 = CryptoLevel1(crypto_pas_2)  # To binary view

        writer.writerow({'resource': crypto_res_3, 'login': crypto_log_3, 'password': crypto_pas_3})


def GenerationPassword(length):
    """ Генерирование нового случайного пароля """
    pas_gen = ''  # Empty password
    for pas_elem in range(length):
        pas_gen += random.choice(lyster_for_pas)  # Password Adding random symbols from lister
    return pas_gen      # Возвращает пароль


def ConfirmUserPass():
    """ Confirm user input password """
    password = stdiomask.getpass(' Password: ')
    confirm_password = stdiomask.getpass(' Confirm password: ')
    return password, confirm_password


def ChangeTypeOfPass(change, resource, login, key, master_password, lister):
    """ Change type of password: user or new generation """
    if change == 1:  # Generation new password
        length = int(input(' Length password (Minimum 8): '))
        if length >= 8:
            password = GenerationPassword(length)
            SaveDataToFile(resource, login, password, key, lister, master_password)
            print('  Your new password - ' + green + password + mc + ' - success saved' + krokodil * 3 + mc)
        elif length < 8:
            while length < 8:
                print(red + '\n Error of confirm or length < 8 characters. Try again' + mc)
                length = int(input(' Length password (Minimum 8): '))
                password = GenerationPassword(length)
                if length >= 8:
                    SaveDataToFile(resource, login, password, key, lister, master_password)
                    print('  Your new password - ' + green + password + mc + ' - success saved' + krokodil * 3 + mc)
        time.sleep(3)
        ClearTerminal()

    elif change == 2:  # Save user password
        print(blue + '\n Minimum password length 8 characters' + mc)
        password, confirm_password = ConfirmUserPass()  # Input password
        if password == confirm_password and len(password) >= 8:     # Если соблюдается оба условия, вызывается функция сохранения в файл
            SaveDataToFile(resource, login, password, key, lister, master_password)
        elif password != confirm_password or len(password) < 8:     # Если не совпадают, вводятся до тех пор, пока условия не будут соблюдены
            while password != confirm_password or len(password) < 8:
                print(red + '\n Error of confirm or length < 8 characters. Try again' + mc)
                password, confirm_password = ConfirmUserPass()
                if confirm_password == password and len(password) >= 8:
                    SaveDataToFile(resource, login, password, key, lister, master_password)
        ClearTerminal()

        print(green + '\n  - Your password ' +
              password[0] +
              password[1] +
              '*********' +
              password[-1] +
              password[-2] + ' successfully saved -  ' + krokodil * 3 + mc)
        time.sleep(2)
        ClearTerminal()
    else:
        print(red + '  -- Error of change. Please, change again --  ' + mc)
        time.sleep(1)
        ClearTerminal()
        MainFun()
    RestartProgram()


def DecryptionResource(encryption_resource, key, master_password, lister):
    """ Decryption encryption resource """
    decryption_res_1 = DecryptoLevel1(encryption_resource)
    decryption_res_2 = DecryptoLevel2(decryption_res_1, key, lister)
    decryption_res_3 = DecryptoLevel3(decryption_res_2, master_password)
    return decryption_res_3


def ShowContent(key, master_password, lister):
    """ Вывод всех сохраненных ресурсов """
    with open(file_date_base, encoding='utf-8') as data:
        s = 0
        reader = csv.DictReader(data, delimiter=',')
        print(yellow + '\n   --- Saved resources ---   ' + '\n'*5 + mc)
        for line in reader:
            encryption_resource = line["resource"]
            decryption_res_3 = DecryptionResource(encryption_resource, key, master_password, lister)
            s += 1
            print(str(s) + '. ' + decryption_res_3)    # Decryption resource

        print(blue + '\n  - Enter "-r" to restart, "-x" to exit'
                     '\n  - Enter "-a", to add new resource',
                     yellow, '\n Select resource by number', mc)


def Auth():
    pin = int(stdiomask.getpass('\n Key (6 numbers): ', mask='*'))  # Encryption key
    key = pin // 10000  # Encryption key (First 2 numbers)  # For Caesar-based encryption
    additional_key = pin % 10000  # Encryption key (Last 4 numbers) for lister
    master_password = stdiomask.getpass(' Secure word: ', mask='*')  # Encryption word
    return key, additional_key, master_password


def DataForResource():
    resource = input(' Resource: ')
    login = input(' Login: ')
    key, additional_key, master_password = Auth()
    lister = AppendInLister(additional_key)  # Change row encryption
    return key, additional_key, master_password, resource, login, lister


def DecryptionBlock(master_password, key, additional_key):
    """ Show resources and decrypt them with keys """
    resource_number = input('\n Change: ')
    if resource_number == '-a':
        ClearTerminal()
        text_add = (green, krokodil,  '\n   --- Add new resource ---   ', krokodil, mc)
        print(' '.join(text_add))

        key, additional_key, master_password, resource, login, lister = DataForResource()     # Ввод данных для ресурса

        print(green + ' 1' + yellow + ' - Generation new pas \n' +
              green + ' 2' + yellow + ' - Save your pas \n' + mc)

        change = int(input(' Change: '))    # Выбор типа пароля: пользовательский или новый сгенерированный
        ChangeTypeOfPass(change, resource, login, key, master_password, lister)

    elif resource_number == '-x':  # Condition exit
        ClearTerminal()  # Clearing terminal
        DateTime()  # Displays completion message
        print(blue, ' --- Program is closet --- ' + '\n', mc)
        quit()  # Exit
    elif resource_number == '-r':  # Condition restart
        ClearTerminal()  # Clearing terminal
        print('\n', green, ' -- Restart -- ', mc)  # Show message of restart
        time.sleep(.8)
        ClearTerminal()
        RestartProgram()    # Restart program

    # Decryption mechanism
    with open(file_date_base, encoding='utf-8') as profiles:
        reader = csv.DictReader(profiles, delimiter=',')
        count = 0
        for line in reader:  # Iterating over lines file
            count += 1
            if count == int(resource_number):   # Выбор ресурса по номеру
                ClearTerminal()
                lister = AppendInLister(additional_key)  # Change row encryption
                ShowContent(key, master_password, lister)
                encryption_resource = line["resource"]
                encryption_login = line["login"]
                encryption_password = line["password"]

                # Decryption resource
                decryption_res_3 = DecryptionResource(encryption_resource, key, master_password, lister)
                # Decryption login
                decryption_log_1 = DecryptoLevel1(encryption_login)
                decryption_log_2 = DecryptoLevel2(decryption_log_1, key, lister)
                decryption_log_3 = DecryptoLevel3(decryption_log_2, master_password)
                # Decryption password
                decryption_pas_1 = DecryptoLevel1(encryption_password)
                decryption_pas_2 = DecryptoLevel2(decryption_pas_1, key, lister)
                decryption_pas_3 = DecryptoLevel3(decryption_pas_2, master_password)

                print('\n Resource:', green, decryption_res_3, mc,
                      '\n Login:', green, decryption_log_3, mc,
                      '\n Password:', green, decryption_pas_3, mc)

    DecryptionBlock(master_password, key, additional_key)  # Recursion


def MainFun():
    """ The main function responsible for the operation of the program """
    if check_file_date_base == bool(False):   # Если файла нет, идет создание файла с ресурсами
        ClearTerminal()     # Очистка терминала
        print(blue + '\n - Enter "-r" for restart - '
                     '\n No resources saved. Add them! \n' + 
                     green + '\n\n Enter six-digit key and remember them \n' + mc)
        # Данные для сохранения
        key, additional_key, master_password, resource, login, lister = DataForResource()

        print(green + '1' + yellow + ' - Generation new pas \n' +
              green + '2' + yellow + ' - Save your pas ' + mc)

        change = int(input(' Change: '))     # Change: generation new password or save user password
        ChangeTypeOfPass(change, resource, login, key, master_password, lister)    # Вызов фунции с выбором типа пароля
        RestartProgram()

    # Reader
    else:
        # Если файл уже создан, выводтся содержимое и дальнейшее взаимодействие с программой происходит тут
        key, additional_key, master_password = Auth()   # Вызов функции ввода ключа и мастер-пароля
        lister = AppendInLister(additional_key)  # Change row encryption
        ShowContent(key, master_password, lister)       # Показ содержимого файла с ресурсами
        DecryptionBlock(master_password, key, additional_key)  # Start cycle


if __name__ == '__main__':
    try:  # Running a program through an exception
        ClearTerminal()
        print(blue, '\n' 'Password Manager v1.2.0 Beta for Linux (BFL) \n by CISCer' '\n', mc)  # Start text
        DateTime()
        MainFun()
    except ValueError:  # With this error (not entered value), the program is restarted
        print(red, '\n' + shit + ' --- ValueError, program is restarted --- ' + shit, mc)
        time.sleep(1.5)
        ClearTerminal()
        MainFun()
