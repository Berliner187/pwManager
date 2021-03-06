#!/usr/bin/env python3
# Password manager v1.4.5.13 Stable For Linux (SFL)
# Resources and all data related to them are encrypted with a single password
# by Berliner187
import os, sys
from csv import DictReader, DictWriter
import random
import datetime
from time import sleep
from shutil import copyfile


def RestartProgram():
    """ Restart Program """
    os.execv(sys.executable, [sys.executable] + sys.argv)


def ClearTerminal():
    """ Clear terminal """
    os.system('cls' if os.name == 'nt' else 'clear')


# Colours
yellow, blue, purple, green, mc, red = "\033[33m", "\033[36m", "\033[35m", "\033[32m", "\033[0m", "\033[31m"

version = 'v1.4.5.14'    # Version program
symbols_for_password = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-='  # List of all symbols
main_symbols = """ abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-=+!@#$%^&*(){}[]'<>,.|/?"""

# Files for work program
main_folder = 'files/'
file_date_base = main_folder + "main_data.dat"     # Файл, в котором лежат пароли
file_lister = main_folder + ".lister.dat"   # Файл со строками
file_self_name = main_folder + ".self_name.dat"  # Файл с именем (никнеймом)
file_hash_password = main_folder + '.hash_password.dat'     # Файл с хэшем пароля
file_notes = main_folder + 'notes.csv'   # Файл с заметками
file_version = main_folder + '.version.log'  # Файл с версией программы
log_fields = ['version', 'datetime', 'installed_modules', 'status']     # Столбцы файла с логами

check_file_date_base = os.path.exists(file_date_base)    # Проверка этого файла на наличие
check_file_lister = os.path.exists(file_lister)   # Проверка этого файла на наличие
check_file_notes = os.path.exists(file_notes)   # Проверка на наличие файла с заметками

if os.path.exists(main_folder) == bool(False):
    os.mkdir(main_folder)


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
    if os.path.exists(file_self_name) == bool(False):  # Создание файла с именем
        with open(file_self_name, "w") as self_name:
            name = input(yellow + ' - Your name or nickname: ' + mc)
            enc_name = enc_module_obs.EncryptionByTwoLevels(name, master_password)
            self_name.write(enc_name)
            self_name.close()
            return Time(name)
    else:  # Чтение из файла с именем и вывод в консоль
        with open(file_self_name, "r") as self_name:
            dec_name = self_name.readline()
            name = enc_module_obs.DecryptionByTwoLevels(dec_name, master_password)
            return Time(name)


def SaveDataToFile(resource, login, password, key, lister, master_password):
    """ Шифрование логина и пароля. Запись в csv-файл """
    with open(file_date_base, mode="a", encoding='utf-8') as data:
        writer = DictWriter(data, fieldnames=['resource', 'login', 'password'])
        if check_file_date_base == bool(False):
            writer.writeheader()    # Запись заголовков
        # Шифрование данных ресурса
        crypto_res = enc_module_obs.EncryptionData(resource, key, master_password, lister)
        crypto_log = enc_module_obs.EncryptionData(login, key, master_password, lister)
        crypto_pas = enc_module_obs.EncryptionData(password, key, master_password, lister)
        writer.writerow({
            'resource': crypto_res,
            'login': crypto_log,
            'password': crypto_pas})


def ConfirmUserPass():
    """ Подтвержение пользовательского пароля """
    def UserInput():
        user_password = hide_password(' Password: ')
        user_confirm_password = hide_password(' Confirm password: ')
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
    """ Выбор пароля: генерирование нового или сохрание """
    def DoForNewGeneratedPassword(resource, login, password, key, lister, master_password):
        SaveDataToFile(resource, login, password, key, lister, master_password)
        print('  Your new password - ' + green + password + mc + ' - success saved')

    def GenerationPassword(length):
        """ Генерирование нового случайного пароля """
        pas_gen = ''  # Empty password
        for pas_elem in range(length):
            pas_gen += random.choice(symbols_for_password)  # Password Adding random symbols from lister
        return pas_gen  # Возвращает пароль

    print('\n',
          green + ' 1' + yellow + ' - Generation new password \n',
          green + ' 2' + yellow + ' - Save your password      \n', mc)
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
        sleep(3)

    elif change == 2:  # Сохранение пользовательского пароля
        password = ConfirmUserPass()  # Ввод пароля
        SaveDataToFile(resource, login, password, key, lister, master_password)
        print(green + '\n  - Your password successfully saved! -  ' + mc)
        sleep(1)
    else:   # Если ошибка выбора
        print(red + '  -- Error of change. Please, change again --  ' + mc)
        sleep(1)
        ChangeTypeOfPass(resource, login, key, master_password, lister)
    ClearTerminal()

    if check_file_date_base == bool(False):  # Перезапуск для корректной работы
        RestartProgram()
    else:
        ShowContent(key, master_password, lister)   # Показ содержимого файла с ресурсами
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
            decryption_res = enc_module_obs.DecryptionData(encryption_resource, key, master_password, lister)
            s += 1
            print(str(s) + '. ' + decryption_res)    # Decryption resource
        print(blue +
              '\n  - Enter "-r" to restart, "-x" to exit'
              '\n  - Enter "-a" to add new resource'
              '\n  - Enter "-d" to remove resource'
              '\n  - Enter "-u" to update program'
              '\n  - Enter "-n" to go to notes'
              '\n  - Enter "-z" to remove ALL data',
              yellow, '\n Select resource by number \n', mc)


