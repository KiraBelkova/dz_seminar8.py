from csv import DictWriter, DictReader
from os.path import exists


file_name = "phone.csv"


class PhoneError(Exception):
    pass


def get_user_data():
    flag = False
    while not flag:
        try:
            first_name = input("Введите имя (не менее двух букв): ")
            if len(first_name) < 2:
                raise NameError("Невалидная длина имени")
            last_name = input("Введите фамилию: ")
            phone_number = int(input("Введите номер телефона (не менее 11 цифр): "))
            if len(str(phone_number)) < 11:
                raise PhoneError("Неверная длина номера")
            flag = True
        except ValueError:
            print("Вы вводите символы вместо цифр")
            continue
        except NameError as err:
            print(err)
            continue
        except PhoneError as err:
            print(err)
            continue
    return first_name, last_name, phone_number


def create_file(file_name):
    with open(file_name, "w", encoding="utf-8") as data:
        f_writer = DictWriter(data, fieldnames=["Имя", "Фамилия", "Телефон"])
        f_writer.writeheader()


def read_file(file_name):
    with open(file_name, encoding="utf-8") as data:
        f_reader = DictReader(data)
        return list(f_reader)


def write_file(file_name):
    user_data = get_user_data()
    res = read_file(file_name)
    for el in res:
        if el["Телефон"] == str(user_data[2]):
            print("Такой пользователь уже существует")
            return
    obj = {"Имя": user_data[0], "Фамилия": user_data[1], "Телефон": user_data[2]}
    res.append(obj)
    with open(file_name, "w", encoding="utf-8", newline="") as data:
        f_writer = DictWriter(data, fieldnames=["Имя", "Фамилия", "Телефон"])
        f_writer.writeheader()
        f_writer.writerows(res)


def copy_data(file_name, file_name_new, line_number):
    res = read_file(file_name)
    if line_number < 1 or line_number > len(res):
        print("Некорректный номер строки")
        return
    obj = res[line_number-1]
    with open(file_name_new, "w", encoding="utf-8", newline="") as data_new:
        f_writer = DictWriter(data_new, fieldnames=["Имя", "Фамилия", "Телефон"])
        f_writer.writeheader()
        f_writer.writerow(obj)
    print("Данные успешно скопированы")


def main():
    while True:
        command = input("Введите команду: ")
        if command == "q":
            break
        elif command == "w":
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name)
            print("Данные успешно записаны")
        elif command == "r":
            if not exists(file_name):
                print("Файл не создан. Создайте его: ")
                continue
            print(*read_file(file_name))
        elif command == "c":
            file_name_new = input("Введите имя нового файла: ")
            line_number = int(input("Введите номер строки, которую нужно скопировать: "))
            copy_data(file_name, file_name_new, line_number)


main()