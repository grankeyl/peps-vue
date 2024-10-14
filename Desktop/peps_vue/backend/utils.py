from datetime import datetime
import json, random

def get_now_date():
    return datetime.now().strftime("%d-%m-%y %H:%M:%S")

def get_now_date_without_time():
    return datetime.now().strftime("%d-%m-%y")

def generate_referal_key() -> str:
    chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    key = ""

    for _ in range(9):
        key += random.choice(chars)

    return str(key)


class Skin:
    
    def __init__(self, skin_id: str):
        self.skin_id = skin_id
        self.category = self.__get_category()

        self.__data = None

    def __get_category(self):
        with open('./../skinsArray.json', 'r', encoding='utf-8') as json_file:
            self.__data = json.load(json_file)
        
        for category, items in self.__data.items():
            if self.skin_id in self.__data[category]['versions']:
                self.category = category
                return category

    def as_dict(self) -> dict:
        try:
            if self.__data is None or self.category is None:
                self.__get_category()

            skin = self.__data[self.category]['versions'][self.skin_id]
            return skin
        except:
            print("Not founded - ", self.skin_id)

    def category_dict(self) -> dict:
        if self.__data:
            return self.__data[self.category]
        else:
            self.__get_category()
            return self.__data[self.category]

