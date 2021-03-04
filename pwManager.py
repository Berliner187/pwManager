#!/usr/bin/env python3
# Password manager v1.4.1 Stable For Linux (SFL)
# by CISCer
import os, sys
from csv import DictReader, DictWriter
from base64 import urlsafe_b64encode, urlsafe_b64decode
import random
import datetime
from time import sleep
from getpass import getpass


def ClearTerminal():
    """ Clear terminal """
    os.system("clear")


def RestartProgram():
    """ Restart Program """
    os.execv(sys.executable, [sys.executable] + sys.argv)


yellow, blue, green, mc, red = "\033[33m", "\033[34m", "\033[32m", "\033[0m", "\033[31m"  # Colours
main_lyster = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-='  # List of all symbols

# Files for work program
file_date_base = "files/main_data.dat"     # Файл, в котором лежат пароли
file_keys = "files/.keys.csv"  # Файл с ключами
lister_file = "files/.lister.dat"   # Файл со строками в кол-ве 10000
self_name_file = "files/.self_name.dat"  # Файл с именем (никнеймом)


check_file_date_base = os.path.exists(file_date_base)    # Проверка этого файла на наличие
check_file_keys = os.path.exists(file_keys)     # Проверка на наличие
check_file_lister = os.path.exists(lister_file)   # Проверка этого файла на наличие
gty_for_listers = 10000     # Число строк в файле listers

if os.path.exists('files') == bool(False):
    os.mkdir('files')

# Уровни шифрования
def CryptoLevel1(text, encoding='utf-8', errors='surrogatepass'):
    """ Translation to binary view """
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def DecryptoLevel1(bits, encoding='utf-8', errors='surrogatepass'):
    """ Translation from binary """
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def CryptoLevel2(password, key, lister):
    """ Encryption based Caesar """
    key = int(key)
    first_message = ''
    second_message = ''
    third_message = ''
    for a in password:  # First pass
        first_message += lister[
            (lister.index(a) - key) % len(lister)]  # Permutation to n-amount of first pass
    for b in first_message:  # Second pass
        second_message += lister[
            (lister.index(b) - key) % len(lister)]  # Permutation to n-amount of second pass
    for c in second_message:  # Third pass
        third_message += lister[
            (lister.index(c) - key) % len(lister)]  # Permutation to n-amount of third pass
    return third_message


def DecryptoLevel2(password, key, lister):
    """ Decryption based Caesar """
    key = int(key)
    first_message = ''
    second_message = ''
    third_message = ''
    for a in password:  # First pass
        first_message += lister[
            (lister.index(a) + key) % len(lister)]  # Permutation to n-amount of first pass
    for b in first_message:  # Second pass
        second_message += lister[
            (lister.index(b) + key) % len(lister)]  # Permutation to n-amount of second pass
    for c in second_message:  # Third pass
        third_message += lister[
            (lister.index(c) + key) % len(lister)]  # Permutation to n-amount of third pass
    return third_message


def CryptoLevel3(message, key):
    """ Base64-based encryption """
    key = str(key)
    enc = []
    for i in range(len(message)):
        key_c = key[i % len(key)]
        enc.append(chr((ord(message[i]) + ord(key_c)) % 256))
    encryption = urlsafe_b64encode("".join(enc).encode()).decode()
    return encryption


def DecryptoLevel3(encryption, key):
    """ Base64-based decryption """
    key = str(key)
    dec = []
    message = urlsafe_b64decode(encryption).decode()
    for i in range(len(message)):
        key_c = key[i % len(key)]
        dec.append(chr((256 + ord(message[i]) - ord(key_c)) % 256))
    return "".join(dec)


def EncryptionByTwoLevels(anything, master_password):
    crypto_start = CryptoLevel3(anything, master_password)
    crypto = CryptoLevel1(crypto_start)
    return crypto


def DecryptionByTwoLevels(anything, master_password):
    decryption_start = DecryptoLevel1(anything)
    decryption = DecryptoLevel3(decryption_start, master_password)
    return decryption


def EncryptionData(data, key, master_password, lister):
    """ Decryption encryption resource """
    encryption_data = CryptoLevel3(data, master_password)
    encryption_data_2 = CryptoLevel2(encryption_data, key, lister)
    encryption_data = CryptoLevel1(encryption_data_2)
    return encryption_data


def DecryptionData(encryption_data, key, master_password, lister):
    """ Decryption encryption resource """
    decryption_data_1 = DecryptoLevel1(encryption_data)
    decryption_data_2 = DecryptoLevel2(decryption_data_1, key, lister)
    decryption_data = DecryptoLevel3(decryption_data_2, master_password)
    return decryption_data