def AuthConfirmPasswordAndGetUniqueSewnKey(master_password, status):
    """ Получение мастер-пароля и доп. ключей """
    def GetKeys():
        key, additional_key = lister_module.HH(master_password)  # Получение новых ключей
        return int(key), int(additional_key)
    if check_file_date_base == bool(False):
        key, additional_key = GetKeys()
        lister_row = lister_module.GL(additional_key, master_password)  # Change row encryption
        return key, lister_row, master_password
    else:
        if status == bool(True):    # Если аргумент status истинен, то идет запрос пароля
            master_password = hide_password(yellow + ' -- Your master-password: ' + mc)
            if master_password == 'x':  # Досрочный выход из программы
                quit()
            # Проверка хэша пароля
            enc_pas = enc_module_obs.EncryptionByTwoLevels(master_password, master_password)
            master_password_from_file = open(file_hash_password)
            enc_pas_from_file = ''
            for hash_pas in master_password_from_file.readlines():
                enc_pas_from_file = hash_pas
            if enc_pas != enc_pas_from_file:
                print(red + '\n --- Wrong password --- ' + mc)
                sleep(1)
                ClearTerminal()
                MainFun()
        key, additional_key = GetKeys()  # Получение ключей
        lister_row = lister_module.GL(additional_key, master_password)  # Change row encryption
        return key, lister_row, master_password


def DataForResource(master_password):
    """ Данные для сохранения (ресурс, логин, пароль) """
    ClearTerminal()
    print(green, '\n   --- Add new resource ---   ', '\n' * 3, mc)  # Текст запроса ввода данных о ресурсе
    resource = input(yellow + ' Resource: ' + mc)
    login = input(yellow + ' Login: ' + mc)
    key, lister_row, master_password = AuthConfirmPasswordAndGetUniqueSewnKey(master_password, False)
    return key, lister_row, resource, login


def UpdateProgram(master_password, key, lister_row, resource, login, status):
    main_file = 'pwManager.py'  # Главный файл программы
    remove_main_folder = 'rm -r pwManager/ -f'
    os.system('git clone https://github.com/Berliner187/pwManager')
    ClearTerminal()

    if os.path.getsize(main_file) != os.path.getsize('pwManager/' + main_file):
        install_or_no = input(yellow + ' - Install? (y/n): ' + mc)
        new_folder_pm = 'pwManager/'    # Новая папка из репозитория проекта
        if install_or_no == 'y':

            def actions_for_install(file):  # Действия для установки
                os.system('cp ' + new_folder_pm + file + ' . ; ')

            actions_for_install(main_file)
            actions_for_install('stars_module.py')
            actions_for_install('enc_module_obs.py')
            actions_for_install('lister_module_obs.py')

            ClearTerminal()
            if status == bool(True):    # Если нет файла с ресурсами, программа перезапускается
                RestartProgram()
        else:
            os.system(remove_main_folder)
            if status == bool(True):   # Если статус требует True
                ShowContent(key, master_password, lister_row)
                DecryptionBlock(master_password, key, lister_row, resource, login)
    else:
        ClearTerminal()
        print(yellow + ' -- Nothing to upgrade, you have latest update -- ' + mc)
        os.system(remove_main_folder)
        sleep(.7)


if check_file_notes == bool(False):     # Создание файла с заметками
    with open(file_notes, mode="a", encoding='utf-8') as file_for_notes:
        open_note = DictWriter(file_for_notes, fieldnames=['name_note', 'note'])
        open_note.writeheader()


