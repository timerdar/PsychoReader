from new_vk_methods import VkMethods
from text_methods import ProcessingText
from psycho_methods import PsychoReader


def local_test(users_ids):
    #анализ текста постов пользователя
    vk = VkMethods()
    out = [[],'']
    for user_id in users_ids:
        user = vk.get_name([user_id])
        messages = vk.get_wall_message([user[0]], count=100)
        rep = analyse(messages)
        s = (result(rep, user[1], user[0]))
        out[0] += [rep + [user[1]] + ['https://vk.com/'+user_id]]
        out[1] += s + '\n'
    return out
#    print("Анализ закончен")


def full_test(users_ids):
    #анализ стен друзей и постов групп пользователя
    #выполняется долго, т.к. для каждого ид(группы и друзья) отправляется запрос через апи(долго)
    vk = VkMethods()
    out = [[],'']
    for user_id in users_ids:
        user = vk.get_name([user_id])
        friends = vk.get_friends_list(user[0])
        groups = vk.get_groups_list(user[0])
        all_users = [user[0]] + friends
        messages = vk.get_wall_message(all_users) + vk.get_wall_message(groups, is_user=False)
        rep = analyse(messages)
        s = result(rep, user[1], user[0])
        out[0] += [rep + [user[1]] + ['https://vk.com/'+user_id]]
        out[1] += s + '\n'
    return out


def analyse(list_of_messages):
    report = []
    text = ''
    for wall_message in list_of_messages:
        temp_text = str(wall_message[1]).replace('<br>', '\n').replace('\n\n', '\n')
        text += temp_text + '\n\n'
    temp_text_0 = ProcessingText.clrText(text, 0)
    temp_text_0 = ProcessingText.spltText(temp_text_0, 0)
    temp_text_1 = ProcessingText.clrText(text, 1)
    temp_text_1 = ProcessingText.spltText(temp_text_1, 1)
    try:
        report.append(len(PsychoReader.effect02(temp_text_1)))
        report.append(len(PsychoReader.effect03(temp_text_1)))
        report.append(len(PsychoReader.effect04(temp_text_0)))
        report.append(len(PsychoReader.effect01(ProcessingText.getInfinitive(temp_text_0))))
        report.append(PsychoReader.direction(text))
        report.append(len(PsychoReader.effect05(temp_text_0)))
    except Exception:
        pass
    return report


def result(report_1, name, user_id):
    totals = ''
    totals += '\n-----------' + name + ' (id - ' + str(user_id) + ')' + '-----------\n'
    totals += "Найдено:\n"
    totals += "- " + str(report_1[0]) + " предложений(-ие) c манипулятивным комментировнием\n"
    totals += "- " + str(report_1[1]) + " предложений(-ие) c ссылкой на авторитет\n"
    totals += "- " + str(report_1[2]) + " предложений(-ие) c гиперболизацие\n"
    totals += "- " + str(report_1[3]) + " предложений(-ие) c искусственным контрастом\n"
    totals += "- " + str(report_1[5]) + " предложений(-ие) c призывом к действию\n"
    totals += "\n............\n\n"
    if report_1[4][0] > 0:
        totals += 'Направленность страницы(в процентах):\n'
        totals += 'Вещества: ' + str(round(report_1[4][1]*100/report_1[4][0], 2)) + '%\n'
        totals += 'Ислам: ' + str(round(report_1[4][2]*100/report_1[4][0], 2)) + '%\n'
        totals += 'Наркомания: ' + str(round(report_1[4][3]*100/report_1[4][0], 2)) + '%\n'
        totals += 'Политика: ' + str(round(report_1[4][4]*100/report_1[4][0], 2)) + '%\n'
        totals += 'Христианство: ' + str(round(report_1[4][5]*100/report_1[4][0], 2)) + '%\n'
        totals += 'Экстримизм: ' + str(round(report_1[4][6]*100/report_1[4][0], 2)) + '%\n'
        totals += 'Суицид: ' + str(round(report_1[4][7]*100/report_1[4][0], 2)) + '%\n'
    else:
        totals += 'направленности страницы определить не удалось, т.к. отсутствуют доступные записи на ' \
                  'стене пользователя.'
    return totals