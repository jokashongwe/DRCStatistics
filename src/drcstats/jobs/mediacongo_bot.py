import json
import hashlib
import logging
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from src.drcstats.utils.simple_robot import SimpleRobot
from src.drcstats.utils.string_normalizations import strim_strip
from pathlib import Path


def page_parser(html_doc: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html_doc, "html.parser")
    table = soup.find("table", class_="table_datas")
    rows = table.find_all("tr")
    offer_list = []
    for row in rows:
        columns = row.find_all("td")
        if not columns or isinstance(columns, int):
            continue
        offer = {}
        for index, column in enumerate(columns):
            column_data = column.string
            match index:
                case 1:
                    offer[
                        "offer_url"
                    ] = f"https://www.mediacongo.net/{column.a['href']}"
                    offer["offer_name"] = column.a.strong.text
                case 2:
                    offer["offer_company_name"] = column_data
                case 3:
                    offer["offer_locations"] = strim_strip(column_data)
                case 4:
                    offer["offer_added_dt"] = column_data
        if offer:
            offer["offer_id"] = hashlib.md5(json.dumps(offer).encode()).hexdigest()
            offer_list.append(offer)
    return offer_list


def start():
    logging.basicConfig(level=logging.INFO)
    robot = SimpleRobot(
        source_name="mediacongo",
        page_url="https://www.mediacongo.net",
        url_format="https://www.mediacongo.net/emplois-titre--societe--page-{page_number}.html",
        max_pages=100,
        fn_parse_page=page_parser,
        path=Path("./generated"),
    )
    robot.start()


if __name__ == "__main__":
    start()
