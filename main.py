#!/usr/bin/env python3
# Password manager v1.5.0.0 Stable For Linux (SFL)
# Resources and notes related to them are encrypted with a single password
# by Berliner187
import os
import sys
from csv import DictReader, DictWriter
import random
from time import sleep
from shutil import copyfile
from werkzeug.security import generate_password_hash, check_password_hash


version = 'v1.5.0.0'    # Version program


def system_action(action):
    """ Restart Program or Clear terminal """
    if action == 'restart':
        os.execv(sys.executable, [sys.executable] + sys.argv)
    elif action == 'clear':
        os.system('cls' if os.name == 'nt' else 'clear')
    elif action == 'either':
        os.execv(sys.executable, [sys.executable] + sys.argv)
        os.system('cls' if os.name == 'nt' else 'clear')


# Colours
yellow, blue, purple, green, mc, red = "\033[33m", "\033[36m", "\033[35m", "\033[32m", "\033[0m", "\033[31m"

# List of all symbols for password
symbols_for_password = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-='

# Files for work program
main_folder = 'data/'
file_date_base = main_folder + "main_data.dat"     # Файл, в котором лежат пароли
file_lister = main_folder + ".lister.dat"   # Файл со строками
file_self_name = main_folder + ".self_name.dat"  # Файл с именем (никнеймом)
file_hash_password = main_folder + '.hash_password.dat'     # Файл с хэшем пароля
file_notes = main_folder + 'notes.csv'   # Файл с заметками
file_version = main_folder + '.version.log'  # Файл с версией программы

fields_for_logs = ['version', 'datetime', 'modules', 'status']     # Столбцы файла с логами
fields_for_main_data = ['resource', 'login', 'password']
fields_for_notes = ['name_note', 'note']
used_modules = ['stars_module_obs.py', 'datetime_obs.py', 'enc_module_obs.py']

check_file_hash_password = os.path.exists(file_hash_password)
check_file_date_base = os.path.exists(file_date_base)    # Проверка этого файла на наличие
check_file_lister = os.path.exists(file_lister)   # Проверка этого файла на наличие
check_file_notes = os.path.exists(file_notes)   # Проверка на наличие файла с заметками

if os.path.exists(main_folder) == bool(False):
    os.mkdir(main_folder)

if check_file_notes == bool(False):     # Создание файла с заметками
    with open(file_notes, mode="a", encoding='utf-8') as file_for_notes:
        open_note = DictWriter(file_for_notes, fieldnames=['name_note', 'note'])
        open_note.writeheader()


def save_data_to_file(resource, login, password, master_password):
    """ Шифрование логина и пароля. Запись в csv-файл """
    with open(file_date_base, mode="a", encoding='utf-8') as data:
        writer = DictWriter(data, fieldnames=fields_for_main_data)
        if check_file_date_base == bool(False):
            writer.writeheader()    # Запись заголовков
        # Шифрование данных ресурса
        enc_res = enc_data(resource, master_password)
        enc_log = enc_data(login, master_password)
        enc_pas = enc_data(password, master_password)
        writer.writerow({
            'resource': enc_res,
            'login': enc_log,
            'password': enc_pas})


def show_decryption_data(master_password):
    """ Показ всех сохраненных ресурсов """
    system_action('clear')
    with open(file_date_base, encoding='utf-8') as data:
        s = 0
        reader = DictReader(data, delimiter=',')
        print(yellow + '\n   --- Saved resources ---   ' + '\n'*3 + mc)
        for line in reader:
            encryption_resource = line["resource"]
            decryption_res = dec_data(encryption_resource, master_password)
            s += 1
            print(str(s) + '. ' + decryption_res)    # Decryption resource
        print(blue +
              '\n  - Enter "-r" to restart, "-x" to exit'
              '\n  - Enter "-a" to add new resource'
              '\n  - Enter "-c" to change master-password ' + red + 'BETA' + blue,
              '\n  - Enter "-d" to remove resource'
              '\n  - Enter "-u" to update program'
              '\n  - Enter "-n" to go to notes'
              '\n  - Enter "-z" to remove ALL data',
              yellow, '\n Select resource by number \n', mc)


