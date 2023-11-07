from pathlib import Path
from duckduckgo_search import DDGS
import json
from src.drcstats.utils.upload import upload_one_company, upload_one_contact
import hashlib
import progressbar
import psycopg2
from fuzzywuzzy import fuzz

def get_list_of(path: str):
    result_list = []
    with open(path, "r+", encoding="utf-8") as file:
        result_list = file.readlines()
    return result_list

def is_exist(object_id:str, field: str, table:str, cur,  country:str):
    query = f"SELECT {field} FROM {table} WHERE {field} = '{object_id}' and {country}"
    cur.execute(query=query)
    result = cur.fetchone()
    return True if result else False

def companies_scrap():
    countries = get_list_of(path="Raw/african_countries_list.txt")
    jobs_list = get_list_of(path="Raw/jobs_list.txt")
    for country in countries:
        country = country.strip()
        print("Country: ", country)
        progress_bar = progressbar.ProgressBar(min_value=0, max_value=len(jobs_list))
        progress_bar.widgets = (
            ["uploading lines: "]
            + [progressbar.widgets.FileTransferSpeed(unit="jobs"), " "]
            + progress_bar.default_widgets()
        )
        progress_bar.start()
        for job in jobs_list:
            job = job.strip()
            job = job.replace(":","")
            conn = psycopg2.connect("dbname=connectcongo user=konnect password=secret123")
            cur = conn.cursor()
            with DDGS() as ddgs:
                keyword = f"{job} {country} Linkedin".strip()
                for result in ddgs.text(keyword, max_results=1000):
                    try:
                        link = result.get("href")
                        title = result.get("title")
                        if "linkedin" not in link:
                            continue
                        
                        if "jobs" in link or "feed" in link:
                            continue
                        contact = None
                        company = None
                        if "company" in link:
                            company_legal_name = title.split("-")[0]
                            company = {
                                "company_legal_name": company_legal_name,
                                "company_country": country,
                                "company_sectors": job.split(" "),
                                "company_description": result.get('body'),
                                "company_social_links": [link],
                            }
                        else:
                            title_parts = title.split("-")
                            if len(title_parts) == 2:
                                continue
                            elif len(title_parts) > 2:
                                company_name = (
                                    title_parts[2]
                                    .lower()
                                    .replace("linkedin", "")
                                    .replace("|", "")
                                    .strip()
                                    .capitalize()
                                )
                                if fuzz.ratio(company_name, job) > 90 or not company_name:
                                    continue
                            company = {
                                "company_legal_name": company_name,
                                "company_social_links": [link],
                                "company_description": result.get("body"),
                                "company_sectors": job.split(" "),
                                "company_country": country,
                            }
                            contact = {
                                "contact_name": title_parts[0],
                                "contact_description": result.get('body'),
                                "contact_role": title_parts[1].strip(),
                                "contact_country": country
                            }
                            contact['contact_id'] =hashlib.md5(f"{json.dumps(contact)}".encode("utf-8")).hexdigest()
                            

                            if not company:
                                continue
                            company['company_id'] = hashlib.md5(f"{json.dumps(company)}".encode("utf-8")).hexdigest()
                            if not is_exist(object_id=company.get('company_legal_name'), field="company_legal_name", table="companies", cur=cur, country=f"company_country = '{country}'"):
                                upload_one_company(company=company, curr=cur) if company else None
                            if not is_exist(object_id=contact.get('contact_id'), field="contact_id", table="contacts", cur=cur,  country=f"contact_country = '{country}'"):
                                upload_one_contact(contact=contact, company_id=company['company_id'], curr=cur) if contact else None
                    except Exception as e:
                        continue
            conn.commit()
            progress_bar.update(progress_bar.value + 1)
        cur.close()
        conn.close()
        progress_bar.finish()

if __name__ == "__main__":
    companies_scrap()