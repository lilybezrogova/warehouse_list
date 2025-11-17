import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Исходные данные
categories = ["Одежда", "Продукты", "Электроника", "Мебель"]
warehouses = ["Склад_А", "Склад_В", "Склад_С"]
names = [f"Товар_{i}" for i in range(1, 31)]

df = pd.DataFrame({
    "Название": np.random.choice(names, size = 30),
    "Категория": np.random.choice(categories, size = 30),
    "Количество": np.random.randint(1, 100, size = 30),
    "Цена за единицу": np.random.randint(10, 10_000, size = 30),
    "Складское помещение": np.random.choice(warehouses, size = 30)
})

df1 = df.drop_duplicates(subset = ["Название", "Складское помещение"]).reset_index(drop = True)

while len(df1) < 30:
    new_row = {
        "Название": np.random.choice(names),
        "Категория": np.random.choice(categories),
        "Количество": np.random.randint(1, 100),
        "Цена за единицу": np.random.randint(10, 10_000),
        "Складское помещение": np.random.choice(warehouses)
    }
    df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
    df1 = df1.drop_duplicates(subset = ["Название", "Складское помещение"]).reset_index(drop = True)

df = df1.reset_index(drop = True)

# Логирование
def log_action(action):
    with open("log.txt", "a", encoding = "utf-8") as f:
        f.write(f"{datetime.now()} - {action}\n")


# Функциональность
def show_data(df): 
    print(f"\nТекущие товары на складе: \n{df}") 
    log_action("Пользователь посмотрел таблицу.")

def add_product(df): # Добавить товар
    try:
        print("\nДобавить новый товар.")
        
        name = input("Введите название товара: ").strip()
        if name not in names:
            name = np.random.choice(names)
            print(f"Название ввели неправильно, выбрано: {name}.")

        category = input(f"Введите категорию ({categories}): ").strip()
        if category not in categories:
            category = np.random.choice(categories)  
            print(f"Категорию ввели неправильно, выбрана случайная: {category}.")

        try:
            cnt = int(input("Введите количество (>= 0): "))
            if cnt < 0:
                print("Количество не может быть < 0, выбрано: 0.")
                cnt = 0
        except:
            cnt = np.random.randint(1, 100) 
            print(f"Количество ввели неправильно, выбрано случайное: {cnt}.")

        try:
            price = int(input("Введите цену за единицу (>=0): "))
            if price < 0:
                print("Цена не может быть < 0, выбрано: 0.")
                price = 0
        except:
            price = np.random.randint(10, 10_000)  
            print(f"Цену ввели неправильно, выбрана случайная: {price}.")

        warehouse = input(f"Введите склад ({warehouses}): ").strip()
        if warehouse not in warehouses:
            warehouse = np.random.choice(warehouses)  
            print(f"Склад ввели неправильно, выбран случайный: {warehouse}.")

        new_row = {
            "Название": name,
            "Категория": category,
            "Количество": cnt,
            "Цена за единицу": price,
            "Складское помещение": warehouse
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index = True)
        print(f"{name} добавлен на {warehouse}.")
        log_action(f"Пользователь добавил {name} на {warehouse}.")
    except Exception as e:
        print("Произошла ошибка при добавлении товара.")
        log_action("Произошла ошибка при добавлении товара.")
    return df

def remove_product(df):  # Удалить товар
    try:
        print("\nУдалить товар.")

        name = input("Введите название товара: ").strip()
        
        if name not in df["Название"].values:
            print(f"Товара '{name}' нет.")
            log_action(f"Пользователь запросил отсутствующий товар '{name}'.")
            return df
        
        df = df[df["Название"] != name]
        print(f"{name} удалён.")
        log_action(f"Пользователь удалил {name}.")  
    except Exception as e:
        print("Произошла ошибка при удалении товара.")
        log_action("Произошла ошибка при удалении товара.")
    return df

