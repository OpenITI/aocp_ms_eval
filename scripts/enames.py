#!/usr/bin/env python

from escriptorium_connector import EscriptoriumConnector
import os
from re import sub
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import zipfile
import xml.dom.minidom as md

if __name__ == '__main__':
    load_dotenv()
    url = str(os.getenv('ESCRIPTORIUM_URL'))
    username = str(os.getenv('ESCRIPTORIUM_USERNAME'))
    password = str(os.getenv('ESCRIPTORIUM_PASSWORD'))
    escr = EscriptoriumConnector(url, username, password)
    documents = escr.get_documents()
    print('epk,book')
    for doc in documents.results:
        print(f'{doc.pk},{doc.name}')
