import psycopg2
from pathlib import Path
import json
import progressbar
import hashlib
import time
import random

def remove_single_quote(string:str):
    result = string.replace("'", "''") if string else ""
    return result.split("(")[0].strip()


def upload_one_company(company: dict, curr):
    cur = curr
    location  = company.get("company_location")
    sectors = company.get("company_sectors")
    address = company.get("company_address")
    company_social_links = company.get("company_social_links")
    if location:
        company['company_city'] = location.split('-')[0].strip()
        company['company_state'] = location.split('-')[-1].strip()
    empty_company_id = company.get("company_id")
    if not empty_company_id:
        empty_company_id = hashlib.md5(f"{json.dumps(company)}".encode("utf-8")).hexdigest()
    query = f""" 
        INSERT INTO public.companies(
        company_id, company_legal_name, company_city, 
        company_state, company_alternative_name, company_sectors,company_social_links, 
        company_address, company_domain, company_source, company_capital, 
        company_rccm, company_tax_number,company_creation_date,company_legal_form, company_desc,company_category, company_country)
        VALUES ('{empty_company_id}', '{remove_single_quote(company.get("company_legal_name"))}', '{company.get("company_city", '')}', 
        '{company.get("company_state", '')}', '{remove_single_quote(company.get("company_alternative_name"))}', 
        '{json.dumps(sectors, ensure_ascii=False)}', '{json.dumps(company_social_links, ensure_ascii=False)}', '{remove_single_quote(address)}', '{company.get("company_domain", '')}', 
        'PNET', '{company.get("company_capital", '')}', '{company.get("company_rccm", '')}', '{company.get("company_tax_number", '')}', 
        TO_DATE('{company.get("company_creation_date") if company.get("company_creation_date") else '1960-01-01' }', 'YYYY-MM-DD'), '{remove_single_quote(company.get("company_legal_form", ''))}',
        '{remove_single_quote(company.get("company_description",''))}', '{company.get("company_category", "")}','{company.get("company_country")}' );
    """
    cur.execute(query=query)


def upload_one_contact(contact: dict, company_id: str, curr):
    if not contact.get('contact_name'):
        return
    cur = curr
    phones = json.dumps(contact.get("contact_phones")).replace("'", "\"") if contact.get("contact_phones") else []
    empty_contact_id = contact.get('contact_id')  if  contact.get('contact_id') else hashlib.md5(f"{json.dumps(contact)}".encode("utf-8")).hexdigest()
    contact_name = contact.get('contact_name').replace("'", " ") if contact.get('contact_name') else ''
    query = f""" 
        INSERT INTO public.contacts(
        contact_id, contact_full_name, contact_phones,contact_role,contact_email, contact_source, company_id, contact_address, contact_desc,contact_country, contact_linkedin_url)
        VALUES ('{empty_contact_id}', '{contact_name}', null, '{remove_single_quote(contact.get('contact_role'))}', '{contact.get("contact_email")}', 'PNET', '{company_id}', null, '{remove_single_quote(contact.get('contact_description'))}', '{contact.get("contact_country")}', '{contact.get('contact_linkedin_url')}');
        """
    cur.execute(query=query)