def GreatingDependingOnDateTime(master_password):
    """ Фунция вывода приветствия в зависимости от времени суток """
    def Time(name):
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
            return total

    if os.path.exists(self_name_file) == bool(False):  # Создание файла с именем
        with open(self_name_file, "w") as self_name:
            name = input(yellow + ' - Your name or nickname: ' + mc)
            enc_name = EncryptionByTwoLevels(name, master_password)
            self_name.write(enc_name)
            self_name.close()
            return Time(name)
    else:  # Чтение из файла с именем и вывод в консоль
        with open(self_name_file, "r") as self_name:
            dec_name = self_name.readline()
            name = DecryptionByTwoLevels(dec_name, master_password)
            return Time(name)


def MakingRows(master_password):
    ClearTerminal()
    print('Making files. Please, wait ...')
    global gty_for_listers
    for q in range(gty_for_listers):
        symb = []
        for j in main_lyster:
            symb.append(j)
        random.shuffle(symb)
        string = ''.join(symb)  # Добавление символов в строку
        # Шифрование строки
        enc_string = CryptoLevel3(string, master_password)
        total = CryptoLevel1(enc_string)
        # Recording data to file
        with open(lister_file, "a") as lister:  # Opening a file as "file"
            lister.write(total)  # Recording an encrypted message
            lister.write('\n')  # Line break
            lister.close()  # Closing the file to save data
    print('\n\n -- All right -- \n')
    sleep(1)
    ClearTerminal()


def AppendInListerFromFile(additional_key, master_password):
    """ Добавление нужной строки из файла в список для дальнейшего использования """
    lister_for_return = []  # Пустой список
    with open(lister_file) as file:  # Файл с рандомными
        s = 0  # Счетчик (по умолчанию 0)
        for row in file:  # Перебор по строкам файла
            s += 1  # Счетчик увеличивается на 1
            if s == additional_key:  # Если значение счетчика равно дополнительному ключу
                dec_row = DecryptoLevel1(row)
                total = DecryptoLevel3(dec_row, master_password)
                for syb in total:  # Перебор строки посимвольно
                    lister_for_return.append(syb)  # Добавление символов в ранее пустой список
    return lister_for_return


def getUniqueSewnKey(master_password):
    """ Make unique key """
    global gty_for_listers
    if check_file_keys == bool(False):
        list_of_key = []
        for i in range(52):
            list_of_key.append(i)
        list_of_additional_key = []
        for a in range(gty_for_listers):  # Заполнения массивва в диапозоне кол-ва строк файла "lister.dat"
            list_of_additional_key.append(a)
        key = random.choices(list_of_key)
        for j in list_of_key:
            key = str(j)
        additional_key = random.choices(list_of_additional_key)  # Выбор случайного значения из массива
        for b in additional_key:
            additional_key = str(b)
        # Encryption unique-key
        crypto_key = EncryptionByTwoLevels(key, master_password)
        crypto_additional_key = EncryptionByTwoLevels(additional_key, master_password)

        with open(file_keys, mode="w", encoding='utf-8') as data:
            writer = DictWriter(data, fieldnames=['key', 'additional_key'])
            if check_file_keys == bool(False):
                writer.writeheader()
            writer.writerow({
                'key': crypto_key,
                'additional_key': crypto_additional_key})
            return str(key), str(additional_key)
    else:
        with open(file_keys, encoding='utf-8') as profiles:
            reader = DictReader(profiles, delimiter=',')
            for row in reader:
                key = row["key"]
                additional_key = row["additional_key"]
            decryption_key = DecryptionByTwoLevels(key, master_password)
            decryption_additional_key = DecryptionByTwoLevels(additional_key, master_password)
            return str(decryption_key), str(decryption_additional_key)


def SaveDataToFile(resource, login, password, key, lister, master_password):
    """ Шифрование логина и пароля. Сохранение в csv-файл """
    with open(file_date_base, mode="a", encoding='utf-8') as data:
        writer = DictWriter(data, fieldnames=['resource', 'login', 'password'])
        if check_file_date_base == bool(False):
            writer.writeheader()
        crypto_res = EncryptionData(resource, key, master_password, lister)
        crypto_log = EncryptionData(login, key, master_password, lister)
        crypto_pas = EncryptionData(password, key, master_password, lister)
        writer.writerow({
            'resource': crypto_res,
            'login': crypto_log,
            'password': crypto_pas})


def ConfirmUserPass():
    """ Confirm user input password """
    def UserInput():
        user_password = getpass(' Input: ')
        user_confirm_password = getpass(' Confirm input: ')
        return user_password, user_confirm_password
    print(blue + '\n Minimum password length 8 characters' + mc)
    password, confirm_password = UserInput()
    # Условаия принятия пароля
    if password == confirm_password and len(password) >= 8:
        return password
    elif password != confirm_password or len(password) < 8:
        while password != confirm_password or len(password) < 8:
            print(red + '\n Error of confirm or length < 8 characters. Try again' + mc)
            password, confirm_password = UserInput()
            if confirm_password == password and len(password) >= 8:
                return password


