import json
import operator

def in_array(lst, e):
    for idx, elt in enumerate(lst) :
        if elt.get("profile_name") and elt.get("profile_linkedin_url") == e.get("profile_linkedin_url"):
            return idx
    return -1
    

def in_array_experience(lst, e):
    for idx, elt in enumerate(lst) :
        if elt.get("experience_role") == e.get("experience_role") and elt.get("experience_linkedin_url") == e.get("experience_linkedin_url"):
            return idx
    return -1

def merge_profiles(profile_list: list[dict]) -> list[dict]:
    """
        Fusioner les profils similaire pour éviter les doublons
    """
    merged_list =  []
    for pf in profile_list:
        pos = in_array(merged_list, pf)
        if pos >= 0 :
            if merged_list[pos].get("profile_social_links") and pf.get("profile_linkedin_url") not in merged_list[pos].get("profile_social_links") :
                merged_list[pos]["profile_social_links"] = merged_list[pos]["profile_social_links"].append(pf.get("profile_linkedin_url"))
            else:
                merged_list[pos]["profile_social_links"] = [pf.get("profile_linkedin_url")]
            
            if merged_list[pos].get("merged_ids"):
                merged_list[pos]["merged_ids"].append(pf.get('id'))
            else:
                merged_list[pos]["merged_ids"] = [pf.get('id')]
        else:
            if "https://cd." in pf.get("profile_linkedin_url"):
                merged_list.append(pf)
    return merged_list

def merge_experiences(profile_list: list[dict]) -> list[dict]:
    """
        Fusioner les experiences similaire pour éviter les doublons
    """
    merged_list =  []
    for pf in profile_list:
        pos = in_array_experience(merged_list, pf)
        if pos >= 0 :
            if merged_list[pos].get("experience_social_links") and pf.get("experience_linkedin_url") not in merged_list[pos].get("experience_social_links") :
                merged_list[pos]["experience_social_links"] = merged_list[pos]["experience_social_links"].append(pf.get("experience_linkedin_url"))
            else:
                merged_list[pos]["experience_social_links"] = [pf.get("experience_linkedin_url")]

            if merged_list[pos].get("experience_origins") and pf.get("experience_origin") not in merged_list[pos].get("experience_origins"):
                merged_list[pos]["experience_origins"] = merged_list[pos]["experience_origins"].append(pf.get("experience_origin"))

            
            if merged_list[pos].get("merged_ids"):
                merged_list[pos]["merged_ids"].append(pf.get('id'))
            else:
                merged_list[pos]["merged_ids"] = [pf.get('id')]
        else:
            if "https://cd." in pf.get("experience_linkedin_url"):
                pf["experience_social_links"] =  [pf.get("experience_linkedin_url")]
                pf["experience_origin"] = f"{pf["experience_origin"]}".lower()
                pf["experience_origins"] =  [pf.get("experience_origin")]
                merged_list.append(pf)
    return merged_list
    
if __name__ == "__main__":

    profiles = []
    experiences = []
    path = "./generated/output_scrap_public_profiles.json"
    lines = []
    with open(path, encoding="UTF-8") as fileIO:
        lines = fileIO.readlines()
    for line in lines:
        profiles.append(json.loads(line))

    path = "./generated/output_scrap_public_experiences.json"
    lines = []
    with open(path, encoding="UTF-8") as fileIO:
        lines = fileIO.readlines()
    for line in lines:
        experiences.append(json.loads(line))

    merged_list = merge_profiles(profiles)
    experience_list = merge_experiences(experiences)

    merged_list.sort(key=operator.itemgetter('profile_name'))
    file_path = "./generated/output_scrap_public_profiles_merged.json"
    for elt in merged_list:
        with open(file_path, "a+", encoding="utf-8") as fileIO:
            fileIO.write(json.dumps(elt, ensure_ascii=False) + "\n")
    file_path = "./generated/output_scrap_public_experiences_merged.json"
    for elt in experience_list:
        with open(file_path, "a+", encoding="utf-8") as fileIO:
            fileIO.write(json.dumps(elt, ensure_ascii=False) + "\n")