def DecryptionBlock(master_password, key, lister_row, resource, login):
    """ Show resources and decrypt them with keys """
    def AddResourceData(resource, login, key, master_password, lister_row):
        if check_file_date_base == bool(False):
            ChangeTypeOfPass(resource, login, key, master_password, lister_row)
        else:
            key, lister_row, resource, login = DataForResource(master_password)  # Ввод данных для ресурса
            ChangeTypeOfPass(resource, login, key, master_password, lister_row)
            DecryptionBlock(master_password, key, lister_row, resource, login)

    if check_file_date_base == bool(True):
        # Decryption mechanism
        change_resource_or_actions = input('\n Change: ')
        try:
            if change_resource_or_actions == '-a':  # Добавление нового ресурса
                AddResourceData(resource, login, key, master_password, lister_row)
            elif change_resource_or_actions == '-u':    # Обновление программы из репозитория
                ClearTerminal()
                UpdateProgram(master_password, key, lister_row, resource, login, True)
                ShowContent(key, master_password, lister_row)
            elif change_resource_or_actions == '-x':  # Условие выхода
                ClearTerminal()  # Clearing terminal
                print(blue, ' --- Program is closet --- \n', mc)
                sys.exit()  # Exit
            elif change_resource_or_actions == '-r':  # Условие перезапуска
                ClearTerminal()  # Clearing terminal
                print('\n', green, ' -- Restart -- ', mc)
                sleep(.5)
                ClearTerminal()
                RestartProgram()  # Restart program
            elif change_resource_or_actions == '-c':
                ClearTerminal()
                # Сверяются хеши паролей
                confirm_master_password = hide_password(yellow + ' -- Enter your master-password: ' + mc)
                hash_confirm_master_password = enc_module_obs.EncryptionByTwoLevels(confirm_master_password, master_password)
                saved_master_password = open(file_hash_password)
                enc_pas_from_file = ''
                for hash_pas in saved_master_password.readlines():
                    enc_pas_from_file = hash_pas
                if hash_confirm_master_password != enc_pas_from_file:
                    print(red + '\n --- Wrong password --- ' + mc)
                    sleep(1)
                else:
                    pass    # Допилить фичу
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
                ShowContent(key, master_password, lister_row)   # Вывод ресурсов
            elif change_resource_or_actions == '-n':    # Добавление зашифрованных заметок
                ClearTerminal()
                while True:     # Старт цикла для работы с заметками
                    def show():     # Показ сохраненных заметок
                        with open(file_notes, encoding='utf-8') as notes:
                            reader_notes = DictReader(notes, delimiter=',')
                            print(yellow + '       ---  Saved notes --- ', '\n' * 3 + mc)
                            number_note = 0     # Номер заметки
                            for name in reader_notes:   # Перебор названий заметок
                                number_note += 1
                                dec_name_note = enc_module_obs.DecryptionData(name["name_note"], key,
                                                                              master_password, lister_row)
                                # Вывод названий заметок и их порядкового номера
                                print(str(number_note) + '.', dec_name_note)
                            print(blue + '\n  - Press "Enter" to go back'
                                         '\n  - Enter "-a" to add new note'
                                         '\n  - Enter "-d" to remove note',
                                  yellow, '\n Select note by number', mc)
                    show()

                    def add_new():  # Добавление новой заметки
                        ClearTerminal()
                        print(blue + '    ---  Add new note  --- \n\n')
                        with open(file_notes, mode="a", encoding='utf-8') as data_note:
                            writer_note_add = DictWriter(data_note, fieldnames=['name_note', 'note'])
                            name_note = input(yellow + ' - Note name: ' + mc)
                            note = input(purple + ' - Note: ' + mc)
                            enc_name_note = enc_module_obs.EncryptionData(name_note, key, master_password, lister_row)
                            enc_note = enc_module_obs.EncryptionData(note, key, master_password, lister_row)
                            writer_note_add.writerow({
                                'name_note': enc_name_note,
                                'note': enc_note})
                        print(green, '   -- Success saved! --')
                        sleep(.3)
                        ClearTerminal()
                        show()

                    def work():     # Работа в лейбле с заметками
                        change_action = input('\n - Change: ')  # Выбор между действиями
                        if change_action == '-a':   # Пользователь выбирает добавление новой заметки
                            add_new()
                        elif change_action == '-d':  # Пользователь выбирает удаление старой заметки
                            print(blue + '\n -- Change by number note -- ' + mc)
                            change_note_by_num = int(input(yellow + ' - Note number: ' + mc))   # Выбор цифрой
                            # Выгрузка старого
                            with open(file_notes, encoding='utf-8') as saved_note:
                                read_note = DictReader(saved_note, delimiter=',')
                                mas_name_note_rm, mas_note_rm = [], []
                                cnt_note = 0
                                for row_note in read_note:
                                    cnt_note += 1
                                    if cnt_note == change_note_by_num:
                                        cnt_note += 1
                                    else:  # Нужные ресурсы добавляются в массивы
                                        mas_name_note_rm.append(row_note["name_note"])
                                        mas_note_rm.append(row_note["note"])
                                saved_note.close()
                            # Перенос в новый файл
                            new_file_notes = 'new_note.dat'
                            with open(new_file_notes, mode="a", encoding='utf-8') as new_notes:
                                write_note = DictWriter(new_notes, fieldnames=['name_note', 'note'])
                                write_note.writeheader()
                                for j in range(cnt_note-2):
                                    write_note.writerow({
                                        'name_note': mas_name_note_rm[j],
                                        'note': mas_note_rm[j]})
                                new_notes.close()
                            # Замена старого файла на актуальный
                            copyfile(new_file_notes, file_notes)  # Старый записывается новым файлом
                            os.system('rm ' + new_file_notes)  # Удаление нового файла
                            ClearTerminal()
                            show()
                        else:   # Вывод дешифрованных данных по выбранной цифре
                            with open(file_notes, encoding='utf-8') as saved_note:  # Открытие в csv-формате
                                read_note = DictReader(saved_note, delimiter=',')   # Чтение библиоткой csv
                                count = 0   # Счетчик
                                for line_of_note in read_note:
                                    count += 1
                                    if count == int(change_action):  # Если счетчик совпадает с выбранным значением
                                        ClearTerminal()
                                        show()  # Показываются сохраненные имена заметок
                                        # Выводится зашифрованный вид выбранной заметки
                                        print(yellow, '\n Name:', green,
                                              enc_module_obs.DecryptionData(line_of_note["name_note"], key,
                                                             master_password, lister_row), mc,
                                              yellow, '\n Note:', green,
                                              enc_module_obs.DecryptionData(line_of_note["note"], key,
                                                             master_password, lister_row), mc)
                        work()  # Рекурсия
                    work()  # Запуск
            elif change_resource_or_actions == '-z':    # Удаление всех данных пользователя
                ClearTerminal()
                print(red + '\n\n - Are you sure you want to delete all data? - ' + mc)
                change_yes_or_no = input(yellow + ' - Remove ALL data? (y/n): ' + mc)   # Запрос подтверждения
                if change_yes_or_no == 'y':
                    os.system('rm -r files/')   # Удаление папки
                    ClearTerminal()
                    quit()
                else:
                    pass
            else:
                with open(file_date_base, encoding='utf-8') as profiles:
                    reader = DictReader(profiles, delimiter=',')
                    s = 0
                    for line in reader:  # Iterating over lines file
                        s += 1
                        if s == int(change_resource_or_actions):
                            ClearTerminal()
                            ShowContent(key, master_password, lister_row)

                            def ResourceTemplate(type, value):  # Шаблон вывода данных о ресурсе
                                print(yellow, type + ':', green,
                                      enc_module_obs.DecryptionData(line[value], key, master_password, lister_row), mc)
                            ResourceTemplate('Resource', 'resource')
                            ResourceTemplate('Login   ', 'login')
                            ResourceTemplate('Password', 'password')
        except ValueError:
            ShowContent(key, master_password, lister_row)   # Показ содежимого
        DecryptionBlock(master_password, key, lister_row, resource, login)  # Рекусрия под-главной функции
    else:
        AddResourceData(resource, login, key, master_password, lister_row)
        RestartProgram()


