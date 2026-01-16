#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_address(data: dict) -> str:
    """ Получает юридический адрес из выписки """

    parts = []
    common_address = data.get("СвАдресЮЛ", {}).get("СвАдрЮЛФИАС", {})
    if common_address:
        mail_index = common_address.get("@attributes", {}).get("Индекс", "")
        city = common_address.get("НаимРегион", "").title()
        street_name = common_address.get("ЭлУлДорСети", {}).get("@attributes", {}).get("Наим", "").title()
        street_type = common_address.get("ЭлУлДорСети", {}).get("@attributes", {}).get("Тип", "").lower()
        street = " ".join([street_name, street_type])

        parts.append(mail_index)
        parts.append(city)
        parts.append(street)

        building_parts = common_address.get("Здание", [])
        for part in building_parts:
            building_name = part.get("@attributes").get("Номер", "").lower()
            building_type = part.get("@attributes", {}).get("Тип", "").lower()
            building = "".join([building_type, building_name])
            parts.append(building)

        office = common_address.get("ПомещЗдания", {}).get("@attributes", {}).get("Номер", "")
        if office:
            parts.append(office)
    else:
        common_address = data.get("СвАдресЮЛ", {}).get("АдресРФ", "")
        mail_index = common_address.get("@attributes").get("Индекс")
        city = common_address.get("Регион", {}).get("@attributes", {}).get("НаимРегион", "").title()
        street_name = common_address.get("Улица", {}).get("@attributes", {}).get("НаимУлица", "").title()
        street_type = common_address.get("Улица", {}).get("@attributes", {}).get("ТипУлица", "").lower()
        street = " ".join([street_name, street_type])
        building_name = common_address.get("@attributes", {}).get("Дом", "").lower()
        building_room = common_address.get("@attributes", {}).get("Кварт", "").lower()
        building_structure = common_address.get("@attributes", {}).get("Корпус", "").lower()
        building = ",".join([building_name, building_structure, building_room])
        parts.append(mail_index)
        parts.append(city)
        parts.append(street)
        parts.append(building)

    result = ",".join(parts)
    return result
