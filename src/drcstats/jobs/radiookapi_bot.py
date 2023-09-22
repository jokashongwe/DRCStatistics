import json
import hashlib
import logging
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from src.drcstats.utils.simple_robot import SimpleRobot
from src.drcstats.utils.string_normalizations import strim_strip


def is_location(text: str):
    text = text.lower()
    return "location" in text or "localisation" in text or "affectation" in text


def prep_text(text):
    return text.replace(".", " ").replace("\n", " ")


def page_parser(html_doc: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html_doc, "html.parser")
    table = soup.find("div", class_="view-offres-d-emploi")
    content = table.find("div", class_="view-content")
    rows = content.find_all("div", class_="views-row")
    offers = []
    for row in rows:
        offer = {}
        if row:
            title = row.find("div", class_="views-field-title")
            body = row.find("div", class_="views-field-body")
            ps = body.find_all("p")
            texts = [p.string for p in ps]
            locations = []
            for text in texts:
                if text and is_location(text):
                    text = text.strip()
                    split_text = text.split(":")
                    if len(split_text) < 2:
                        continue
                    locations = strim_strip(split_text[1])
            added = row.find("div", class_="views-field-created")
            added_dt = added.span.string
            added_dt = added_dt.replace("/", ".").split("-")[0].strip()
            _title = title.h2.a.string
            _split_title = []
            job_name = ""
            job_company = ""
            if ":" in _title:
                _split_title = _title.split(":")
                job_name = prep_text(_split_title[1])
                job_company = prep_text(_split_title[0])
            elif "," in _title:
                _split_title = _title.split(",")
                job_name = prep_text(_split_title[0])
                job_company = prep_text(_split_title[1])
            else:
                job_name = prep_text(_title)
                job_company = prep_text(_title)

            if job_name.count(",") > 2:
                names = job_name.split(",")
                for name in names:
                    offer = {}
                    offer[
                        "offer_url"
                    ] = f"https://www.radiookapi.net{title.h2.a['href']}"
                    offer["offer_title"] = name.strip()
                    offer["offer_company_name"] = job_company.strip()
                    offer["offer_locations"] = {"cities": locations}
                    offer["offer_added_dt"] = added_dt
                    offer["offer_id"] = hashlib.md5(
                        json.dumps(offer).encode()
                    ).hexdigest()
                    offers.append(offer)
            else:
                offer["offer_url"] = f"https://www.radiookapi.net{title.h2.a['href']}"
                offer["offer_title"] = job_name.strip()
                offer["offer_company_name"] = job_company.strip()
                offer["offer_locations"] = {"cities": locations}
                offer["offer_added_dt"] = added_dt
                offer["offer_id"] = hashlib.md5(json.dumps(offer).encode()).hexdigest()
                offers.append(offer)
    return offers


def start():
    logging.basicConfig(level=logging.INFO)
    robot = SimpleRobot(
        source_name="radiookapi",
        page_url="https://www.radiookapi.net",
        url_format="https://www.radiookapi.net/offres-demploi/page/280?page={page_number}",
        max_pages=289,
        fn_parse_page=page_parser,
        path="out/",
    )
    robot.start()


if __name__ == "__main__":
    start()
