import os
from typing import List, Tuple, Dict
import csv
from content.content_parts import Content_Part

def content_loader(content_sources: Dict, content_folder: str) -> Dict[str, Content_Part]:
    new_content_sources = {}
    for content_part in content_sources.keys():
        content_file = content_sources[content_part]
        content_file_name =  os.path.join(os.getcwd(), content_folder, content_file)
        tsv_dialogs = open(content_file_name, encoding='utf-8')
        phrases = csv.reader(tsv_dialogs, delimiter="\t")
        rows = [row for row in phrases]
        headers = rows[0]
        body = rows[1:]
        new_content_sources[content_part] = Content_Part(headers, body)
    return  new_content_sources