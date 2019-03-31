from importlib import reload
import json as js
import module1
import module2


def _read_file(fl_names):
    try:
        print('read users files.')
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
            #print(dct_users)
            del cmds
        #print(dct_users)
    except IOError as ioerr:
        print('problems with files.', ioerr)
        del dct_users
        return dct_users
    finally:
        return dct_users


def _update_json(cur_dct, tmp_dct, name_wrk):
    # берем ключи, делаем дикт с ними
    # сравниваем количество элементах в списках
    # может быть сравниваем элементы
    print('CUR_DCT\n',cur_dct)
    print('TMP_DCT\n',tmp_dct)
    #cur_dct = sorted(cur_dct)
    #tmp_dct = sorted(tmp_dct)
    # проверяем сколько значений есть в каждом ключе
    print(cur_dct.keys())
    print(tmp_dct.keys())
    # проверка что уже имеем дело с копией
    if bool(tmp_dct):
        print('по очереди перебираем ключи')
        print('сравниваем количество команд каждого пользователя')
        for key in cur_dct.keys():
            print('************************************')
            print('Изменения ',key,':')
            if len(cur_dct[key]) != len(tmp_dct[key]):
                if len(cur_dct[key]) > len(tmp_dct[key]):
                    print('появилась новая команда.', cur_dct[key][-1])
                else:
                    print('удалена последняя команда.')
                    print('команда:', tmp_dct[key][-1])
                    print('тек. послед. ком', cur_dct[key][-1])
            else:
                if cur_dct[key] != tmp_dct[key]:
                    print('подмена команды.')
                    print('изначально:',tmp_dct[key][-1])
                    print('стало:', cur_dct[key][-1])
                else:
                    print('нет.')

    js_data = _read_json(name_wrk)
    print('JS_DCT\n',js_data)


def _read_json(name_jsfile):
    print('*********************************','\nread json file')
    # его не обязательно читать
    with open(name_jsfile, "r") as read_file:
        return js.load(read_file)


if __name__ == '__main__':
    try:
        n = 'None'
        # словарь хранящий копию логов о пользователе
        tmp_dct = {}
        print('first start app')
        while n != 'n':
            # 1. Input cmd in files 1,2,3
            dct_wrk = _read_file(['file_user1.txt',
                                  'file_user2.txt',
                                  'file_user3.txt'])

            # 2. Analyse:
            if type(dct_wrk) != type(tmp_dct):
                print('разные входные типы')
            elif not isinstance(dct_wrk, dict):
                print('left не dict')
            elif not isinstance(tmp_dct, dict):
                print('right не dict')
            else:
                _update_json(dct_wrk, tmp_dct, 'file.json')
            # 3. Refresh file.json with some changes

            # думал изначально что может понадобиться какая-то работа
            # с реальными модулями или группами
            # module1.foo1()
            # module1.foo2()
            # module2.foo3()


            n = input('refresh? y or n: ')
            print('\n*********************************')
            # Если что-то поменялось то обновляем модули
            if n == 'y':
                module1 = reload(module1)
                module2 = reload(module2)
                # Запоминаем последние изменения
                tmp_dct = dct_wrk.copy()
            else:
                del tmp_dct
                del dct_wrk

    except ValueError as err:
        print('some error', err)
    finally:
        print('end_app')
