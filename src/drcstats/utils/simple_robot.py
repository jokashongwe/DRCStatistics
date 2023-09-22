from typing import Callable, List, Dict
from progressbar import ProgressBar
import requests
import logging
import time
import json
import os
from pathlib import Path
from datetime import datetime


class SimpleRobot:
    def __init__(
        self,
        source_name: str,
        page_url: str,
        url_format: str,
        max_pages: int,
        fn_parse_page: Callable[[str], List[Dict]],
        path: Path = None,
    ) -> None:
        self.page_url = page_url
        self.source_name = source_name
        self.url_format = url_format
        self.max_pages = max_pages
        self.fn_parse_page = fn_parse_page
        self.path = path

    def start(self):
        logging.info(f"Start processing {self.source_name}\n")
        formatted_date = str(datetime.fromtimestamp(time.time())).split('.')[0]
        formatted_date = formatted_date.replace(':', '_').replace('-', '_').replace(' ', '_')
        filename = f"output_{self.source_name}_{formatted_date}.ndjson"
        if not self.path:
            self.path = Path(os.getcwd())
        file_path = Path(self.path, filename)
        if not file_path.parent.exists():
            file_path.parent.mkdir()
        logging.info(f"output filename {filename}\n")
        progress_bar = ProgressBar(min_value=0, max_value=self.max_pages)
        progress_bar.start()
        with open(file_path, "a+", encoding="utf-8") as fileIO:
            for current_page in range(1, self.max_pages):
                progress_bar.update(current_page)
                html_doc = self.parse(current_page)
                if not html_doc:
                    break
                parsed_list = self.fn_parse_page(html_doc)
                if not parsed_list:
                    break
                for parsed in parsed_list:
                    fileIO.write(json.dumps(parsed) + "\n")
        progress_bar.finish()
        logging.info(f"End scrapping for {self.source_name}\n")

    def parse(self, next_index) -> str | None:
        current_url = self.url_format.format(page_number=next_index)
        response = requests.get(url=current_url)
        if response.status_code > 201:
            return None
        return response.text
