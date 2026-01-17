#!/usr/bin/python
# -*- coding: utf-8 -*-

ceo_dict = {
    "ликвидатор": "Ликвидатор общества",
    "генеральный": "Генеральный директор общества",
    "генеральный директор": "Генеральный директор общества",
}

def get_ceo(data: dict)-> str:

    """ Получает генерального директора """

    ceo_name_common = data.get("СведДолжнФЛ", {})
    ceo_name = ceo_name_common.get("СвДолжн", {}).get("@attributes", {}).get("НаимДолжн", "").strip().lower()
    ceo = ceo_dict[ceo_name]
    name = ceo_name_common.get("СвФЛ").get("@attributes").get("Имя", "")
    surname = ceo_name_common.get("СвФЛ").get("@attributes").get("Фамилия", "")
    patronymic = ceo_name_common.get("СвФЛ").get("@attributes").get("Отчество", "")
    return f"{ceo}: {surname} {name} {patronymic}".title()