import json
import os

class GramDateBase:
    def __init__(self, GRAMBASE):
        if not GRAMBASE.endswith(".gram"):
            raise ValueError("Имя файла должно иметь расширение '.gram'")
        self.GRAMBASE = GRAMBASE
        self.data = {}
        self.is_open = False

    def create_table(self, **kwargs):
        if os.path.exists(self.GRAMBASE):
            raise FileExistsError(f"Ошибка: Таблица '{self.GRAMBASE}' уже существует. Используйте open_table для изменения.")
        self.data = kwargs
        self.save_data()
        return self

    def open_table(self):
        if self.is_open:
            raise RuntimeError("Ошибка: Таблица уже открыта.")
        try:
            with open(self.GRAMBASE, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError(f"Ошибка: Таблица '{self.GRAMBASE}' не найдена или повреждена.")
        self.is_open = True
        return self

    def closeSave_table(self):
        if self.is_open:
            self.save_data()
            self.is_open = False
        else:
            raise RuntimeError("Ошибка: Попытка закрыть таблицу, которая не была открыта.")
        return self

    def delete_table(self):
        if os.path.exists(self.GRAMBASE):
            os.remove(self.GRAMBASE)
        else:
            raise FileNotFoundError(f"Ошибка: Таблица '{self.GRAMBASE}' не существует.")
        return self

    def delete_key(self, key):
        if not self.is_open:
            raise RuntimeError("Ошибка: Сначала необходимо открыть таблицу с помощью open_table().")
        if key in self.data:
            del self.data[key]
        else:
            raise KeyError(f"Ошибка: Ключ '{key}' не найден.")
        return self

    def create_key(self, key, value):
        if not self.is_open:
            raise RuntimeError("Ошибка: Сначала необходимо открыть таблицу с помощью open_table().")
        self.data[key] = value
        return self

    def save_data(self):
        with open(self.GRAMBASE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def __enter__(self):
        self.open_table()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closeSave_table()

    def run(self, **kwargs):
        if not kwargs:
            return f"Запуск базы данных: {self.GRAMBASE}"
        else:
            for db_file, value in kwargs.items():
                if db_file.endswith(".gram") and value is True:
                    return f"Запуск базы данных: {db_file}"
                else:
                    raise ValueError("Неверный формат аргументов для run(). Используйте gram.run(имя_файла.gram=True)")

    def update(self, key, value):
        if not self.is_open:
            self.open_table()
        for user_id in self.data:
            if isinstance(self.data[user_id], dict):
                self.data[user_id][key] = value
        self.save_data()
        self.closeSave_table()
        return "Данные успешно обновлены."

    def help(self):
        help_text = """
Доступные команды и методы GramDateBase:

  create_table(**kwargs)       - Создать новую базу с переданными данными
  open_table()                 - Открыть существующую базу
  closeSave_table()            - Сохранить изменения и закрыть базу
  create_key(key, value)       - Добавить или обновить ключ в базе
  delete_key(key)              - Удалить ключ из базы
  delete_table()               - Удалить файл базы
  update(key, value)           - Пакетное обновление всех записей
  save_data()                  - Сохранить данные в файл
  help()                      - Показать это сообщение

Пример использования:
  gram = GramDateBase("test.gram")
  gram.create_table(user1={"name": "Иван"})
  gram.open_table()
  gram.create_key("city", "Moscow")
  gram.update("age", 30)
  gram.closeSave_table()
"""
        print(help_text)

