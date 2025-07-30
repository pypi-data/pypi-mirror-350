from random import seed, shuffle, randint
from cfile.core import Sequence, Function, Declaration, Statement, Block, Type, FunctionCall, \
    FunctionReturn
from generators.profiling1.function_generator import FunctionGenerator
from cfile import StyleOptions
from cfile.writer import Writer
import subprocess
from generators.base_module import BaseTaskManager
from wonderwords import RandomWord

from generators.scripts.random_words.generate_random_words import NamesGenerator

int_type = Type("int")


class TaskFindingSlowFunctionGenerator(BaseTaskManager):
    """Генератор программы с вызовами функций, одна из которых выполняется
            дольше отстальных."""

    def __init__(self,
                 # число генерируемых функций
                 number_functions: int = 10,
                 # Минимальное число итераций выполнения элементарного вычислительного блока,
                 # на которое отличаются генерируемые функции
                 delta_iterations: int = 4000000,
                 ):
        if number_functions <= 0:
            raise ValueError("Неверно указано число функций")

        self.number_functions = number_functions
        self.delta_iterations = delta_iterations

    def _generate_function_names(self, number_functions,random_seed) -> list[str]:
        '''Генерация имён функций'''
        generator_word = NamesGenerator(random_seed)
        func_names = []
        for i in range(0,number_functions):
            func_names.append(generator_word.generate_name(i))
        return func_names

    def _generate_elemental_block(self) -> Block:
        '''Генерация элементарного вычислительного блока'''
        generator = FunctionGenerator(self.delta_iterations,
                                      self.delta_iterations)
        return generator.generate_block(1, 1, 1, 1)

    def _create_function_body(self,
                              elemental_block: Block,
                              n_iterations: int,
                              called_functions: list[Function] = []
                              ) -> Block:
        '''Создание тела функции с элементарным вычислительным блоком, выполненным n_iterations раз, и вызовами функций'''
        function_body = Block()
        function_body.append(
            FunctionCall("for", [f"int i = 0; i < {n_iterations}; i++"])
        )
        function_body.append(elemental_block)
        for called_function in called_functions:
            function_body.append(
                Statement(FunctionCall(called_function.name))
            )
        return function_body

    def _create_main(self, called_functions: list[Function] = []) -> Sequence:
        '''Создание тела функции main с вызовами функций'''
        code = Sequence()
        main_function = Function("main", "int")
        code.append(Declaration(main_function))
        function_body = Block()
        for function in called_functions:  # вызов всех функций в функции main
            function_body.append(Statement(FunctionCall(function.name)))
        function_body.append(Statement(FunctionReturn(0)))
        code.append(function_body)

        return code

    def _write_and_compile(self, code: Sequence, output: str):
        '''Создание файла с исходным кодом и его компиляция'''
        cfilename = self._get_cfilename(output)
        writer = Writer(StyleOptions())
        writer.write_file(code, cfilename)
        print(f'Файл с исходным кодом сгенерирован, он доступен по пути {cfilename}')
        subprocess.run(['gcc', '-pg', '-w', cfilename, '-o', output])
        print(f'Бинарик успешно сгенерирован, он доступен по пути {output}')

    def _generate_place_in_rating(self):
        return randint(1, self.number_functions)

    def create_task(self, random_seed, output: str) -> int:
        """Генерация исходного кода с заданием и его компиляция.
        Возвращает место функции, которую нужно найти, по времени выполнения, начиная с самой медленной"""

        seed(random_seed)
        place_in_rating = self._generate_place_in_rating()
        code = Sequence()

        function_names = self._generate_function_names(self.number_functions,random_seed)
        functions = [
            Function(name, int_type)
            for name in function_names
        ]
        numbers_elemental_iterations = [i for i in range(self.number_functions)]
        shuffle(numbers_elemental_iterations)

        # блок кода, выполняемый в каждой функции определённое число раз
        elemental_block = self._generate_elemental_block()

        for function, number_iterations in zip(
                functions, numbers_elemental_iterations
        ):
            code.append(Declaration(function))
            function_body = self._create_function_body(
                elemental_block, number_iterations
            )  # генерация тела функции с выполнением одного и того же блока кода number_iterations раз
            code.append(function_body)

        code.extend(self._create_main(functions))
        self._write_and_compile(code, output)
        return place_in_rating

    def _get_cfilename(self, output: str):
        substrs = output.split('.')
        if len(substrs) > 1:
            return '.'.join(substrs[:len(substrs) - 1]) + '.c'
        else:
            return output + '.c'

    def verify_task(self,
                    filename: str,
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
            prof_process = subprocess.run(['gprof', '-bp', filename, 'gmon.out'],
                                          capture_output=True,
                                          text=True)
        except Exception:
            raise OSError('Ошибка запуска утилиты gprof')
        lines = prof_process.stdout.split('\n')
        table = lines[5:len(lines) - 1]
        if not table:
            raise OSError(
                'Ошибка получения данных о профилировании с помощью gprof.')
        if not 1 <= place_in_rating <= len(table):
            raise ValueError(f'Не существует функции с местом по времени выполнения {place_in_rating}')
        first_row = table[place_in_rating - 1].split()
        expected_answer = first_row[-1]
        return expected_answer == answer
