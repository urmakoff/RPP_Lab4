import os
import csv


class Person:
    def __init__(self, full_name):
        self.full_name = full_name

    def __setattr__(self, key, value):
        if key == "full_name":
            if not isinstance(value, str) or value.strip() == "":
                raise ValueError("ФИО должно быть строкой")
        object.__setattr__(self, key, value)

    def __repr__(self):
        return f"{self.full_name}"


class Worker(Person):
    def __init__(self, worker_id, full_name, position, experience):
        super().__init__(full_name)
        self.worker_id = worker_id
        self.position = position
        self.experience = experience

    def __setattr__(self, key, value):
        if key == "worker_id":
            if not isinstance(value, int) or value <= 0:
                raise ValueError("Номер должен быть положительным числом")
        elif key == "position":
            if not isinstance(value, str) or value.strip() == "":
                raise ValueError("Должность должна быть строкой")
        elif key == "experience":
            if not isinstance(value, int) or value < 0:
                raise ValueError("Стаж не может быть отрицательным")
        object.__setattr__(self, key, value)

    def __repr__(self):
        return f"№ {self.worker_id}: {self.full_name}, {self.position}, стаж {self.experience}"

    @staticmethod
    def from_csv_row(row):
        return Worker(int(row[0]), row[1], row[2], int(row[3]))

    @staticmethod
    def csv_header():
        return ["№", "ФИО", "должность", "трудовой стаж"]

    def to_csv_row(self):
        return [self.worker_id, self.full_name, self.position, self.experience]


class WorkerCollection:
    def __init__(self):
        self.workers = []
        self.index = 0

    def add_worker(self, worker):
        self.workers.append(worker)

    def __getitem__(self, index):
        return self.workers[index]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.workers):
            worker = self.workers[self.index]
            self.index += 1
            return worker
        raise StopIteration

    def __repr__(self):
        text = ""
        for worker in self.workers:
            text += repr(worker) + "\n"
        return text

    @staticmethod
    def count_files():
        count = 0
        for item in os.listdir():
            if os.path.isfile(item):
                count += 1
        return count

    def sort_by_position(self):
        return sorted(self.workers, key=lambda worker: worker.position)

    def sort_by_experience(self):
        return sorted(self.workers, key=lambda worker: worker.experience)

    def workers_with_experience_more_than(self, min_experience):
        for worker in self.workers:
            if worker.experience > min_experience:
                yield worker

    def positions_generator(self):
        for worker in self.workers:
            yield worker.position

    def get_next_id(self):
        if len(self.workers) == 0:
            return 1
        max_id = self.workers[0].worker_id
        for worker in self.workers:
            if worker.worker_id > max_id:
                max_id = worker.worker_id
        return max_id + 1

    def load_from_file(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                worker = Worker.from_csv_row(row)
                self.add_worker(worker)

    def save_to_file(self, filename):
        with open(filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(Worker.csv_header())
            for worker in self.workers:
                writer.writerow(worker.to_csv_row())


workers = WorkerCollection()
workers.load_from_file("data.csv")

while True:
    print("\nМЕНЮ")
    print("1 - Показать количество файлов в папке")
    print("2 - Показать всех работников")
    print("3 - Сортировка по должности")
    print("4 - Сортировка по стажу")
    print("5 - Показать работников со стажем больше заданного")
    print("6 - Добавить нового работника")
    print("7 - Сохранить данные в файл")
    print("8 - Показать работника по индексу")
    print("9 - Показать все должности")
    print("0 - Выход")

    choice = input("Выберите пункт меню: ")

    if choice == "1":
        print("Количество файлов в папке:", WorkerCollection.count_files())

    elif choice == "2":
        print("\nСписок работников:")
        for worker in workers:
            print(worker)

    elif choice == "3":
        print("\nСортировка по должности:")
        for worker in workers.sort_by_position():
            print(worker)

    elif choice == "4":
        print("\nСортировка по стажу:")
        for worker in workers.sort_by_experience():
            print(worker)

    elif choice == "5":
        min_experience = int(input("Введите минимальный стаж: "))
        print("\nПодходящие работники:")
        for worker in workers.workers_with_experience_more_than(min_experience):
            print(worker)

    elif choice == "6":
        new_id = workers.get_next_id()
        full_name = input("Введите ФИО: ")
        position = input("Введите должность: ")
        experience = int(input("Введите стаж: "))

        new_worker = Worker(new_id, full_name, position, experience)
        workers.add_worker(new_worker)

        print("Работник добавлен.")
        print("Его номер:", new_id)

    elif choice == "7":
        workers.save_to_file("data.csv")
        print("Данные сохранены в файл.")

    elif choice == "8":
        index = int(input("Введите индекс: "))
        print(workers[index])

    elif choice == "9":
        print("\nДолжности работников:")
        for position in workers.positions_generator():
            print(position)

    elif choice == "0":
        print("Программа завершена.")
        break

    else:
        print("Такого пункта меню нет.")