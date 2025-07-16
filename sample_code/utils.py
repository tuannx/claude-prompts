
import json
import datetime

def format_date(date):
    return date.strftime("%Y-%m-%d")

def parse_json(json_str):
    return json.loads(json_str)

def calculate_discount(price, discount_percent):
    return price * (1 - discount_percent / 100)
