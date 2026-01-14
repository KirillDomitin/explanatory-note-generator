#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_registration_date(data: dict)-> str:
    return data.get("@attributes", {}).get("ДатаОГРН", "")