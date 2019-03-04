import bs4 as bs
import requests

API_key = "9ce9667447c7fe8f909b2464236be5ca"


def prettify_str(str_to_prettify):
    return str_to_prettify.rstrip().replace(u'\xa0', u' ')


def get_menus():
    menus = {}
    restaurants = {"kandelabr": "16506739", "arrosto": "16506695", "smrtak": "16507270"}

    for name, id in restaurants.items():
        src = requests.get(f"https://developers.zomato.com/api/v2.1/dailymenu?res_id={id}",
                           headers={'user_key': API_key})
        menus[name] = [] if len(src.json()["daily_menus"]) == 0 else src.json()["daily_menus"][0]["daily_menu"]["dishes"]
    return menus


def get_kandelabr():
    data = get_menus()
    kandelabr = []
    for dish in data["kandelabr"]:
        kandelabr.append(
            {"name": prettify_str(dish['dish']['name']), "price": prettify_str(str(dish['dish']['price']))})
    return kandelabr


def get_smrtak():
    data = get_menus()
    smrtak = []
    for dish in data["smrtak"]:
        name = dish['dish']['name']
        if "Polévky" in name or "Menu" in name or "Váha" in name or "Hlavní" in name:
            continue
        smrtak.append({"name": prettify_str(name), "price": prettify_str(str(dish['dish']['price']))})
    return smrtak


def get_arrosto():
    data = get_menus()
    arrosto = []
    for dish in data["arrosto"]:
        name = dish['dish']['name']
        if "POLÉVKY" in name or "HLAVNÍ" in name or "TIP" in name or "PIZZA" in name or "DEZERT" in name or \
                "STÁLÁ" in name or "SPECIÁL" in name or "ZELENINOVÉ" in name:
            continue
        arrosto.append({"name": prettify_str(name), "price": prettify_str(str(dish['dish']['price']))})
    return arrosto


def get_v_case():
    # V case scraping
    v_case_req = requests.get("http://www.restauracevcase.cz/cz/poledni-menu")
    # fix encoding
    v_case_req.encoding = v_case_req.apparent_encoding
    v_case_soup = bs.BeautifulSoup(v_case_req.text, "lxml")
    v_case_table = v_case_soup.find_all("table", class_="jidla")
    soups = []
    meals = []
    for i, table in enumerate(v_case_table[:-3]):
        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) == 0:
                continue
            if i == 0:
                soups.append({"name": tds[0].text, "price": tds[2].text})
            else:
                meals.append(
                    {"name": str(tds[0].text).replace("\t", " "), "price": str(tds[2].text).replace(u'\xa0', u' ')})
    return soups + meals
