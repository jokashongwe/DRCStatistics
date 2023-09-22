import json
from typing import Tuple, List, Any
import re
import psycopg2
from pathlib import Path
import os


def sanitize_value(value: str):
    if type(value) != str:
        return value
    value = value.upper()

    parsed_value = (
        value.replace("DES ", "")
        .replace("DE ", "")
        .replace("DU ", "")
        .replace("D'", "")
        .replace("APPEL A CANDIDATURE", "")
        .replace(" QUI ", "")
        .replace(" SERA ", "")
        .replace(" BASE ", "")
        .replace("'", "")
        .replace("À", "")
        .replace("AU ", "")
        .replace("EN ", "")
        .replace("(E)", "")
        .replace("À", "")
        .replace("SARL", "")
        .replace(" SA ", "")
        .replace("S.A", "")
        .replace("S A", "")
        .replace("SARLU ", "")
        .replace("POSTES ", "")
        .replace(" SAS ", "")
        .replace("ET ", "")
        .replace("AUX ", "")
        .replace("POUR ", "")
        .replace("OU ", "")
        .replace("AVEC ", "")
        .replace("(", " - ")
        .replace(")", "")
    ).strip()

    parsed_value = re.sub(r'^LA *', '', parsed_value)
    parsed_value = re.sub(r"^LE *", "", parsed_value)
    parsed_value = re.sub(r"^LES *", "", parsed_value)
    return parsed_value


def upload_single_file(path: Path, source: str = None):
    with open(path, "r") as file:
        for line in file.readlines():
            offer = json.loads(line.replace("'", "''"))
            offer["offer_source"] = source
            upload_element(
                offer,
                [
                    "offer_id",
                    "offer_name",
                    "offer_title",
                    "offer_url",
                    "offer_company_name",
                    "offer_locations",
                    "offer_added_dt",
                    "offer_source",
                ],
            )


def get_values(data: dict, keys: list) -> dict[str, str]:
    dict_values = {
        key: f"""'{sanitize_value(data.get(key)[:255]) if key != 'offer_added_dt' else "-".join(data.get(key).split('.')[::-1])}'"""
        for key in keys
        if data.get(key) and key not in ['offer_id', 'offer_url']
    }
    dict_values['offer_id'] = f"'{data['offer_id']}'"
    dict_values['offer_url'] = f"'{data.get('offer_url')}'"
    return dict_values


def upload_element(data: dict, keys: list):
    dict_values = get_values(data, keys)
    locations = dict_values.get("offer_locations")
    if locations:
        d_locations = locations.replace("'", "").replace("[", "").replace("]", "")
        dict_values["offer_locations"] = f"'{d_locations}'"
    values = dict_values.values()
    n_keys = dict_values.keys()
    n_keys = [key if key != "offer_title" else "offer_name" for key in n_keys]
    sql = f""" INSERT INTO offers({",".join(n_keys)}) VALUES({",".join(values)}) """

    conn = psycopg2.connect(
        "dbname=drcstats user=postgres password=postgres host=127.0.0.1"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    # Creating a database
    cursor.execute(sql)
    print("Data inserted successfully........")
    # Closing the connection
    conn.close()


def create_database(dbname: str):
    conn = psycopg2.connect(
        "dbname=postgres user=postgres password=postgres host=127.0.0.1"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    sql = f"""CREATE database {dbname}"""
    # Creating a database
    cursor.execute(sql)
    print("Database created successfully........")
    # Closing the connection
    conn.close()


def create_table(query: str = None):
    conn = psycopg2.connect(
        "dbname=drcstats user=postgres password=postgres host=192.168.104.211"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    sql = f"""
        CREATE TABLE offers (
            OFFER_ID VARCHAR(255) NOT NULL PRIMARY KEY,
            OFFER_URL VARCHAR(255) NULL,
            OFFER_NAME VARCHAR(255) NULL,
            OFFER_COMPANY_NAME VARCHAR(255) NULL,
            offer_locations JSON NULL
        )
    """
    # Creating a database
    cursor.execute(query or sql)
    print("SQL executed successfully........")
    # Closing the connection
    conn.close()


def upload_offers() -> None:
    file_path = Path("../generated/offers")
    files = os.listdir(file_path)
    for file in files:
        path = Path(file_path, file)
        upload_single_file(path=path, source=file.split("_")[1])


if __name__ == "__main__":
    upload_offers()
    # create_table("truncate offers")
    pass
