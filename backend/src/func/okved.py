#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_okved(data: dict) -> list:

    """ Получает список окведов"""

    activities_common = data.get("СвОКВЭД", {})
    main_activities = activities_common.get("СвОКВЭДОсн", [])
    add_activities = activities_common.get("СвОКВЭДДоп", [])

    # Если ОКВЭД один из выписки приходит словарь вместо списка
    if isinstance(main_activities, dict):
        main_activities = [main_activities]
    if isinstance(add_activities, dict):
        add_activities = [add_activities]

    activities = main_activities + add_activities

    activities_list = [
        f"{act.get("@attributes", "").get("КодОКВЭД", "")} - {act.get("@attributes", "").get("НаимОКВЭД", "")}" for act
        in activities
    ]
    return activities_list