def auth_with_password():    # Auth Confirm Password
    """ Получение мастер-пароля и доп. ключей """
    master_password = hide_password(yellow + ' -- Your master-password: ' + mc)
    if master_password == 'x':  # Досрочный выход из программы
        quit()
    # Проверка хэша пароля
    with open(file_hash_password, 'r') as hash_pas_from_file:
        hash_password = check_password_hash(hash_pas_from_file.readline(), master_password)
        if hash_password == bool(False):
            print(red + '\n --- Wrong password --- ' + mc)
            sleep(1)
            system_action('clear')
            system_action('restart')
        else:
            return master_password


def data_for_resource():
    """ Данные для сохранения (ресурс, логин, пароль) """
    system_action('clear')
    print(green, '\n   --- Add new resource ---   ', '\n' * 3, mc)  # Текст запроса ввода данных о ресурсе
    resource = input(yellow + ' Resource: ' + mc)
    login = input(yellow + ' Login: ' + mc)
    return resource, login


def confirm_user_password(type_pas):
    """ Подтвержение пользовательского пароля """
    def user_input_password():
        print(blue + '\n Minimum password length 8 characters' + mc)
        user_password = hide_password(' Password: ')
        if user_password == 'x':
            quit()
        user_confirm_password = hide_password(' Confirm password: ')  # hide_password(' Confirm password: ')
        if user_password != user_confirm_password or len(user_password) < 8:
            print(red + '\n Error of confirm. Try again \n' + mc)
            user_input_password()
        else:
            return user_password

    def generation_new_password():
        """ Генерирование нового случайного пароля """
        length_new_pas = int(input(yellow + ' - Length password (Minimum 8): ' + mc))
        new_password = ''  # Empty password
        for pas_elem in range(length_new_pas):
            new_password += random.choice(symbols_for_password)  # Password Adding random symbols from lister
        if len(new_password) > 8:
            return new_password  # Возвращает пароль
        else:
            print(red + '\n Error of confirm. Try again \n' + mc)
            generation_new_password()

    # Условаия принятия и подтверждения пароля
    if type_pas == 'self':
        password = user_input_password()
        return password
    elif type_pas == 'master':
        master_password = user_input_password()
        if check_file_hash_password == bool(False):  # Создание хэша
            hash_to_file = generate_password_hash(master_password)
            with open(file_hash_password, 'w') as hash_pas:
                hash_pas.write(hash_to_file)
                hash_pas.close()
        return master_password
    elif type_pas == 'gen_new':
        password = generation_new_password()
        print('  Your new password - ' + green + password + mc + ' - success saved')
        return password


def change_type_of_password():
    """ Выбор пароля: генерирование нового или сохрание пользовательского """

    print('\n',
          green + ' 1' + yellow + ' - Generation new password \n',
          green + ' 2' + yellow + ' - Save your password      \n', mc)

    change_type = int(input('Change (1/2): '))
    if change_type == 1:  # Generation new password
        password = confirm_user_password('gen_new')
        return password
    elif change_type == 2:  # Сохранение пользовательского пароля
        password = confirm_user_password('self')
        return password
    else:   # Если ошибка выбора
        print(red + '  -- Error of change. Please, change again --  ' + mc)
        change_type_of_password()
    sleep(2)
    system_action('clear')


