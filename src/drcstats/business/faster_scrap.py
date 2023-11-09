from pathlib import Path
from duckduckgo_search import DDGS
import json
from src.drcstats.utils.upload import (
    upload_one_company,
    upload_one_contact,
    remove_single_quote,
)
import hashlib
import progressbar
import psycopg2
from fuzzywuzzy import fuzz
import urllib.parse
import multiprocessing as mp
import os
from concurrent.futures import ThreadPoolExecutor

PROCESSORS = os.cpu_count() * 2
THREADS = 5
BUCKET = 5
THREADS_WORKERS = 5
THREADS_BUCKET = 5
RESULTS = 400


def get_list_of(path: str):
    result_list = []
    with open(path, "r+", encoding="utf-8") as file:
        result_list = file.readlines()
    return result_list


JOBS_LIST = get_list_of(path="Raw/jobs_list.txt")


def parse_string(value: str):
    string_arr = [e for e in value if e.isalnum() or e == " "]
    return ("".join(string_arr)).strip()


def is_exist(
    object_id: str, field: str, where_expr: str, table: str, cur, country: str = ""
):
    query = f"SELECT {field} FROM {table} WHERE {where_expr};"
    # print("\nQuery: ", query)
    cur.execute(query=query)
    return cur.fetchone()


def list_iterator(object_list: list, count=5):
    while object_list:
        yield object_list[:count]
        object_list = object_list[count:]


def parse_company_name(value: str):
    return parse_string(
        value.lower().replace("linkedin", "").replace("|", "").strip().capitalize()
    )


def thread_processor(job: str, country: str):
    job = parse_string(job).strip()
    conn = psycopg2.connect("dbname=connectcongo user=konnect password=secret123")
    cur = conn.cursor()
    with DDGS() as ddgs:
        keyword = f"{job} {country} Linkedin".strip()
        for result in ddgs.text(keyword, max_results=RESULTS):
            try:
                link = result.get("href")
                title = result.get("title")
                if "linkedin" not in link:
                    continue

                if "jobs" in link or "feed" in link or "posts" in link:
                    continue

                contact = None
                company = None
                if "company" in link:
                    company_legal_name = title.split("-")[0]
                    company = {
                        "company_legal_name": remove_single_quote(
                            parse_company_name(company_legal_name)
                        ),
                        "company_country": country,
                        "company_sectors": job.split(" "),
                        "company_description": remove_single_quote(result.get("body")),
                        "company_social_links": [urllib.parse.quote(link)],
                    }
                else:
                    title_parts = title.split("-")
                    if len(title_parts) <= 2:
                        continue
                    elif len(title_parts) > 2:
                        company_name = parse_company_name(
                            title_parts[2 if len(title_parts) == 3 else 3]
                        )
                        if fuzz.ratio(company_name, job) > 90:
                            continue
                    company = {
                        "company_legal_name": remove_single_quote(company_name),
                        "company_social_links": [link],
                        "company_description": "",
                        "company_sectors": job.split(" "),
                        "company_country": country,
                    }
                    contact = {
                        "contact_name": parse_string(title_parts[0]),
                        "contact_description": remove_single_quote(result.get("body")),
                        "contact_role": parse_string(title_parts[1].strip()),
                        "contact_linkedin_url": link,
                        "contact_country": country,
                    }
                    contact["contact_id"] = hashlib.md5(
                        f"{json.dumps(contact)}".encode("utf-8")
                    ).hexdigest()
                    if not company:
                        continue

                    company_name = company.get("company_legal_name")
                    if not company_name:
                        continue
                    company["company_id"] = hashlib.md5(
                        f"{json.dumps(company)}".encode("utf-8")
                    ).hexdigest()
                    company_name = company_name.lower().replace(country.lower(), "")
                    
                    company_exists = is_exist(
                        object_id=company_name,
                        field="company_id, company_legal_name",
                        table="companies",
                        cur=cur,
                        where_expr=f"company_country = '{country}' AND company_legal_name ilike '{company_name}%'",
                    )
                    # print("\nResult company: ", company_exists)
                    if company and not company_exists:
                        upload_one_company(company=company, curr=cur)
                    company_id = (
                        company_exists[0] if company_exists else company["company_id"]
                    )
                    contact_exists = (
                        is_exist(
                            object_id=contact.get("contact_id"),
                            field="contact_full_name",
                            table="contacts",
                            cur=cur,
                            where_expr=f"contact_linkedin_url = '{link}'",
                        )
                        if contact
                        else None
                    )
                    # print(f"\nContact_id: {contact.get("contact_id")}\nContact_exists: ", contact_exists) if contact else None
                    if contact and contact.get("contact_name") and not contact_exists:
                        upload_one_contact(
                            contact=contact,
                            company_id=company_id,
                            curr=cur,
                        )
            except Exception as e:
                continue
            conn.commit()
            cur.close()
            conn.close()


def get_companies(country:str):
    conn = psycopg2.connect("dbname=connectcongo user=konnect password=secret123")
    curr = conn.cursor()
    query = f"SELECT company_id, company_legal_name FROM companies WHERE company_country ='{country}' AND len(company_legal_name) > 1"
    curr.execute(query)
    companies = []
    for company_id, company_legal_name in curr.fetchall():
        if len(companies) >= 5:
            yield companies
            companies  = []
        companies.append({"company_id": company_id, "company_legal_name":company_legal_name})
    curr.close()
    conn.close()


def companies_scrap_executor(countries: list):
    """
        companies_scrap_executor
        Scrap for companies and contacts with Multiprocessing and MultiThreading
    """
    for country in countries:
        country = country.strip()
        
        for selected_jobs in list_iterator(JOBS_LIST, THREADS_BUCKET):
            pool = ThreadPoolExecutor(max_workers=THREADS_WORKERS)
            [
                pool.submit(thread_processor, job=job, country=country)
                for job in selected_jobs
            ]
            pool.shutdown(wait=True)


def companies_scrap():
    countries = get_list_of(path="Raw/african_countries_list.txt")

    progress_bar = progressbar.ProgressBar(min_value=0, max_value=len(countries))
    progress_bar.widgets = (
        ["uploading lines: "]
        + [progressbar.widgets.FileTransferSpeed(unit="countries"), " "]
        + progress_bar.default_widgets()
    )
    progress_bar.start()
    with mp.Pool(processes=PROCESSORS) as pool:
        for selected_countries in list_iterator(object_list=countries, count=BUCKET):
            pool.map(companies_scrap_executor, selected_countries)
            progress_bar.update(progress_bar.value + BUCKET)
    progress_bar.finish()


if __name__ == "__main__":
    companies_scrap()
    # print(parse_string("Special $#! characters + ...  spaces 888323"))
