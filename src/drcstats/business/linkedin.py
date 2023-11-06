from duckduckgo_search import DDGS
import time
import json
import psycopg2
from typing import List, Dict
from src.drcstats.utils.upload import upload_contact_parsed
from fuzzywuzzy import fuzz

def is_person(result: str, company: str):
    name = result.split("|")[0]
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
            file.write(json.dumps(rec, ensure_ascii=False) + "\n")


def process_linkedin(dbname: str, query: str, suffix: str = "RDC") -> List[str]:
    conn = psycopg2.connect(f"dbname={dbname} user=konnect password=secret123")
    curr = conn.cursor()
    curr.execute(query)
    for company_id, company_legal_name in curr.fetchall():
        contacts = []
        try:
            contacts = search_linkedin(
                company_id=company_id, company=company_legal_name, suffix=suffix
            )
        except Exception as e:
            print(e)
            continue
        if len(contacts) <= 0:
            continue
        upload_contact_parsed(cur=curr, contacts=contacts, conn=conn)
    curr.close()
    conn.close()


def process_linkedin_for_contact(dbname: str, query_results: tuple=None, query:str=None):
    conn = psycopg2.connect(f"dbname={dbname} user=konnect password=secret123")
    curr = conn.cursor()
    curr.execute(f"SELECT contact_id, contact_full_name FROM contacts where contact_linkedin_url is null")
    for contact_id, contact_full_name in curr.fetchall():
        print("Contact name: ", contact_full_name)
        try:
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(f"{contact_full_name}", max_results=50) if fuzz.partial_ratio(contact_full_name, r.get('title')) >= 60]
                contact_links = [{'title': r.get('title'), 'link': r.get("href")} for r in results]
                contact_value = json.dumps(contact_links[:5], ensure_ascii=False).replace("'", "")
                if results:
                    curr.execute(f"UPDATE contacts set contact_links = '{contact_value}' where contact_id = '{contact_id}';")
                    conn.commit()
                else:
                    print(f"No result for: {contact_full_name}")
        except Exception as e:
            raise e
            continue
    curr.close()
    conn.close()

def search_linkedin(company_id: str, company: str, suffix="RDC"):
    with DDGS() as ddgs:
        results = [
            r
            for r in ddgs.text(f"{company} {suffix} linkedin", max_results=100)
            if is_person(r.get("title"), company=company)
            and (
                company_in_string(value=r.get("title"), company=company)
                or company_in_string(value=r.get("body"), company=company)
            )
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
                "contact_company_id": company_id,
            }
            for r in results
        ]
        print(f"{len(contacts)} contacts found for company: {company}")
        return contacts


if __name__ == "__main__":
    query = query = f"SELECT company_id, company_legal_name FROM companies WHERE company_source = 'PNET' order by company_legal_name asc;"
    process_linkedin(dbname="connectcongo", query=query)
    #process_linkedin_for_contact(dbname="connectcongo")