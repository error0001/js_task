from importlib import reload
import json as js
import module1
import module2
import os


def _read_file(fl_names):
    """
    :param fl_names: список названий файлов
    :return: словарь с командами пользователей
    """
    try:
        print('Читаем пользовательские файлы...')
        dct_users = {}
        for fl_name in fl_names:
            cmds = []
            with open(fl_name, 'r') as data:
                commands = data.readlines()
                for line in commands:
                    cmds.append(line.split())
            # Удаляем лишние буквы для ключей, к-е будут в dict
            # file_userN.txt как userN
            # Добавляем ключи в словарь и сразу заполняем список данными
            tmp_name = fl_name[5:-4]
            # к ключам добавляем значения (а именно команды пользователей)
            dct_users.update({tmp_name: cmds})
            del cmds
    except IOError as ioerr:
        print('Проблема с пользовательскими файлами.', ioerr)
        del dct_users
        return dct_users
    finally:
        return dct_users


def _print_mono_str(rng,symb):
    """
    напечатает строку с одним символом в N кол-во раз
    на скорую руку написсал для рамки в консоли.
    :param rng:
    :param symb:
    """
    smlr = ''
    for i in range(rng):
        smlr += symb
    print(smlr)


def _update_json(cur_dct, tmp_dct, json_name):
    """
    :param cur_dct: рабочий словарь с данными из пользовательских файлов
    :param tmp_dct: копия рабочего словаря для поиска разницы
    :param json_name: имя файла типа json
    """
    #js_data = _read_json(json_name)
    js_data  = _stream_json(name_jsfile=json_name,
                            mode='r')
    # в случае если появились изменения в пользователских файлах
    # tmp_dct обновится в конце, если flag_update будет True
    flag_update = False
    # перебираем все ключи с пользовательскими командами
    for key in cur_dct.keys():
        #print('************************************')
        _print_mono_str(33,'*')
        print('Изменения ',key,':')
        # вытаскиваем порядковый номер пользователя
        # чтобы перебирать аргументы команд в json
        key_nmb = int(key[4:]) - 1

        if len(cur_dct[key]) != len(tmp_dct[key]):
            if len(cur_dct[key]) > len(tmp_dct[key]):
                print('- Появилась новая команда: ', cur_dct[key][-1])

                _refresh_json(nmb_prm=key_nmb,
                              wrk_dct=cur_dct,
                              key_dct=key,
                              js_data=js_data,
                              js_name=json_name)

                flag_update = True
            else:
                print('- Удалена последняя команда: ', tmp_dct[key][-1])
                print('- Текущая команда: ', cur_dct[key][-1])

                _refresh_json(nmb_prm=key_nmb,
                              wrk_dct=cur_dct,
                              key_dct=key,
                              js_data=js_data,
                              js_name=json_name)

                flag_update = True
        else:
            try:
                if cur_dct[key] != tmp_dct[key]:
                    print('- Изменение послед. команды: ')
                    print('- Было: ',tmp_dct[key][-1])
                    print('- Стало: ', cur_dct[key][-1])

                    _refresh_json(nmb_prm=key_nmb,
                                  wrk_dct=cur_dct,
                                  key_dct=key,
                                  js_data=js_data,
                                  js_name=json_name)

                    flag_update = True
                else:
                    print('нет.')
            except IndexError as ind_err:
                print('- Ошибка, все команды удалены', ind_err)
    if flag_update is True:
        tmp_dct.clear()
        tmp_dct = cur_dct.copy()

    print('json обновлен')


def _refresh_json(nmb_prm,
                  wrk_dct,
                  key_dct,
                  js_data,
                  js_name):
    """
    :param nmb_prm: порядковый номер параметра, который пропорционален
    номеру пользователя
    :param wrk_dct: рабочий словарь с командами пользователей
    :param key_dct: ключ с меткой номера пользователя, тип userN
    """
    js_data['commands'][nmb_prm]["module"] = wrk_dct[key_dct][-1][0]
    js_data['commands'][nmb_prm]["name"] = wrk_dct[key_dct][-1][1]
    js_data['commands'][nmb_prm]["function"] = wrk_dct[key_dct][-1][2]
    _stream_json(js_name, 'w', js_data)


def _stream_json(name_jsfile, mode, js_dct=js):
    """
    :param mode: 'w' - записать, 'r' - считать
    :param js_dct: json ~dict
    :return: если читаем возвращаем json объект
    """
    _print_mono_str(33, '*')
    if mode == 'r':
        print('Читаем json файл...')
        with open(name_jsfile, "r") as read_file:
            return js.load(read_file)
    elif mode == 'w':
        print('Записываем в json файл...')
        with open(name_jsfile, "w") as write_file:
            js.dump(js_dct, write_file)


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
        n = 'q'
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

            _print_mono_str(33,'*')
            n = input('refresh? y or n: ')
            if n == 'y':
                # Если что-то поменялось то обновляем модули
                module1 = reload(module1)
                module2 = reload(module2)
            else:
                del dct_wrk
    except ValueError as err:
        print('some error', err)
    finally:
        del tmp_dct
        print('Stop.')
