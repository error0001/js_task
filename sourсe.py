import json as js

if __name__ == '__main__':
    try:
        print('start_app')
        # 1. Input cmd in files 1,2,3
        # 2. Analyse:
        # - new cmd,
        # - del cmd,
        # - chg cmd
        # 3. Refresh file.json with some changes

    except ValueError as err:
        print('some error', err)
    finally:
        print('end_app')
