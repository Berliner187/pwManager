#!/usr/bin/env python3
# Password Manager Server Solution v1.0.2 Stable For Linux (SFL)
# Based on stable version 1.4.4
# by Berliner187
# Resources and all data related to them are encrypted with a single password
import os, sys
from csv import DictReader, DictWriter
from base64 import urlsafe_b64encode, urlsafe_b64decode
import random
import datetime
from time import sleep
from getpass import getpass
from shutil import copyfile

yellow, blue, green, mc, red = "\033[33m", "\033[36m", "\033[32m", "\033[0m", "\033[31m"  # Colours
main_lyster = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-='  # List of all symbols
# Символы, которые не могут использоваться
forbidden_symbols = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-=!@#$%^&*()"№;:?'


def ClearTerminal():
    """ Clear terminal """
    os.system('cls' if os.name == 'nt' else 'clear')


def RestartProgram():
    """ Restart Program """
    os.execv(sys.executable, [sys.executable] + sys.argv)


ClearTerminal()
print(blue, '\n' ' Password Manager Server Solution v1.0.3 Stable For Linux (SFL) \n by Berliner187' '\n', mc)
user_input_name = input(yellow + ' -- Enter your login: ' + mc)
if len(user_input_name) < 5:
    print(red + ' - Your login too short, try again ' + mc)
    sleep(.7)
    RestartProgram()
for syb in user_input_name:
    for check_register in forbidden_symbols:
        if syb == check_register:
            ClearTerminal()
            print(red + '\n\n\n   -- Unacceptable symbols in login -- ' + red)
            sleep(1)
            RestartProgram()
# Files for work program
users_folder = 'users/'
if os.path.exists(users_folder) == bool(False):     # Папка с юзерами
    os.mkdir(users_folder)
main_folder = users_folder + user_input_name + '/' + 'files/'   # Папка с юзерскими файлами
hash_password_file = main_folder + ".hash_password.dat"
file_date_base = main_folder + "main_data.dat"     # Файл, в котором лежат основные данные
file_keys = main_folder + ".keys.csv"  # Файл с ключами
lister_file = main_folder + ".lister.dat"   # Файл со строками в кол-ве 10000
self_name_file = main_folder + ".self_name.dat"  # Файл с именем (никнеймом)
file_master_hash = main_folder + ".file_master_hash.dat"     # Файл с хэшированным паролем
check_file_date_base = os.path.exists(file_date_base)    # Проверка этого файла на наличие
check_file_keys = os.path.exists(file_keys)     # Проверка на наличие
check_file_lister = os.path.exists(lister_file)   # Проверка этого файла на наличие
gty_for_listers = 1000     # Число строк в файле listers


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
    enc_data = ''
    for a in password:  # First pass
        enc_data += lister[
            (lister.index(a) - key) % len(lister)]  # Permutation to n-amount of first pass
    return enc_data


def DecryptoLevel2(password, key, lister):
    """ Decryption based Caesar """
    key = int(key)
    dec_data = ''
    for a in password:  # First pass
        dec_data += lister[
            (lister.index(a) + key) % len(lister)]  # Permutation to n-amount of first pass
    return dec_data


def CryptoLevel3(message, key):
    """ Base64-based encryption """
    key, message = str(key), str(message)
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


def EncryptionByTwoLevels(anything, master_password):   # Encryption by two levels
    crypto_start = CryptoLevel3(anything, master_password)
    crypto = CryptoLevel1(crypto_start)
    return crypto


def DecryptionByTwoLevels(anything, master_password):   # Decryption by two levels
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


def getUserSavedName(master_password):
    with open(self_name_file, "r") as self_name:
        dec_name = self_name.readline()
        name = DecryptionByTwoLevels(dec_name, master_password)
    return name


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
        name = getUserSavedName(master_password)
        return Time(name)