def update_cnt(df): # Изменить количество товара на конкретном складе
    try:
        print("\nИзменить количество товара на конкретном складе.")

        name = input("Введите название товара: ").strip()
        warehouse = input(f"Введите склад ({warehouses}): ").strip()

        mask = ((df["Название"] == name) & (df["Складское помещение"] == warehouse))
        if not mask.any():
            print(f"Товара '{name}' на складе '{warehouse}' нет.")
            log_action(f"Пользователь запросил отсутствующий товар '{name}' на складе '{warehouse}'.")
            return df

        try:
            new_cnt = int(input("Введите новое количество (>= 0): "))
            if new_cnt < 0:
                print("Количество не может быть < 0, выбрано: 0.")
                new_cnt = 0
        except:
            new_cnt = np.random.randint(1, 100)
            print(f"Количество ввели неправильно, выбрано случайное: {new_cnt}.")

        df.loc[mask, "Количество"] = new_cnt
        print(f"Количество {name} на {warehouse} изменено на {new_cnt}.")
        log_action(f"Пользователь изменил количество {name} на {warehouse} на {new_cnt}.")
    except Exception as e:
        print("Произошла ошибка при изменении количества товара.")
        log_action("Произошла ошибка при изменении количества товара.")
    return df

def update_price(df): # Изменить цену товара на всех или на одном складе
    try:
        print("\nИзмененить цену товара на всех или на одном складе.")

        name = input("Введите название товара: ").strip()
        warehouse = input(f"Введите склад ({warehouses}) или оставьте пустым (для всех складов): ").strip()
        
        if warehouse:
            mask = ((df["Название"] == name) & (df["Складское помещение"] == warehouse))
        else:
            mask = (df["Название"] == name)
        
        if not mask.any():
            print(f"Товара '{name}' на складе '{warehouse}' нет.")
            log_action(f"Пользователь запросил отсутствующий товар '{name}' на складе '{warehouse}'.")
            return df
        
        try:
            new_price = int(input("Введите новую цену (>=0 ): "))
            if new_price < 0:
                print("Цена не может быть < 0, выбрано: 0.")
                new_price = 0
        except:
            new_price = np.random.randint(10, 10_000)
            print(f"Цену ввели неправильно, выбрана случайная: {new_price}.")
        
        df.loc[mask, "Цена за единицу"] = new_price
        print(f"Цена {name} изменена на {new_price}.")
        log_action(f"Пользователь изменил цену {name} на {new_price}.")
    except Exception as e:
        print("Произошла ошибка при изменении цены товара.")
        log_action("Произошла ошибка при изменении цены товара.")
    return df

def total_sum(df): # Общая стоимость всех товаров
    total = (df["Количество"] * df["Цена за единицу"]).sum()
    print(f"Общая стоимость всех товаров: {total}.")
    log_action(f"Пользователь запросил общую стоимость всех товаров.")

def avr_price(df): # Средняя цена по категориям
    avr_price = df.groupby("Категория")["Цена за единицу"].mean()
    print(f"Средняя цена по категориям: \n{avr_price}.")
    log_action(f"Пользователь запросил среднюю цену по категориям.")

def top5_expensive(df): # Топ-5 самых дорогих позиций
    top5 = df.sort_values('Цена за единицу', ascending = False).head(5)
    print(f"Топ-5 самых дорогих позиций: \n{top5}")
    log_action(f"Пользователь запросил топ-5 самых дорогих позиций.")

def cnt_category(df): # Число товаров одной категории
    cnt = df.groupby("Категория")["Количество"].sum()
    print(f"Число товаров по категориям: \n{cnt}.")
    log_action(f"Пользователь запросил число товаров одной категории.")

def cnt_warehouse(df): # Число товаров на одном складе
    cnt = df.groupby("Складское помещение")["Количество"].sum()
    print(f"Число товаров на каждом складе: \n{cnt}.")
    log_action(f"Пользователь запросил число товаров на каждом складе.")

def fltr_category(df): # Фильтрация товаров по категории
    print("\nФильтрация товаров по категории.")

    category = input(f"Введите категорию для фильтрации ({categories}): ").strip()
    f = df[df["Категория"] == category]
    if f.empty:
        print(f"Категории '{category}' нет.")
        log_action(f"Категории '{category} нет'.")  
    else:
        print(f"Фильтрация товаров по категории '{category}':\n{f}")
        log_action(f"Пользователь запросил фильтрацию по категории '{category}'.")

