from duckduckgo_search import DDGS
import time
import json
import psycopg2
from typing import List, Dict
from src.drcstats.utils.upload import upload_contact_parsed
from requests import request
from pathlib import Path
from src.drcstats.utils.universal_scrapper import universal_parser

COMPANY_SECTORS_KEY = [
    "Mining", "Technology", "Beauty", "Import", "Placement", "Consulting", 
    "Cosmetics", "Massage", "Software", "Agriculture", "Livestock", "Forestry", "Agro-forestry",
    "Copper", "Cobalt", "Coltan", "Consulting", "Finance", "Banking", "Telecommunication", "Forest", "Wood", "Alcohol", "Bar",
    "Micro-finance", "Telephony", "Internet", "Networks", "Payroll", "Trade", "Mobile", "Transport",
    "Rental", "Service", "Assistance", "Research", "Architecture", "Construction", "Building",
    "Sport", "Fitness", "Make-up", "Depilation", "Hairdressing", "Club", "Equipment", "Electricity", "Mechanics", "Repair",
    "Supply", "Delivery", "Restaurant", "Catering", "Kitchen", "Household", "Cleaning", "Repair",
    "Photography", "Humor", "Entertainment", "Cinema", "Art", "Culture", "Training", "Education", "Accountant", "Accounting",
    "Tax", "Management", "Export", "Freight", "Travel", "Tourism", "Train", "Plane", "Aviation", "Protection",
    "Communication", "Fishing", "Real Estate", "Immo", "Security", "Guarding", "Cabinet", "Lawyer", "Assurrance", "Credit",
    "Consultation", "Laboratory", "Analysis", "Medical", "Pharmaceutical", "Pharmaceuticals", "Medicines", "Apprenticeship", "Transfer",
    "Import", "Export", "Distribution", "Food", "Production", "Processing", "Marketing", "Chips", "Developer",
    "CVM", "CVS", "CEO", "Geologist", "Geographer", "Pastor", "Animator", "Trainer", "Professor", "Engineer"
]


def is_person(result: str, company:str):
    name  = result.split("|")[0]
    no_space_company = company.replace(" ", "")
    return "-" in name and name != company and no_space_company != name

def company_in_string(value: str, company: str):
    company = company.lower()
    no_space_company = company.replace(" ", "")
    value = value.lower()
    return company in value or no_space_company in value

def write_file_to_json(records: List[Dict], filename) -> None:
    with open(filename, "a+", encoding="utf-8") as file:
        for rec in records:
            file.write(
                json.dumps(rec, ensure_ascii=False)
                + "\n"
            )

def process_linkedin(dbname: str) -> List[str]:
    filename  = f"generated/process_linkedin_contacts_{int(time.time())}.json"
    conn = psycopg2.connect(f"dbname={dbname} user=konnect password=secret123")
    curr = conn.cursor()
    query = f"SELECT company_id, company_legal_name  FROM companies order by company_legal_name;"
    curr.execute(query)
    for sector in COMPANY_SECTORS_KEY:
        try:
            contacts = search_linkedin(company_id=None, company=sector)
            if len(contacts) <= 0:
                continue
            upload_contact_parsed(cur=curr, contacts=contacts, conn=conn)
        except:
            continue
    curr.close()
    conn.close()

def companies_scrap(sectors: list):
    path = 'Raw/african_countries_list.txt'
    with open(path, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            print("Country: ", line, end=" ")
            with DDGS() as ddgs:
                for sector in sectors:
                    keyword = f"list of {sector} company in {line}".strip()
                    results = [
                        r.get('href')
                        for r in ddgs.text(keyword, max_results=10)
                        if 'list' in r.get('title').lower() and 'wiki' not in r.get('href')
                    ]
                    for result in results:
                        print(" Link: ", result)
                        response = request(url=result, method="GET")
                        if response.status_code > 201:
                            continue
                        text = response.text
                        if "<table>" not in text:
                            continue
                        filename = int(time.time())
                        file_path = Path(f'generated/{line.lower()}/{line}_{filename}.json')
                        universal_parser(text=text, filename=file_path)

def search_linkedin(company_id:str, company:str):
    with DDGS() as ddgs:
        results = [
            r
            for r in ddgs.text(f"{company} rdc linkedin", max_results=50)
            if is_person(r.get("title"), company=company)
            and (company_in_string(value=r.get("title"), company=company) or company_in_string(value=r.get("body"), company=company))
        ]
        contacts = [
            {
                "contact_name": r.get("title").split("-")[0].strip()[:255],
                "contact_linkedin_url": r.get("href")[:255],
                "contact_role": r.get("title").split("-")[1].strip()[:255],
                "contact_email": None,
                "contact_nationality": None,
                "contact_phones": None,
                "contact_birthday": None,
                "contact_address": None,
                "contact_company_id": company_id
            }
            for r in results
        ]
        print(f"{len(contacts)} contacts found for company: {company}")
        return contacts

if __name__ == "__main__":
    companies_scrap(sectors=COMPANY_SECTORS_KEY)
