from pathlib import Path
from duckduckgo_search import DDGS
import json
from src.drcstats.utils.upload import (
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


def parse_name(value: str):
    return parse_string(
        value.lower().replace("linkedin", "").replace("|", "").strip().capitalize()
    )


def thread_processor(query: str, country: str):
    query = parse_string(query).strip()
    with DDGS() as ddgs:
        keyword = f"{query} {country} Linkedin".strip()

        for result in ddgs.text(keyword, max_results=RESULTS):
            try:
                link = result.get("href")
                title = result.get("title")
                if "linkedin" not in link:
                    continue
                actuality = None
                if "jobs" in link or "feed" in link or "posts" in link:
                    actuality = {
                        "actuality_title": title,
                        "actuality_link": link,
                        "actuality_company_name": query,
                    }

                profile = None
                company = None
                experience = None
                
                if not "company" in link:
                    title_parts = title.split("-")
                    if len(title_parts) <= 2:
                        continue
                    elif len(title_parts) > 2:
                        name = parse_name(
                            title_parts[2 if len(title_parts) == 3 else 3]
                        )
                        if fuzz.ratio(name, query) > 90:
                            continue
                    if not (query.lower() in parse_string(title_parts[0]).lower()):
                        profile = {
                            "profile_name": parse_string(title_parts[0]),
                            "profile_role": parse_string(title_parts[1].strip()),
                            "profile_description": result.get("body"),
                            "profile_origin": query,
                            "profile_linkedin_url": link,
                            "profile_country": country,
                        }
                        profile["id"] = hashlib.md5(
                            f"{json.dumps(profile)}".encode("utf-8")
                        ).hexdigest()

                        experience = {
                            "experience_origin": query,
                            "experience_profile_id": profile.get("id"),
                            "experience_link": link,
                        }

                    experience["id"] = hashlib.md5(
                        f"{json.dumps(experience)}".encode("utf-8")
                    ).hexdigest()
                    # print("\nResult company: ", exists)

                if company:
                    file_path = "./generated/output_scrap_public_companies.json"
                    with open(file_path, "a+", encoding="utf-8") as fileIO:
                        fileIO.write(json.dumps(company, ensure_ascii=False) + "\n")

                if profile:
                    file_path = "./generated/output_scrap_public_profiles.json"
                    with open(file_path, "a+", encoding="utf-8") as fileIO:
                        fileIO.write(json.dumps(profile, ensure_ascii=False) + "\n")

                if experience:
                    file_path = "./generated/output_scrap_public_experiences.json"
                    with open(file_path, "a+", encoding="utf-8") as fileIO:
                        fileIO.write(json.dumps(experience, ensure_ascii=False) + "\n")

                if actuality:
                    file_path = "./generated/output_scrap_public_actualities.json"
                    with open(file_path, "a+", encoding="utf-8") as fileIO:
                        fileIO.write(json.dumps(actuality, ensure_ascii=False) + "\n")
            except Exception as e:
                continue


def readCompanies(filename: str):
    list = []
    with open(filename, encoding="UTF-8") as companyFile:
        for line in companyFile.readlines():
            list.append(line)
    return list


def get_companies():
    companies = []
    filename = "./Raw/public_companies.txt"
    company_names = readCompanies(filename)
    for legal_name in company_names:
        companies.append({"legal_name": legal_name})
    return companies


def companies_scrap_executor():
    """
    companies_scrap_executor
    Scrap for companies and profiles with Multiprocessing and MultiThreading
    """
    companies = get_companies()
    progress_bar = progressbar.ProgressBar(min_value=0, max_value=len(companies))
    progress_bar.widgets = (
        ["Scrapping Companies: "]
        + [progressbar.widgets.FileTransferSpeed(unit="companies"), " "]
        + progress_bar.default_widgets()
    )
    progress_bar.start()
    for company in companies:
        thread_processor(query=company.get("legal_name"), country="RDC")
        progress_bar.update(progress_bar.value + 1)
    progress_bar.finish()


def companies_scrap():
    companies_scrap_executor()


if __name__ == "__main__":
    companies_scrap()
    # print(parse_string("Special $#! characters + ...  spaces 888323"))
