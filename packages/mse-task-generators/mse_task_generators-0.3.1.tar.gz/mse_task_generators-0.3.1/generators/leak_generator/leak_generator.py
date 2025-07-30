import subprocess
import random
import re
import chardet

from generators.base_module import BaseTaskManager
from generators.scripts.random_words.generate_random_words import NamesGenerator


class LeaksGenerator(BaseTaskManager):
    """
    Класс предоставляет возможность генерировать код и проверять ответ студента.
    Код сгенерированный этим классом содержит ошибку,
    связанную с утечкой памяти. Код помещается в файл leaks_generated.
    """

    answers = {}

    def __init__(self, leak_scenarios,rand_seed_names=None):
        self.leak_scenario = leak_scenarios
        self.delete_free_scenarios = []
        self.pointless_condition_scenarios = []
        self.wrong_pointer_scenario = 0
        self.wrong_counter_scenarios = []
        self.pointer_offset = 0
        self.randomized_func_names = rand_seed_names if rand_seed_names is not None else ['academy','dynamic']



    def process_task3(self):
        """
        Функция обрабатывает задачy, в которой утечка должна происходить
        из-за потери доступа к выделенной области памяти в результате смещения указателя на некоторое число)
        генерирует место, в которое будет добавлена ошибка, ведущая к утечке,
        и значение, на которое будет смещаться указатель.
        Данные о сгенерированных значениях записывает в файл answers, необходимый для автопроверки ответа студента
        :return:
        """
        place_dict = {1:self.randomized_func_names[0],2:self.randomized_func_names[1],3:self.randomized_func_names[0]}
        print("Рандомно выбранные названия функций 'get_word' и 'get_text' соответственно: ",self.randomized_func_names)
        if self.wrong_pointer_scenario not in [1,2]:
            print("Ошибка не была включена в сгенерированный код (cм -h/--help")
        print("Место:", place_dict.get(self.wrong_pointer_scenario))
        self.pointer_offset = random.choice([1,2,3,4,5,6,7])
        print("Выбранное смещение:",self.pointer_offset)
        with open("answers", "w") as answer_file:
            answer_file.write(f"Место:{place_dict.get(self.wrong_pointer_scenario)}\n"
                       f"Смещение:{self.pointer_offset}")


    def libraries_and_signatures(self):
        """
        Функция возвращает строки кода на C, необходимые для включения библиотек,
        добавления директив препроцессора и сигнатур функций
        :return:
        """
        return """#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INIT_WORD_SIZE 16
#define INIT_TEXT_SIZE 8

char* get_word(FILE* file);
void free_text(char** text, int count); 
char** get_text(FILE* file, int* count);
void print_text(char** text, int count);
"""

    def get_word_function(self):
        """
        Функция возвращает строки кода на C, необходимые для прочтения и сохранения слов из файла text1.txt.
        Читается следующий символ из файла, он сохраняется в массив, так до момента пока не встретится
        конец файла, символ переноса строки или пробел. Далее возвращается полученный массив символов (слово).
        В данной функции происходит выбор некоторых строк, которые попадут, или не попадут в код на С,
        в зависимости от того, какие условия генерации выбирает пользователь генератора.
        :return:
        """
        code = """
char* get_word(FILE* file){
    int size = INIT_WORD_SIZE;
    char* word = (char*)malloc(size * sizeof(char));
    if (!word) {
        fprintf(stderr, "Memory allocation error for word\\n");
        exit(EXIT_FAILURE);
    }
    int index = 0;
    char c;
    while ((c = fgetc(file)) != EOF && c != ' ' && c != '\\n'){
        if (index >= size - 1){
            size *= 2;
            word = (char*)realloc(word, size * sizeof(char));
            if (!word) {
                fprintf(stderr, "Memory reallocation error for word\\n");
                exit(EXIT_FAILURE);
            }
        }
        word[index++] = c;
    }
    word[index] = '\\0';
    if (index==0 && c!=' '){"""
        # если юзер выбрал сценарий с неверным условием и рандом выбрал это место кода - добавим условие
        if 2 == self.leak_scenario and 4 in self.pointless_condition_scenarios:
            code += """
        if (word[index]!='\\0'){"""
        # если юзер не выбрал сценарий с отсутствием вызова free или рандом не выбрал это место кода - free добавляется
        if 1 != self.leak_scenario or 4 not in self.delete_free_scenarios:
            code += """
        free(word);"""
        # закрываем сегмент условного оператора, если он был открыт, иначе ничего не добавляем к коду
        code += """
        }""" if 2 == self.leak_scenario and 4 in self.pointless_condition_scenarios else ""
        code += """
        return NULL;
    }"""
        #если юзер выбрал сценарий с ошибкой указателя и рандом выбрал это место кода - добавим ошибочное выражение
        code+=f"""
    return word+{self.pointer_offset};""" if 3 == self.leak_scenario and 2 == self.wrong_pointer_scenario else """
    return word;"""
        code+="""
}
"""
        return code


    def get_text_function(self):
        """
        Функция возвращает строки кода на C, необходимые для прочтения и сохранения всего текста из файла text1.txt.
        Сохранение текста в массиве указателей на символ происходит путем многократного вызова функции get_word,
        указатель на первый символ каждого слова сохраняется как элемент массива text.
        В данной функции происходит выбор некоторых строк, которые попадут, или не попадут в код на С,
        в зависимости от того, какие условия генерации выбирает пользователь генератора.
        :return:
        """
        code = """
char** get_text(FILE* file, int* count){
    int size = INIT_TEXT_SIZE;
    char** text = (char**)malloc(size * sizeof(char*));
    if (!text){
        fprintf(stderr, "Memory allocation error for text\\n");
        exit(EXIT_FAILURE);
    }"""
        code+="""
    *count = 5;""" if 4 == self.leak_scenario and 3 in self.wrong_counter_scenarios else """
    *count = 0;"""
        code +="""
    char* word;
    while ((word = get_word(file)) != NULL){
        if (*count >= size) {
            size *= 2;
            text = (char**)realloc(text, size * sizeof(char*));
            if (!text){
                fprintf(stderr, "Memory reallocation error for text\\n");
                exit(EXIT_FAILURE);
            }
        }
        text[(*count)++] = word;"""

        if 4 == self.leak_scenario and 2 in self.wrong_counter_scenarios:
            code += """
        count--;"""
        code += """
    }"""
        code+="""
    return text;
}
"""
        return code


    def print_text_function(self):
        """
        Функция возвращает строки кода на C, необходимые для вывода массива указателей на символ.
        :return:
        """
        code = """
void print_text(char** text, int count){
    for (int i = 0; i < count; i++){
        printf("%s ", text[i]);
    }
    printf("\\n"); 
}
"""
        return code


    def free_text_function(self):
        """
        Функция возвращает строки кода на C, необходимые для корректного освобождения памяти,
        выделенного под массив указателей на символ.
        :return:
        """
        code = """
void free_text(char** text, int count){
    for (int i = 0; i < count; i++){"""
        #если юзер выбрал сценарий с неверным условием и рандом выбрал это место кода - добавим условие
        if 2 == self.leak_scenario and 1 in self.pointless_condition_scenarios:
            code += """
        if (i!=0){"""
        #если юзер не выбрал сценарий с отсутствием вызова free или рандом не выбрал это место кода - free добавляется
        if 1 != self.leak_scenario or 1 not in self.delete_free_scenarios:
            code += """
        free(text[i]);"""
        #закрываем сегмент условного оператора, если он был открыт, иначе ничего не добавляем к коду
        code += """
        }""" if 2 == self.leak_scenario and 1 in self.pointless_condition_scenarios else ""
        code += """
    }"""

        # если юзер выбрал сценарий с неверным условием и рандом выбрал это место кода - добавим условие
        if 2 == self.leak_scenario and 2 in self.pointless_condition_scenarios:
            code += """        
    if (!text){"""
        # если юзер не выбрал сценарий с отсутствием вызова free или рандом не выбрал это место кода - free добавляется
        if 1 != self.leak_scenario or 2 not in self.delete_free_scenarios:
            code += """
    free(text);"""
        # закрываем сегмент условного оператора, если он был открыт, иначе ничего не добавляем
        code += """
    }""" if 2 == self.leak_scenario and 2 in self.pointless_condition_scenarios else ""

        code += '\n}\n'
        return code


    def main_function(self):
        """
        Функция возвращает строки кода на C, представляющие собой главную функцию, в которой происходит вызов функций
        для считывания текста из файла.
        :return:
        """
        #первая строка мейна- перенаправление ошибок, чтобы не было видно тип ошибки при выводе результата по типу
        # free() - invalid pointer
        code = """
int main(){
    const char* text_to_read = "Динамическая память является ресурсом операционной системы и выделяется по явному запросу процесса.";
    freopen("/dev/null", "w", stderr);    
    FILE* file = fmemopen((void*)text_to_read, strlen(text_to_read), "r");
    if (!file) {
        fprintf(stderr, "Failed to create memory file");
        return EXIT_FAILURE;
    }
    int count;
    char** text = get_text(file, &count);"""
        #если юзер выбрал сценарий с ошибкой указателя и рандом выбрал это место кода - добавим ошибочное выражение
        if 3 == self.leak_scenario and 1 == self.wrong_pointer_scenario:
            code += f"""
    text+={self.pointer_offset};"""

        #если юзер выбрал сценарий с ошибкой счетчика и рандом выбрал это место кода - добавим ошибочное выражение
        if 4 == self.leak_scenario and 1 in self.wrong_counter_scenarios:
            code += """
    count++;"""

        code += """       
    print_text(text,count);
    fclose(file);"""
        # если юзер выбрал сценарий с неверным условием и рандом выбрал это место кода - добавим условие
        if 2 == self.leak_scenario and 3 in self.pointless_condition_scenarios:
            code += """
    if (!text){"""
        # если юзер не выбрал сценарий с отсутствием вызова free или рандом не выбрал это место кода - free добавляется
        if 1 != self.leak_scenario or 3 not in self.delete_free_scenarios:
            code += """
    free_text(text, count);"""
        # закрываем сегмент условного оператора, если он был открыт, иначе ничего не добавляем
        code += """
    }""" if 2 == self.leak_scenario and 3 in self.pointless_condition_scenarios else ""

        code += """
    return 0;\n}\n"""
        return code

    def generated_leaky_code(self):
        """
        Функция собирает все части кода на С и возвращает весь текст программы
        :return:
        """
        code = self.libraries_and_signatures()
        code += self.get_word_function()
        code += self.get_text_function()
        code += self.print_text_function()
        code += self.free_text_function()
        code += self.main_function()
        return code




    def create_task(self, output: str, wrong_pointer_scenario: int, seed):
        random.seed(seed)
        if 1 == self.leak_scenario:
            # выбор для того, где будет удалена строка free()
            self.delete_free_scenarios = random.sample([1, 2, 3, 4], int(input
                                                                         ('Сколько удалений функции free() добавить в код?: ')))
            print("Free delete scenarios:", self.delete_free_scenarios)
        if 2 == self.leak_scenario:
            # выбор того, где будет добавлено неверное условие
            self.pointless_condition_scenarios = random.sample([1, 2, 3, 4], int(input
                                                                         ('Сколько неверных условий добавить в код?: ')))
            print("pointless condition scenarios:", self.pointless_condition_scenarios)
        if 3 == self.leak_scenario:
            # выбор того, где будет добавлена ошибка указателя на область
            self.wrong_pointer_scenario = wrong_pointer_scenario
            self.process_task3()
        if 4 == self.leak_scenario:
            # выбор того, где будет добавлена ошибка счетчика
            self.wrong_counter_scenarios = random.sample([1,2,3],int(input
                                                                         ('Сколько ошибок счетчика добавить в код?: ')))
            print("Wrong counter scenarios:", self.wrong_counter_scenarios)

        generated_code = self.generated_leaky_code()
        substrs = output.split('.')
        if len(substrs) > 1:
            cfilepath = '.'.join(substrs[:len(substrs) - 1]) + '.c'
        else:
            cfilepath = output + '.c'
        with open(cfilepath, "w") as file:
            file.write(generated_code)
        print(f"\nСгенерированные файлы доступны по пути {output}, {cfilepath}")
        print("Чтобы увидеть ответы, проверьте содержимое файла answers")
        compile_command = ["gcc", "-g", cfilepath, "-o", output]
        subprocess.run(compile_command, capture_output=True, text=True)

        # Запуск valgrind и перенаправление вывода в файл
        valgrind_command = [
            "valgrind",
            "--leak-check=full",
            "--track-origins=yes",
            "-s",
            f"./{output}"
        ]

        with open("valgrind_leak_check.txt", "w") as valgrind_output_file:
            subprocess.run(valgrind_command, stdout=valgrind_output_file, stderr=subprocess.STDOUT)

        # Чтение файла с выводом valgrind и извлечение числа после "in use at exit:"
        total_leak_size = None

        with open("valgrind_leak_check.txt", "rb") as valgrind_file:
            raw_data = valgrind_file.read()
            encoding = chardet.detect(raw_data)["encoding"]  # {'encoding': 'utf-8', 'confidence': 0.99}
            try:
                valgrind_output = raw_data.decode(encoding, errors="ignore")
            except (UnicodeDecodeError, LookupError):  # если кодировка не найдена
                valgrind_output = raw_data.decode("utf-8", errors="ignore")
            match = re.search(r"in use at exit:\s*([\d,]+)\s*bytes", valgrind_output)
            if match:
                total_leak_size = int(match.group(1).replace(",", ""))

        #добавление ответа в файл answers
        with open("answers", "a") as answer_file:
                answer_file.write(f"\nУтекло:{total_leak_size}")

        # Вывод результата
        if total_leak_size is not None:
            print(f"Общий объем утечки памяти: {total_leak_size} байт")
        else:
            print("Не удалось найти информацию об утечке памяти.")

        # Удаление существующей директории generated, если она есть
        # if os.path.exists("generated"):
        #     shutil.rmtree("generated")

        # # Создание новой директории generated
        # os.makedirs("generated", exist_ok=True)

        # # Перемещение файлов в директорию generated
        # files_to_move = ["leaks_generated"]
        # for file_name in files_to_move:
        #     if os.path.exists(file_name):
        #         shutil.move(file_name, os.path.join("generated", file_name))
        #     else:
        #         print(f"Файл '{file_name}' не найден и не был перемещён.")





    @classmethod
    def process_task3_check(cls, file_path):
        """
        Чтение файла с правильными ответами и заполнение словаря answers.
        :param file_path: Путь к файлу с правильными ответами.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    # Убираем лишние пробелы и невидимые символы
                    key = key.strip()
                    value = value.strip()
                    cls.answers[key] = value

    @staticmethod
    def get_input(answer):
        """
        Получение ввода от пользователя в формате "get_word;3;100".
        :return: Ввод пользователя.
        """
        while True:
            user_input = answer
            # Проверяем, что ввод содержит ровно три значения, разделённые точкой с запятой
            if len(user_input.split(';')) == 3:
                return user_input
            else:
                print("Ошибка: Ввод должен быть в формате 'get_word;3;100'. Попробуйте ещё раз.")
                exit(1)

    @classmethod
    def check_third_answer(cls, user_input):
        """
        Проверка ответа пользователя на соответствие правильным ответам.
        :param user_input: Ввод пользователя.
        :return: True, если ответ верный, иначе False.
        """
        user_values = user_input.split(';')

        users_answer = {
            "Место": user_values[0].strip(),
            "Смещение": user_values[1].strip(),
            "Утекло": user_values[2].strip()
        }

        # Проверяем, есть ли все значения из users_answer в answers
        for key, value in users_answer.items():
            if key not in cls.answers or cls.answers[key] != value:
                print(f'ERROR: значение "{key}" неверно')
                return False  # Если хотя бы одно значение не совпадает, возвращаем False

        return True

    def verify_task(self, answer):
        self.process_task3_check('answers')
        user_input = self.get_input(answer)
        if self.check_third_answer(user_input):
            print("Верно!")
        else:
            print("Ответ неверен, попробуйте ещё.")
