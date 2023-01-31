import vk_api
from my_data import MyVkData


class VkMethods:

    vk_session = vk_api.VkApi(login=MyVkData.LOGIN, password=MyVkData.GET_PASSWORD(), app_id=MyVkData.APP_ID, scope='wall, offline, friends, groups', api_version='5.131')
    vk_session.auth()

    vk = vk_session.get_api()

    def get_name(self, id):
        #принимает на вход один id и возвращает список [id, 'Имя Фамилия']
        result = []
        try:
            user = self.vk.users.get(user_ids=id)
        except Exception:
            return None
        else:
            name = user[0]['first_name'] + " " + user[0]['last_name']
            result += [user[0]['id']] + [name]
            return result

    def get_friends_list(self, id):
        #принимает на вход один id и выдает список id друзей пользователя
        friends = self.vk.friends.get(user_id=id)
        return friends['items']

    def get_groups_list(self, id):
        #принимает один id и возвращает список с id групп
        groups = self.vk.groups.get(user_id=id)
        return groups['items']



    def get_wall_message(self, ids, is_user=True, count=1):
        #принимает на вход - список id, по которым нужно пройти, is_user - для валидации
        #групп и пользователей
        #выдает на выходе список, состоящий из списка [id, str каждого сообщения]
        messages = []
        for one_id in ids:
            try:
                if is_user:
                    message = self.vk.wall.get(owner_id=one_id, count=count, filter='owner')
                else:
                    message = self.vk.wall.get(owner_id=one_id*(-1), count=count, filter='owner')
            except:
                Exception
            else:

                if message['items']:
                    for item in message['items']:
                        if item['text'] != '':
                            messages.append([one_id, item['text']])
        return messages