def ChangeTypeOfPass(resource, login, key, master_password, lister):
    """ Change type of password: user or generation """
    def DoForNewGeneratedPassword(resource, login, password, key, lister, master_password):
        SaveDataToFile(resource, login, password, key, lister, master_password)
        print('  Your new password - ' + green + password + mc + ' - success saved')

    def GenerationPassword(length):
        """ Генерирование нового случайного пароля """
        pas_gen = ''  # Empty password
        for pas_elem in range(length):
            pas_gen += random.choice(main_lyster)  # Password Adding random symbols from lister
        return pas_gen  # Возвращает пароль

    change = int(input('Change (1/2): '))
    if change == 1:  # Generation new password
        length = int(input(' Length password (Minimum 8): '))
        if length >= 8:
            password = GenerationPassword(length)
            DoForNewGeneratedPassword(resource, login, password, key, lister, master_password)
        elif length < 8:
            while length < 8:
                print(red + '\n Error of confirm or length < 8 characters. Try again' + mc)
                length = int(input(' Length password (Minimum 8): '))
                password = GenerationPassword(length)
                if length >= 8:
                    DoForNewGeneratedPassword(resource, login, password, key, lister, master_password)

    elif change == 2:  # Save user password
        password = ConfirmUserPass()  # Input password
        SaveDataToFile(resource, login, password, key, lister, master_password)

        print(green + '\n  - Your password ' +
              '*' * len(password) +
              password[-1] +
              password[-2] +
              ' successfully saved -  ' + mc)
    else:
        print(red + '  -- Error of change. Please, change again --  ' + mc)
        sleep(1)
        ChangeTypeOfPass(resource, login, key, master_password, lister)
    sleep(.6)
    ClearTerminal()

    if check_file_date_base == bool(False):
        RestartProgram()
    else:
        ShowContent(key, master_password, lister)       # Показ содержимого файла с ресурсами
        DecryptionBlock(master_password, key, lister, resource, login)  # Start cycle


def ShowContent(key, master_password, lister):
    """ Показ всех сохраненных ресурсов """
    ClearTerminal()
    with open(file_date_base, encoding='utf-8') as data:
        s = 0
        reader = DictReader(data, delimiter=',')
        print(yellow + '\n   --- Saved resources ---   ' + '\n'*3 + mc)
        for line in reader:
            encryption_resource = line["resource"]
            decryption_res = DecryptionData(encryption_resource, key, master_password, lister)
            s += 1
            print(str(s) + '. ' + decryption_res)    # Decryption resource

        print(blue + '\n  - Enter "-r" to restart, "-x" to exit'
                     '\n  - Enter "-a", to add new resource',
                     yellow, '\n Select resource by number', mc)


def CloseAndRestartProgram(change):
    if change == '-x':  # Condition exit
        ClearTerminal()  # Clearing terminal
        print(blue, ' --- Program is closet --- \n', mc)
        quit()  # Exit
    elif change == '-r':  # Condition restart
        ClearTerminal()  # Clearing terminal
        print('\n', green, ' -- Restart -- ', mc)  # Show message of restart
        sleep(.5)
        ClearTerminal()
        RestartProgram()  # Restart program


def AuthConfirmPasswordAndGetUniqueSewnKey(master_password):
    def GetKeys():
        key, additional_key = getUniqueSewnKey(master_password)  # Получение новых ключей
        return int(key), int(additional_key)

    if check_file_date_base == bool(False):
        print(blue + ' Enter secure word and remember them' + mc)
        key, additional_key = GetKeys()
        lister_row = AppendInListerFromFile(additional_key, master_password)  # Change row encryption
        return key, lister_row, master_password
    else:
        master_password = getpass(' Your secure word: ')
        try:
            CloseAndRestartProgram(master_password)
        except ZeroDivisionError:
            print(red + '- Incorrect input -' + mc)
            sleep(1)
            MainFun()
        key, additional_key = GetKeys()
        lister_row = AppendInListerFromFile(additional_key, master_password)  # Change row encryption
        return key, lister_row, master_password


def TextAddNewResource():
    ClearTerminal()
    text_add = (green, '\n   --- Add new resource ---   ', '\n' * 3, mc)
    print(' '.join(text_add))


