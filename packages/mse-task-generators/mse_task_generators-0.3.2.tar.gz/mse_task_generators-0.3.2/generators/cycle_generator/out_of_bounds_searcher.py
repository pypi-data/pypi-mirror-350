import re
import os

def find_potential_array_out_of_bounds(c_code):
    '''Функция ищет некорректные строки кода с ошибкой в массиве'''
    # Найти объявления массивов
    array_declarations = {}  # Словарь для хранения имен массивов и их размеров
    array_declarations_use = {}  # Словарь для хранения присвоений массивов
    # issues = {}  # Словарь для хранения найденных проблем
    lines_and_issues = {} # Словарь для хранения найденных проблем и номеров строк
    assignments = {}
    # Разбиваем код на строки
    lines = c_code.splitlines()

    num = 1
    # Проходим по каждой строке
    for line in lines:
        # Паттерн для поиска объявлений динамических массивов с использованием malloc
        array_alloc = re.match(r'\s*int\s*\*\s*(\w+)\s*=\s*\(int\*\)\s*malloc\((\d+)\s*\*\s*sizeof\(int\)\);', line)
        assignment_pattern = re.match(r'\s*(\w+)\[(.*?)\]\s*=\s*(.*?);', line)
        if array_alloc:
            array_name = array_alloc.group(1)
            array_size = int(array_alloc.group(2))
            array_declarations[array_name] = array_size
        if assignment_pattern:
            assignments[num] = line
            # Если найдено присвоение, сохраняем индекс
            index_expr = assignment_pattern.group(2).strip()
            array_declarations_use[num] = index_expr
        num += 1
    # Регулярное выражение для поиска условий цикла for
    pattern = r'for\s*\((.*?)\)\s*{'
    # Найти все совпадения
    matches = re.findall(pattern, c_code, re.DOTALL)
    
    for match in matches:
        # Извлечение переменной цикла
        loop_index = match.split('=')[0].strip()
        # Находит числа после знака '='
        assignment_number = re.search(r'=\s*([-+]?\d+)', match)
        # Находит числа после знаков сравнения
        comparison_number = re.search(r'([<>]=?)\s*([-+]?\d+)', match)
        # Определение границ цикла (начальное и конечное значения)
        if assignment_number and comparison_number:
            start_index = int(assignment_number.group(1))
            end_index = int(comparison_number.group(2))

        for line_number, index_arr in array_declarations_use.items():
            # Проверка индексов на выход за границы
            if loop_index in index_arr:
                if (start_index < 0 or start_index >= array_size) and (end_index < 0 or end_index >= array_size):
                    probl = f"начальный {start_index} и конечный {end_index} индексы за пределами массива {array_name}"
                elif start_index < 0 or start_index >= array_size:
                    probl = f"начальный индекс {start_index} за пределами массива {array_name}"
                elif end_index < 0 or end_index >= array_size:
                    probl = f"конечный индекс {end_index} за пределами массива {array_name}"
                # Добавляем в словарь номера строк в коде и соответствующую ошибку
                lines_and_issues[line_number] = probl

    
    return lines_and_issues


def find_potential_errors_array_out_of_bounds(filename):
    '''Функция считывает содержимое файла с кодом и запускает функцию поиска ошибки'''
    answer = []
    try:
        # Читаем содержимое файла
        with open(filename, "r") as f:
            c_code = f.read()

        # Ищем потенциальные проблемы
        issues_in_code = find_potential_array_out_of_bounds(c_code)

        if issues_in_code:
            # print("Обнаружены потенциальные проблемы:")
            for line, description in issues_in_code.items():
                # Выводим номер строки с ошибкой
                # print("Строка с ошибкой:", line)
                # Выводим описание каждой проблемы
                # print(f"Описание: {description}")
                answer.append(int(line))
        #else:
            #print("Потенциальных проблем с выходом за границы массива не обнаружено.")
            
    # Обработка ошибки, если файл не найден
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")
    
    return answer


if __name__ == "__main__":
    pathe = os.path.dirname(__file__) + "/generators_files"
    filename = os.path.join(pathe, "generated_code_with_cycle.c")
    ans  = find_potential_errors_array_out_of_bounds(filename)
    