def fltr_warehouse(df): # Фильтрация товаров по складу
    print("\nФильтрация товаров по складу.")

    warehouse = input(f"Введите склад для фильтрации ({warehouses}): ").strip()
    f = df[df["Складское помещение"] == warehouse]
    if f.empty:
        print(f"Cклада '{warehouse}' нет.")
        log_action(f"Склада '{warehouse} нет'.")
    else:
        print(f"Фильтрация товаров по {warehouse}:\n{f}")
        log_action(f"Пользователь запросил фильтрацию по {warehouse}.")

def order_product(df): # Заказать один или несколько товаров
    try:
        print("\nЗаказать один или несколько товаров.")

        name = input("Введите название товара для заказа: ").strip()
        cnt = int(input("Введите количество товара для заказа: "))
        
        df1 = df[(df["Название"] == name) & (df["Количество"] > 0)]
        if df1.empty:
            print(f"Товара '{name}' нет.")
            log_action(f"Товара '{name}' нет.")
            return df
        
        if len(df1) > 1:
            print("Товар есть на нескольких складах:")
            print(df1[["Название", "Складское помещение", "Количество"]])
            warehouse = input("Выберите склад для заказа: ").strip()
            mask = (df["Название"] == name) & (df["Складское помещение"] == warehouse)
        else:
            mask = (df["Название"] == name)
            warehouse = df1.iloc[0]["Складское помещение"]
        
        if df.loc[mask, "Количество"].iloc[0] < cnt:
            print(f"{name}' не хватает на {warehouse}. Доступное количество товара: {df.loc[mask, 'Количество'].iloc[0]}")
            log_action(f"Пользователь хотел заказать {name}, но на {warehouse} его не хватает.")
            return df
        
        df.loc[mask, "Количество"] -= cnt
        print(f"Заказ: {cnt} шт. {name} со {warehouse}")
        log_action(f"Пользователь заказал {cnt} шт. {name} со {warehouse}")
    except Exception as e:
        print("Произошла ошибка при заказе товара.")
        log_action("Произошла ошибка при заказе товара.")
    return df

def min_max_price_warehouse(df):  # Вывод товаров, цена которых больше и меньше всего на конкретном складе
    try:
        print("\nВывод товаров, цена которых больше и меньше всего на конкретном складе.")

        warehouse = input(f"Введите склад ({warehouses}): ").strip()
        
        if warehouse not in warehouses:
            warehouse1 = np.random.choice(warehouses)
            print(f"Склада '{warehouse}' нет, выбран случайный: '{warehouse1}'.")
            warehouse = warehouse1

        df1 = df[(df["Складское помещение"] == warehouse) & (df["Количество"] > 0)]
        if df1.empty:
            print(f"На {warehouse} товаров нет.")
            log_action(f"На {warehouse} товаров нет.")
        
        max_t = df1.loc[df1["Цена за единицу"].idxmax()]
        min_t = df1.loc[df1["Цена за единицу"].idxmin()]
        
        print(f"Товар с максимальной ценой на {warehouse}: \n{max_t}")
        print(f"Товар с минимальной ценой на {warehouse}: \n{min_t}")
        log_action(f"Пользователь запросил товары, цена которых больше и меньше всего на конкретном {warehouse}.")
                
    except Exception as e:
        print("Произошла ошибка при выводе товаров, цена которых больше и меньше всего на конкретном складе.")
        log_action("Произошла ошибка при выводе товаров, цена которых больше и меньше всего на конкретном складе.")

def show_category(df): # Вывод всех товаров определённой категории
    try:
        print("\nВывод всех товаров определённой категории.")

        category = input(f"Введите категорию ({categories}): ").strip()
        
        fltr = df[df["Категория"] == category]
        if fltr.empty:
            print(f"Товаров категории '{category}' нет.")
            log_action(f"Товаров категории '{category}' нет.")
        else:
            print(f"Все товары категории '{category}': \n{fltr}")
            log_action(f"Пользователь запросил вывод всех товаров категории '{category}'.")
    except Exception as e:
        print("Произошла ошибка при выводе всех товаров по категории.")
        log_action("Произошла ошибка при выводе всех товаров по категории.")

