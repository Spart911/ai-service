
# -*- coding: utf-8 -*-
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    PER,
    NamesExtractor,
    Doc, LOC
)
import re
from PIL import Image, ImageDraw
import easyocr

def filter_unique_elements(list1, list2):
    # Приводим элементы второго списка к нижнему регистру
    lower_list2 = [item.lower() for item in list2]

    # Фильтруем элементы первого списка, оставляя только те, которых нет во втором списке с учетом регистра
    result = [item for item in list1 if item.lower()  in lower_list2]

    return result
def find_missing_elements(list_with_asterisks, list_without_asterisks):
    result_list = []

    for item in list_without_asterisks:
        if '*' not in item and item not in list_with_asterisks:
            result_list.append(item)

    return result_list
def capitalize_first_letter_in_all(input_list):
    """
    Принимает список строк и возвращает список с первой буквой в верхнем регистре, а остальными в нижнем.
    """
    result_list = []

    for input_string in input_list:
        # Проверяем, все ли буквы в верхнем регистре
        if input_string.isupper():
            # Преобразуем первую букву в верхний регистр, а остальные в нижний
            result_list.append(input_string.capitalize())
        else:
            # Если не все буквы в верхнем регистре, добавляем строку без изменений
            result_list.append(input_string)

    return result_list
def is_valid_home_format(home_string):
    # Регулярное выражение для формата "д.178/1"
    date_pattern = re.compile(r'\b(?:д|кв)\.\d+(?:/\d+)?\b', flags=re.IGNORECASE)

    return bool(date_pattern.match(home_string))

def is_valid_date_format(date_string):
    date_pattern = re.compile(r'\b\d{2}.\d{2}.\d{4}(г\.)?\b|\b\d{2}.\d{2}.\d{4}')

    return bool(date_pattern.match(date_string))
def is_valid_cost_format(cost_string):
    cost_pattern = re.compile(r'\b\d+(?:р\.|р)\b')

    return bool(cost_pattern.match(cost_string))
def read_string_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"Строка успешно прочитана из файла: {file_path}")
            return content
    except Exception as e:
        print(f"Ошибка при чтении строки из файла: {e}")
        return None

def read_and_create_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Убираем скобки и разделяем текст на слова
    words = [word.strip('[],') for word in content.split()]

    # Удаляем повторяющиеся слова
    unique_words = list(set(words))

    return unique_words
def remove_duplicates(list1, list2):
    unique_list1 = list(set(list1) - set(list2))
    return unique_list1
def save_string_to_file(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Строка успешно сохранена в файл: {file_path}")
    except Exception as e:
        print(f"Ошибка при сохранении строки в файл: {e}")
def replace_numbers_with_asterisks(my_list):
    result_list = []
    chek_ot = 0
    chek_front_ot_zak = 0
    chek_front_ot_fz = 0
    chek_cite_street = 0
    chek_state= 0
    for item in my_list:
        if chek_state == 0 and "." not in item  and "ФЗ"  not in item or (is_valid_date_format(item) and chek_ot == 0) or is_valid_home_format(item) or is_valid_cost_format(item):
            modified_item = ''.join('*' if c.isdigit() & c.isdigit() else c for c in item)
            if chek_cite_street == 1:
                modified_item = "*****"
            result_list.append(modified_item)
        else:
            if "@"  in item or "https://"  in item:
                modified_item = "*****"
                result_list.append(modified_item)
            else:
                result_list.append(item)
        if (item == "от" and chek_front_ot_zak == 1) or (item == "от" and chek_front_ot_fz == 1):
            chek_ot = 1
        else:
            chek_ot = 0

        if item == "ул." or item == "г." or item == "г.о." :
            chek_cite_street = 1
        else:
            chek_cite_street = 0



        if item ==  "ст." or item ==  "(ст.":
            chek_state = 1
        else:
            chek_state = 0



        if (item == "от" and chek_front_ot_zak == 1) or (item == "от" and chek_front_ot_fz == 1):
            chek_ot = 1
        else:
            chek_ot = 0
        if item == "закона":
            chek_front_ot_zak = 1
            chek_front_ot_fz = 0
        else:
            chek_front_ot_zak = 0

        if item == "ФЗ":
            chek_front_ot_fz = 1
            chek_front_ot_zak = 0
        else:
            chek_front_ot_fz = 0
    return result_list
def replace_elements_with_asterisks(list1, list2):
    for i in range(len(list1)):
        for element in list2:
            if element in list1[i]:
                list1[i] = list1[i].replace(element, '******')
def create_rectangles(image_path, result, words_to_hide, ListCoordinate):
    # Load the image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Iterate through each word and check if it needs to be hidden
    for detection, coordinates in zip(result, ListCoordinate):
        word = detection
        print(word)
        # Check if the word needs to be hidden
        if any(hidden_word in word for hidden_word in words_to_hide):
            # Extract the correct coordinates format (x0, y0, x1, y1) from ListCoordinate
            x0, y0, x1, y1 = coordinates[0][0], coordinates[0][1], coordinates[2][0], coordinates[2][1]
            # Draw a rectangle to hide the word
            draw.rectangle([x0, y0, x1, y1], fill="black")

    # Save the image with hidden words outside the loop
    img.save("output_image.jpg")


def extract_text_from_image(image_path, List, ListCoordinate, languages=['en','ru']):
    # Initialize the EasyOCR Reader with the selected languages
    reader = easyocr.Reader(languages)

    # Get the result of text recognition
    result = reader.readtext(image_path)
    for detection in result:
        List.append(detection[1])
        ListCoordinate.append(detection[0])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ListCoordinate = []
    file_path = 'text_file.txt'
    # Path to the image
    image_path = 'test.jpg'
    file_path_exeption = 'exeption.txt'
    List = []
    result_list = []
    ListADD = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря", "мужской", "женский", "Мужской", "Женский"]
    ListExeption = read_and_create_list(file_path_exeption)
    index = 0
    extract_text_from_image(image_path, List ,ListCoordinate)




    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    emb = NewsEmbedding()

    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)
    ner_tagger = NewsNERTagger(emb)

    names_extractor = NamesExtractor(morph_vocab)

    # text_first = read_string_from_file(file_path)
    # text_second = text_first.split()
    text = ", ".join(capitalize_first_letter_in_all(List))
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)
    for span in doc.spans:
        if span.type == PER:
            result_list.append(span.text)
        if span.type == LOC:
            result_list.append(span.text)
    modified_list = find_missing_elements(replace_numbers_with_asterisks(List), List)
    result_list = ListExeption + filter_unique_elements(List, result_list) + modified_list
    result_list = remove_duplicates(result_list, ListExeption)
    result_list = ListADD + result_list
    # text_end = " ".join(str(item) for item in result_list)
    # save_string_to_file("text_del.txt", text_end)
    create_rectangles(image_path, List ,result_list ,ListCoordinate)

    # print(modified_list)
    # replace_elements_with_asterisks(modified_list, result_list)
    # print(modified_list)
    # text_end = " ".join(modified_list)
    # save_string_to_file(file_path, text_end)








