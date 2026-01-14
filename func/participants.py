#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_participants(data: dict) -> list:

    """ Получаем учередителей с долей уставного капитала """

    participants_list = []
    participants_common = data["СвУчредит"]
    participants = participants_common.get("УчрФЛ", [])
    if not isinstance(participants, list):
        participants = [participants]

    for participant in participants:
        name = participant.get("СвФЛ").get("@attributes", {}).get("Имя", "")
        surname = participant.get("СвФЛ").get("@attributes", {}).get("Фамилия", "")
        patronymic = participant.get("СвФЛ").get("@attributes", {}).get("Отчество", "")
        stock_share = participant.get("ДоляУстКап", {}).get("РазмерДоли", {}).get("Процент", "")
        full_name = " ".join([surname, name, patronymic]).title()
        participants_list.append("{} с долей {} процентов;".format(full_name, stock_share))

    return participants_list