#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

from .moks import MOCK_RESPONSES
from ..func import get_address, get_ceo, get_charter_capital, get_okved, get_participants, get_registration_date

# Добавляем корень backend в sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

common_data = MOCK_RESPONSES[0]["СвЮЛ"]


def test_address_success():
    result = get_address(common_data)
    assert result == "125009,Г.Москва,Тверская ул,д.5/7,стр.2,подв. 3, помещ.vii, комн.12, офис 4б"


def test_ceo_success():
    result = get_ceo(common_data)
    assert result == "Генеральный Директор Общества: Соколов Алексей Петрович"


def test_charter_capital_success():
    result = get_charter_capital(common_data)
    assert result == "15000 (пятнадцать тысяч) рублей."


def test_charter_capital_okved():
    result = get_okved(common_data)
    assert result == ['52.29 - Деятельность вспомогательная прочая, связанная с перевозками',
                      '52.10 - Деятельность по складированию и хранению',
                      '49.41 - Деятельность автомобильного грузового транспорта']


def test_charter_single_participants():
    result = get_participants(common_data)
    assert result == ['Соколов Алексей Петрович с долей 100 процентов;']


def test_charter_multi_participants():
    result = get_participants(MOCK_RESPONSES[1]['СвЮЛ'])
    assert result == ['Соколов Алексей Петрович с долей 70 процентов;',
                      'Волкова Марина Ивановна с долей 30 процентов;']


def test_registration_date():
    result = get_registration_date(common_data)
    assert result == '2015-06-22'
