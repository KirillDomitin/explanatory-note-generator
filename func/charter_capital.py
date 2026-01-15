#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_charter_capital(data: dict)-> str:
    return data.get("СвУстКап", {}).get("@attributes").get("СумКап", "")