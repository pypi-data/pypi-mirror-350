import argparse
import subprocess
from generators.cycle_generator.cycle_generator_file import CCodeGenerator
from generators.scripts.yandex_disk.upload_yadisk import upload_file_to_yadisk


def get_args():
    main_parser = argparse.ArgumentParser(
        description="Генерация задачи: Поиск строк, в которых происходит выход за границы массива."
    )

    mode_subparsers = main_parser.add_subparsers(dest='mode', required=True)
    init_parser = mode_subparsers.add_parser('init')
    check_parser = mode_subparsers.add_parser('check')

    init_parser.add_argument(
        "--seed", "-s",
        type=str,
        help="целое число, которое используется в качестве начального значения для генерации случайных чисел"
    )
    init_parser.add_argument('-yd', '--yadisk', default="Yes",
                             help="Yes или No, в зависимости от того нужно ли загружать файл на Яндекс.Диск. По умолчанию установлено значение Yes")
    init_parser.add_argument('-yd_token', '--yadisk_token', default=None,
                             help="OAuth-токен для доступа к Яндекс.Диску. Если не указан, используется токен по умолчанию в коде.")
    init_parser.add_argument('-d', '--max_depth', type=int,
                             help="Количество циклов for")
    init_parser.add_argument('-n', '--max_num_of_array', type=int,
                             help="Максимальное количество строк, с присваиванием значений элементам массива на один цикл for.")
    init_parser.add_argument("--output", "-o",
                             type=str, default="a.out",
                             help="Путь к выходному исполняемомоу файлу")
    check_parser.add_argument("--filepath", "-b",
                              type=str, default="a.с",
                              help="Путь к файлу с исходным кодом")
    check_parser.add_argument("--answer", "-a", type=str, help="ответ")

    return main_parser.parse_args()


def main():
    args = get_args()
    if args.mode == "init":
        try:
            # Запрашиваем у пользователя ввод максимальной глубины вложенности циклов
            max_depth = args.max_depth
            if max_depth < 1 or max_depth > 10:  # Проверяем, что введенное значение положительное
                # Если значение меньше 1, выбрасываем исключение
                raise ValueError(
                    "Количество должно быть положительным целым числом, меньше 10.")
            # Запрашиваем у пользователя ввод максимальной глубины вложенности циклов
            max_num_of_array = args.max_num_of_array
            if max_num_of_array < 1 or max_num_of_array > 10:  # Проверяем, что введенное значение положительное
                # Если значение меньше 1, выбрасываем исключение
                raise ValueError(
                    "Количество должно быть положительным целым числом, меньше 10.")
        except ValueError as e:  # Обрабатываем исключения, возникающие при некорректном вводе
            print(f"Ошибка ввода: {e}")  # Выводим сообщение об ошибке
        else:  # Если исключений не возникло
            # Создаем экземпляр класса CCodeGenerator с заданной глубиной
            generator = CCodeGenerator(
                max_depth=max_depth, max_num_of_array=max_num_of_array, random_seed=args.seed)
            output = args.output
            substrs = output.split('.')
            if len(substrs) > 1:
                cfilepath = '.'.join(substrs[:len(substrs) - 1]) + '.c'
            else:
                cfilepath = output + '.c'
            # Вызываем метод для записи сгенерированного кода в файл
            generator.create_task(cfilepath)
            binfilename = output.split('/')[-1]
            # Сообщаем пользователю об успешном завершении операции
            print(f"Исполняемый файл успешно сгенерирован и записан в файл: {output}")
            compile_command = ["gcc", "-g", cfilepath, "-o", output]
            subprocess.run(compile_command, capture_output=True, text=True)
            # Опциональная загрузка на Яндекс.Диск
            if args.yadisk in ["yes", "Yes", "Y"]:
                upload_file_to_yadisk(output, binfilename, args.yadisk_token)

    elif args.mode == "check":
        filepath = args.filepath
        result = CCodeGenerator.verify_task(filepath, args.answer)
        print(result)


if __name__ == "__main__":
    main()