def MainFun():
    """ The main function responsible for the operation of the program """
    if check_file_date_base == bool(False):   # Если файла нет, идет создание файла с ресурсами
        print(blue + "\n  - Encrypt your passwords with one master-password -    "
                     "\n  -           No resources saved. Add them!         -  \n"
                     "\n ----                That's easy!                 ---- \n",
              red,
                     "\n         Программа не поддерживает русский язык          ",
              yellow,
                     '\n --              Создание мастер-пароля               -- '
                     '\n --    Только не используйте свой банковский пароль,  -- '
                     '\n          я не сильно вкладывался в безопасность         '
                     '\n                     этой программы                      ' + mc)
        master_password = ConfirmUserPass()     # Создание мастер-пароля
        hash_pas = open(file_hash_password, 'w')    # Открытие файла с хэшем
        enc_pas = enc_module_obs.EncryptionByTwoLevels(master_password, master_password)   # Шифрование мастер-пароля
        hash_pas.write(enc_pas)     # Хэш записывается в файл
        hash_pas.close()    # Закрытие файла
        if check_file_lister == bool(False):    # Если файла со строкасм нет, то они генерируются
            lister_module.CL(master_password, main_symbols)
        print(GreatingDependingOnDateTime(master_password))     # Вывод приветствия
        sleep(.5)
        key, lister_row, resource, login = DataForResource(master_password)     # Ввод данных для ресурса
        DecryptionBlock(master_password, key, lister_row, resource, login)  # Старт цикла
    else:
        # Если файл уже создан, выводтся содержимое и дальнейшее взаимодействие с программой происходит тут
        key, lister_row, master_password = AuthConfirmPasswordAndGetUniqueSewnKey(None, True)
        ClearTerminal()
        print(GreatingDependingOnDateTime(master_password))
        sleep(.5)
        ShowContent(key, master_password, lister_row)       # Показ содержимого файла с ресурсами
        DecryptionBlock(master_password, key, lister_row, None, None)  # Старт цикла


