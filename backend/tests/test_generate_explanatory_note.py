#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

from .moks import MOCK_RESPONSES
from ..servises.generate_explanatory_note import explanatory_note

# Добавляем корень backend в sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_explanatory_note_single_participant(mocker):
    # Мокаем requests.get
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_RESPONSES[0]
    mocker.patch("requests.get", return_value=mock_response)

    result = explanatory_note(770101001)

    assert result is not None
    assert result == {'charter_capital': '15000',
                      'legal_address': '125009,Г.Москва,Тверская ул,д.5/7,стр.2,3, ПОМЕЩ.VII, КОМН.12, ОФИС 4Б',
                      'full_company_name': 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ЗВЕЗДА ЛОГИСТИК"',
                      'ceo_name': 'Соколов Алексей Петрович',
                      'activities_list': ['52.29 - Деятельность вспомогательная прочая, связанная с перевозками',
                                          '52.10 - Деятельность по складированию и хранению',
                                          '49.41 - Деятельность автомобильного грузового транспорта'],
                      'short_company_name': 'ООО "ЗВЕЗДА ЛОГИСТИК"',
                      'registration_date': '2015-06-22',
                      'participants': ['Соколов Алексей Петрович с долей 100 процентов;']
                      }


def test_explanatory_note_multi_participant(mocker):
    # Мокаем requests.get
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_RESPONSES[1]
    mocker.patch("requests.get", return_value=mock_response)

    result = explanatory_note(770101001)

    assert result is not None
    assert result["full_company_name"] == 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ЗВЕЗДА ЛОГИСТИК"'
    assert result["short_company_name"] == 'ООО "ЗВЕЗДА ЛОГИСТИК"'
    assert result["registration_date"] == '2015-06-22'
    assert result["legal_address"] == '125009,Г.Москва,Тверская ул,д.5/7,стр.2,3, ПОМЕЩ.VII, КОМН.12, ОФИС 4Б'
    assert result["charter_capital"] == '15000'
    assert result["participants"] == ['Соколов Алексей Петрович с долей 70 процентов;',
                                      'Волкова Марина Ивановна с долей 30 процентов;']
    assert result["activities_list"] == ['52.29 - Деятельность вспомогательная прочая, связанная с перевозками',
                                         '52.10 - Деятельность по складированию и хранению',
                                         '49.41 - Деятельность автомобильного грузового транспорта']
    assert result["ceo_name"] == 'Соколов Алексей Петрович'