def upload_company(filename: Path, dbname="connectcongo", with_contact=False):
    try:
        current_line = None
        with open(file=filename, encoding="utf-8", mode="r") as file:
            conn = psycopg2.connect(f"dbname={dbname} user=konnect password=secret123")
            cur = conn.cursor()
            lines = file.readlines()
            progress_bar = progressbar.ProgressBar(min_value=0, max_value=len(lines))
            progress_bar.widgets = (
                ["uploading lines: "]
                + [progressbar.widgets.FileTransferSpeed(unit="lines"), " "]
                + progress_bar.default_widgets()
            )
            progress_bar.start()
            keys = []
            for line in lines:
                current_line = line.strip()
                company = json.loads(line)
                empty_company_id = company.get('company_id') if company.get('company_id') else hashlib.md5(f"{line}".encode("utf-8")).hexdigest() 
                if empty_company_id in keys or not empty_company_id:
                    progress_bar.update(progress_bar.value + 1)
                    continue
                keys.append(empty_company_id)
                sectors = company.get("company_sectors")
                address = company.get("company_address")
                location  = company.get("company_location")
                if location:
                    company['company_city'] = location.split('-')[0].strip()
                    company['company_state'] = location.split('-')[-1].strip()
                query = f""" 
                    INSERT INTO public.companies(
                    company_id, company_legal_name, company_city, 
                    company_state, company_alternative_name, company_sectors, 
                    company_address, company_domain, company_source, company_capital, 
                    company_rccm, company_tax_number,company_creation_date,company_legal_form, company_desc,company_category, company_country)
                    VALUES ('{empty_company_id}', '{remove_single_quote(company.get("company_legal_name"))}', '{company.get("company_city", 'Kinshasa')}', 
                    '{company.get("company_state", '')}', '{remove_single_quote(company.get("company_alternative_name"))}', 
                    '{json.dumps(sectors, ensure_ascii=False)}', '{remove_single_quote(address)}', '{company.get("company_domain", '')}', 
                    'PNET', '{company.get("company_capital", '')}', '{company.get("company_rccm", '')}', '{company.get("company_tax_number", '')}', 
                    TO_DATE('{company.get("company_creation_date") if company.get("company_creation_date") else '2023-11-02' }', 'YYYY-MM-DD'), '{remove_single_quote(company.get("company_legal_form", ''))}',
                    '{remove_single_quote(company.get("company_description",''))}', '{company.get("company_category")}', 'Democratic Republic of the Congo' );
                """
                contact = company.get('company_contact')
                if contact and with_contact :
                    contact = company.get('company_contact')
                    phones = json.dumps(contact.get("contact_phones")).replace("'", "\"") if contact.get("contact_phones") else []
                    empty_contact_id =hashlib.md5(f"{line}{time.time() + random.randint(1, 1000)}".encode("utf-8")).hexdigest()
                    contact_name = contact.get('contact_name').replace("'", " ") if contact.get('contact_name') else ''
                    query = f""" 
                        INSERT INTO public.contacts(
                        contact_id, contact_full_name, contact_phones, contact_email, contact_source, company_id, contact_address)
                        VALUES ('{empty_contact_id}', '{contact_name}', '{phones}', '{contact.get("contact_email")}', 'PNET', '{empty_company_id}', null);
                    """
                cur.execute(query=query)
                progress_bar.update(progress_bar.value + 1)
            conn.commit()
            progress_bar.finish()
            cur.close()
            conn.close()

    except Exception as error:
        print("current_line: ", current_line)
        raise error
    
def upload_contact_parsed(cur, contacts, conn, country:str):
    progress_bar = progressbar.ProgressBar(min_value=0, max_value=len(contacts))
    progress_bar.widgets = (
        ["uploading lines: "]
        + [progressbar.widgets.FileTransferSpeed(unit="contacts"), " "]
        + progress_bar.default_widgets()
    )
    progress_bar.start()
    for contact in contacts:
        line = json.dumps(contact)
        empty_contact_id =hashlib.md5(f"{line}".encode("utf-8")).hexdigest()
        contact_name = contact.get("contact_name").replace("'", "-") if contact.get("contact_name") else ''
        address = contact.get("contact_address").replace("'", " ") if contact.get("contact_address") else ''
        nationality = contact.get('contact_nationality') if contact.get('contact_nationality') else ""
        if "né" in nationality:
            nationality = "CD"
        # check if exists
        query = f"SELECT contact_id FROM contacts WHERE contact_id = '{empty_contact_id}';"
        cur.execute(query)
        contact_id = cur.fetchone()
        if contact_id:
            continue
        if not contact.get('contact_company_id'):
            query = f""" 
                INSERT INTO public.contacts(
                contact_id, contact_full_name, contact_phones, contact_email, contact_source,
                contact_address, contact_role, contact_nationality, contact_linkedin_url, contact_country)
                VALUES ('{empty_contact_id}', '{remove_single_quote(contact_name)}', '{contact.get("contact_contact_phones") if contact.get("contact_contact_phones") else [] }', 
                '{contact.get("contact_email",'')}', 'LINKEDIN', '{address}', 
                '{remove_single_quote(contact.get('contact_role'))}', '{nationality}', '{remove_single_quote(contact.get('contact_linkedin_url'))}', '{country}');
            """
        else:
            query = f""" 
                INSERT INTO public.contacts(
                contact_id, contact_full_name, contact_phones, contact_email, contact_source, company_id,
                contact_address, contact_role, contact_nationality, contact_linkedin_url, contact_country)
                VALUES ('{empty_contact_id}', '{remove_single_quote(contact_name)}', '{contact.get("contact_contact_phones") if contact.get("contact_contact_phones") else [] }', 
                '{contact.get("contact_email",'')}', 'LINKEDIN', '{contact.get('contact_company_id')}', '{address}', 
                '{remove_single_quote(contact.get('contact_role'))}', '{nationality}', '{remove_single_quote(contact.get('contact_linkedin_url'))}', '{country}');
            """
        cur.execute(query=query)
        progress_bar.update(progress_bar.value + 1)
    conn.commit()
    progress_bar.finish()

