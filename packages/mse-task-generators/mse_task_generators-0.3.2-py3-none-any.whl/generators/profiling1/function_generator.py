import cfile
from random import randint, choice
from cfile.core import Variable, Statement, Declaration, Block, Type, Assignment, FunctionCall
from generators.profiling1.variables import StaticArray, Counter
from generators.profiling1.random_expressions import get_expression

int_type = Type("int")


class FunctionGenerator:
    def __init__(self,
                 min_n_iterations_for=40,  # минимальное число итераций в цикле
                 max_n_iterations_for=50,  # максимальное число итераций в цикле
                 min_n_new_vars_in_block=5,
                 max_n_new_vars_in_block=5,
                 min_length_math_expression=4,
                 max_length_math_expression=4,
                 min_assignments_in_block=5,
                 max_assignments_in_block=5,
                 min_arr_size=10,
                 max_arr_size=20,
                 min_int_value=1,
                 max_int_value=1000,
                 minuses_threshold=0.5,
                 brackets_threshold=0,
                 ):

        self.min_n_new_vars_in_block = min_n_new_vars_in_block
        self.max_n_new_vars_in_block = max_n_new_vars_in_block
        self.minuses_threshold = minuses_threshold
        self.brackets_threshold = brackets_threshold
        self.min_length_math_expression = min_length_math_expression
        self.max_length_math_expression = max_length_math_expression
        self.min_assignments_in_block = min_assignments_in_block
        self.max_assignments_in_block = max_assignments_in_block
        self.min_arr_size = min_arr_size
        self.max_arr_size = max_arr_size
        self.min_int_value = min_int_value
        self.max_int_value = max_int_value
        self.min_n_iterations_for = min_n_iterations_for
        self.max_n_iterations_for = max_n_iterations_for

        self.arithmetic_operators = ["+", "-", "*"]
        self.cmp_operations = [">", "<", ">=", "<=", "==", "!="]
        self.writer = cfile.Writer(cfile.StyleOptions())

    def generate_int_vars_from_any_vars(self,
                                        vars: list[Variable]
                                        ) -> list[Variable]:
        """Генерация переменных типа int из переременных int и int*"""
        int_type_vars = []
        for var in vars:
            if isinstance(var, StaticArray):
                int_type_vars.append(var[randint(0, var.array - 1)])
            elif not isinstance(var, Counter):
                int_type_vars.append(var)
        return int_type_vars

    def generate_math_expression(self, vars: list[Variable]) -> str:
        """Генерация мат. выражения из переменных"""
        int_type_vars = self.generate_int_vars_from_any_vars(vars)
        var_names = [int_type_var.name for int_type_var in int_type_vars]
        return get_expression(var_names,
                              self.arithmetic_operators,
                              randint(self.min_length_math_expression, self.max_length_math_expression),
                              randint(1, 100000),
                              minuses_threshold=self.minuses_threshold,
                              brackets_treshold=self.brackets_threshold
                              )

    def generate_operator_if(self, vars: list[Variable]) -> FunctionCall:
        operator = choice(self.cmp_operations)
        condition = self.generate_math_expression(vars) + \
            f" {operator} " + self.generate_math_expression(vars)
        return FunctionCall("if", [condition])

    def generate_operator_for(self,
                              existing_vars: list[Variable],
                              ) -> FunctionCall:
        """Генерация оператора for"""
        seq_number = len(existing_vars)
        counter = Counter(f"i{seq_number + 1}", int_type)
        counter_declaration = self.writer.write_str_elem(
            Declaration(counter, 0))
        n_iterations = randint(self.min_n_iterations_for,
                               self.max_n_iterations_for, )
        stop_condition = f"{counter.name} < {n_iterations}"
        step = f"{counter.name}++"
        return FunctionCall("for", [f"{counter_declaration}; {stop_condition}; {step}"])

    def generate_assignment(self, vars: list[Variable]) -> Assignment:
        """Генерация заданий переменных значениями мат. выражений из сущ. переменных"""
        var = choice(vars)
        if isinstance(var, StaticArray):
            element = var[randint(0, var.array - 1)]
            return Assignment(element, self.generate_math_expression(vars))
        elif not isinstance(var, Counter):
            return Assignment(var, self.generate_math_expression(vars))

    def generate_vars(self, vars_num, existing_vars: list[Variable] = []) -> list[Variable]:
        """Генерация новых переменных"""

        seq_number = len(existing_vars)

        vars = [None for _ in range(vars_num)]
        for i in range(vars_num):
            var_type = choice([Variable, StaticArray])
            if var_type is StaticArray:
                var = StaticArray(f"x{seq_number + i}",
                                  int_type, randint(self.min_arr_size, self.max_arr_size))
            else:
                var = Variable(f"x{seq_number + i}", int_type)
            vars[i] = var

        return vars

    def generate_var_declaration(self, var) -> Declaration:
        """Генерация объявления переменной"""
        if isinstance(var, StaticArray):
            return Declaration(var,
                               [
                                   randint(self.min_int_value,
                                           self.max_int_value)
                                   for _ in range(var.array)
                               ])
        else:
            return Declaration(var,
                               randint(self.min_int_value, self.max_int_value))

    def generate_block(self,
                       min_nesting_depth_for,  # минимальная глубина вложенности циклов
                       max_nesting_depth_for,  # максимальная глубина вложенности циклов
                       min_n_nested_for,  # минимальное число вложенных циклов
                       max_n_nested_for,  # максимальное число вложенных циклов
                       existing_vars: list[Variable] = [],
                       ) -> Block:
        """
        Возвращает блок кода с объявлением, заданием переменных и
         определённым числом циклов с определённой вложенностью, в которых
         генерируются такие же блоки.
        """
        block = Block()

        # объявление и задание новых переменных
        number_new_vars = randint(
            self.min_n_new_vars_in_block, self.max_n_new_vars_in_block
        )
        new_vars = self.generate_vars(number_new_vars, existing_vars)
        for var in new_vars:
            block.append(Statement(self.generate_var_declaration(var)))
        vars = existing_vars + new_vars

        # задание переменных значениями мат. выражений из сущ. переменных
        number_assignments = randint(self.min_assignments_in_block,
                                     self.max_assignments_in_block)
        for i in range(number_assignments):
            block.append(
                Statement(self.generate_assignment(vars)))

        # создание циклов с такими же блоками
        n_for_in_block = randint(min_n_nested_for, max_n_nested_for)
        if max_nesting_depth_for:
            for i in range(n_for_in_block):
                cur_max_nesting_depth_for = randint(min_nesting_depth_for,
                                                    max_nesting_depth_for)
                if cur_max_nesting_depth_for == 0:
                    continue

                block.append(self.generate_operator_for(vars))

                if min_nesting_depth_for == 0:
                    next_min_n_nested_for = 0
                else:
                    next_min_n_nested_for = min_nesting_depth_for - 1
                next_max_n_nested_for = cur_max_nesting_depth_for - 1
                block.append(self.generate_block(
                    next_min_n_nested_for,
                    next_max_n_nested_for,
                    min_n_nested_for,
                    max_n_nested_for,
                    vars,)
                )

        return block

    def generate_function_body(self,
                               min_n_nested_for,  # минимальное число вложенных циклов
                               max_n_nested_for,  # максимальное число вложенных циклов
                               min_n_parallel_for,  # минимальное число параллельных циклов в блоке
                               max_n_parallel_for,  # максимальное параллельных циклов в блоке
                               ) -> Block:
        """
        Возвращает тело функции с объявлением, заданием переменных и
         определённым числом циклов с определённой вложенностью, в которых
         генерируются такие же блоки.
        """
        body = self.generate_block(min_n_nested_for,
                                   max_n_nested_for,
                                   min_n_parallel_for,
                                   max_n_parallel_for
                                   )
        #body.append(Statement(FunctionReturn(0)))
        return body