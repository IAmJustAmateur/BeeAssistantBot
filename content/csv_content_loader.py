import os
from typing import Dict
import csv
import logging
from content.content_parts import Content_Part


def content_loader(content_sources: Dict, content_folder: str) -> Dict[str, Content_Part]:
    new_content_sources = {}
    dialogs_folder = os.path.join(os.getcwd(), content_folder)

    for content_part in content_sources.keys():
        content_file = content_sources[content_part]
        content_file_name =  os.path.join(os.getcwd(), dialogs_folder, content_file)
        logging.info(f'content_file: {content_file_name} before loading')
        try:
            csv_dialogs = open(content_file_name, encoding='utf-8')
            logging.info(f'content_file: {content_file_name} loaded')
            phrases = csv.reader(csv_dialogs)
            rows = [row for row in phrases]
            headers = rows[0]
            body = rows[1:]
            new_content_sources[content_part] = Content_Part(headers, body)
        except IOError:
            logging.info(f"error loading {content_file_name}")
    return  new_content_sources