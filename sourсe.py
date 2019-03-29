import json as js


def _read_file(fl_names):
    try:
        dct_users = {}
        print('start read files.')
        cmds = []
        for fl_name in fl_names:
            # Удаляем лишние буквы для ключей, к-е будут в dict
            # file_userN.txt как userN
            dct_users.update({fl_name[5:-4]:'None'})
            print(dct_users)
            with open(fl_name, 'r') as data:
                cmds = data.readlines()
                # we know, than files will auto. closed
                # реализовать сразу запись в json файл
            for line in cmds:
                print(line.split())
                    #cmds.append(line.split)
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