def upload_contact(filename: Path, dbname="connectcongo"):
    try:
        current_line = None
        with open(file=filename, encoding="utf-8", mode="r") as file:
            conn = psycopg2.connect(f"dbname={dbname} user=konnect password=secret123")
            cur = conn.cursor()
            lines = file.readlines()
            progress_bar = progressbar.ProgressBar(min_value=0, max_value=len(lines))
            progress_bar.widgets = (
                ["uploading lines: "]
                + [progressbar.widgets.FileTransferSpeed(unit="lines"), " "]
                + progress_bar.default_widgets()
            )
            progress_bar.start()
            for line in lines:
                current_line = line
                contact = json.loads(line)
                empty_contact_id =hashlib.md5(f"{line}".encode("utf-8")).hexdigest()
                contact_name = contact.get("contact_name").replace("'", "-") if contact.get("contact_name") else ''
                address = contact.get("contact_address").replace("'", " ") if contact.get("contact_address") else ''
                birthday = contact.get('contact_birthday');
                birthday = '01/01/1960' if "n" in birthday or "CD" in birthday else birthday
                if "-" in birthday:
                    parts = birthday.split("-")
                    birthday=f"{parts[2]}/{parts[1]}/{parts[0]}"
                nationality = contact.get('contact_nationality') if contact.get('contact_nationality') else ""
                if "né" in nationality:
                    nationality = "CD"
                # check if exists
                query = f"SELECT contact_id FROM contacts WHERE contact_id = '{empty_contact_id}'"
                cur.execute(query)
                contact_id = cur.fetchone()
                if contact_id:
                    continue
                query = f""" 
                    INSERT INTO public.contacts(
                    contact_id, contact_full_name, contact_phones, contact_email, contact_source, company_id,
                    contact_address, contact_role, contact_nationality, contact_birthday, contact_country)
                    VALUES ('{empty_contact_id}', '{contact_name}', '{contact.get("contact_contact_phones") if contact.get("contact_contact_phones") else [] }', 
                    '{contact.get("contact_email",'')}', 'PNET', '{contact.get('contact_company_id')}', '{address}', 
                    '{remove_single_quote(contact.get('contact_role'))}', '{nationality}',TO_DATE('{birthday}', 'DD/MM/YYYY'), 'Democratic Republic of the Congo');
                """
                cur.execute(query=query)
                progress_bar.update(progress_bar.value + 1)
            conn.commit()
            progress_bar.finish()
            cur.close()
            conn.close()

    except Exception as error:
        print("current_line: ", current_line)
        raise error


if __name__ == "__main__":
    current_folder = Path(__file__).parent
    upload_list = ["public_companies.json", "minihydro.json","arsp.json","produced_guce_company_1698999754.json", "produced_fec_company_1697796196.json"]
    #for company_filename in upload_list:
    #    generated_folder = Path(current_folder.parent.parent.parent, "uploads", company_filename)
    #    # print("gen: ", generated_folder)
    #    upload_company(generated_folder)
    contact_uploads = ["produced_guce_contact_1698999754.json"]
    for contact_filename in contact_uploads:
        generated_folder = Path(current_folder.parent.parent.parent, "uploads", contact_filename)
        # print("gen: ", generated_folder)
        upload_contact(generated_folder)

