# -*- coding: utf-8 -*-

import re
import pymorphy2


class ProcessingText:

    pymorphy = pymorphy2.MorphAnalyzer(lang='ru-old')

    @staticmethod
    def clrText(input_text, type):
        # "Очистка" текста от знаков препинания, сокращений и лишних пробелов
        # ВНИМАНИЕ: на будущее нужно учесть различные расстановки знаков препинания " - " и "-", например
        # type = 0 - поиск символов
        # type = 1 - поиск символов без учета кавычек
        # type = 2 - поиск символов без учета символа '#'
        # Элементы в list д.б. отсортированы по увеличению числа символов
        if type == 0:
            unwntd_chars = ['🦄', '🔸', '📱', '❗', '❤️', '😍', '💜', '💛', '💙', '❤', '😈', ',', '-', '—', ';', ':', '"', "'",
                            '»', '«', "(", ')', '*', '<', '>', '[', ']', '{', '}', '+', "/", '_', '@', '#', '$', '№',
                            '%', '\n']
            end_sentence_chars = ['???', '!!!', '...', '??', '!!', '?!', '!?', '..', '.', '!', '?']
        elif type == 1:
            unwntd_chars = ['🦄', '🔸', '📱', '❗', '❤️', '😍', '💜', '💛', '💙', '❤', '😈', ',', '-', '—', ';', ':',
                            "(", ')', '*', '<', '>', '[', ']', '{', '}', '+', "/", '_', '@', '#', '$', '№',
                            '%', '\n']
            end_sentence_chars = ['???', '!!!', '...', '??', '!!', '?!', '!?', '..', '.', '!', '?']
        elif type == 2:
            unwntd_chars = ['🦄', '🔸', '📱', '❗', '❤️', '😍', '💜', '💛', '💙', '❤', '😈', ',', '-', '—', ';', ':', '"', "'",
                            '»', '«', "(", ')', '*', '<', '>', '[', ']', '{', '}', '+', "/", '_', '@', '$', '№',
                            '%', '\n']
            end_sentence_chars = ['???', '!!!', '...', '??', '!!', '?!', '!?', '..', '.', '!', '?']
        text = ''
        i = 0
        while i < len(input_text):
            # Остается только окончание - либо " " либо ". "
            flag = False
            for j in unwntd_chars:
                if input_text[i:i + len(j)] == j:
                    text += ' '
                    i += len(j)
                    flag = True
                    break
            for j in end_sentence_chars:
                if input_text[i:i + len(j)] == j:
                    text += '. '
                    i += len(j)
                    flag = True
                    break
            if flag == True:
                continue
            # Обычные символы переносим без изменений
            else:
                text = text + input_text[i]
                i += 1
        text = re.sub('лат\.', 'лат', text)
        text = re.sub('анг\.', 'анг', text)
        text = re.sub('англ\.', 'англ', text)
        text = re.sub('т\.д\.', 'тд', text)
        text = re.sub('т\. д\.', 'тд', text)
        text = re.sub('т\.п\.', 'тп', text)
        text = re.sub('т\. п\.', 'тп', text)
        text = re.sub('т\.к\.', 'тк', text)
        text = re.sub('т\. к\.', 'тк', text)
        text = re.sub('к\.т\.н\.', 'ктн', text)
        text = re.sub('к\. т\. н\.', 'ктн', text)
        text = re.sub(' .\.', '', text)
        text = re.sub(' \.', '.', text)
        input_text = text
        i = 0
        text = ''
        while i < len(input_text):
            if input_text[i:i + 2] == '  ':
                i += 1
            else:
                text += input_text[i]
                i += 1

        return text

    @staticmethod
    def spltText(input_text, type):
        # Разбивка теста сначала на предложения, затем на слова
        # input_text[1][0] - первое слово из второго предложения
        # type == 0 - разбивка по предложениям и словам
        # type == 1 - разбивка по предложениям
        list_input_text = input_text.split('. ')
        i = 0
        if type == 0:
            while i < len(list_input_text):
                if len(list_input_text[i]) == 0:
                    del list_input_text[i]
                    continue
                list_input_text[i] = list_input_text[i].split(' ')
                i += 1
        else:
            while i < len(list_input_text):
                if len(list_input_text[i]) == 0:
                    del list_input_text[i]
                    continue
                i += 1
        return list_input_text

    @staticmethod
    def getInfinitive(input_list):
        # На вход подается двумерный массив input_list, элементы которого - токены исходного текста
        # На выходе - тот же массив с приведенными к инфинитиву токенами
        res_list = []
        sentense = 0
        while sentense < len(input_list):
            sent = []
            for word in range(0, len(input_list[sentense])):
                sent += [ProcessingText.pymorphy.parse(input_list[sentense][word])[0].normal_form]
            sentense += 1
            res_list.append(sent)
        return res_list

    @staticmethod
    def dwnld_dictionaries(num):
        # Загрузка словаря.
        # На вход подается номер словаря,
        # Возвращается список, из списков слов расположенных с строках словаря
        path = r"dictionaries\base" + str(num) + '.csv'
        readFile = open(path, 'r')
        dictionary = readFile.read()
        readFile.close()
        dictionary = dictionary.split('\n')
        for i in range(len(dictionary)):
            if len(dictionary[i]) == 0:
                del dictionary[i]
                continue
            dictionary[i] = dictionary[i].split(',')
            j = 0
            while (dictionary[i][j] != '') and (j < len(dictionary[i])-1):
                j += 1
            dictionary[i] = dictionary[i][:j]
        return dictionary

    @staticmethod
    def get_pos(word):
        # Определение части речи
        # На вход подается текст
        # На выходе текст:
        # NOUN    имя существительное           [хомяк]
        # ADJF    имя прилагательное (полное)   [хороший]
        # ADJS    имя прилагательное (краткое)  [хорош]
        # COMP    компаратив                    [лучше, получше, выше]
        # VERB    глагол (личная форма)         [говорю, говорит, говорил]
        # INFN    глагол (инфинитив)            [говорить, сказать]
        # PRTF    причастие (полное)            [прочитавший, прочитанная]
        # PRTS    причастие (краткое)           [прочитана]
        # GRND    деепричастие                  [прочитав, рассказывая]
        # NUMR    числительное                  [три, пятьдесят]
        # ADVB    наречие                       [круто]
        # NPRO    местоимение-существительное   [он]
        # PRED    предикатив                    [некогда]
        # PREP    предлог                       [в]
        # CONJ    союз                          [и]
        # PRCL    частица                       [бы, же, лишь]
        # INTJ    междометие
        return ProcessingText.pymorphy.parse(word)[0].tag.POS

    @staticmethod
    def write_excel(count_words, i_stuff, i_islam, i_addiction, i_politic, i_christ, i_extremism, i_suicide):
        pass
