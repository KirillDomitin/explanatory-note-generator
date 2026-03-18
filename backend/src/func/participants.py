#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_participants(data: dict) -> list:

    """ Получаем учередителей с долей уставного капитала """

    participants_list = []
    participants_common = data["СвУчредит"]
    participants_fl = participants_common.get("УчрФЛ", [])
    participants_ul = participants_common.get("УчрЮЛРос", [])
    if not isinstance(participants_fl, list):
        participants_fl = [participants_fl]

    if not isinstance(participants_ul, list):
        participants_ul = [participants_ul]

    for participant in participants_fl:
        name = participant.get("СвФЛ").get("@attributes", {}).get("Имя", "")
        surname = participant.get("СвФЛ").get("@attributes", {}).get("Фамилия", "")
        patronymic = participant.get("СвФЛ").get("@attributes", {}).get("Отчество", "")
        stock_share = participant.get("ДоляУстКап", {}).get("РазмерДоли", {}).get("Процент", "")
        full_name = " ".join([surname, name, patronymic]).title()
        participants_list.append("{} с долей {} процентов;".format(full_name, stock_share))

    for participant in participants_ul:
        name = participant.get("НаимИННЮЛ", {}).get("@attributes", {}).get("НаимЮЛПолн")
        stock_share = participant.get("ДоляУстКап", {}).get("РазмерДоли", {}).get("Процент", "")
        participants_list.append("{} с долей {} процентов;".format(name, stock_share))
    return participants_list