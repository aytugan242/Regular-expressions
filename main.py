import csv
import re
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

# создаем список и добавлем в него шапку таблицы
result = [contacts_list[0]]
# проходимся по списку: имя, фамилия, отчество распределяем по своим ячейкам, остальные данные оставляем как есть
for i in range(1, len(contacts_list)):
  s = " ".join(contacts_list[i][:3]).strip().split(" ")
  res_s = [i for i in s if i]
  result.append([
      res_s[0], res_s[1], res_s[2] if len(res_s) > 2 else " ",
      contacts_list[i][3], contacts_list[i][4], contacts_list[i][5],
      contacts_list[i][6]
  ])

#  подготовили pattern для телефонных номеров
pattern = r"(\+7|8)?\s*\(*(\d{3})\)*[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})\s*\(*([доб\.]*\s*\d{4})?\)*"
pattern_comp = re.compile(pattern)

# обновляем номера по формату +7(\2)\3-\4-\5 \6
for i in range(1, len(result)):
  result_tel = pattern_comp.sub(r"+7(\2)\3-\4-\5 \6", result[i][5])
  result[i][5] = result_tel

# Функция для объединения данных по фамилия, имя
def merge_duplicates(data):
    merged = {}
    for i in data[1:]:
        key = (i[0], i[1])
        if key in merged:
            if i[2]:
                merged[key][2] = i[2]
            if i[3]:
                merged[key][3] = i[3]
            if i[4]:
                merged[key][4] = i[4]
            if i[5]:
                merged[key][5] = i[5]
            if i[6]:
                merged[key][5] = i[6]
        else:
            merged[key] = i
    return [data[0]] + list(merged.values())


if __name__ == "__main__":
    merged_data = merge_duplicates(result)
    pprint(merged_data)
    # код для записи файла в формате CSV
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(merged_data)