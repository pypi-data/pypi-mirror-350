import argparse
from generators.leak_generator.leak_generator import LeaksGenerator
from generators.scripts.random_words.generate_random_words import NamesGenerator
from generators.scripts.yandex_disk.upload_yadisk import upload_file_to_yadisk


def get_args():
    main_parser = argparse.ArgumentParser(
        description="Генерация задачи на утечку памяти"
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
    init_parser.add_argument('-f', '--wrong_pointer_scenario', type=int, default=1,
                             help="Выбор функции с ошибкой: 1 - get_text; 2 - get_word (см. сгенерированный код, названия функций при генерации правильного ответа будут иными)")
    init_parser.add_argument("--output", "-o",
                             type=str, default="a.out",
                             help="Путь к выходному исполняемомоу файлу")
    check_parser.add_argument("--filepath", "-b",
                              type=str, default="a.out",
                              help="Путь к файлу с исходным кодом")
    check_parser.add_argument(
        "--answer", "-a", type=str, help='Ответ в формате строки "get_word;3;100"')


    return main_parser.parse_args()


def main():
    args = get_args()
    if args.mode == "init":
        generator_word = NamesGenerator(args.seed)
        noun1 = generator_word.generate_name(1)
        noun2 = generator_word.generate_name(2)
        generator = LeaksGenerator(3,[noun1,noun2])
        generator.create_task(args.output, args.wrong_pointer_scenario, args.seed)

        # Опциональная загрузка на Яндекс.Диск
        binfilename = args.output.split('/')[-1]
        if args.yadisk in ["yes", "Yes", "Y"]:
            upload_file_to_yadisk(args.output, binfilename, args.yadisk_token)

    elif args.mode == "check":
        generator = LeaksGenerator(3)
        generator.verify_task(str(args.answer))


if __name__ == "__main__":
    main()
