import json
import operator

def in_array(lst, e):
    for idx, elt in enumerate(lst) :
        if elt.get("profile_name") == e.get("profile_name") and elt.get("profile_linkedin_url") == e.get("profile_linkedin_url"):
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
            
            if not merged_list[pos].get("profile_description") == pf.get("profile_description"):
                merged_list[pos]["profile_description"] = f"{merged_list[pos]["profile_description"]}<br/>{pf.get("profile_description")}"
            
            if merged_list[pos].get("merged_ids"):
                merged_list[pos]["merged_ids"].append(pf.get('id'))
            else:
                merged_list[pos]["merged_ids"] = [pf.get('id')]
        else:
            if "https://cd." in pf.get("profile_linkedin_url"):
                merged_list.append(pf)
    return merged_list
    
if __name__ == "__main__":

    profiles = []
    path = "./generated/output_scrap_public_profiles.json"
    lines = []
    with open(path, encoding="UTF-8") as fileIO:
        lines = fileIO.readlines()
    for line in lines:
        profiles.append(json.loads(line))

    merged_list = merge_profiles(profiles)
    merged_list.sort(key=operator.itemgetter('profile_name'))
    file_path = "./generated/output_scrap_public_profiles_merged.json"
    for elt in merged_list:
        with open(file_path, "a+", encoding="utf-8") as fileIO:
            fileIO.write(json.dumps(elt, ensure_ascii=False) + "\n")