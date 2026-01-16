#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_ceo(data: dict)-> str:

    """ Получает генерального директора """

    ceo_name_common = data.get("СведДолжнФЛ", {}).get("СвФЛ", {}).get("@attributes")
    name = ceo_name_common.get("Имя")
    surname = ceo_name_common.get("Фамилия")
    patronymic = ceo_name_common.get("Отчество", "")
    return f"{surname} {name} {patronymic}".title()