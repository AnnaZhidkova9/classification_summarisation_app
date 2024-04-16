import tkinter as tk
from tkinter import ttk
import pandas as pd
import json
import sqlite3
from datetime import datetime
import webbrowser
import textwrap
from heapq import nlargest
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import feedparser
import requests
from bs4 import BeautifulSoup as bs
from ttkthemes import ThemedStyle
from tkinter import ttk, messagebox

"""Функция для получения данных с базы данных по выбранному журналу(сайту)"""
def get_data_databese(journal_name):
    # Устанавливаем соединение с базой данных
    
    #get_news_rss()

    date_database = {
            'Название статьи': [],
            'Ссылка на статью': [],
            'Дата публикации': [],
            'Текст статьи': [],
            'Тема':[],
            'Суммаризация': []
            }
    
    conn = sqlite3.connect('Arctic_11_01_24.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для выборки всех данных из таблицы 'articles'
    cursor.execute("SELECT * FROM articles WHERE journal = ?", (journal_name,))
    # Получаем все строки, возвращаемые запросом
    articles = cursor.fetchall()
    # Выводим каждую строку
    for article in articles:
        id, journal, site, name, publication_date, text, classification = article
        
        date_object = datetime.strptime(publication_date, '%a, %d %b %Y %H:%M:%S %z')
        
        # Извлечение только числа месяца и года
        day_month_year = date_object.strftime("%d.%m.%Y")
        
        summarized_text = summarize_text(text)
        
        # Добавление значений в словарь
        date_database['Название статьи'].append(name)
        date_database['Ссылка на статью'].append(site)
        date_database['Дата публикации'].append(day_month_year)
        date_database['Текст статьи'].append(text)
        date_database['Тема'].append(classification)
        date_database['Суммаризация'].append(summarized_text)
        
        
    df = pd.DataFrame(date_database)
    
    # Сортировка по дате
    df['Дата публикации'] = pd.to_datetime(df['Дата публикации'], format='%d.%m.%Y')
    df.sort_values(by='Дата публикации', inplace=True, ascending=False)
    # Преобразование столбца 'Дата публикации' в формат datetime
    df['Дата публикации'] = pd.to_datetime(df['Дата публикации'])
    # Форматирование объектов datetime в желаемый формат
    df['Дата публикации'] = df['Дата публикации'].dt.strftime('%d.%m.%Y')
    
        
    # Закрываем соединение с базой данных
    conn.close()
    return df

def get_data_databese_topic(topic_name):
    date_database = {
            'Название статьи': [],
            'Ссылка на статью': [],
            'Дата публикации': [],
            'Текст статьи': [],
            'Тема':[],
            'Суммаризация': []
            }
    
    conn = sqlite3.connect('Arctic_11_01_24.db')
    cursor = conn.cursor()
    journal_name = site_var.get()
    print(journal_name)
    print(topic_name)
    cursor.execute("SELECT * FROM articles WHERE classification=? AND journal=?", (topic_name, journal_name))
    articles = cursor.fetchall()
    # Выводим каждую строку
    for article in articles:
        id, journal, site, name, publication_date, text, classification = article
        #print(f"ID: {id}, Journal: {journal}, Site: {site}, Name: {name}, Publication Date: {publication_date}, Text: {text}")
        
        date_object = datetime.strptime(publication_date, '%a, %d %b %Y %H:%M:%S %z')
        
        # Извлечение только числа месяца и года
        day_month_year = date_object.strftime("%d.%m.%Y")
        
        summarized_text = summarize_text(text)
        
        # Добавление значений в словарь
        date_database['Название статьи'].append(name)
        date_database['Ссылка на статью'].append(site)
        date_database['Дата публикации'].append(day_month_year)
        date_database['Текст статьи'].append(text)
        date_database['Тема'].append(classification)
        date_database['Суммаризация'].append(summarized_text)
        
        
    df = pd.DataFrame(date_database)
    
    # Сортировка по дате
    df['Дата публикации'] = pd.to_datetime(df['Дата публикации'], format='%d.%m.%Y')
    df.sort_values(by='Дата публикации', inplace=True, ascending=False)
    # Преобразование столбца 'Дата публикации' в формат datetime
    df['Дата публикации'] = pd.to_datetime(df['Дата публикации'])
    # Форматирование объектов datetime в желаемый формат
    df['Дата публикации'] = df['Дата публикации'].dt.strftime('%d.%m.%Y')
    
        
    # Закрываем соединение с базой данных
    conn.close()
    return df
    

"""Функция сортировки по дате"""
def sort_by_date():
    journal_name = site_var.get()
    data = get_data_databese(journal_name)
    df_temp_sort = pd.DataFrame(data, columns=['Название статьи', 'Ссылка на статью','Дата публикации', 'Текст статьи', 'Суммаризация'])
    df_temp_sort['Дата публикации'] = pd.to_datetime(df_temp_sort['Дата публикации'], dayfirst=True)
    df_sorted = df_temp_sort.sort_values(by='Дата публикации', ascending=True)
    update_table(df_sorted)
    

"""Функция поиска по названию статьи"""
def search_news():
    search_query = search_var.get().lower() # Получение запроса пользователя
    journal_name = site_var.get() # Получение выбранного сайта
    data = get_data_databese(journal_name) # Получение данных по выбранному сайту
    
    # Фильтрация данных по названию статьи
    filtered_data = data[data['Название статьи'].str.lower().str.contains(search_query)]
    
    # Обновление таблицы с отфильтрованными данными
    update_table(filtered_data)
    
"""Функция суммаризации по заданному числу предложений"""
def summarize():
    # Получение числа предложений, введенного пользователем
    num_sentences_str = sentence_var.get()
    
    # Проверка, является ли введенное значение числом
    if not num_sentences_str.isdigit():
        # Если не число, выводим окно с ошибкой
        messagebox.showerror('Ошибка', 'Введено не число. Пожалуйста, введите число предложений.')
        return # Прерываем выполнение функции
    
    # Преобразование строки в число
    num_sentences = int(num_sentences_str)
    
    # Получение выбранного пользователем сайта
    journal_name = site_var.get()
    
    # Получение данных из базы данных
    data = get_data_databese(journal_name)
    
    # Применение функции summarize_text к тексту каждой статьи
    for index, row in data.iterrows():
        text = row['Текст статьи']
        summarized_text = summarize_text(text, num_sentences=num_sentences)
        
        # Обновление суммаризации в данных
        data.at[index, 'Суммаризация'] = summarized_text
    
    # Обновление таблицы с суммаризированными данными
    update_table(data)

"""Функция для активации гиперссылки"""
def open_link(event):
    # Получение элемента, на который нажали
    item = tree.item(tree.focus())
    # Получение URL из значения ячейки 'Ссылка на статью'
    url = item['values'][2] # Предполагается, что 'Ссылка на статью' - это третий столбец
    # Открытие URL в браузере
    webbrowser.open(url)

"""Функция переноса по строкам текста(статьи, названия, суммаризации)"""
def wrap(string, length):
    if string is None:
        return ""
    else:
        return '\n'.join(textwrap.wrap(string, length))

"""Функция обновления таблицы"""
def update_table(df):
    # Очистка таблицы
    for i in tree.get_children():
        tree.delete(i)
    # Добавление строк в таблицу
    for index, row in df.iterrows():
        name_state = wrap(row['Название статьи'], 37)
        summari = wrap(row['Суммаризация'],  105)
        topic = wrap(row['Тема'],  30)
        tree.insert('', 'end', values=(name_state, row['Дата публикации'], row['Ссылка на статью'], topic, summari), tags=('link',))   

"""Функция возвращает список сайтов"""
def get_name_websites():
    web_s = []
    with open('structure_5.json') as f:
        journal_structure = json.load(f)
    for journal in journal_structure["websites"]:
        web_s.append(journal)
    return web_s

"""Функция возвращает выбранный пользователем САЙТ и вызывает функцию обновления таблицы"""
def on_site_selected(event):
    journal_name = site_var.get()
    data = get_data_databese(journal_name)
    update_table(data)

"""Функция возвращает выбранную пользователем ТЕМУ и вызывает функцию обновления таблицы"""
def on_topic_selected(event):
    topic_name = topic_var.get()
    data = get_data_databese_topic(topic_name)
    update_table(data)
    
"""Функция сбрасывает настройки с выбором темы, и выводит все статьи по данному сайту"""    
def reset_table():
    journal_name = site_var.get()
    data = get_data_databese(journal_name)
    update_table(data)
    topic_var.set('')
    
"""Функция - генерация шинглов для суммаризации"""
def generate_shingles(text, k):
    words = text.split()
    shingles = set()

    for i in range(len(words) - k + 1):
        shingle = ' '.join(words[i:i+k])
        shingles.add(shingle)

    return shingles

"""Функция - схожесть для суммаризации"""
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    similarity = intersection / union if union != 0 else 0

    return similarity

"""Функция - суммаризация"""
def summarize_text(text, num_sentences=3, shingle_size=10):
    # Разделяем текст на предложения
    sentences = text.split('.')
    texts = [sentence.strip() for sentence in sentences if sentence.strip()]

    shingles_list = [generate_shingles(text, shingle_size) for text in texts]

    similarity_matrix = [[jaccard_similarity(set1, set2) for set2 in shingles_list] for set1 in shingles_list]

    main_text_index = 0
    max_similarity_sum = sum(similarity_matrix[0])
    for i in range(1, len(similarity_matrix)):
        current_similarity_sum = sum(similarity_matrix[i])
        if current_similarity_sum > max_similarity_sum:
            max_similarity_sum = current_similarity_sum
            main_text_index = i

    summary_sentences = sorted(range(len(texts)), key=lambda x: similarity_matrix[main_text_index][x], reverse=True)[:num_sentences]

    summary = [texts[i] for i in summary_sentences]

    compressed_text = ". ".join(summary) + '.'
    return compressed_text

root = tk.Tk()
root.title("Классификация и суммаризация статей")
root.minsize(1550, 400) 
root.geometry('1450x900+230+50')

# Использование темы оформления ttkthemes
style = ThemedStyle(root)
style.set_theme("radiance")  # Выбор темы

# Настройка окна для адаптивного изменения размера
root.rowconfigure(0, )
root.rowconfigure(1, )
root.rowconfigure(2, )
root.rowconfigure(3, weight=1)
root.columnconfigure(0, weight=4)

# Создание метки над полем ввода
search_label = ttk.Label(root, text="Поиск по названию:")
search_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')

# Создание поля ввода для поиска
search_var = tk.StringVar(root)
search_entry = ttk.Entry(root, textvariable=search_var, width=35)
search_entry.grid(row=1, column=0, padx=20, pady=0, sticky='w')

# Создание кнопки для выполнения поиска
search_button = ttk.Button(root, text="Поиск", command=search_news)
search_button.grid(row=1, column=1, padx=0, pady=10, sticky='w')

# Создание метки над полем ввода для выбора сайта
site_label = ttk.Label(root, text="Выбор сайта:")
site_label.grid(row=0, column=2, padx=10, pady=10, sticky='w')

# Создание раскрывающегося списка для выбора сайта
sites = get_name_websites() 
site_var = tk.StringVar(root)
site_var.set(sites[0]) # Установка значения по умолчанию
site_dropdown = ttk.Combobox(root, textvariable=site_var, values=sites, width=35, state = 'readonly')
site_dropdown.grid(row=1, column=2, padx=10, pady=10, sticky='w')

# Создание метки над полем ввода
sentences_label = ttk.Label(root, text="Желаемое число предложений в реферате:")
sentences_label.grid(row=0, column=5, padx=10, pady=10, sticky='w')

# Создание поля для выбора числа предложений
sentence_var = tk.StringVar(root)
sentence_var.set("3")
sentence_entry = ttk.Spinbox(root, textvariable=sentence_var, from_=1, to=5, width=55)
sentence_entry.grid(row=1, column=5, padx=10, pady=10, sticky='w')

# Создание кнопки для выполнения суммаризации по заданному числу предложений
sentences_enter_button = ttk.Button(root, text="Применить", command=summarize)
sentences_enter_button.grid(row=1, column=6, padx=10, pady=10, sticky='w')

# Создание метки над полем ввода
search_label = ttk.Label(root, text="Выбор тематики:")
search_label.grid(row=0, column=3, padx=10, pady=10, sticky='w')

# Создание раскрывающегося списка для выбора тематики
topics = ['Indigenous Arctic', 'Geopolitical Security', 'Maritime Routes', 'International Governance', 
          'Permafrost', 'Collaborative research and diplomatic engagement in the Arctic', 'Unclassified']        
topic_var = tk.StringVar(root)
topic_dropdown = ttk.Combobox(root, textvariable=topic_var, values=topics, width=35, state = 'readonly')
topic_dropdown.grid(row=1, column=3, padx=10, pady=10, sticky='w')

journal_name = site_var.get() # Изначальный
data = get_data_databese(journal_name)

site_dropdown.bind("<<ComboboxSelected>>", lambda event: on_site_selected(event))

topic_dropdown.bind("<<ComboboxSelected>>", lambda event: on_topic_selected(event))

# Создание кнопки для отмены выбора тематики
enter_button = ttk.Button(root, text="Отменить", command=reset_table)
enter_button.grid(row=1, column=4, padx=10, pady=10, sticky='w')

# Создание таблицы
tree = ttk.Treeview(root, columns=('Название статьи', 'Дата публикации', 'Ссылка на статью', 'Классификация','Суммаризация'), show='headings')

s = ttk.Style()
s.configure('Treeview', rowheight = 183) # Установка высоты строки

journal_name = site_var.get() # Изначальный
data = get_data_databese(journal_name)

# Установка ширины столбцов
tree.column('Название статьи', minwidth=300, width=300, stretch=False, anchor='center')
tree.column('Дата публикации', minwidth=160, width=160, stretch=False, anchor='center')
tree.column('Ссылка на статью', minwidth=0, width=0, stretch=False, anchor='center')
tree.column('Классификация', minwidth=300, width=300, stretch=False, anchor='center')
tree.column('Суммаризация', minwidth=500, width=500, stretch=True, anchor='w')

# Настройка заголовков столбцов
tree.heading('Название статьи', text='Название статьи')
tree.heading('Дата публикации', text='Дата публикации')
tree.heading('Ссылка на статью', text='Ссылка на статью')
tree.heading('Классификация', text='Тематика')
tree.heading('Суммаризация', text='Реферат')

# Создание Scrollbar
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
scrollbar.grid(row=3, column=7, sticky='nsw', padx=10, pady=10)
# Настройка таблицы для использования Scrollbar
tree.configure(yscrollcommand=scrollbar.set)

# Привязка события нажатия к элементам с тегом 'link'
tree.tag_bind('link', '<Button-1>', open_link)

# Размещение таблицы в окне
tree.grid(row=3, column=0, padx=10, pady=10, columnspan=7, sticky='nsew')

# Заполнение таблицы данными
update_table(data)

root.mainloop()
