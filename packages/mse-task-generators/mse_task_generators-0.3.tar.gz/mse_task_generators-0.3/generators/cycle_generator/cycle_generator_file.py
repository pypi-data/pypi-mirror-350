import random
from generators.base_module import BaseTaskManager
from generators.cycle_generator.out_of_bounds_searcher import find_potential_errors_array_out_of_bounds
from generators.scripts.random_words.generate_random_words import NamesGenerator


class CCodeGenerator(BaseTaskManager):
    def __init__(self, max_depth=1, max_num_of_array=1, random_seed=None):
        self.max_depth = max_depth # Количество циклов в коде
        self.max_num_of_array = max_num_of_array # Максимальное количество строк, с присваиванием значений элементам массива на один цикл
        self.rand_seed = random_seed if random_seed is not None else 42  # Устанавливаем seed (42 по умолчанию)
        random.seed(self.rand_seed)  # Устанавливаем random
        # Исходный код на C
        ''' c_code_part1:
            Первая часть исходного кода задачи, 
            Parameters:
            number (int): число - первый множитель
        '''
        self.c_code_part1 = r"""
#include <stdio.h>
#include <stdlib.h>

int main() 
{
    int number = 3;
"""
        ''' c_code_part3:
            Третья часть исходного кода задачи, 
            В данной части возвращается 0
        '''
        self.c_code_part3 = r"""
    return 0;
}
"""

    def generate_random_number(self):
        '''Функция генерирует и возвращает случайное число от -100 до 100'''
        return random.randint(-100, 100)
    
    def generate_random_positive_number(self):
        '''Функция генерирует и возвращает случайное число от 0 до 100'''
        return random.randint(0, 100)
    
    def generate_random_negative_number(self):
        '''Функция генерирует и возвращает случайное число от -100 до -1'''
        return random.randint(-100, -1)

    def random_comparison_operator_less(self):
        '''Функция случайно выбирает и возвращает оператор сравнения'''
        return random.choice(['<=', '<'])

    def random_comparison_operator_more(self):
        '''Функция случайно выбирает и возвращает оператор сравнения'''
        return random.choice(['>=', '>'])

    def generate_incorrect_cycle(self, current_depth, index_name):
        '''Функция генерирует некорректную строку кода с ошибкой в цикле for'''
        # Получение индекса для текущего цикла
        index_in_cycle = f"{index_name}_{current_depth}"
        # for (index_in_cycle = number_one; index_in_cycle <= number_two ; index_in_cycle++) 
        # Генерация случайных чисел для  цикла
        if random.randint(1, 2) == 1: 
            number_one =  random.randint(0, 15)
            number_two = self.generate_random_number()
        else: 
            number_one = self.generate_random_negative_number()
            number_two = self.generate_random_positive_number() 
        # Если number_one и number_two в допустимом диапазоне, 
        # Изменяем одно из значений на некорректное
        if (number_one >= 0 or number_one < 10) or (number_two >= 0 or number_two < 10):
            # Генерируем случайное значение вне диапазона массива
            number_two = random.randint(10, 100) 
        # Формирование строки для инициализации индекса цикла
        final_index_i = f"{index_in_cycle} = {number_one}" 
        # Проверка, находится ли number_one вне допустимого диапазона
        # Если number_one в допустимом диапазоне, обрабатываем number_two
        increment = number_two >= (11 if number_one >= 0 and number_one < 10 else number_one)
        # Генерация условия выхода из цикла с оператором сравнения
        operator_func = self.random_comparison_operator_less if increment else self.random_comparison_operator_more
        operator_for_condition = operator_func()
        # Конечное условие выхода из цикла
        final_condition = f"{index_in_cycle} {operator_for_condition} {number_two}"
        # Конечное условие изменения счетчика
        final_counter_change = f"{index_in_cycle}{'++' if increment else '--'}"
        # Соединяем условия выхода из цикла и изменения счетчика в одну строку
        string_for = f"for ({final_index_i}; {final_condition}; {final_counter_change})"
        return string_for

    def generate_cycle_code_with_array(self, depth, array_name, index_name):
        '''Функция генерирует часть кода с циклом for и массивом в нем'''
        tabs = "    "  # Определение отступа 
        open_bracket = r"{"  # Открывающая фигурная скобка для блока кода
        close_bracket = r"}"  # Закрывающая фигурная скобка для блока кода
        close_brackets = ""  # Инициализация пустой строки для хранения закрывающей фигурной скобки для блока кода
        array_code = "" # Инициализация пустой строки для хранения присвоений
        index_in_for = f"{index_name}_{depth}" # Индекс для цикла
        change_index = "" # Переменная для изменения индекса

        # Генерация цикла
        nested_code = self.generate_incorrect_cycle(depth, index_name)  # Генерация кода для цикла
        loop_for = f"{tabs}{nested_code} {open_bracket}\n"  # Добавление кода цикла
        close_brackets += f"{tabs}{close_bracket}\n"  # Добавление закрывающей скобки
        array_count = random.randint(1, self.max_num_of_array) # Случайное количество строк, с присваиванием значений элементам массива в цикле
        
        # Цикл для генерации кода в зависимости от количества строк, с присваиванием значений элементам массива
        for current_depth in range(1, array_count + 1):
            number_rand = self.generate_random_number() # Случайное число для добавления к произведению
            # Добавление строк присвоений
            array_code += f"{tabs}{tabs}{array_name}[{index_in_for}{change_index}] = {index_in_for} * {number_rand} * number;\n"
            change_index = f" - {current_depth }" # "" " - 1" " - 2" " - 3"
        # Добавление сгенерированных частей к коду с циклом
        loop_for += array_code + close_brackets
        return loop_for

    def generate_incorrect_c_code(self):
        '''Функция генерирует некорректный код с ошибкой в цикле for'''
        indices = "    int "  # Инициализация строки для объявления переменных индексов
        final_part_init = "" # Инициализация пустой строки для хранения указателей и выделения памяти на массивы
        final_part_for = ""  # Инициализация пустой строки для хранения присвоений
        final_part_free = "" # Инициализация пустой строки для хранения освобождения памяти
        # Инициализация генератора с seed
        generator_word = NamesGenerator(self.rand_seed)
        noun = generator_word.generate_name(0)
        # Добавление строк указателей и выделения памяти на массивы
        final_part_init = f"    int* {noun} = (int*)malloc(10 * sizeof(int));\n"
        # Добавление строки очищения массива
        final_part_free = f"    free({noun});\n"
        # Генерация циклов
        for cycle in range(1, self.max_depth + 1):
            index_name = generator_word.generate_name(cycle)
            indices += f"{index_name}_{cycle}"  # Добавление индекса к строке объявлений переменных
            if cycle < self.max_depth:
                indices += ", "  # Добавление запятой для следующего индекса
            # Генериция частей для одного цикла
            part_for = self.generate_cycle_code_with_array(cycle, noun, index_name)
            # Добавление сгенерированных частей к коду
            final_part_for += part_for
        indices += ";\n"  # Добавление последнего индекса с точкой с запятой
        # Формирование полного кода C, объединяя все части
        c_code = self.c_code_part1 + indices + final_part_init + final_part_for + final_part_free + self.c_code_part3
        return c_code  # Возврат сгенерированного кода

    def create_task(self, file_path):
        '''Функция записывает код с ошибкой в файл'''
        # Генерируем некорректный код с ошибкой в цикле
        c_code = self.generate_incorrect_c_code()
        # Получаем директорию из пути к файлу
        # directory = os.path.dirname(file_path)
        # Создаём директорию, если она не существует
        # os.makedirs(directory, exist_ok=True)
        # Открываем и записываем полученный код в файл
        with open(file_path, 'w') as file:
            file.write(c_code)

    @staticmethod
    def read_students_answer(answer):
        ''' Функция считывает значения с консоли, разделенные пробелами, и добавляет их в массив.'''
        try:
            user_input = answer
            values_str = user_input.split()  # Разбиваем строку на список строк
            values = [int(val) for val in values_str]  # Преобразуем строки в числа
            return values
        except ValueError:
            print("Ошибка: В ответе введены некорректные значения. Введите числа, разделенные пробелами.")
            return []  # Возвращаем пустой список в случае ошибки

    @staticmethod
    def compare_arrays_unordered(array1, array2):
        ''' Функция сравнивает два массива и возвращает True, если они идентичны, иначе возвращает False.'''
        if set(array1) == set(array2):
            return True
        else:
            return False
        
    @classmethod
    def verify_task(cls, filepath, answer):
        ''' Функция сравнивает ответы студента и скрипта поиска ошибок, возвращает True или False.'''
        searcher_answer = find_potential_errors_array_out_of_bounds(filepath)
        students_answer = cls.read_students_answer(answer)
        flag_correct = cls.compare_arrays_unordered(searcher_answer, students_answer)
        return flag_correct



