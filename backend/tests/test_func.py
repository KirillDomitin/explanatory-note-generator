#!/usr/bin/python
# -*- coding: utf-8 -*-

import func
from .moks import MOCK_RESPONSES

common_data = MOCK_RESPONSES[0]["СвЮЛ"]


def test_address_success():
    result = func.get_address(common_data)
    assert result == '125009,Г.Москва,Тверская ул,д.5/7,стр.2,3, ПОМЕЩ.VII, КОМН.12, ОФИС 4Б'


def test_ceo_success():
    result = func.get_ceo(common_data)
    assert result == 'Соколов Алексей Петрович'


def test_charter_capital_success():
    result = func.get_charter_capital(common_data)
    assert result == '15000'


def test_charter_capital_okved():
    result = func.get_okved(common_data)
    assert result == ['52.29 - Деятельность вспомогательная прочая, связанная с перевозками',
                      '52.10 - Деятельность по складированию и хранению',
                      '49.41 - Деятельность автомобильного грузового транспорта']


def test_charter_single_participants():
    result = func.get_participants(common_data)
    assert result == ['Соколов Алексей Петрович с долей 100 процентов;']


def test_charter_multi_participants():
    result = func.get_participants(MOCK_RESPONSES[1]['СвЮЛ'])
    assert result == ['Соколов Алексей Петрович с долей 70 процентов;',
                      'Волкова Марина Ивановна с долей 30 процентов;']

def test_registration_date():
    result = func.get_registration_date(common_data)
    assert result == '2015-06-22'