def MakingRows(master_password):
    ClearTerminal()
    print(yellow + 'Making files. Please, wait ...' + mc)
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
    ClearTerminal()
    print(green + '\n\n ---  All right! --- \n' + mc)
    sleep(.7)
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
        for a in range(gty_for_listers):  # Заполнения массива в диапозоне кол-ва строк файла "lister.dat"
            list_of_additional_key.append(a)
        key = random.choice(list_of_key)
        additional_key = random.choice(list_of_additional_key)  # Выбор случайного значения из массива
        # Encryption unique-key
        crypto_key = EncryptionByTwoLevels(key, master_password)
        crypto_additional_key = EncryptionByTwoLevels(additional_key, master_password)
        key, additional_key = str(key), str(additional_key)

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
        user_password = getpass(' Password: ')
        user_confirm_password = getpass(' Confirm password: ')
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
        ClearTerminal()
        print(green + '\n  - Your password successfully saved! -  ' + mc)
    else:
        print(red + '  -- Error of change. Please, change again --  ' + mc)
        sleep(1)
        ChangeTypeOfPass(resource, login, key, master_password, lister)
    sleep(2)
    ClearTerminal()

    if check_file_date_base == bool(False):     # Перезапуск для корректной работы дальше
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
        name = getUserSavedName(master_password)
        print(yellow + '\n   --- ' + name + "'s saved resources --- " + '\n'*3 + mc)
        for line in reader:
            encryption_resource = line["resource"]
            decryption_res = DecryptionData(encryption_resource, key, master_password, lister)
            s += 1
            print(str(s) + '. ' + decryption_res)    # Decryption resource
        print(blue + '\n  - Enter "-x" to exit                ',
                     '\n  - Enter "-a" to add new resource    ',
                     '\n  - Enter "-u" to update the program from the repository',
                     '\n  - Enter "-d" to remove resource'
                     '\n  - Enter "-q" to change another user ',
              yellow, '\n  Select resource by number', mc)


def AuthConfirmPasswordAndGetUniqueSewnKey(master_password, status):
    """ Get secure_word, unique-keys """
    def GetKeys():
        key, additional_key = getUniqueSewnKey(master_password)  # Получение новых ключей
        return int(key), int(additional_key)

    if check_file_date_base == bool(False):
        key, additional_key = GetKeys()
        lister_row = AppendInListerFromFile(additional_key, master_password)  # Change row encryption
        return key, lister_row, master_password
    else:
        if status == bool(True):
            master_password = getpass(yellow + ' - Your secure word: ' + mc)
            # Проверка хэша пароля
            enc_pas = EncryptionByTwoLevels(master_password, master_password)
            master_password_from_file = open(hash_password_file)
            enc_pas_from_file = ''
            for hash_pas in master_password_from_file.readlines():
                enc_pas_from_file = hash_pas
            if enc_pas == enc_pas_from_file:
                pass
            else:
                print(red + '\n --- Wrong password --- ' + mc)
                sleep(1.4)
                ClearTerminal()
                MainFun(None)
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
    key, lister_row, master_password = AuthConfirmPasswordAndGetUniqueSewnKey(master_password, False)
    return key, lister_row, resource, login


