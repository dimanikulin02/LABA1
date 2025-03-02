import math
from scipy.constants import R
from constant_9 import *


def multiply_elements(arr):
    product = 1
    for num in arr:
        product *= num
    return product


# 1) Рассчитать стоимость каждого ИР 1 категории (1.6 - 1.11)

# S_приобретенная
def calculate_buy_cost_of_kth_resource_at_year_t(purchase_year_IR_cost: int, first_year: int, tk: int, Tk_plan: int,
                                                 k: int):
    """
    Рассчитывает приведённую к t-му году эксплуатации стоимость приобретённого k-го ресурса.(1.6)

        :param purchase_year_IR_cost: Стоимость ИР в год его приобретения;
        :param tk: Текущий год эксплуатации, в смысле по счету (Например: 2-й);
        :param first_year: Первый год эксплуатации;
        :param Tk_plan: Кол-во лет в которых планирует эксплуатировать;

    :return:
        :buy_cost: Приведенная стоимость k-го ресурса к t-му году эксплуатации

    """
    # массив отраслевых индексов изменения цен по прошествии g-го года эксплуатации ИР
    current_year = first_year + tk - 1
    planned_year = first_year + Tk_plan - 1

    industry_price_index_g_year_arr = [price_change_indices[year] for year in range(first_year, current_year) if
                                       year in price_change_indices]
    buy_cost = (purchase_year_IR_cost * multiply_elements(industry_price_index_g_year_arr) * (
            1 - ((tk - 1) / Tk_plan)))
    buy_cost = round(buy_cost, 2)

    output = (
        "\n"
        f"Рассчет стоимости эксплуатации ПРИОБРЕТЕННОГО, {k}-го ресурса \n"
        "---------------------------------------------------------------\n"
        f"Cтоимость {k}-го ИР в год его приобретения: {purchase_year_IR_cost}\n"
        f"Текущий год эксплуатации {k}-го ИР: {current_year}\n"
        f"Массив лет и отраслевых индексов, в которые велась эксплуатация: {[year for year in range(first_year, current_year)]}, {industry_price_index_g_year_arr}\n"
        f"До какого года планируется эксплуатация ИР: {planned_year}\n"
        f"ПРИВЕДЕННАЯ стоимость {k}-го ИР: {buy_cost}\n"
        "\n"
    )

    return buy_cost, output
# S_базовая
def calculate_base_development_IR_cost(employee_labor_costs: dict[int: dict[str: float]], material_costs_total: float):
    """
    Рассчитывает базовую стоимость разработки k-го ИР на g-ом году разработки.(1.7)

        :param employee_labor_costs: {number_employee: {"wages_coast": float, "insurance_contributions": float }}
                                     wages_coast затраты на оплату труда number_employee-го сотрудника, по разработке k-го ИР
                                     insurance_contributions_rate - отчисления в фонды страхования (процент от затрат на оплату труда) в течение g-го года;
        :param material_costs_total: Общие затраты на расходные материалы при разработке k-го ИР в течение g-го года разработки;

    :return:
        :base_development_cost_k_g: Базовая стоимость разработки k-го ИР на g-ом году разработки.

    """

    total_employee_cost = 0
    for i in employee_labor_costs.items():
        total_employee_cost = total_employee_cost + (i[1]["Зарплата сотрудников"] + i[1]["Отчисления сотрудников"])

    base_development_cost_k_g = total_employee_cost + material_costs_total
    base_development_cost_k_g = round(base_development_cost_k_g, 2)

    return base_development_cost_k_g
# S_накопленная
def calculate_accumulated_IR_cost(accumulated_IR_cost_years: float, total_cost_g_year: float, year: int, k):
    """
    Расчет приведенной к t-му году разработки накопленной стоимости разрабатываемого k-го ИР.(1.8 - 1.9)

        :param accumulated_IR_cost_years: Накопительная стоимость разработки, за прошлые годы;
        :param total_cost_g_year: Базовая стоимость разработки за t год;
        :param year: Год, за который необходимо посчитать накопительную стоимость разработки;

    :return:
        :accumulated_IR_k_cost_new: Накопительная стоимость разработки к t году;

    """

    accumulated_IR_cost = (accumulated_IR_cost_years * price_change_indices[year]) + total_cost_g_year
    accumulated_IR_cost = round(accumulated_IR_cost, 2)

    return accumulated_IR_cost
