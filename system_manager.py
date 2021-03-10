#!/usr/bin/env python3
import os, sys


def EnterNickName():
    print('Enter your nickname')
    user_input_name = input('@')
    return user_input_name


names_file = 'names.dat'
if os.path.exists(names_file) == bool(False):
    with open(names_file, 'w') as f:
        user_input_name = EnterNickName()  # Функция ввода имени
        f.write(user_input_name)
        f.close()


def EnterPassword():
    password = input('Password: ')
    return password


names_open_file = open(names_file).readlines()      # Открытие файла с юзерами
if os.path.exists(names_file) == bool(True):
    user_input_name = EnterNickName()
    for name in names_open_file:     # Перебор среди сохраненных имен
        if name == user_input_name:
            print('действия с сохраненным именем')
            password = EnterPassword()
        else:
            print('Такого аккаунта нет. Создать?')
            change = input('(y/n): ')
            if change == 'y':
                user_input_name = EnterNickName()
                file_with_names = open(names_file)
                file_with_names.write(user_input_name)