def filter_price(df): # Фильтрация данных по цене в заданном диапазоне
    try:
        print("\nФильтрация данных по цене в заданном диапазоне.")
        
        try:
            min_price = int(input("Введите минимальную цену: "))
            if min_price < 0:
                print("Минимальная цена не может быть < 0, выбрано 0.")
                min_price = 0
        except:
            min_price = np.random.randint(0, df["Цена за единицу"].max())
            print(f"Минимальную цену ввели неправильно, выбрана случайная: {min_price}.")
        
        try:
            max_price = int(input("Введите максимальную цену: "))
            if max_price < min_price:
                print(f"Максимальная цена < минимальной цены, максимальная цена выбрана {min_price + 1000}.")
                max_price = min_price + 1000
        except:
            max_price = np.random.randint(min_price, df["Цена за единицу"].max())
            print(f"Максимальную цену ввели неправильно, выбрана случайная: {max_price}.")
        
        df1 = df[(df["Цена за единицу"] >= min_price) & (df["Цена за единицу"] <= max_price)]
        if df1.empty:
            print(f"Товаров в диапазоне цен ({min_price}-{max_price}) нет.")
            log_action(f"Товаров в диапазоне цен ({min_price}-{max_price}) нет.")
        else:
            print(f"Товары в диапазоне цен ({min_price}-{max_price}): \n{df1}")
            log_action(f"Пользователь запросил фильтрацию товаров по цене в диапазоне ({min_price}-{max_price}).")
            
    except Exception:
        print("Произошла ошибка при фильтрации товаров по цене в заданном диапазоне.")
        log_action("Произошла ошибка при фильтрации товаров по цене в заданном диапазоне.")

# Визуализация
def plot_warehouse_cnt(df): # Диаграмма заполненности складов
    try:        
        df1 = df["Складское помещение"].value_counts()
        df1.plot(kind = "bar", color = "skyblue")
        plt.title("Заполненность складов")
        plt.ylabel("Количество товаров")
        plt.xlabel("Склад")
        file = "plot_warehouse.png"
        plt.savefig(file)
        plt.show()
        print(f"Диаграмма заполненности складов сохранена в файл '{file}'.")
        log_action("Пользователь запросил диаграмму заполненности складов.")
    except Exception as e:
        print("Произошла ошибка при построении диаграммы складов.")
        log_action("Произошла ошибка при построении диаграммы складов.")

def plot_total_t(df): # График числа товаров (сумма со всех складов)
    try:
        df1 = df.groupby("Складское помещение")["Количество"].sum()
        df1.plot(kind = "bar", color = "lightgreen")
        plt.title("Сумма со всех складов")
        plt.ylabel("Количество")
        plt.xlabel("Склад")
        file = "plot_total_t.png"
        plt.savefig(file)
        plt.show()
        print(f"График числа товаров (сумма со всех складов) сохранен в файл '{file}'.")
        log_action("Пользователь просмотрел график числа товаров (сумма со всех складов).")
    except Exception as e:
        print("Произошла ошибка при построении графика числа товаров (сумма со всех складов).")
        log_action("Произошла ошибка при построении графика числа товаров (сумма со всех складов).")

def plot_warehouse_price(df): # График стоимости товаров на конкретном складе
    try:
        warehouse = input(f"Введите склад для графика ({warehouses}): ").strip()
        if warehouse not in warehouses:
            warehouse1 = np.random.choice(warehouses)
            print(f"Склад ввели неправильно, выбран случайный: {warehouse1}.")
            warehouse = warehouse1
        
        df1 = df[df["Складское помещение"] == warehouse].copy()  
        df1["Стоимость"] = df1["Количество"] * df1["Цена за единицу"]
        df1.plot(x = "Название", y = "Стоимость", kind = "bar", legend = False)
        plt.title(f"Стоимость товаров на {warehouse}")
        plt.ylabel("Стоимость")
        plt.xlabel("Товар")
        file = f"plot_warehouse_price_{warehouse}.png"
        plt.savefig(file)
        plt.show()
        print(f"График стоимости товаров на конкретном складе сохранен в файл '{file}'.")
        log_action(f"Пользователь просмотрел график стоимости товаров на {warehouse}.")
    except Exception as e:
        print(f"Произошла ошибка при построении графика стоимости товаров на {warehouse}.")
        log_action(f"Произошла ошибка при построении графика стоимости товаров на {warehouse}.")