# S_разработанная
def discounted_IR_cost_to_l_year(accumulated_IR_cost: int, tk: int,
                                 first_year: int, Tk_plan: int, k:int):
    """
    Рассчитывает приведённую к l-му году эксплуатации стоимость разработанного k-го ИР.(1.10)

        :param accumulated_IR_cost: Накопительная стоимость приведенной к t-му году разработки k-го ИР;
        :param tk: Текущий год эксплуатации;
        :param first_year: Первый год, в который началась вестись эксплуатация;
        :param Tk_plan: Планируемый срок эксплуатации ИР

    :return:
        :buy_cost: Приведенная стоимость разработанного k-го ресурса к l-му году эксплуатации

    """
    current_year = first_year + tk - 1
    planned_year = first_year + Tk_plan - 1
    # массив отраслевых индексов изменения цен по прошествии g-го года эксплуатации разработанных ИР
    industry_price_index_g_year_arr = [price_change_indices[year] for year in range(first_year, current_year) if
                                       year in price_change_indices]

    # массив отраслевых индексов изменения цен по прошествии g-го года эксплуатации разработанных ИР
    buy_cost = (accumulated_IR_cost * multiply_elements(industry_price_index_g_year_arr) * (
            1 - ((tk - 1) / Tk_plan)))
    buy_cost = round(buy_cost, 2)

    output = (
        "\n"
        f"Рассчет стоимости эксплуатации РАЗРАБОТАННОГО, {k}-го ресурса \n"
        "---------------------------------------------------------------\n"
        f"Cтоимость {k}-го ИР в год окончания его разработки: {accumulated_IR_cost}\n"
        f"Текущий год эксплуатации {k}-го ИР: {current_year}\n"
        f"Массив лет и отраслевых индексов, в которые велась эксплуатация: {[year for year in range(first_year, current_year)]}, {industry_price_index_g_year_arr}\n"
        f"До какого года планируется эксплуатация ИР: {planned_year}\n"
        f"ПРИВЕДЕННАЯ стоимость {k}-го ИР: {buy_cost}\n"
        "\n"
    )

    return buy_cost, output
# S_обслуживания
def calculate_current_IR_maintenance_cost(employee_labor_costs: dict[int: dict[str: float]],
                                          material_costs_total: float, k: int):
    """
    Рассчитывает стоимость обслуживания k-го ИР в текущем году.(1.11)

        :param k: Номер ресурса;
        :param employee_labor_costs: {number_employee: {"wages_coast": float, "insurance_contributions": float}}
                                     wages_coast затраты на оплату труда number_employee-го сотрудника, по обслуживанию k-го ИР
                                     insurance_contributions_rate - отчисления в фонды страхования в течение текущего года;
        :param material_costs_total: Общие затраты на расходные материалы при обслуживании k-го ИР в течение текущего года;

    :return:
        :total_cost_g_year: Общая стоимость обслуживания k-го ИР в текущем году.

    """
    total_employee_cost = 0

    for i in employee_labor_costs.items():
        total_employee_cost = total_employee_cost + (i[1]["Зарплата сотрудников"] + i[1]["Отчисления сотрудников"])

    total_cost_g_year = total_employee_cost + material_costs_total
    total_cost_g_year = round(total_cost_g_year, 2)
    output = (
        "\n"
        f"Расчет стоимости обслуживания ресурса №{k}\n"
        "------------------------------------\n"
        f"Стоимость обслуживания: {total_cost_g_year}\n"
        "\n"
    )
    return total_cost_g_year, output






















# 2) Рассчитать стоимость каждого ИР 2 категории (1.12 - 1.22)

