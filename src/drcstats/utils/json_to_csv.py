from pathlib import Path
import json
import csv
from typing import List, Dict


def json_to_csv(file: Path, extension: str = "json"):
    """
        Cette méthode convertis un fichier json en CSV
        :file Path fichier à convertir
    """
    json_data = []
    data = []
    with open(file=file, mode="r", encoding="UTF-8") as fileReader:
        data = fileReader.readlines()
    json_data: List[Dict] = [json.loads(line.strip()) for line in data]
    if not json_data:
        raise "Empty data file"
    keys = json_data[0].keys()
    ext = f".{extension}"
    dest_filename = str(file).replace(ext, "_converted.csv")
    with open(dest_filename, "a+", encoding="utf-8") as fileIO:
        fileWriter = csv.writer(fileIO, lineterminator="\n")
        fileWriter.writerow(keys)
        fileWriter.writerows([e.values() for e in json_data])
            

if __name__ == '__main__':
    json_to_csv(Path("./generated/output_mediacongo_2023_12_23_09_00_43.ndjson"), "ndjson")