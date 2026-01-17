#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from .moks import MOCK_RESPONSES
from ..servises.generate_explanatory_note import explanatory_note

# Добавляем корень backend в sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.mark.asyncio
async def test_explanatory_note_single_participant(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_RESPONSES[0]
    mock_response.raise_for_status = mocker.Mock()

    mock_get = AsyncMock(return_value=mock_response)
    mocker.patch("httpx.AsyncClient.get", mock_get)
    result = await explanatory_note(770101001)

    assert result is not None
    assert result == {'charter_capital': "15000 (пятнадцать тысяч) рублей.",
                      'legal_address': "125009,Г.Москва,Тверская ул,д.5/7,стр.2,подв. 3, помещ.vii, комн.12, офис 4б",
                      'full_company_name': 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ЗВЕЗДА ЛОГИСТИК"',
                      'ceo_name': "Генеральный Директор Общества: Соколов Алексей Петрович",
                      'activities_list': ['52.29 - Деятельность вспомогательная прочая, связанная с перевозками',
                                          '52.10 - Деятельность по складированию и хранению',
                                          '49.41 - Деятельность автомобильного грузового транспорта'],
                      'short_company_name': 'ООО "ЗВЕЗДА ЛОГИСТИК"',
                      'registration_date': '2015-06-22',
                      'participants': ['Соколов Алексей Петрович с долей 100 процентов;']
                      }

@pytest.mark.asyncio
async def test_explanatory_note_multi_participant(mocker):
    # Мокаем requests.get
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_RESPONSES[0]
    mock_response.raise_for_status = mocker.Mock()

    mock_get = AsyncMock(return_value=mock_response)
    mocker.patch("httpx.AsyncClient.get", mock_get)
    result = await explanatory_note(770101001)

    assert result is not None
    assert result["full_company_name"] == 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ЗВЕЗДА ЛОГИСТИК"'
    assert result["short_company_name"] == 'ООО "ЗВЕЗДА ЛОГИСТИК"'
    assert result["registration_date"] == '2015-06-22'
    assert result["legal_address"] == "125009,Г.Москва,Тверская ул,д.5/7,стр.2,подв. 3, помещ.vii, комн.12, офис 4б"
    assert result["charter_capital"] == "15000 (пятнадцать тысяч) рублей."
    assert result["participants"] == ['Соколов Алексей Петрович с долей 100 процентов;']
    assert result["activities_list"] == ['52.29 - Деятельность вспомогательная прочая, связанная с перевозками',
                                         '52.10 - Деятельность по складированию и хранению',
                                         '49.41 - Деятельность автомобильного грузового транспорта']
    assert result["ceo_name"] == "Генеральный Директор Общества: Соколов Алексей Петрович"
