from main import system_action


def update(master_password, status):
    main_file = 'pwManager.py'  # Главный файл программы
    remove_main_folder = 'rm -r pwManager/ -f'
    os.system('git clone https://github.com/Berliner187/pwManager')
    system_action('clear')

    if os.path.getsize(main_file) != os.path.getsize('pwManager/' + main_file):
        install_or_no = input(yellow + ' - Install? (y/n): ' + mc)
        new_folder_pm = 'pwManager/'    # Новая папка из репозитория проекта
        if install_or_no == 'y':

            def actions_for_install(file):  # Действия для установки
                os.system('cp ' + new_folder_pm + file + ' . ; ')

            actions_for_install(main_file)
            actions_for_install('stars_module.py')
            actions_for_install('enc_module_obs.py')

            system_action('either')
        else:
            os.system(remove_main_folder)
            if status == bool(True):
                show_decryption_data(master_password)
                decryption_block(master_password)
    else:
        system_action('clear')
        print(yellow + ' -- Nothing to upgrade, you have latest update -- ' + mc)
        os.system(remove_main_folder)
        sleep(.7)