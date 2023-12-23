
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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_path = 'text_file.txt'
    file_path_exeption = 'exeption.txt'
    List = []
    ListExeption = read_and_create_list(file_path_exeption)
    index = 0
    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    emb = NewsEmbedding()

    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)
    ner_tagger = NewsNERTagger(emb)

    names_extractor = NamesExtractor(morph_vocab)

    text_first = read_string_from_file(file_path)
    text_second = text_first.split()
    modified_list = replace_numbers_with_asterisks(text_second)
    text = ", ".join(modified_list)
    doc = Doc(text)
    doc.segment(segmenter)
    # print(doc.tokens[:5])
    # print(doc.sents[:5])
    # print("______________________________\n")
    doc.tag_morph(morph_tagger)
    # print(doc.tokens[:5])
    # doc.sents[0].morph.print()
    # print("______________________________\n")
    # for token in doc.tokens:
    #     token.lemmatize(morph_vocab)
    # print(doc.tokens[:5])
    # {_.text: _.lemma for _ in doc.tokens}
    # print("______________________________\n")
    doc.parse_syntax(syntax_parser)
    # print(doc.tokens[:5])
    # doc.sents[0].syntax.print()
    # print("______________________________\n")
    doc.tag_ner(ner_tagger)
    # print(doc.spans[:5])
    # doc.ner.print()
    # print("______________________________\n")
    for span in doc.spans:
        if span.type == PER:
            List.append(span.text)
        if span.type == LOC:
            List.append(span.text)
    ListMonth = ["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"]
    result_list = remove_duplicates(List, ListExeption)
    replace_elements_with_asterisks(modified_list, ListMonth)
    print(modified_list)
    replace_elements_with_asterisks(modified_list, result_list)
    print(modified_list)
    text_end = " ".join(modified_list)
    save_string_to_file(file_path, text_end)
    # print(doc.spans[:5])
    # {_.text: _.normal for _ in doc.spans if _.text != _.normal}
    # print("______________________________\n")
    # for span in doc.spans:
    #     if span.type == PER:
    #         span.extract_fact(names_extractor)
    #
    # print(doc.spans[:5])
    # {_.normal: _.fact.as_dict for _ in doc.spans if _.type == PER}
# See PyCharm help at https://www.jetbrains.com/help/pycharm/