def plot_category(df): # Круговая диаграмма: доля категорий в общей стоимости всех товаров
    try:
        df1 = df.copy()
        df1["Стоимость"] = df1["Количество"] * df1["Цена за единицу"]
        df2 = df1.groupby("Категория")["Стоимость"].sum()
        df2.plot(kind = "pie", autopct = "%1.1f%%", startangle = 90)
        plt.title("Доля категорий в общей стоимости всех товаров")
        plt.ylabel("")
        file = "plot_category.png"
        plt.savefig(file)
        plt.show()
        print(f"Круговая диаграмма сохранена в файл '{file}'.")
        log_action("Пользователь просмотрел круговую диаграмму: доля категорий в общей стоимости всех товаров.")
    except Exception as e:
        print("Произошла ошибка при построении круговой диаграммы: доля категорий в общей стоимости всех товаров.")
        log_action("Произошла ошибка при построении круговой диаграммы: доля категорий в общей стоимости всех товаров.")

#  Экспорт данных
def export_csv(df):
    try:
        file = input("Введите имя файла для сохранения (.csv): ").strip()
        if file[-4:] != ".csv":
            file += ".csv"
        df.to_csv(file, index = False, encoding = "utf-8-sig")
        print(f"Экспорт данных в файл '{file}'.")
        log_action(f"Пользователь экспортировал данные в файл '{file}'.")
    except Exception as e:
        print("Произошла ошибка при сохранении данных в CSV.")
        log_action("Произошла ошибка при сохранении данных в CSV.")

# Меню
def menu(df):
    while True:
        print("""
Меню:
1. Показать товары
2. Добавить товар
3. Удалить товар
4. Изменить количество товара на конкретном складе
5. Изменить цену товара на всех или на одном складе
6. Общая стоимость всех товаров
7. Средняя цена по категориям
8. Топ-5 самых дорогих позиций
9. Число товаров одной категории
10. Число товаров на одном складе
11. Фильтрация товаров по категории
12. Фильтрация товаров по складу
13. Заказать один или несколько товаров
14. Вывод товаров, цена которых больше и меньше всего на конкретном складе
15. Вывод всех товаров определённой категории
16. Фильтрация данных по цене в заданном диапазоне
17. Построить диаграмму заполненности складов.
18. Построить график числа товаров (сумма со всех складов).
19. Построить график стоимости товаров на конкретном складе.
20. Построить круговую диаграмму: доля категорий в общей стоимости всех
товаров.
21. Сохранить данные в CSV
0. Выход
""")
        choice = input("Выбор: ").strip()

        if choice == "0":
            print("Выход из программы.")
            break
        elif choice == "1":
            show_data(df)
        elif choice == "2":
            df = add_product(df)
        elif choice == "3":
            df = remove_product(df)
        elif choice == "4":
            df = update_cnt(df)
        elif choice == "5":
            df = update_price(df)
        elif choice == "6":
            total_sum(df)
        elif choice == "7":
            avr_price(df)
        elif choice == "8":
            top5_expensive(df)
        elif choice == "9":
            cnt_category(df)
        elif choice == "10":
            cnt_warehouse(df)
        elif choice == "11":
            fltr_category(df)
        elif choice == "12":
            fltr_warehouse(df)
        elif choice == "13":
            df = order_product(df)
        elif choice == "14":
            min_max_price_warehouse(df)
        elif choice == '15':
            show_category(df)
        elif choice == "16":
            filter_price(df)
        elif choice == "17":
            plot_warehouse_cnt(df)
        elif choice == "18":
            plot_total_t(df)
        elif choice == "19":
            plot_warehouse_price(df)
        elif choice == "20":
            plot_category(df)
        elif choice == "21":
            export_csv(df)
        else:
            print("Некорректный ввод.")
    return df

# Запуск
print("Список склада")
menu(df)