def decryption_block(master_password):
    """ Show resources and decrypt them with keys """

    def text_prompting_you_to_choose_something(text):
        print(blue + '\n -- ' + text + ' -- \n' + mc)

    def prompting_to_input_something():
        change_something = int(input(yellow + ' - Resource number: ' + mc))
        return change_something

    def add_resource_data(master_password):
        if check_file_date_base == bool(False):
            resource, login = data_for_resource()
            password = change_type_of_password()
            save_data_to_file(resource, login, password, master_password)
            system_action('restart')
        else:
            resource, login = data_for_resource()  # Ввод данных для ресурса
            password = change_type_of_password()
            save_data_to_file(resource, login, password, master_password)
            show_decryption_data(master_password)

    if check_file_date_base == bool(True):
        # Decryption mechanism
        change_resource_or_actions = input('\n Change: ')
        try:
            if change_resource_or_actions == '-a':  # Добавление нового ресурса
                add_resource_data(master_password)
            elif change_resource_or_actions == '-u':    # Обновление программы из репозитория
                system_action('clear')
                update(master_password, True)
                show_decryption_data(master_password)
            elif change_resource_or_actions == '-x':  # Условие выхода
                system_action('clear')  # Clearing terminal
                print(blue, ' --- Program is closet --- \n', mc)
                sys.exit()  # Exit
            elif change_resource_or_actions == '-r':  # Условие перезапуска
                system_action('clear')  # Clearing terminal
                print('\n', green, ' -- Restart -- ', mc)
                sleep(.4)
                system_action('clear')
                system_action('restart')  # Restart program
            elif change_resource_or_actions == '-c':
                system_action('clear')
                # Сверяются хеши паролей
                confirm_master_password = hide_password(yellow + ' -- Enter your master-password: ' + mc)
                hash_confirm_master_password = enc_data(confirm_master_password, master_password)
                saved_master_password = open(file_hash_password)
                enc_pas_from_file = ''
                for hash_pas in saved_master_password.readlines():
                    enc_pas_from_file = hash_pas
                if hash_confirm_master_password != enc_pas_from_file:
                    print(red + '\n --- Wrong password --- ' + mc)
                    sleep(1)
                else:
                    pass    # Допилить фичу
                show_decryption_data(master_password)
            elif change_resource_or_actions == '-d':    # Удаление ресурса
                text_prompting_you_to_choose_something('Change by number resource')
                change_res_by_num = prompting_to_input_something()
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
                    writer = DictWriter(new_data, fieldnames=fields_for_main_data)
                    writer.writeheader()
                    for i in range(cnt - 2):
                        writer.writerow({
                            'resource': mas_res[i],
                            'login': mas_log[i],
                            'password': mas_pas[i]})
                    new_data.close()
                copyfile(new_file_date_base, file_date_base)    # Старый записывается новым файлом
                os.system('rm ' + new_file_date_base)   # Удаление нового файла
                show_decryption_data(master_password)   # Вывод ресурсов
            elif change_resource_or_actions == '-n':    # Добавление зашифрованных заметок
                system_action('clear')
                while True:     # Старт цикла для работы с заметками
                    def show():     # Показ сохраненных заметок
                        with open(file_notes, encoding='utf-8') as notes:
                            reader_notes = DictReader(notes, delimiter=',')
                            print(yellow + '       ---  Saved notes --- ', '\n' * 3 + mc)
                            number_note = 0     # Номер заметки
                            for name in reader_notes:   # Перебор названий заметок
                                number_note += 1
                                dec_name_note = dec_data(name["name_note"], master_password)
                                # Вывод названий заметок и их порядкового номера
                                print(str(number_note) + '.', dec_name_note)
                            print(blue + '\n  - Press "Enter" to go back'
                                         '\n  - Enter "-a" to add new note'
                                         '\n  - Enter "-d" to remove note',
                                  yellow, '\n Select note by number', mc)
                    show()

                    def add_new():  # Добавление новой заметки
                        system_action('clear')
                        print(blue + '    ---  Add new note  --- \n\n')
                        with open(file_notes, mode="a", encoding='utf-8') as data_note:
                            writer_note_add = DictWriter(data_note, fieldnames=fields_for_notes)
                            name_note = input(yellow + ' - Note name: ' + mc)
                            note = input(purple + ' - Note: ' + mc)
                            enc_name_note = enc_data(name_note, master_password)
                            enc_note = enc_data(note, master_password)
                            writer_note_add.writerow({
                                'name_note': enc_name_note,
                                'note': enc_note})
                        print(green, '   -- Success saved! --')
                        sleep(.3)
                        system_action('clear')
                        show()

                    def work():     # Работа в лейбле с заметками
                        change_action = input('\n - Change: ')  # Выбор между действиями
                        if change_action == '-a':   # Пользователь выбирает добавление новой заметки
                            add_new()
                        elif change_action == '-d':  # Пользователь выбирает удаление старой заметки
                            text_prompting_you_to_choose_something('Change by number note')
                            change_note_by_num = prompting_to_input_something()
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
                                write_note = DictWriter(new_notes, fieldnames=fields_for_notes)
                                write_note.writeheader()
                                for j in range(cnt_note-2):
                                    write_note.writerow({
                                        'name_note': mas_name_note_rm[j],
                                        'note': mas_note_rm[j]})
                                new_notes.close()
                            # Замена старого файла на актуальный
                            copyfile(new_file_notes, file_notes)  # Старый записывается новым файлом
                            os.system('rm ' + new_file_notes)  # Удаление нового файла
                            system_action('clear')
                            show()
                        else:   # Вывод дешифрованных данных по выбранной цифре
                            with open(file_notes, encoding='utf-8') as saved_note:  # Открытие в csv-формате
                                read_note = DictReader(saved_note, delimiter=',')   # Чтение библиоткой csv
                                count = 0   # Счетчик
                                for line_of_note in read_note:
                                    count += 1
                                    if count == int(change_action):  # Если счетчик совпадает с выбранным значением
                                        system_action('clear')
                                        show()  # Показываются сохраненные имена заметок
                                        # Выводится зашифрованный вид выбранной заметки
                                        print(yellow, '\n Name:', green,
                                              dec_data(line_of_note["name_note"], master_password), mc,
                                              yellow, '\n Note:', green,
                                              dec_data(line_of_note["note"], master_password), mc)
                        work()  # Рекурсия
                    work()  # Запуск
            elif change_resource_or_actions == '-z':    # Удаление всех данных пользователя
                system_action('clear')
                print(red + '\n\n - Are you sure you want to delete all data? - ' + mc)
                change_yes_or_no = input(yellow + ' - Remove ALL data? (y/n): ' + mc)   # Запрос подтверждения
                if change_yes_or_no == 'y':
                    os.system('rm -r files/')   # Удаление папки
                    system_action('clear')
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
                            system_action('clear')
                            show_decryption_data(master_password)

                            def resource_template(type_data, value):  # Шаблон вывода данных о ресурсе
                                print(yellow, type_data, ':', green, dec_data(line[value], master_password), mc)

                            resource_template('Resource', 'resource')
                            resource_template('Login   ', 'login')
                            resource_template('Password', 'password')
        except ValueError:
            show_decryption_data(master_password)   # Показ содежимого
        decryption_block(master_password)  # Рекусрия под-главной функции
    else:
        add_resource_data(master_password)
        system_action('restart')


