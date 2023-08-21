import json


class GoBack(Exception):
    pass


class IncorrectName(Exception):
    pass


class PhoneBook:
    _fio_fields_names = ('surname', 'name', 'patronymic_name')
    _not_fio_fields_names = ('organization', 'work_phone', 'personal_phone')
    _all_fields_names = _fio_fields_names + _not_fio_fields_names
    _edit_fields_names = ("фамилию", "имя", "отчество", "организацию",
                          "рабочий телефон", "личный телефон")

    def __init__(self, page_size: int, book_name: str = 'book.json'):
        self._book_name = book_name
        self._page_size = page_size
        self._load()

    def start(self):
        """
        Единственный публичный метод класса. Отображает меню действий и
        выполняет их.
        """
        # Создаем словарь с возможными действиями пользователя
        actions = {
            '1': self._display_entries,
            '2': self._add_entry,
            '3': self._edit_entry,
            '4': self._search
        }

        while True:
            # Выводим стартовое сообщение с возможными действиями
            self._print_start_message()

            # Получаем выбор пользователя

            choice = input("Выберите действие: ")


            # Действия, не выполнимые за один шаг, могут быть отменены в любой
            # момент
            if choice in ('2', '3', '4'):
                print('\n0 - Назад\n')

            # Если выбранное действие существует в словаре,
            # выполняем соответствующую функцию
            if choice in actions:
                action: callable = actions[choice]
                try:
                    action()
                except (GoBack, IncorrectName):
                    # GoBack - возникает при отмене действия
                    # IncorrectName - возникает при вводе неправильного ФИО
                    pass
            elif choice == '0':
                break
            else:
                print("\nНеверный ввод")

    def _load(self) -> dict:
        """
        Загружает информацию из файла
        :return: Словарь в формате:
            {
                ФИО_0 : {
                     'organization': value,
                     'work_phone': value,
                     'personal_phone': value
                     },
                ФИО_1 : {...}
            }
        """
        try:
            with open(self._book_name, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            # Исключение срабатывает только при первом запуске
            self._save(data={})

    def _save(self, data: dict):
        """
        Сохраняет словарь в файл
        """
        with open(self._book_name, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def _display_entries(self, entries: dict = None):
        """
        Отображает все существующие записи
        """
        if entries is None:
            entries = self._load()

        if not entries:
            print("\nЗаписи не найдены\n")
        else:
            print('\nНайдены записи:')

        shown_entries: int = 0

        for fullname, values in entries.items():
            self._display_entry(fullname, values)
            shown_entries += 1

            # Проверяем постраничную пагинацию и выбираем действие
            if shown_entries % self._page_size == 0 and shown_entries < \
                    len(entries):

                print(f'Показано записей: {shown_entries}/{len(entries)}\n\n'
                      'Следующая страница - 1\n'
                      'Выход на главную - Любая кнопка\n')

                nextt = input('Выберите действие: ')
                nextt = nextt.strip()
                if nextt != '1':
                    break

    @staticmethod
    def _display_entry(fullname: str, values: dict):
        """
        Отображает одну запись
        """
        fullname: list = fullname.split()
        print(f"Фамилия: {fullname[0]}\n"
              f"Имя: {fullname[1]}\n"
              f"Отчество: {fullname[2]}\n"
              f"Организация: {values['organization']}\n"
              f"Рабочий телефон: {values['work_phone']}\n"
              f"Личный телефон: {values['personal_phone']}\n"
              "------------\n")

    def _add_entry(self):
        """
        Добавляет новую запись
        """
        # Заполняем ФИО
        fullname, fullname_list = self._get_fullname(self._add_entry)

        # Загружаем информацию из файла
        book: dict = self._load()

        # Проверяем ФИО на уникальность
        if fullname in book:
            print('Такое фио уже занято')
            self._add_entry()
            return

        # Заполняем все поля кроме ФИО и личного телефона(т.к. он опциональный)
        values: list = [self._fill_field(x) for x in
                        self._edit_fields_names[3:-1]]

        # Заполняем личный телефон, если значение пустое, то ставим "-"
        values.append(self._fill_field('личный телефон',
                                       optional=True) or '-')

        # Формируем новую запись
        entry: dict = {fullname: {x: y for x, y in
                                  zip(self._not_fio_fields_names, values)}}
        # Добавляем запись в файл
        book |= entry
        self._save(book)

        # Отображаем новую запись на экран
        print(f"\nЗапись добавлена:")
        self._display_entry(fullname, entry[fullname])

    def _edit_entry(self):
        """
        Обновляет существующую запись
        """
        # Получаем ФИО
        fullname, fullname_list = self._get_fullname(self._edit_entry)

        # Загружаем информацию из файла
        book: dict = self._load()
        print(fullname, fullname_list)
        # Проверяем наличие записи
        if fullname not in book:
            print("\nЗапись не найдена\n")
            self._edit_entry()
            return

        # Формируем словарь с новыми данными
        new_data: dict = self._get_input_data()

        # Проверяем затронули ли обновления ФИО (уникальный ключ словаря)
        if new_fullname := self._check_fio_changes(
                new_data=new_data, fullname=fullname_list):

            # Проверяем не занято ли такое ФИО
            if new_fullname in book:
                print('\nТакое фио уже занято')
                return

            # Удаляем старую запись и добавляем вместо неё новую
            book[fullname] |= new_data
            book[new_fullname] = book.pop(fullname)
            fullname = new_fullname
        else:
            # Обновляем запись
            book[fullname] |= new_data

        # Сохраняем
        self._save(book)

        # Отображаем результат
        print("\nЗапись отредактирована: ")
        self._display_entry(fullname, book[fullname])

    def _search(self):
        # Загружаем информацию из файла
        book: dict = self._load()

        # Формируем данные для поиска из заполненных полей
        search_data: dict = self._get_input_data()
        result = dict()
        mask = list()

        # Проверяем есть ли среди данных, связанные с ФИО
        for field in self._fio_fields_names:
            if field in search_data:
                mask.append(search_data[field])
                search_data.pop(field)
            else:
                mask.append('')

        # Находим все записи, соответсвующие критериям поиска
        for fullname, values in book.items():
            fullname_list = fullname.split()
            if search_data and \
                    all(x == y for x, y in zip(fullname_list, mask) if y) and \
                    all(search_data[key] in values[key] for key in
                        search_data):
                result[fullname] = (book[fullname])

        # Отображаем полученный результат
        self._display_entries(result)

    def _get_input_data(self) -> dict:
        """
        :return: Введённые данные в виде словаря
        """
        # Заполняем поля (любое поле опционально)
        values: list = [self._fill_field(x, optional=True) for x in
                        self._edit_fields_names]
        data: dict = {x: y for x, y in
                      zip(self._all_fields_names, values) if y}
        return data

    @staticmethod
    def _fill_field(field_name: str, optional: bool = False) -> str:
        """
        Получает данные от пользователя
        :return: Введённая юзером строка
        """
        input_str: str = f"Введите {field_name} (опционально): " if optional \
            else f"Введите {field_name}: "

        entrance: str = input(input_str)
        if not optional:
            # Проверяем, чтобы поле было точно заполнено
            while not entrance:
                entrance: str = input(input_str)

        entrance: str = entrance.strip().title()

        if entrance == '0':
            raise GoBack

        return entrance

    def _check_fio_changes(self, new_data: dict, fullname: list) -> str:
        """
        Проверяет были ли изменения связанные с ФИО во время обновления

        :return: Новое значение ФИО, если оно изменилось
        """
        new_fullname = str()
        for num, field in enumerate(self._fio_fields_names):
            if field in new_data:
                fullname.insert(num, new_data[field])
                fullname.pop(num + 1)
                new_fullname: str = ' '.join(fullname)
                new_data.pop(field)
        if new_fullname:
            return new_fullname

    @staticmethod
    def _print_start_message():
        print("1 - Вывести записи\n"
              "2 - Добавить запись\n"
              "3 - Редактировать запись\n"
              "4 - Поиск записей\n"
              "0 - Выход\n")

    def _get_fullname(self, func: callable) -> tuple[str, list[str]]:
        """
        Проверяет введённое ФИО на валидность (3 слова)

        :return: ФИО в виде строки и ФИО в виде списка
        """
        fullname: str = self._fill_field('ФИО')
        fullname_list: list = fullname.split()

        if len(fullname_list) != 3:
            print("\nФИО должно состоять из 3 слов")

            func()
            raise IncorrectName
        return fullname, fullname_list
