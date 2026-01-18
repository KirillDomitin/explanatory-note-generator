import logging

import requests
import httpx

from func import get_address, get_ceo, get_charter_capital, get_okved, get_participants, get_registration_date, get_response
from settings import URL, HEADERS

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


async def explanatory_note(inn: int):
    logger.info(f"Запрос ИНН: {inn}")

    try:
        response = await get_response(URL.format(inn))
        response.raise_for_status()
    except httpx.HTTPError as e:
        raise ValueError(f"API вернул ошибку: {e}")

    try:
        result = response.json()
        logger.info(f"Ответ валидирован")
    except Exception as e:
        raise ValueError("Ответ API не является валидным JSON") from e

    try:
        common = result["СвЮЛ"]
    except KeyError:
        raise ValueError("В ответе API отсутствует блок 'СвЮЛ'") from None

    try:
        common_name = common["СвНаимЮЛ"]
        full_company_name = common_name["@attributes"]["НаимЮЛПолн"]
        short_company_name = common_name["СвНаимЮЛСокр"]["@attributes"]["НаимСокр"]
    except (KeyError, TypeError) as e:
        logger.error("Не удалось получить название компании — отсутствует или неверный формат блока 'СвНаимЮЛ'")
        raise ValueError(
            "Не удалось получить название компании — отсутствует или неверный формат блока 'СвНаимЮЛ'") from e

    try:
        registration_date = get_registration_date(common)
    except Exception as e:
        logger.error(f"Не удалось получить дату регистрации: {str(e)}")
        raise ValueError(f"Не удалось получить дату регистрации: {str(e)}") from e

    try:
        legal_address = get_address(common)
    except Exception as e:
        logger.error(f"Не удалось получить юридический адрес: {str(e)}")
        raise ValueError(f"Не удалось получить юридический адрес: {str(e)}") from e

    try:
        charter_capital = get_charter_capital(common)
    except Exception as e:
        logger.error(f"Не удалось получить уставный капитал: {str(e)}")
        raise ValueError(f"Не удалось получить уставный капитал: {str(e)}") from e

    try:
        participants = get_participants(common)
    except Exception as e:
        logger.error(f"Не удалось получить участников: {str(e)}")
        raise ValueError(f"Не удалось получить участников: {str(e)}") from e

    try:
        activities_list = get_okved(common)
    except Exception as e:
        logger.error(f"Не удалось получить список ОКВЭД: {str(e)}")
        raise ValueError(f"Не удалось получить список ОКВЭД: {str(e)}") from e

    try:
        ceos = get_ceo(common)
        if len(ceos) == 1:
            staff_administration = ""
        else:
            staff_administration = "1"
    except Exception as e:
        logger.error(f"Не удалось получить данные генерального директора: {str(e)}")
        raise ValueError(f"Не удалось получить данные генерального директора: {str(e)}") from e

    logger.info("Все поля успешно извлечены")
    return {
        "full_company_name": full_company_name,
        "short_company_name": short_company_name,
        "registration_date": registration_date,
        "legal_address": legal_address,
        "charter_capital": charter_capital,
        "participants": participants,
        "activities_list": activities_list,
        "ceos": ceos,
        "staff_administration": staff_administration
    }
