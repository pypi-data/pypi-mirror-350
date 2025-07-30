import argparse
from generators.profiling1.finding_slow_function import TaskFindingSlowFunctionGenerator
from generators.profiling1.finding_slow_function_in_function import TaskFindingSlowFuncInFuncGenerator
from generators.scripts.yandex_disk.upload_yadisk import upload_file_to_yadisk


def get_args():
    main_parser = argparse.ArgumentParser(
        description="""
        Генерация исходного кода программы для задачи на профилирование
        """)

    task_subparsers = main_parser.add_subparsers(dest='task', required=True)

    task1_parser = task_subparsers.add_parser('finding_in_main')
    task1_mode_subparsers = task1_parser.add_subparsers(dest='mode', required=True)
    task1_init_parser = task1_mode_subparsers.add_parser('init')
    task1_check_parser = task1_mode_subparsers.add_parser('check')

    task2_parser = task_subparsers.add_parser('finding_in_find_me')
    task2_mode_subparsers = task2_parser.add_subparsers(dest='mode', required=True)
    task2_init_parser = task2_mode_subparsers.add_parser('init')
    task2_check_parser = task2_mode_subparsers.add_parser('check')

    for check_parser in [task1_check_parser, task2_check_parser]:
        check_parser.add_argument("--filepath", "-b",
                                  type=str, default="a.out",
                                  help="имя бинарного файла")
        check_parser.add_argument("--answer", "-a",
                                  type=str,
                                  help="ответ")

    for init_parser in [task1_init_parser, task2_init_parser]:
        init_parser.add_argument("--delta_iterations", "-i",
                                 type=int, default=4000000,
                                 help='Минимальное различие количества итериций выполнения одного и того же блока в каждой функции (default=4000000)')
        init_parser.add_argument("--output", "-o",
                                 type=str, default="a.out",
                                 help="имя выходного файла")
        init_parser.add_argument('-yd', '--yadisk', default="Yes",
                                 help="Yes или No, в зависимости от того нужно ли загружать файл на Яндекс.Диск. По умолчанию установлено значение Yes")
        init_parser.add_argument('-yd_token', '--yadisk_token', default=None,
                                 help="OAuth-токен для доступа к Яндекс.Диску. Если не указан, используется токен по умолчанию в коде.")
    

    for parser in [task1_init_parser, task2_init_parser, task1_check_parser, task2_check_parser]:
        parser.add_argument("--seed", "-s",
                            type=str,
                            help="целое число, которое используется в качестве начального значения для генерации случайных чисел")
    for parser in [task1_init_parser, task1_check_parser]:
        parser.add_argument("--number_funcrions", "-f",
                            type=int, default=10,
                            help="число генерируемых функций")
    for parser in [task2_init_parser, task2_check_parser]:
        parser.add_argument("--range_nested_fcalls", "-n",
                            type=str, default='3,4',
                            help='диапазон числа вложенных вызовов функций - "<min>,<max>"')

    task2_init_parser.add_argument("--range_depth_fcalls", "-d",
                                   type=str, default='3,4',
                                   help='диапазон глубины вызовов функций - "<min>,<max>"')
    task2_init_parser.add_argument("--range_depth_f_find_me", "-D",
                                   type=str, default='1,2',
                                   help='диапазон глубины вызовов, на которой находится функция, в которой нужно найти медленную - "<min>,<max>"')

    return main_parser.parse_args()


def main():
    args = get_args()
    try:
        match args.task:
            case "finding_in_main":
                match args.mode:
                    case "init":
                        generator = TaskFindingSlowFunctionGenerator(
                            args.number_funcrions,
                            args.delta_iterations,
                        )
                        place_in_rating = generator.create_task(args.seed, args.output)
                        print(
                            f"Место функции, которую нужно найти, по времени выполнения, начиная с самой медленной - {place_in_rating}"
                        )

                        # Опциональная загрузка на Яндекс.Диск 
                        if args.yadisk in ["yes", "Yes", "Y"]:
                            file_name = args.output.split('\\')[-1]
                            upload_file_to_yadisk(args.output, file_name, args.yadisk_token)
                    
                    case "check":
                        generator = TaskFindingSlowFunctionGenerator(
                            args.number_funcrions,
                        )
                        check_result = generator.verify_task(args.filepath, args.answer, args.seed)
                        print(f"Результать проверки: {check_result}")

            case "finding_in_find_me":
                match args.mode:
                    case "init":
                        generator = TaskFindingSlowFuncInFuncGenerator(
                            tuple(map(int, args.range_nested_fcalls.split(","))),
                            tuple(map(int, args.range_depth_fcalls.split(","))),
                            tuple(map(int, args.range_depth_f_find_me.split(","))),
                            args.delta_iterations,
                        )
                        place_in_rating = generator.create_task(args.seed, args.output)
                        print(
                            f"Место функции, которую нужно найти в find_me, по времени выполнения, начиная с самой медленной - {place_in_rating}"
                        )

                        # Опциональная загрузка на Яндекс.Диск 
                        if args.yadisk in ["yes", "Yes", "Y"]:
                            file_name = args.output.split('\\')[-1]
                            upload_file_to_yadisk(args.output, file_name, args.yadisk_token)

                    case "check":
                        generator = TaskFindingSlowFuncInFuncGenerator(
                            tuple(map(int, args.range_nested_fcalls.split(","))),
                        )
                        check_result = generator.verify_task(args.filepath, args.answer, args.seed)
                        print(f"Результать проверки: {check_result}")


    except FileNotFoundError as e:
        print(e)
        exit(-1)

if __name__ == "__main__":
    main()