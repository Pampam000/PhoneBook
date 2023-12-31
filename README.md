# Привет! Это выполненное [тестовое задание](https://docs.google.com/document/d/1dIH7lY05hNLSluZgOYsRyTrvLmyz4CnNEtJFFXBbS-c/edit) для компании "Effective Mobile"!

## Для запуска программы нужен один из двух компонентов:
- docker
- python 3.10

## Способы запуска программы:
  * С помощью докер 
      - ```docker-compose up --build -d```
      - ```docker exec -ti phone_book python main.py```
        
  * Без докера
      - ```python main.py```

### Вся информация хранится в файле json-формата в таком виде:
``` {
ФИО_0 : {
   'organization': value,
   'work_phone': value,
   'personal_phone': value
    },
ФИО_1 : {...}
}
```

#### Программа не чувствительна к регистру

#### Функциональные кнопки:

    1. Вывести записи
    Выбрав эту опцию, вы получите n-записей из каталога, где n - значение 
    пагинации(page_size), указанное при запуске программы.
    Увидев n записей, вы можете посмотреть следующие, 
    для этого нужно нажать "1" ещё раз, иначе нажмите любую клавишу 
    и вы перейдёте в главное меню
    
    2. Добавить запись
    После выбора этой опции, вы должны будете по порядку ввести обязательные
    поля (ФИО, организация, рабочий телефон), поле "личный телефон" - 
    опционально. 
    Если ФИО уже существует, программа сообщит вам об этом.
    При попытке пропустить обязателньое поле - программа будет предлагать вам 
    ввести его до тех пор, пока оно не будет заполнено.
    
    3. Редактировать запись
    Выбирая эту опцию, сначала вам нужно ввести ФИО. Если такая запись 
    существует, вам нужно будет указать значения редактируемых полей. 
    Если запись не найдена, программа предложит вам вести ФИО повторно. 
    При изменении ФИО, программа проверит не занято ли это имя.
    Все поля при редактировании опциональны.
    
    4. Поиск записей
    Выполняет поиск по всем записям, исходя из введённых вами критериев. 
    Все поля опциональны. Если результатом поиска являются несколько записей,
    то они будут выведены на экран аналогчно п.1
    Поиск будет жёстким(==) для ФИО и мягким(in) для остальных полей
    Если не указать ни одного критерия поиска, то ни одна запись не найдётся
    
    0. Выход
    Заканчивает выполнение программы.
    При нажатии на "0" во время выполнения опций 2, 3, 4 - вы будете направлены
    в главное менюs