def DataForResource(master_password):
    """ Данные для сохранения (ресурс, логин, пароль) """
    if check_file_date_base == bool(False):
        TextAddNewResource()
    resource = input(yellow + ' Resource: ' + mc)
    login = input(yellow + ' Login: ' + mc)
    key, lister_row, master_password = AuthConfirmPasswordAndGetUniqueSewnKey(master_password)
    return key, lister_row, resource, login


def DecryptionBlock(master_password, key, lister_row, resource, login):
    """ Show resources and decrypt them with keys """
    def AddResourceData(resource, login, key, master_password, lister_row):
        TextAddNewResource()

        def TextChangePassword():
            print(green + ' 1' + yellow + ' - Generation new password \n' +
                  green + ' 2' + yellow + ' - Save your password \n' + mc)

        if check_file_date_base == bool(False):
            TextChangePassword()
            ChangeTypeOfPass(resource, login, key, master_password, lister_row)
        else:
            key, lister_row, resource, login = DataForResource(master_password)  # Ввод данных для ресурса
            TextChangePassword()
            ChangeTypeOfPass(resource, login, key, master_password, lister_row)
            DecryptionBlock(master_password, key, lister_row, resource, login)

    if check_file_date_base == bool(True):
        # Decryption mechanism
        change_resource_or_actions = input('\n Change: ')
        if change_resource_or_actions == '-a':
            AddResourceData(resource, login, key, master_password, lister_row)
        elif change_resource_or_actions == '-u':
            def ActionsUpdate(command):
                os.system(command)
            ClearTerminal()
            ActionsUpdate('git clone https://github.com/Berliner187/pwManager')
            ActionsUpdate('cp pwManager/pwManager.py .; rm -r pwManager/')
            ClearTerminal()
            print(green + ' -- Update successfully! -- ' + mc)
            sleep(2)
            ActionsUpdate('./pwManager.py')
        CloseAndRestartProgram(change_resource_or_actions)
        with open(file_date_base, encoding='utf-8') as profiles:
            reader = DictReader(profiles, delimiter=',')
            count = 0   # Счетчик
            for line in reader:  # Iterating over lines file
                count += 1
                if count == int(change_resource_or_actions):   # Выбор ресурса по номеру
                    ClearTerminal()
                    ShowContent(key, master_password, lister_row)
                    encryption_resource = line["resource"]
                    encryption_login = line["login"]
                    encryption_password = line["password"]

                    # Decryption data from file
                    decryption_res = DecryptionData(encryption_resource, key, master_password, lister_row)
                    decryption_log = DecryptionData(encryption_login, key, master_password, lister_row)
                    decryption_pas = DecryptionData(encryption_password, key, master_password, lister_row)

                    print('\n Resource:', green, decryption_res, mc,
                          '\n Login:   ', green, decryption_log, mc,
                          '\n Password:', green, decryption_pas, mc)

        DecryptionBlock(master_password, key, lister_row, resource, login)
    else:
        AddResourceData(resource, login, key, master_password, lister_row)
        RestartProgram()


def MainFun():
    """ The main function responsible for the operation of the program """
    if check_file_date_base == bool(False):   # Если файла нет, идет создание файла с ресурсами
        ClearTerminal()     # Очистка терминала
        print(blue + "\n  - Encrypt your passwords with one master-password -    "
                     "\n  -           No resources saved. Add them!         -  \n" +
                     "\n ---                 That's easy!                  --- \n" + mc)
        print(yellow + ' -- Pick a master-password --' + mc)
        master_password = ConfirmUserPass()
        if check_file_lister == bool(False):
            MakingRows(master_password)
        print(GreatingDependingOnDateTime(master_password))
        sleep(.7)
        # Данные для сохранения
        key, lister_row, resource, login = DataForResource(master_password)     # Ввод данных для ресурса
        DecryptionBlock(master_password, key, lister_row, resource, login)  # Start cycle
    # Reader
    else:
        # Если файл уже создан, выводтся содержимое и дальнейшее взаимодействие с программой происходит тут
        key, lister_row, master_password = AuthConfirmPasswordAndGetUniqueSewnKey(None)
        ClearTerminal()
        print(GreatingDependingOnDateTime(master_password))
        sleep(.7)
        ShowContent(key, master_password, lister_row)       # Показ содержимого файла с ресурсами
        DecryptionBlock(master_password, key, lister_row, None, None)  # Start cycle


if __name__ == '__main__':
    try:  # Running a program through an exception
        ClearTerminal()
        print(blue, '\n' 'Password Manager v1.4.1 Beta-Stable For Linux (SFL) \n by Berliner187' '\n', mc)  # Start text
        MainFun()
    except ValueError:  # With this error (not entered value), the program is restarted
        print(red, '\n' + ' --- ValueError, program is restarted --- ', mc)
        sleep(2)
        ClearTerminal()
        RestartProgram()