import json as js


def _read_file(fl_names):
    try:
        print('start read files.')
        dct_users = {}
        for fl_name in fl_names:
            cmds = []
            with open(fl_name, 'r') as data:
                commands = data.readlines()
                # we know, than files will auto. closed
                for line in commands:
                    cmds.append(line.split())
            # Удаляем лишние буквы для ключей, к-е будут в dict
            # file_userN.txt как userN
            # Добавляем ключи в словарь и сразу заполняем список данными
            tmp_name = fl_name[5:-4]
            dct_users.update({tmp_name: cmds})
            print(dct_users)
            del cmds
        print(dct_users)
    except IOError as ioerr:
        print('problems with files.', ioerr)



if __name__ == '__main__':
    try:
        print('start_app')
        # 1. Input cmd in files 1,2,3
        _read_file(['file_user1.txt',
                    'file_user2.txt',
                    'file_user3.txt'])
        # 2. Analyse:
        # - new cmd,
        # - del cmd,
        # - chg cmd
        # 3. Refresh file.json with some changes

    except ValueError as err:
        print('some error', err)
    finally:
        print('end_app')
