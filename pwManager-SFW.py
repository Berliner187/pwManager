# Password Manager program v1.1.3 Stable for Windows (BFW)
# by CISCer
import os
import csv
import base64
import random
import datetime
import time


# Colours
yellow, blue, green, mc, red = "\033[33m", "\033[34m", "\033[32m", "\033[0m", "\033[31m"  # mc - clean colours


try:
    import pyperclip
    import emoji
except ModuleNotFoundError:
    print(yellow + "... Wait ..." + mc)
    os.system("pip3 install pyperclip")
    os.system("pip install emoji")
    print(green + "--- Success ---" + mc)

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
    """ Фунция вывода времени суток """
    self_name_file = "files/.self_name.dat"     # Файл с именем (никнеймом)
    if os.path.exists(self_name_file) == False:     # Создание файла с именем
        with open(self_name_file, "w") as self_name:
            name = input(yellow + 'Your name or nickname: ' + mc)
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


# Перевод в двоичный вид
def text2bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


# Перевод из двоичного вида
def bits2text(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def CryptoBase64(message, key):
    enc = []
    for i in range(len(message)):
        key_c = key[i % len(key)]
        enc.append(chr((ord(message[i]) + ord(key_c)) % 256))
    encryption = base64.urlsafe_b64encode("".join(enc).encode()).decode()
    return encryption


def DecryptoBase64(encryption, key):
    dec = []
    message = base64.urlsafe_b64decode(encryption).decode()
    for i in range(len(message)):
        key_c = key[i % len(key)]
        dec.append(chr((256 + ord(message[i]) - ord(key_c)) % 256))
    return "".join(dec)


def ClearTerminal():
    """ Очистка консоли """
    print('\n'*100)


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
    print(green, '-- RESTART --', '\n' * 100, mc)
    time.sleep(1)
    ClearTerminal()


listers_file = os.path.exists("files/.listers.dat")
if listers_file == False:
    fuckingMakingFiles()


# Добавление символов из файла в список
def AppendInLister(oper_key):
    lyster_shuffle = []  # Пустой список
    with open("files/.listers.dat") as file:  # Файл с рандомными
        s = 0  # Счетчик (по умолчанию 0)
        for row in file:  # Перебор по строкам файла
            s += 1  # Счетчик увеличивается на 1
            if s == oper_key:  # Если значение счетчика равно опер-ключу
                for syb in row:  # Перебор строки посимвольно
                    lyster_shuffle.append(syb)  # Добавление символов в ранее пустой список
    return lyster_shuffle


# Encryption by Caesar
def CryptoCaesar(password, key_caesar, lister):
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

# Decryption by Caesar
def DecryptoCaesar(password, key_caesar, lister):
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


def fuckingSaveDataIfTrue(resource, login, password, key, lister, key_word):
    """ Шифрование логина и пароля. Сохранение в csv-файл (если этот файл есть) """
    with open(file_date_base, mode="a", encoding='utf-8') as data:
        fieldnames = ['resource', 'login', 'password']
        writer = csv.DictWriter(data, fieldnames=fieldnames)

        crypto_base_log = CryptoBase64(login, key_word)
        crypto_caesar_log = CryptoCaesar(crypto_base_log, key, lister)  # Next comes 3-pass encryption
        crypto_base_log = text2bits(crypto_caesar_log)  # To binary view

        crypto_base_pas = CryptoBase64(password, key_word)
        crypto_caesar_pas = CryptoCaesar(crypto_base_pas, key, lister)  # Next comes 3-pass encryption
        crypto_base_pas = text2bits(crypto_caesar_pas)  # To binary view

        writer.writerow({'resource': resource, 'login': crypto_base_log, 'password': crypto_base_pas})


def PasswordGeneraton():
    """ Генерирование нового случайного пароля """
    password_new = ''  # Password
    length = 24  # Amount
    for pass_gen in range(length):
        password_new += random.choice(lyster_for_pas)  # Password Adding random symbols from lister
    return password_new


def StartApp():
    """ The main function responsible for the operation of the program """

    def ChangeMethodSavePassword(change, resource, login, key, lister, key_word):
        """ Change: save user password or generation new """
        if change == 1:
            password = PasswordGeneraton()
            fuckingSaveDataIfFalse(resource, login, password, key, lister, key_word)
            print('Your new password - ' + green + password + mc + ' - success saved' + krokodil * 3 + mc)
            pyperclip.copy(password)
            time.sleep(2)
            ClearTerminal()
            StartApp()
        elif change == 2:
            password = input('Password: ')
            fuckingSaveDataIfTrue(resource, login, password, key, lister, key_word)
            ClearTerminal()
            print(green + '- Your password ' +
                  password[0] +
                  password[1] + '***' +
                  password[-1] + ' success saved -' + krokodil * 3 + mc)
            time.sleep(2)
            ClearTerminal()
            StartApp()
        else:
            print(red + shit + 'Error, please, change again' + shit + mc)
            time.sleep(1)
            ClearTerminal()
            StartApp()
    DateTime()
    # Если файла нет, создание файла с ресурсами
    if os.path.exists(file_date_base) == False:

        def fuckingSaveDataIfFalse(resource, login, password, key, lister, key_word):
            """ Шифрование логина и пароля. Сохранение в csv-файл (если этого файла нет)"""
            with open(file_date_base, mode="a", encoding='utf-8') as data:
                fieldnames = ['resource', 'login', 'password']
                writer = csv.DictWriter(data, fieldnames=fieldnames)
                writer.writeheader()

                crypto_base_log = CryptoBase64(login, key_word)
                crypto_caesar_log = CryptoCaesar(crypto_base_log, key, lister)  # Next comes 3-pass encryption
                crypto_base_log = text2bits(crypto_caesar_log)  # To binary view

                crypto_base_pas = CryptoBase64(password, key_word)
                crypto_caesar_pas = CryptoCaesar(crypto_base_pas, key, lister)  # Next comes 3-pass encryption
                crypto_base_pas = text2bits(crypto_caesar_pas)  # To binary view

                writer.writerow({'resource': resource, 'login': crypto_base_log, 'password': crypto_base_pas})

        print('\n', 'There are no resources saved. Add them:')
        resource = input('Resource: ')
        login = input('Login: ')

        pin = int(input('Key (6 numbers): '))  # Encryption key
        key_word = input('Secure word: ')
        key = pin // 10000
        oper_key = pin % 10000
        lister = AppendInLister(oper_key)

        print(green + '1' + yellow + ' - Generation new pas; ' + green + '2' + yellow + ' - save your pas: ' + mc)

        change = int(input('Change: '))
        ChangeMethodSavePassword(change, resource, login, key, lister, key_word)

    # Reader
    if os.path.exists(file_date_base) == True:
        # Если файл уже создан, выводтся содержимое и дальнейшее взаимодействие с программой происходит тут
        with open(file_date_base, encoding='utf-8') as data:
            s = 0
            reader = csv.DictReader(data, delimiter=',')
            print('\n'*5 + yellow + '--- Saved resources ---' + mc)
            for line in reader:
                s += 1
                print(str(s) + '.', line["resource"])

            print('\n' + blue + 'Enter "-r" to restart, "-x" to exit''\n' +
                  'Enter "-a", to add new resource''\n' +
                  yellow + 'Select resource by number ''\n' + mc)

            def ShowSolidarity():
                password_new = ''  # Password
                length = 21  # Amount
                for pass_gen in range(length):
                    password_new += random.choice(lyster_for_pas)  # Password Adding random symbols from lister

                resource_number = input('\n\n''Input: ')
                if resource_number == '-a':
                    print('\n' + green + krokodil + '-- Add new resource --' + krokodil + mc)
                    resource = input('Resource: ')
                    login = input('Login: ')

                    pin = int(input('Key (6 numbers): '))  # Encryption key
                    key = pin // 10000
                    oper_key = pin % 10000
                    lister = AppendInLister(oper_key)
                    key_word = input('Secure word: ')

                    print(green + '1' + yellow + ' - Generation new pas; ' +
                          green + '2' + yellow + ' - save your pas: ' + mc)

                    change = int(input('Change: '))
                    ChangeMethodSavePassword(change, resource, login, key, lister, key_word)

                elif resource_number == '-x':  # Condition exit
                    ClearTerminal()  # Clearing terminal
                    print(blue, '--- Program is closet ---' + '\n', mc)
                    quit()  # Exit
                elif resource_number == '-r':  # Condition restart
                    ClearTerminal()  # Clearing terminal
                    print('\n''-- Restart --')  # Show message of restart
                    StartApp()  # Start main function

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

                            pin = int(input('\n''Key (6 numbers): '))  # Encryption key
                            master_password = input('Secure word: ')
                            key = pin // 10000
                            oper_key = pin % 10000
                            lister = AppendInLister(oper_key)
                            # Decryption login
                            decryption_bin_log_one = bits2text(login)
                            decryption_caesar_log = DecryptoCaesar(decryption_bin_log_one, key, lister)
                            decryption_base_log = DecryptoBase64(decryption_caesar_log, master_password)
                            # Decryption password
                            decryption_bin_pas_one = bits2text(password)  # To binary view
                            decryption_caesar_pas = DecryptoCaesar(decryption_bin_pas_one, key, lister)
                            decryption_base_pas = DecryptoBase64(decryption_caesar_pas, master_password)

                            print('\n' +
                                  resource + ' --> ' +
                                  green + decryption_base_log + ' --> ' +
                                  decryption_base_pas + mc)
                            pyperclip.copy(decryption_base_pas)     # Copy password
                ShowSolidarity()
            ShowSolidarity()


if __name__ == '__main__':
    try:  # Running a program through an exception
        print(blue, '\n' 'Password manager v1.1.3 Beta for Windows' '\n' 'by CISCer' '\n', mc)  # Start text
        time.sleep(2)
        ClearTerminal()
        StartApp()
    except ValueError:  # With this error (not entered value), the program is restarted
        print(red, '\n' + shit + '--- ValueError, program is restarted ---' + shit, mc)
        time.sleep(1.5)
        ClearTerminal()
        StartApp()