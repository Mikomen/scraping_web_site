import csv
import random
from time import sleep

import requests
from bs4 import BeautifulSoup
import json

url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'accept': '*/*'
}
req = requests.get(url, headers= headers)
src = req.text
with open("index.html", "w", encoding='utf-8') as file:
    file.write(src)


with open("index.html", encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "html")
all_product_href = soup.find_all('a', class_="mzr-tc-group-item-href")

all_category = {}

for item in all_product_href:
    item_name = item.text
    item_link = "https://health-diet.ru" + item.get('href')

    all_category[item_name] = item_link

with open("all_category.json", "w", encoding='utf-8') as file:
    json.dump(all_category, file, indent=4, ensure_ascii=False)

with open("all_category.json", encoding='utf-8') as file:
    all_categorys = json.load(file)

count = 0
iteration = int(len(all_categorys)) - 1
print(f"Всего итерации{count}")
for category_name, category_link in all_categorys.items():

    rep = [","," ", "-", "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")


    req = requests.get(url=category_link, headers=headers)
    src = req.text

    with open(f"data/{count}_{category_name}.html", "w", encoding='utf-8') as file:
        file.write(src)

    with open(f"data/{count}_{category_name}.html", encoding='utf-8') as file:
        src = file.read()

    # alert_block = soup.find(class_="uk-alert-danger")
    # if alert_block is not None:
    #     continue

    soup = BeautifulSoup(src, "html")
    table_inf = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    product = table_inf[0].text
    calory = table_inf[1].text
    proteins = table_inf[2].text
    fats = table_inf[3].text
    carb = table_inf[4].text

    with open(f"data/{count}_{category_name}.csv", "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
                (
                    product,
                    calory,
                    proteins,
                    fats,
                    carb

                )
            )
    products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

    product_info = []

    for item in products_data:
        product_tds = item.find_all("td")

        title = product_tds[0].find("a").text
        calory = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carb = product_tds[4].text

        product_info.append({
            "Title": title,
            "Calory": calory,
            "Proteins": proteins,
            "Fats": fats,
            "Carb": carb
        })

        with open(f"data/{count}_{category_name}.csv", "a", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                    (
                        title,
                        calory,
                        proteins,
                        fats,
                        carb

                    )
                )

        with open(f"data/{count}_{category_name}.json", "a", encoding="utf-8") as file:
            json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f"Итерация  {count}. {category_name}  записан!!!")
    iteration = iteration - 1

    if iteration == 0:
        print("Работа завершено")
        break

    print(f"Осталось итерации: {iteration}")
    sleep(random.randrange(2, 4))