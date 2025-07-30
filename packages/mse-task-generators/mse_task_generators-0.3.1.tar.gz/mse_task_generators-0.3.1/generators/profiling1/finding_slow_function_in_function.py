from random import choice, seed, randint, shuffle
from cfile.core import Sequence, Function, Declaration, Type
from generators.profiling1.finding_slow_function import TaskFindingSlowFunctionGenerator
import subprocess

int_type = Type("int")


class TaskFindingSlowFuncInFuncGenerator(TaskFindingSlowFunctionGenerator):
    """Генератор программы с вызовами функций, в числе которых есть функция find_me,
    в которой одна из вызываемых функций выполняется дольше остальных"""

    def __init__(self,
                 # диапазон числа вложенных вызовов функций
                 range_nested_fcalls: tuple[int, int] = (3, 4),
                 # диапазон глубины вызовов функций
                 range_depth_fcalls: tuple[int, int] = (3, 4),
                 # диапазон глубины вызовов, на которой находится функция, в которой нужно найти медленную
                 range_depth_f_find_me: tuple[int, int] = (1, 2),
                 # диапазон числа итераций цикла for
                 delta_iterations: int = 4000000,
                 ):
        ranges = [
            range_nested_fcalls,
            range_depth_fcalls,
            range_depth_f_find_me
        ]
        for range in ranges:
            if range[0] > range[1]:
                raise ValueError("Неверный ввод диапазона")

        self.range_nested_fcalls = range_nested_fcalls
        self.range_depth_fcalls = range_depth_fcalls
        self.range_depth_f_find_me = range_depth_f_find_me
        self.delta_iterations = delta_iterations

    def _generate_place_in_rating(self):
        return randint(1, self.range_nested_fcalls[0])

    def create_task(self, random_seed, output: str) -> int:
        """Генерация программы
        Возвращает место функции, которую нужно найти среди вызванных из find_me, по времени выполнения, начиная с самой медленной"""

        seed(random_seed)
        place_in_rating = self._generate_place_in_rating()
        seq_num = 0  # последовательность чисел для имён функций
        max_num_functions = sum([
            self.range_nested_fcalls[1] ** depth
            for depth in range(1, self.range_depth_fcalls[1] + 1)
        ])
        function_names = self._generate_function_names(max_num_functions,random_seed)
        function_calls = {}  # словарь для графа вызовов
        numbers_elemental_iterations = {} # словарь для элементарных итераций в функциях

        depth_fcalls = randint(
            self.range_depth_fcalls[0], self.range_depth_fcalls[1])
        depth_f_find_me = randint(
            self.range_depth_f_find_me[0], self.range_depth_f_find_me[1])  # глубина find_me
        main_function = Function("main", int_type)

        functions_on_cur_depth = [main_function]
        for cur_depth in range(1, depth_fcalls + 1):  # построение графа вызовов
            functions_on_prev_depth = functions_on_cur_depth
            functions_on_cur_depth = []
            for f in functions_on_prev_depth:
                nested_fcalls = randint(
                    self.range_nested_fcalls[0], self.range_nested_fcalls[1])
                function_calls[f] = [
                    Function(function_names[seq_num + i], int_type) for i in range(nested_fcalls)
                ] # функции вызванные из f
                cur_numbers_elemental_iterations = [i for i in range(len(function_calls[f]))]
                shuffle(cur_numbers_elemental_iterations)
                numbers_elemental_iterations.update(
                    dict(zip(function_calls[f], cur_numbers_elemental_iterations))
                ) # добавление в словарь числа элементарных итераций для каждой функции
                seq_num += len(function_calls[f])
                functions_on_cur_depth += function_calls[f]
            if cur_depth == depth_f_find_me:  # найдена глубина find_me
                # выбор функции find_me
                f_find_me = choice(functions_on_cur_depth)
                f_find_me.name = 'find_me'

        for f in functions_on_cur_depth:  # функции, не вызывающие функции
            function_calls[f] = []

        code = Sequence()
        called_functions_in_main = function_calls.pop(main_function)
        # блок кода, выполняемый в каждой функции определённое число раз
        elemental_block = self._generate_elemental_block()
        for function, calls in reversed(function_calls.items()):
            code.append(Declaration(function))
            function_body = self._create_function_body(
                elemental_block,
                numbers_elemental_iterations[function],
                calls
            ) # генерация тела функции с выполнением одного и того же блока кода определённое число раз
            code.append(function_body)

        code.extend(self._create_main(called_functions_in_main))
        self._write_and_compile(code, output)
        return  place_in_rating

    def verify_task(self, filename: str,
                    answer: str,
                    random_seed
        ) -> bool:
        '''Проверка ответа на задание'''
        seed(random_seed)
        place_in_rating = self._generate_place_in_rating()

        try:
            subprocess.run([f"./{filename}"])
        except FileNotFoundError:
            raise FileNotFoundError(f'Файл {filename} не найден')
        except OSError:
            raise OSError(f'Ошибка запуска {filename}')
        try:
            prof_process = subprocess.run(['gprof', '-b', filename, 'gmon.out', '--graph=find_me'],
                                          capture_output=True,
                                          text=True)
        except Exception:
            raise OSError('Ошибка запуска утилиты gprof')
        table = prof_process.stdout.split('\n' + '-' * 47 + '\n')[:-1]
        if not table:
            raise OSError(
                'Ошибка получения данных о профилировании с помощью gprof.')
        # разделение строк таблицы по переносам строки
        table = [row.split('\n') for row in table]
        table[0] = table[0][6:]  # удаление заголовка и шапки таблицы
        row_with_called_functions = None
        for row in table:  # поиск строки таблицы с вызванными функциями из find_me
            # в строке таблицы приведены функции вызванные из find_me
            if 'find_me' in row[1]:
                row_with_called_functions = row
                break

        # разделение по столбцам таблицы
        row_with_called_functions = [line.split()
                                     for line in row_with_called_functions]
        # функции вызванные из find_me
        called_functions = row_with_called_functions[2:]
        # сортировка времени
        if not 1 <= place_in_rating <= len(called_functions):
            raise ValueError(f'Не существует функции с местом по времени выполнения {place_in_rating}')
        called_functions = sorted(
            called_functions, key=lambda function: float(function[0]), reverse=True)
        # имя функции выполняющейся дольше остальных
        expected_answer = called_functions[place_in_rating - 1][3]
        return expected_answer == answer
