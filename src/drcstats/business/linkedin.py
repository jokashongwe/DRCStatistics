from duckduckgo_search import DDGS
import time
import json
import psycopg2
from typing import List, Dict
from src.drcstats.utils.upload import upload_contact_parsed

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
    query = f"SELECT company_id, company_legal_name FROM companies WHERE company_source = 'FC' order by company_legal_name asc;"
    curr.execute(query)
    for company_id, company_legal_name in curr.fetchall():
        contacts = []
        try:    
            contacts = search_linkedin(company_id=company_id, company=company_legal_name)
        except Exception as e:
            print(e)
            continue
        if len(contacts) <= 0:
            continue
        upload_contact_parsed(cur=curr, contacts=contacts, conn=conn)
    curr.close()
    conn.close()


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
                "contact_name": r.get("title").split("-")[0].strip()[:244],
                "contact_linkedin_url": r.get("href")[:255],
                "contact_role": r.get("title").split("-")[1].strip()[:244],
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
    process_linkedin(dbname="connectcongo")
