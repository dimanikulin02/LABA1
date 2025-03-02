from category_1st_calculator import ResourceInfo1stCategory
from category_2st_calculator import ResourceInfo2stCategory
from drawTable import ExcelGenerator

from constant_9 import *

years_list = list(price_change_indices.keys())
years_list.append(years_list[-1] + 1)



# Считаем стоимость ИР 1 категории
list_ir = {"ir_1": ir_1_info, "ir_2": ir_2_info, "ir_3": ir_3_info, "ir_4": ir_4_info, "ir_5": ir_5_info}
res_1st_inf = ResourceInfo1stCategory(resource_info, list_ir)
res_1st_inf.process_obs_ir()
exel_data = res_1st_inf.data_exel

# Отрисовываем таблицу в XLSX и PDF
# generator = ExcelGenerator(data_dictionary, years_list, exel_data)
# generator.run()

# Исходные данные для 2-го этапа
cost_IR_1st_category = res_1st_inf.IR_cost
res_2st_inf = ResourceInfo2stCategory(cost_IR_1st_category, data_dictionary)
res_2st_inf.run()





