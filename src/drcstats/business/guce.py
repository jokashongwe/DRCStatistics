import requests
import os
from pathlib import Path
import time
import json
from typing import List, Dict
from src.drcstats.utils.string_normalizations import strim_strip
import progressbar
import hashlib

COMPANY_SECTORS_KEY = [
    "Mine","mines","Minier", "Minière", "Informatique","Beauté", "Importation", "Import", "Placement", "Sous-traitance", 
    "Cosmétique", "Massage", "Logiciel", "Logiciels", "Agriculture", "élevage", "Foresterie", "Agro-foresterie",
    "Cuivre", "Cobalt", "Coltan", "Conseil", "Finance", "Banque", "Télécommunication","Fôret","bois","Alcool", "Bar",
    "Micro-finance", "Téléphonie", "Internet", "Réseaux","Paie", "Commerce","Mobile", "Transport",
    "Location", "Service", "Assistance", "Recherche", "Architecture", "Construction", "Bâtiment",
    "Sport","Fitness", "Maquillage", "épillation", "Coiffure", "Club", "Equipements","électricité","Mécanique","réfection"
    "Fourniture", "Livraison", "Restaurant","Restauration", "Cuisine", "Ménager","nettoyage","Cleaning", "Réparation",
    "Photographie", "Humour", "Spectacle", "Cinéma", "Art","Culture", "Formation","éducation", "Comptable", "Comptabilité"
    "Fiscalité", "Gestion", "Export", "Fret", "Voyage","Tourisme","Train","Avion","Aviation","protection",
    "Communication", "Pêche","Immobilier","Immo","Sécurité","gardiennage","Cabinet","Avocat","Assurrance", "Crédit",
    "Consultation","Laboratoire", "Analyse", "Médicale","Pharmaceutique", "Pharmaceutiques", "Médicaments","apprentissage","Transfert",
    "Importation","Exportation","distribution","alimentaires","production", "transformation", "commercialisation","chips"
]

def write_file_to_json(records: List[Dict], filename) -> None:
    with open(filename, "a+", encoding="utf-8") as file:
        for rec in records:
            file.write(
                json.dumps(rec, ensure_ascii=False)
                + "\n"
            )


def get_companies():
    total = 20000
    rows = 100
    n_pages = int(total / rows) + 1
    url = "https://guichetunique.cd/api/all"
    company_destination_filename = str(
        Path(
            os.path.join(
                os.getcwd(),
                "generated",
                f"produced_guce_company_{int(time.time())}.json",
            )
        )
    )
    raw_company_filename = company_destination_filename.replace(
        "company", "raw_company"
    )
    processing_progress_bar = progressbar.ProgressBar(max_value=total, min_value=0)
    processing_progress_bar.widgets = (
        ["processing pages: "]
        + [progressbar.widgets.FileTransferSpeed(unit="pages"), " "]
        + processing_progress_bar.default_widgets()
    )
    processing_progress_bar.start()
    with open("C:\\Users\\jonathan\\workspace\\DRCStatistics\\generated\\produced_guce_raw_company_1697794472.json", encoding="utf-8") as file:
        for line in file.readlines() :
            #request = requests.get(f"{url}/{page+1}", auth=("admin", "@pi_GUCE_pub"))
            if True:
                try:
                    company_data = json.loads(line)
                except:
                    print("error line: ", processing_progress_bar.value)
                    continue
                raw_companies = [company_data]
                # write_file_to_json(records=raw_companies, filename=raw_company_filename)
                companies = []
                contacts = []
                for raw_company in raw_companies:
                    objet_social = raw_company.get("objetSocial") if raw_company.get("objetSocial") else ""
                    objet_social = objet_social.lower().replace(" ",",").replace(";",",").split(",")
                    sectors = [ sector for sector in COMPANY_SECTORS_KEY if sector.lower() in objet_social ]
                    city = f"{raw_company.get("site")}".split("/")[0]
                    city = city.split(" ")[1] if " " in city else city
                    revenue_cdf = raw_company.get("capitalSocial").replace("CDF", "").strip() if raw_company.get("capitalSocial") else "0"
                    revenue = 0
                    try:
                        revenue_cdf = int(revenue_cdf)
                        revenue  = revenue_cdf / 1600
                    except:
                        revenue_cdf = None
                        revenue = 0
                    
                    if revenue > 1000000:
                        category = "A" # More than 1 Million
                    elif revenue > 100000:
                        category = "B" # More than 100 Thousands
                    elif revenue > 10000:
                        category = "C"
                    else:
                        category = "D"
                    company = {
                        "company_legal_name": raw_company.get("denominationSociale"),
                        "company_alternative_name": raw_company.get("sigle"),
                        "company_city": city,
                        "company_state": None,
                        "company_description": raw_company.get("objetSocial"),
                        "company_sectors": sectors, 
                        "company_address": raw_company.get("adresseSiegeSocial"),
                        "company_category": category,
                        "company_domain": None,
                        "company_capital": f'{revenue_cdf} CDF' if revenue > 0 else None,
                        "company_legal_form": raw_company.get("formeJuridique"),
                        "company_creation_date": raw_company.get("dateImmatriculationRCCM"),
                        "company_rccm": raw_company.get("rccm"),
                        "company_tax_number": raw_company.get("idnat")
                    }
                    company["company_id"] = hashlib.md5(
                        f"{raw_company.get('entityId')}".encode("utf-8")
                    ).hexdigest()
                    contact_birthday = f"{raw_company.get("dirigeant").split(",")[1]}".strip() if ',' in raw_company.get("dirigeant") else ""
                    contact_birthday = contact_birthday.replace("né(e) le", "")
                    contact = {
                        "contact_name": raw_company.get("dirigeant").split(",")[0],
                        "contact_birthday": f"{contact_birthday.split("à")[0]}".strip(),
                        "contact_phones": [],
                        "contact_email": None,
                        "contact_nationality": f"{raw_company.get("dirigeant").split(",")[-1]}".strip() if ',' in raw_company.get("dirigeant") else None,
                        "contact_role": raw_company.get("fonction"),
                        "contact_address": raw_company.get("adresseDirigeant"),
                        "contact_company_id": company["company_id"],
                    }
                    contact["contact_id"] = hashlib.md5(
                        json.dumps(contact).encode("utf-8")
                    ).hexdigest()
                    contacts.append(contact)
                    companies.append(company)
                write_file_to_json(records=companies, filename=company_destination_filename)
                write_file_to_json(
                    records=contacts,
                    filename=company_destination_filename.replace("company", "contact"),
                )
            processing_progress_bar.update(processing_progress_bar.value + 1)
    processing_progress_bar.finish()


if __name__ == "__main__":
    get_companies()
