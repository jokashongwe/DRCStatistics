import psycopg2


REPAIR_SCRIPTS = [
    "update public.companies set company_domain=null where company_domain = 'None';",
    "update public.companies set company_category=null where company_category = 'None';",
    "update public.companies set company_legal_name=replace(company_legal_name, '*', '') where company_legal_name like '%*%';",
    "update public.companies set company_legal_name=replace(company_legal_name, '#', '') where company_legal_name like '%#%';",
    "update public.companies set company_legal_name=replace(company_legal_name, '@', '') where company_legal_name like '%@%';",
    "update public.companies set company_legal_name=replace(company_legal_name, '\"', '') where company_legal_name like '%\"%';",
    "update public.companies set company_legal_name=replace(company_legal_name, ':', '') where company_legal_name like '%:%';",
    "update public.companies set company_legal_name=replace(company_legal_name, '&', '') where company_legal_name like '%&%';",
    "update public.companies set company_legal_name=replace(company_legal_name, ',', '') where company_legal_name like '%,%';",
    "update public.companies set company_legal_name=replace(company_legal_name, ';', '') where company_legal_name like '%;%';",
    "update public.companies set company_state=null where company_state = 'None';",
    "update public.companies set company_city=null where company_city = 'None';",
    "update public.companies set company_city=null where company_city = '';",
    "update public.contacts set contact_email=null where contact_email = 'None';",
    "update public.contacts set contact_address=null where contact_address = '';",
    "delete from contacts where contact_full_name ilike '%:%';",
    "delete from contacts where contact_full_name ilike '%#%';",
    "delete from contacts where contact_full_name ilike '%*%';",
    """
    update public.companies 
    set company_city=split_part(split_part(company_address,'V/', 2), ', P/', 1)
    where company_city is null and company_address is not null and company_address != 'None'
    """,
    """
    update public.companies 
    set company_state=split_part(company_address, 'P/', 2)
    where company_state is null and company_address is not null and company_address != 'None'
    """
]

def repair(dbname:str):
    conn = psycopg2.connect(f"dbname={dbname} user=konnect password=secret123")
    curr = conn.cursor()
    for repair in REPAIR_SCRIPTS:
        curr.execute(repair)
    conn.commit()
    curr.close()
    conn.close()

if __name__ == "__main__":
    repair(dbname="connectcongo")