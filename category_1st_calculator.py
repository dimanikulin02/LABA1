from typing import Union
from formula_script import *

class ResourceInfo1stCategory:
    def __init__(self, obs_ir, list_ir_info):
        self.generated_profit = None
        self.data_exel = []
        self.obs_ir = obs_ir
        self.ir_info = list_ir_info

        self.buy_cost = 0
        self.total_cost_g_year = 0
        self.development_cost = 0
        self.generated_profit = 0
        self.total_cost = 0

        # Словарь с ценами ИР, для 2-го этапа
        self.IR_cost = {}

        # Для второго этапа нам получается нужно получать self.total_cost по каждому ИР

        # Формирование шаблона data
        headers_years = [""] * 2 + list(price_change_indices.keys())
        headers_years.append(headers_years[-1] + 1)
        self.data_pattern = [
            headers_years,
            [""] * len(headers_years)
        ]

    def process_obs_ir(self):

        # Идем по общему словарю с ресурсами
        for number_IR, info_IR in self.obs_ir.items():
            # Обнуление переменных
            self.buy_cost = 0
            self.total_cost_g_year = 0
            self.development_cost = 0
            self.generated_profit = 0
            self.total_cost = 0

            property_IR = info_IR[0]
            first_year = info_IR[1]
            tk = info_IR[2]
            Tk_plan = info_IR[3] if info_IR[3] >= tk else tk

            # Проверяем, есть ли информация по ресурсу
            if f'ir_{number_IR}' in list(self.ir_info.keys()):

                if "приобретаемый" in property_IR:
                    self.calculateAcquisitionCost(number_IR, first_year, tk, Tk_plan)

                if "обслуживаемый" in property_IR:
                    self.calculateMaintenanceCost(number_IR)

                if "разрабатываемый" in property_IR:
                    self.calculateDevelopmentCost(number_IR, tk, Tk_plan, )

                if "приносящий прибыль" in property_IR:
                    self.calculateProfitGeneratingCost(number_IR)

                self.calculateTotalCost(number_IR)
                self.IR_cost.update({number_IR: self.total_cost})

    # Расчет приобретаемой части ресурса
    def calculateAcquisitionCost(self, number_IR: int, first_year: int, tk: int, Tk_plan: int):
        """
        Функция занимается расчетом приобретаемой части ресурса для k-го ресурса. Ищет информация для ее расчета и формирует строки для Exel.

            :param number_IR:
            :param first_year: Год начала эксплуатации ресурса;
            :param tk: Какой год эксплуатации идет сейчас;
            :param Tk_plan: Планируемое кол-во лет эксплуатации;

        :return:
        """
        IR_info = self.ir_info.get(f'ir_{number_IR}', None)

        if IR_info:
            IR_info = IR_info["Сведения по приобретению ресурса"]
            purchase_year_IR_cost = IR_info["Стоимость в год приобретения"]
            self.buy_cost, output_str = calculate_buy_cost_of_kth_resource_at_year_t(purchase_year_IR_cost, first_year,
                                                                                     tk, Tk_plan, number_IR)
            self.display_info(output_str)
            self.generate_data_exel("приобретаемый", [purchase_year_IR_cost, first_year, tk, Tk_plan, number_IR])
        else:
            output = (
                "\n"
                f"Рассчет стоимости эксплуатации ПРИОБРЕТЕННОГО, {number_IR}-го ресурса \n"
                "---------------------------------------------------------------\n"
                "ОШИБКА, нет информации по ресурсу "
            )
            self.display_info(output)

    # Расчет обсуживаемой части ресурса
    def calculateMaintenanceCost(self, number_IR: int):
        """
        Функция ищет и считает информацию для обслуживаемой части ресурса.
        :param number_IR:
        :return:
        """

        employee_labor_costs = {}
        IR_info = self.ir_info.get(f'ir_{number_IR}', None)

        if IR_info:
            IR_info = IR_info["Сведения по обслуживанию ресурса"]
            material_costs_total = float(IR_info["Затраты на расходные материалы"][0])

            for key, value in IR_info.items():
                if isinstance(value, dict):
                    for employee, amounts in value.items():
                        employee_id = int(employee)
                        if employee_id not in employee_labor_costs:
                            employee_labor_costs[employee_id] = {}
                        employee_labor_costs[employee_id][key] = float(amounts[0])

            self.total_cost_g_year, output = calculate_current_IR_maintenance_cost(employee_labor_costs,
                                                                                   material_costs_total, number_IR)
            self.display_info(output)
            self.generate_data_exel("обслуживаемый", [self.total_cost_g_year, number_IR])

        else:
            output = (
                "\n"
                f"Расчет стоимости обслуживания ресурса №{number_IR}\n"
                "------------------------------------\n"
                f"По ресурсу №{number_IR} НЕТ ИНФОРМАЦИИ\n"
                "\n"
            )
            self.display_info(output)

    # Расчет разрабатываемой части ресурса
    def calculateDevelopmentCost(self, number_IR: int, tk: int, Tk_plan: int):
        """
        По идее должна собирать данные, для расчета и маршрутизировать что ли расчеты +
        формировать правильные массивы, приведенные для Exel таблицы, а так-же записывать в глобальную переменную класса итоговую стоимость

        :return:
        """

        IR_info = self.ir_info.get(f'ir_{number_IR}', None)

        if IR_info:
            development_data_by_year = {}
            IR_info = IR_info["Сведения по разработке ресурса"]
            first_year_development = IR_info["Первый год разработки"]
            list_years_development = IR_info["Годы разработки"]
            staff_wages = IR_info["Зарплата сотрудников"]
            staff_contributions = IR_info["Отчисления сотрудников"]
            material_expenses = IR_info[
                "Затраты на расходные материалы"] if "Затраты на расходные материалы" in IR_info.keys() else []

            # Идем по годам разработки
            for index_year in range(len(list_years_development)):
                employee_labor_costs = {}

                # Считаем базовую стоимость
                for index_staff, wage in staff_wages.items():
                    if wage[index_year]:
                        employee_labor_costs[index_staff] = {"Зарплата сотрудников": wage[index_year]}
                for index_staff, contributions in staff_contributions.items():
                    if contributions[index_year]:
                        employee_labor_costs[index_staff].update({"Отчисления сотрудников": contributions[index_year]})

                material_costs_total = material_expenses[index_year] if material_expenses else 0.00
                base_development_cost_k_g = calculate_base_development_IR_cost(employee_labor_costs,
                                                                               material_costs_total)

                # Считаем Накопительную стоимость
                if list_years_development[index_year] == first_year_development:
                    development_data_by_year[first_year_development] = {"Базовая стоимость": base_development_cost_k_g,
                                                                        "Накопительная стоимость": base_development_cost_k_g}
                else:
                    year = list_years_development[index_year - 1]
                    base_development_cost_k_g = base_development_cost_k_g
                    accumulated_IR_cost = calculate_accumulated_IR_cost(
                        development_data_by_year[year]["Накопительная стоимость"], base_development_cost_k_g, year,
                        number_IR)

                    development_data_by_year[year + 1] = {"Базовая стоимость": base_development_cost_k_g,
                                                          "Накопительная стоимость": accumulated_IR_cost}

            # Считаем стоимость эксплуатации РАРЗАРБОТАННОГО ИР
            last_year = list(development_data_by_year.keys())[-1]
            purchase_year_IR_cost = development_data_by_year[last_year]["Накопительная стоимость"]
            self.development_cost, output = discounted_IR_cost_to_l_year(purchase_year_IR_cost, tk, last_year, Tk_plan, number_IR)

            # output = (
            #     "\n"
            #     f"Расчет стоимость разработки {number_IR}-го ресурса\n"
            #     "--------------------\n"
            # )
            for year, data in development_data_by_year.items():
                output += f"{year} Базовая стоимость: {data['Базовая стоимость']}, Накопительная стоимость: {data['Накопительная стоимость']}\n"
            output += f"Приведённая стоимость эксплуатации разрабатываемого ИР: {self.development_cost}\n"
            output += "\n"
            self.display_info(output)
            self.generate_data_exel("разрабатываемый", [development_data_by_year, number_IR])

    # Расчет части ресурса приносящей прибыль
    def calculateProfitGeneratingCost(self, number_IR):
        """
        Все прост, найти по номеру ресурса прибыль
        :param number_IR:
        :return:
        """
        IR_info = self.ir_info.get(f'ir_{number_IR}', None)
        if IR_info:
            IR_info = IR_info["Сведения по приносимой прибыли"]
            self.generated_profit = IR_info["Приносимая прибыль"]
            output = (
                "\n"
                f"Расчет приносимой прибыли {number_IR}-го ресурса\n"
                "----------------------------------------------------\n"
                f"Приносимая прибыль: {self.generated_profit}\n"
                "\n"
            )
            self.display_info(output)
            self.generate_data_exel("приносящий прибыль", [number_IR])

    def calculateTotalCost(self, number_IR):
        """
        Функция считает ОБЩАЯ стоимость
        :return:
        """
        array = [self.buy_cost, self.total_cost_g_year, self.development_cost, self.generated_profit]

        self.total_cost = sum(array)
        output = (
            "\n"
            f"Расчет ОБЩЕЙ стоимости {number_IR}-го ресурса\n"
            "----------------------------------------------------\n"
            f"ОБЩАЯ стоимость: {self.total_cost}\n"
            f"array: {array}\n"
            "\n"
        )

        self.display_info(output)
        self.generate_data_exel("ОБЩАЯ стоимость", [number_IR])

    def display_info(self, output_str: str):
        """
        Функция занимается логирование происходящих рамс четов и выводом информации в терминал
        :param output_str:
        """
        print(output_str)

    def generate_data_exel(self, property_IR: str, info: Union[int, dict[int, dict[str, float]]]):
        """
        Функция создает правильные строки для Exel
        :param property_IR: Свойcтво ИР;
        :param info: Информация по ИР;
        :return:
        """

        if property_IR == "приобретаемый":
            data = self.data_pattern[-1].copy()
            data[0] = info[-1]
            data[1] = "Стоимость приобретения"
            index = self.data_pattern[0].index(info[1])
            data[index] = info[0]
            self.data_exel.append(data)

            data = self.data_pattern[-1].copy()
            data[0] = info[-1]
            data[1] = "Приведенаая стоимость приобретения"
            data[-1] = self.buy_cost
            self.data_exel.append(data)

        if property_IR == "обслуживаемый":
            data = self.data_pattern[-1].copy()
            data[0] = info[-1]
            data[1] = "Стоимость обслуживания"
            data[-1] = info[0]
            self.data_exel.append(data)

        if property_IR == "разрабатываемый":
            # Базовая стоимость
            data = self.data_pattern[-1].copy()
            data[0] = info[-1]
            data[1] = "Базовая стоимость разработки"
            for i in info[0].keys():
                index = self.data_pattern[0].index(i)
                data[index] = info[0][i]["Базовая стоимость"]
            self.data_exel.append(data)

            # Накопительная стоимость
            data = self.data_pattern[-1].copy()
            data[0] = info[-1]
            data[1] = "Накопленная стоимость разработки"
            for i in info[0].keys():
                index = self.data_pattern[0].index(i)
                data[index] = info[0][i]["Накопительная стоимость"]
            self.data_exel.append(data)

            # Приведённая стоимость эксплуатации
            data = self.data_pattern[-1].copy()
            data[0] = info[-1]
            data[1] = "Приведённая стоимость эксплуатации"
            data[-1] = self.development_cost
            self.data_exel.append(data)

        if property_IR == "приносящий прибыль":
            data = self.data_pattern[-1].copy()
            data[0] = info[-1]
            data[1] = "Прибыль"
            data[-1] = self.generated_profit
            self.data_exel.append(data)

        if property_IR == "ОБЩАЯ стоимость":
            data = self.data_pattern[-1].copy()
            data[0] = info[-1]
            data[1] = "ОБЩАЯ стоимость"
            data[-1] = self.total_cost
            self.data_exel.append(data)