def launcher():
    """ The main function responsible for the operation of the program """
    if check_file_date_base == bool(False):   # Если файла нет, идет создание файла с ресурсами
        print(blue +
              "\n  - Encrypt your passwords with one master-password -    "
              "\n  -           No resources saved. Add them!         -  \n"
              "\n ----                That's easy!                 ---- \n",
              red,
              "\n         Программа не поддерживает русский язык          ",
              yellow,
              '\n --              Создание мастер-пароля               -- '
              '\n --    Только не используйте свой банковский пароль,  -- '
              '\n          я не сильно вкладывался в безопасность         '
              '\n                     этой программы                      ' + mc)

        master_password = confirm_user_password('master')  # Создание мастер-пароля
        greeting(master_password)  # Вывод приветствия
        sleep(.5)
        decryption_block(master_password)
        system_action('restart')
    else:
        # Если файл уже создан, выводтся содержимое и дальнейшее взаимодействие с программой происходит тут
        master_password = auth_with_password()
        system_action('clear')
        greeting(master_password)  # Вывод приветствия
        sleep(.5)
        system_action('clear')
        show_decryption_data(master_password)       # Показ содержимого файла с ресурсами
        decryption_block(master_password)  # Старт цикла


if __name__ == '__main__':
    system_action('clear')
    try:
        from logo import elba
        from enc_module import enc_data, dec_data
        from datetime_obs import greeting
        from stars_module_obs import hide_password
        from update import update

        elba()
        print(blue, "\n Password Manager", version, "Stable For Linux (SFL) \n by Berliner187 ", '\n' * 3, mc)
        launcher()

    except ModuleNotFoundError:
        pass
    except ValueError:
        print(red, '\n' + ' --- Critical error, program is restarted --- ', mc)
        sleep(1)
        system_action('clear')
        print(red + ' -- You can try to update the program -- \n' + mc)
        change = input(yellow + ' - Update? (y/n): ' + mc)
        if change == 'y':  # Если получает запрос от юзера
            update(None, False)
        system_action('clear')