def DecryptionBlock(master_password, key, lister_row, resource, login):
    """ Show resources and decrypt them with keys """
    def AddResourceData(resource, login, key, master_password, lister_row):
        def TextChangePassword():
            print(green + ' 1' + yellow + ' - Generation new password \n' +
                  green + ' 2' + yellow + ' - Save your password \n' + mc)
        TextAddNewResource()
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
        try:
            change_resource_or_actions = input('\n Change: ')
            if change_resource_or_actions == '-a':  # Добавление нового ресурса
                AddResourceData(resource, login, key, master_password, lister_row)
            elif change_resource_or_actions == '-u':    # Обновление программы
                ClearTerminal()
                main_file = 'system_manager.py'
                delite_after_update = 'rm -r pwManager/ -f'
                os.system('git clone https://github.com/Berliner187/pwManager')
                if os.path.getsize(main_file) != os.path.getsize('pwManager/' + main_file):
                    change = input(yellow + ' - Update? (y/n): ' + mc)
                    if change == 'y':
                        os.system('cp pwManager/' + main_file + ' .; ' + delite_after_update)
                        ClearTerminal()
                        print(green + ' -- Update successfully! -- ' + mc)
                        sleep(1)
                        os.system('./' + main_file)
                    else:
                        os.system(delite_after_update)
                        ShowContent(key, master_password, lister_row)
                else:
                    ClearTerminal()
                    print(yellow + ' -- Nothing to upgrade, you have latest update -- ' + mc)
                    os.system(delite_after_update)
                    sleep(.7)
                    ShowContent(key, master_password, lister_row)
            elif change_resource_or_actions == '-d':    # Удаление ресурса
                print(blue + '\n -- Change by number resource -- ' + mc)
                change_res_by_num = int(input(yellow + ' - Resource number: ' + mc))
                # Выгрузка старого
                with open(file_date_base, encoding='utf-8') as saved_resource:
                    reader = DictReader(saved_resource, delimiter=',')
                    mas_res, mas_log, mas_pas = [], [], []
                    cnt = 0
                    for row in reader:
                        cnt += 1
                        if cnt == change_res_by_num:    # Перескакивает выбранный юзером и не добавляется
                            cnt += 1
                        else:   # Нужные ресурсы добавляются в массивы
                            mas_res.append(row["resource"])
                            mas_log.append(row["login"])
                            mas_pas.append(row["password"])
                    saved_resource.close()
                # Перенос в новый файл
                new_file_date_base = 'new_data.dat'
                with open(new_file_date_base, mode="a", encoding='utf-8') as new_data:
                    writer = DictWriter(new_data, fieldnames=['resource', 'login', 'password'])
                    writer.writeheader()
                    for i in range(cnt - 2):
                        writer.writerow({
                            'resource': mas_res[i],
                            'login': mas_log[i],
                            'password': mas_pas[i]})
                    new_data.close()
                copyfile(new_file_date_base, file_date_base)    # Старый записывается новым файлом
                os.system('rm ' + new_file_date_base)   # Удаление нового файла
                ShowContent(key, master_password, lister_row)
                DecryptionBlock(master_password, key, lister_row, resource, login)
            elif change_resource_or_actions == '-x':  # Условие выхода
                ClearTerminal()  # Clearing terminal
                print(blue, ' --- Program is closet --- \n', mc)
                sys.exit()  # Exit
            elif change_resource_or_actions == '-q':  # Условие перезапуска
                ClearTerminal()  # Clearing terminal
                RestartProgram()  # Restart program
            else:
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
                            # Дешифровка ресурса
                            decryption_res = DecryptionData(encryption_resource, key, master_password, lister_row)
                            decryption_log = DecryptionData(encryption_login, key, master_password, lister_row)
                            decryption_pas = DecryptionData(encryption_password, key, master_password, lister_row)
                            # Вывод данных по ресурсу
                            print('\n Resource:', green, decryption_res, mc,
                                  '\n Login:   ', green, decryption_log, mc,
                                  '\n Password:', green, decryption_pas, mc)
        except ValueError:
            ClearTerminal()
            ShowContent(key, master_password, lister_row)
            DecryptionBlock(master_password, key, lister_row, resource, login)
        DecryptionBlock(master_password, key, lister_row, resource, login)
    else:
        AddResourceData(resource, login, key, master_password, lister_row)
        RestartProgram()


def MainFun(master_password):
    """ The main function responsible for the operation of the program """
    if check_file_date_base == bool(False):   # Если файла нет, идет создание файла с ресурсами
        ClearTerminal()     # Очистка терминала
        print(blue + "\n  - Encrypt your passwords with one master-password -    "
                     "\n  -           No resources saved. Add them!         -  \n",
                     "\n ---                 That's easy!                  --- \n", mc)
        print(yellow + '\n --          Pick a master-password --          '
                       '\n - Только не используйте свой банковский пароль,'
                       '\n      я не сильно вкладывался в безопасность    '
                       '\n              этой программы ' + mc)
        if os.path.exists(main_folder) == bool(False):
            os.mkdir(main_folder)
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
        key, lister_row, master_password = AuthConfirmPasswordAndGetUniqueSewnKey(None, True)
        ClearTerminal()
        print(GreatingDependingOnDateTime(master_password))
        sleep(.7)
        ClearTerminal()
        ShowContent(key, master_password, lister_row)       # Показ содержимого файла с ресурсами
        DecryptionBlock(master_password, key, lister_row, None, None)  # Start cycle


try:  # Running a program through an exception
    if os.path.exists(main_folder) == bool(False):
        print(yellow + ' - There is no such account. Create? - ' + mc)
        change = input('\n (y/n): ')
        if change == 'y':
            if os.path.exists(users_folder + user_input_name) == bool(False):  # Папка с юзером
                os.mkdir(users_folder + user_input_name)
            main_folder = users_folder + user_input_name + '/' + 'files/'  # Папка с юзерскими файлами
            if os.path.exists(main_folder) == bool(False):
                os.mkdir(main_folder)
            master_password = ConfirmUserPass()
            hash_pas = open(hash_password_file, 'w')
            enc_pas = EncryptionByTwoLevels(master_password, master_password)
            hash_pas.write(enc_pas)
            hash_pas.close()
            MainFun(master_password)
        if change == 'n':
            ClearTerminal()
            RestartProgram()
    else:
        MainFun(None)
except ValueError:  # With this error (not entered value), the program is restarted
    print(red, '\n' + ' --- Critical error, program is restarted --- ', mc)
    sleep(1)
    ClearTerminal()
    RestartProgram()