def WriteLogsToFile(status):   # Функция записи в файл версии
    global file_version
    with open(file_version, mode="a", encoding='utf-8') as log_data:
        log_writer = DictWriter(log_data, fieldnames=log_fields, delimiter=';')

        def GetDateTime():      # Получение и форматирование текущего времени
            hms = datetime.datetime.today()  # Дата и время
            day, month, year = hms.day, hms.month, hms.year     # Число, месяц, год
            hour = hms.hour  # Формат часов
            minute = hms.minute  # Формат минут
            second = hms.second  # Формат секунд
            time_format = str(hour) + ':' + str(minute) + ':' + str(second)
            date_format = str(day) + '.' + str(month) + '.' + str(year)
            total = str(time_format) + '-' + str(date_format)
            return ''.join(total)

        def GetInstalledModules():
            file_type = 'obs.py'
            any_file = os.listdir('.')
            modules = []
            for file in any_file:
                if file.endswith(file_type):
                    modules.append(file)
            return modules

        log_writer.writerow({
            log_fields[0]: version,     # Запись версии
            log_fields[1]: GetDateTime(),     # Запись даты и времени
            log_fields[2]: GetInstalledModules(),     # Запись установленных модулей
            log_fields[3]: status})


if __name__ == '__main__':
    try:  # Running a program through an exception
        import enc_module_obs
        import lister_module_obs
        from stars_module_obs import hide_password

        lister_module = lister_module_obs
        ClearTerminal()
        print(blue, '\n Password Manager', version, 'Stable For Linux (SFL) \n by Berliner187' '\n', mc)  # Start text

        if os.path.exists(file_version) == bool(False):     # Создание, если его нет
            with open(file_version, mode="a", encoding='utf-8') as data:
                logg_writer = DictWriter(data, fieldnames=log_fields, delimiter=';')
                logg_writer.writeheader()  # Запись заголовков
            WriteLogsToFile('OK')    # Запись версии в файл
        else:
            with open(file_version, encoding='utf-8') as version_from_file:
                log_reader = DictReader(version_from_file, delimiter=';')
                last_v = ''
                for last_version in log_reader:
                    if version != last_version["version"]:   # Если не совпадают, перезаписывается актуальной версией
                        WriteLogsToFile('Update')   # Запись версии в файл
        MainFun()
    except ModuleNotFoundError:
        WriteLogsToFile('ModuleNotFoundError')
        print(green + ' - Installing the missing module - ' + mc)
        sleep(1)

        def actions_for_install(file):  # Действия для установки
            os.system('cp pwManager/' + file + ' . ; ')

        os.system('git clone https://github.com/Berliner187/pwManager')
        actions_for_install('stars_module_obs.py')
        actions_for_install('enc_module_obs.py')
        actions_for_install('lister_module_obs.py')
        os.system('rm -r pwManager/ -f')
        RestartProgram()
    except ValueError:  # With this error (not entered value), the program is restarted
        WriteLogsToFile('ValueError')
        print(red, '\n' + ' --- Critical error, program is restarted --- ', mc)
        sleep(1)
        ClearTerminal()
        print(red + ' -- You can try to update the program -- \n' + mc)
        change = input(yellow + ' - Update? (y/n): ' + mc)
        if change == 'y':   # Если получает запрос от юзера
            UpdateProgram(None, None, None, None, None, True)
        RestartProgram()
