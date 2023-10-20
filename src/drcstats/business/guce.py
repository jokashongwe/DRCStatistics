import requests
import os
from pathlib import Path
import time
import json
from typing import List, Dict, TextIO
from src.drcstats.utils.string_normalizations import strim_strip
import progressbar
import hashlib


def write_file_to_json(records: List[Dict], filename) -> None:
    with open(filename, "a+") as file:
        for rec in records:
            file.write(
                json.dumps(rec)
                .encode("utf-8", errors="ignore")
                .decode("utf-8")
                + "\n"
            )


def get_companies():
    total = 18478
    rows = 100
    n_pages = int(total / rows) + 1
    url = "https://guichetunique.cd/api/all"
    company_destination_filename = str(
        Path(
            os.path.join(
                os.getcwd(),
                "generated",
                f"produced_guce_company_1697794472.json",
            )
        )
    )
    raw_company_filename = company_destination_filename.replace(
        "company", "raw_company"
    )
    processing_progress_bar = progressbar.ProgressBar(max_value=n_pages)
    processing_progress_bar.widgets = (
        ["processing pages: "]
        + [progressbar.widgets.FileTransferSpeed(unit="pages"), " "]
        + processing_progress_bar.default_widgets()
    )
    processing_progress_bar.start()
    for page in range(158, 185):
        request = requests.get(f"{url}/{page+1}", auth=("admin", "@pi_GUCE_pub"))
        if f"{request.status_code}" == "200":
            company_data = request.json()
            raw_companies = company_data.get("societes")
            write_file_to_json(records=raw_companies, filename=raw_company_filename)
            companies = []
            contacts = []
            for raw_company in raw_companies:
                contact = {
                    "contact_name": raw_company.get("dirigeant").split(",")[0],
                    "contact_birthday": raw_company.get("dirigeant").split(",")[1] if ',' in raw_company.get("dirigeant") else None,
                    "contact_phones": [],
                    "contact_email": None,
                    "contact_role": raw_company.get("fonction"),
                    "contact_address": raw_company.get("adresseDirigeant"),
                }
                contact["contact_id"] = hashlib.md5(
                    json.dumps(contact).encode("utf-8")
                ).hexdigest()
                company = {
                    "company_legal_name": raw_company.get("denominationSociale"),
                    "company_alternative_name": raw_company.get("sigle"),
                    "company_city": None,
                    "company_state": raw_company.get("site").replace("\\/", " ").split(" ")[1] if raw_company.get("site") else  None,
                    "company_sectors": strim_strip(raw_company.get("objetSocial")) if raw_company.get("objetSocial") else None,
                    "company_address": raw_company.get("adresseSiegeSocial"),
                    "company_domain": None,
                    "company_capital": raw_company.get("capitalSocial"),
                    "company_contact": contact,
                }
                company["company_id"] = hashlib.md5(
                    json.dumps(contact).encode("utf-8")
                ).hexdigest()
                contacts.append(contact)
                companies.append(company)
            write_file_to_json(records=companies, filename=company_destination_filename)
            write_file_to_json(
                records=contacts,
                filename=company_destination_filename.replace("company", "contact"),
            )
        processing_progress_bar.update(page + 1)
    processing_progress_bar.finish()


if __name__ == "__main__":
    get_companies()
