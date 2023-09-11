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

    for doc in documents.results:
        document_parts = escr.get_document_parts(doc.pk).results
        transcriptions = escr.get_document_transcriptions(doc.pk)
        if len(transcriptions) < 1:
            continue
        tpk = transcriptions[0].pk
        parts = [x for x in document_parts if x.transcription_progress == 100]
        if len(parts) > 0:
            os.makedirs(doc.name, exist_ok=True)
            for p in parts:
                bytes = escr.get_image(p.image.uri)
                im = Image.open(BytesIO(bytes))
                base = sub(r'^.*\.pdf_page', 'page',
                           sub(r'\.(png|jpg|tif)$', '', os.path.basename(p.image.uri)))
                imfile = doc.name + '/' + base + '.png'
                print(imfile)
                im.save(imfile)
                zar = escr.download_part_alto_transcription(doc.pk, p.pk, tpk)
                zip = zipfile.ZipFile(BytesIO(zar))
                for f in zip.infolist():
                    if f.filename != 'METS.xml':
                        xmlfile = doc.name + '/' + sub(r'^.*\.pdf_page', 'page', f.filename)
                        content = zip.read(f)
                        print(xmlfile)
                        dom = md.parse(BytesIO(content))
                        pretty = dom.toprettyxml()
                        pretty = os.linesep.join([s for s in pretty.splitlines() if s.strip()])
                        pretty = sub(r'<fileName>[^<]+</fileName>',
                                     f'<fileName>{base}.png</fileName>', pretty)

                        with open(xmlfile, 'w') as outf:
                            outf.write(pretty)

