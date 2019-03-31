from importlib import reload
import json as js
import module1
import module2


def _read_file(fl_names):
    try:
        print('Read users files...')
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
        print('Problems with files.', ioerr)
        del dct_users
        return dct_users
    finally:
        return dct_users


def _update_json(cur_dct, tmp_dct, name_wrk):
    # берем ключи, делаем дикт с ними
    # сравниваем количество элементах в списках
    # может быть сравниваем элементы
    #print('CUR_DCT\n',cur_dct)
    #print('TMP_DCT\n',tmp_dct)
    # проверяем сколько значений есть в каждом ключе
    #print(cur_dct.keys())
    #print(tmp_dct.keys())
    # считываем json файл
    js_data = _read_json(name_wrk)
    # 'по очереди перебираем ключи'
    # 'сравниваем количество команд каждого пользователя'
    flag_update = False
    for key in cur_dct.keys():
        print('************************************')
        print('Изменения ',key,':')
        # вытаскиваем порядковый номер пользователя

        # чтобы перебирать аргументы команд в json
        key_nmb = int(key[4:]) - 1

        if len(cur_dct[key]) != len(tmp_dct[key]):
            if len(cur_dct[key]) > len(tmp_dct[key]):
                print('появилась новая команда.', cur_dct[key][-1])
                flag_update = True
            else:
                print('удалена последняя команда.')
                print('команда:', tmp_dct[key][-1])
                print('тек. послед. ком', cur_dct[key][-1])
                flag_update = True
        else:
            try:
                if cur_dct[key] != tmp_dct[key]:
                    print('подмена команды.')
                    print('изначально:',tmp_dct[key][-1])
                    print('стало:', cur_dct[key][-1])

                    _write_json(name_wrk,
                                js_data,
                                cur_dct,
                                'replace')

                    flag_update = True
                else:
                    print('нет.')
            except IndexError as ind_err:
                print('все команды удалены',ind_err)
    if flag_update is True:
        tmp_dct.clear()
        tmp_dct = cur_dct.copy()

    print('json обновлен')

def _read_json(name_jsfile):
    print('*********************************','\nread json file')
    # его не обязательно читать
    with open(name_jsfile, "r") as read_file:
        return js.load(read_file)


def _write_json(name_jsfile,
                wrk_js_data,
                wrk_dct,
                status):
    print('*********************************','\nread json file')
    # replace data
    if status == 'replace':
        js_data['commands'][key_nmb]["module"] = wrk_dct[key][-1][0]
        js_data['commands'][key_nmb]["name"] = wrk_dct[key][-1][1]
        js_data['commands'][key_nmb]["function"] = wrk_dct[key][-1][2]

    with open(name_jsfile, "w") as write_file:
        json.dump(wrk_js_data, write_file)


def _check_instance(left, right):
    # проверяет объекты как словари
    """
    ...
    ряд условий с проверками словаря на валидность
    ...
    """
    if isinstance(left, dict) or isinstance(right, dict):
        return True
    return False


if __name__ == '__main__':
    try:
        n = 'None'
        # словарь хранящий копию логов о пользователе
        tmp_dct = {}
        print('Start.')
        while n != 'n':
            # 1. Получаем данные по пользователям из файлов.
            dct_wrk = _read_file(['file_user1.txt',
                                  'file_user2.txt',
                                  'file_user3.txt'])

            # Если копия словаря пуста, то делаем копию
            if not bool(tmp_dct):
                tmp_dct = dct_wrk.copy()

            # 2. Проверка на совместимость типов.
            if _check_instance(dct_wrk, tmp_dct):
                # 3. Работа с json файлом
                _update_json(dct_wrk, tmp_dct, 'file.json')
            else:
                print('Error with users files.')

            n = input('refresh? y or n: ')
            print('\n*********************************')
            # Если что-то поменялось то обновляем модули
            if n == 'y':
                module1 = reload(module1)
                module2 = reload(module2)
                # очищаем данные с временноо словаря
                # tmp_dct.clear()
            else:
                del tmp_dct
                del dct_wrk

    except ValueError as err:
        print('some error', err)
    finally:
        print('Stop.')
