#!/usr/bin/python
# -*- coding: utf-8 -*-
from num2words import num2words

def get_charter_capital(data: dict)-> str:
    number = data.get("СвУстКап", {}).get("@attributes").get("СумКап", "")
    num2word = num2words(number, lang="ru")
    return f"{number} ({num2word}) рублей."