# Среднее значение по рангам
def calculate_average_IR_cost(list_IR:list[int], rank:int):
    """
    Вычисляет среднее значение стоимости ИР по группам, взятых по рангам.(1.12)
        :param list_IR: Список ИР;
        :param rank: Ранг;

    :return:
        :output: Строка для записи логов в консоль;
        :average_value: Среднее значение;
    """

    average_value = sum(list_IR)/len(list_IR)

    output = (
        "\n"
        f"Расчет средней стоимости ИР в группе с рангом {rank}\n"
        "------------------------------------\n"
        f"Средняя стоимость: {average_value}\n"
        f"Массив значений ИР: {list_IR}\n"
        
        "\n"
    )
    return  average_value, output
#d_EK
def calculate_d_EK_couple_rank(E_R1:float, E_R2:float, R1:int, R2: int, number_couple:int):
    """
     Рассчитывает величину d_EK для пар стоимостей ИР E_R1 и E_R2, для всех R, где R_2 > R1.(1.13)

        :param E_R1: Средняя стоимость в группе с рангом R1;
        :param E_R2: Средняя стоимость в группе с рангом R2;
        :param R1:
        :param R2:
        :param number_couple: Номер пары;

    :return:
        :d_Ek:
        :output: Строка для записи логов в консоль;

    """

    d_EK = (E_R2/E_R1) ** (1/(R2-R1))
    d_EK = round(d_EK, 3)

    output = (
        "\n"
        f"Расчет d_EK для {number_couple}-й группы ИР {R1}-{R2}\n"
        "------------------------------------\n"
        f"d_EK: {d_EK}\n"
        "\n"
    )
    return d_EK, output
# Средняя геометрическая d_Ek
def geometric_mean_d_Ek(list_d_Ek:list[float]):
    """
    Считает среднюю геометрическую списка d_Ek. (1.14)
        :param list_d_Ek: Массив d_Ek;

    :return:
        :mean_d_Ek:
        :output: Строка для записи логов в консоль;;

    """

    product = 1
    for number in list_d_Ek:
        product *= number

    mean_d_Ek = product ** (1 / len(list_d_Ek))
    mean_d_Ek = round(mean_d_Ek,3)

    output = (
        "\n"
        f"Расчет средней геометрической списка d_Ek: {list_d_Ek}\n"
        "------------------------------------\n"
        f"Средняя геометрическая d_Ek: {mean_d_Ek}\n"
        "\n"
    )

    return mean_d_Ek, output
# Проверка условий рангового превосходства
def check_rank_domination(data_d_Ek:list[float]):
    """
    Функция занимается проверкой рангового превосходства для пар ИР, где элементы d_Ek < S_e. (1.15)
        :param data_d_Ek: Массив значений d_Ek;
    :return:
        :True or False;
    """
    for i in range(len(data_d_Ek)):
        if i+1 < len(data_d_Ek):
            if i >= i+1:
                return False
    return True
# Значение E_r если у точки R_rank, есть толчки слева и справа
def calculate_er_interpolation(E_R1, E_R2, mean_d_E, R_rank, R1, R2):
    """
    Ищет границы диапазона вероятных значений E_R

        :param E_R1: Известное ближайшее значение слева от точки;
        :param E_R2: Известное ближайшее значение справа от точки;
        :param mean_d_E: Средняя геометрическая роста стоимости одной ступени;
        :param R_rank: Ранг точки, для которой ищем границы;
        :param R1: Ранг точки слева;
        :param R2: Ранг точки справа;

    :return:
        :E_r: Интерполирования стоимость ИР;

    """

    a = E_R1 * (mean_d_E ** (R_rank-R1))
    b = E_R2 / (mean_d_E ** (R2-R_rank))
    E_r = (a + b) / 2
    E_r = round(E_r, 3)

    return E_r
# Значение E_r, если R_rank левее имеющихся точек
def calculate_er_extrapolation(R_rank:int, R_border:int, mean_d_E: float, Er_border:float ):
    """

    :param R_rank:
    :param R_border:
    :param mean_d_E:
    :param Er_border:

    :return:
    """

    if R_rank > R_border:
        x = R_rank - R_border
        E_r = Er_border * (mean_d_E ** x)
    else:
        y = R_border - R_rank
        E_r = Er_border / (mean_d_E ** y)
    output = ""

    E_r = round(E_r, 3)
    return E_r, output



