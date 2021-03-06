import os
import xml.etree.ElementTree as ET
import urllib.request
import json 
import time

pmid_file = "pmid-augustinlu-set.txt"

with open(pmid_file) as f:
    pmid_ids = f.readlines()

pub_list = []

for i in range(len(pmid_ids)):
#for i in range(10):
    pmid_id = pmid_ids[i].strip()
    # url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=' + pmid_id
    # f = urllib.urlopen(url)
    # myfile = f.read()

    #pmid_id = "32460492"
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid_id}&rettype=xml'
    print(f'URL: {url}')

    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36'
        }
    )

    f = urllib.request.urlopen(req, timeout=60)
    xml = f.read()
    tree = ET.ElementTree(ET.fromstring(xml))

    journal = tree.find('.//ISOAbbreviation').text
    pub_year = tree.find('.//PubDate/Year').text
    pub_year = int(pub_year)
    title = tree.find('.//ArticleTitle').text

    abstract = ""
    try: 
        abstract = tree.find('.//AbstractText').text
    except:
        print(f'ERROR: {pmid_id}')
    
    pmid_url = f'http://www.ncbi.nlm.nih.gov/pubmed/{pmid_id}'

    tmp = {'name': title, 'date': pub_year, 'description': abstract, 'publisher': journal, 'url': pmid_url}
    pub_list.append(tmp)

    time.sleep(2)

tmp_pub_list = sorted(pub_list, key = lambda i: i['date'])
tmp_pub_list.reverse()

for i in range(len(tmp_pub_list)):
    item = tmp_pub_list[i]
    item.update( {"_id": (i+1)})

with open("publications.json", 'w') as f:
    tmp = json.dumps(tmp_pub_list, indent=2)
    print(tmp, file=f)


# Example
## Output
# {
#     "name" : "PathVisio-MIM: PathVisio plugin for creating and editing Molecular Interaction Maps (MIMs).",
#     "date" : "2011",
#     "description" : "MOTIVATION: A plugin for the Java-based PathVisio pathway editor has been developed to help users draw diagrams of bioregulatory networks according to the Molecular Interaction Map (MIM) notation. Together with the core PathVisio application, this plugin presents a simple to use and cross-platform application for the construction of complex MIM diagrams with the ability to annotate diagram elements with comments, literature references and links to external databases. This tool extends the capabilities of the PathVisio pathway editor by providing both MIM-specific glyphs and support for a MIM-specific markup language file format for exchange with other MIM-compatible tools and diagram validation.\nAVAILABILITY: The PathVisio-MIM plugin is freely available and works with versions of PathVisio 2.0.11 and later on Windows, Mac OS X and Linux. Information about MIM notation and the MIMML format is available at http://discover.nci.nih.gov/mim. The plugin, along with diagram examples, instructions and Java source code, may be downloaded at http://discover.nci.nih.gov/mim/mim_pathvisio.html.\n",
#     "publisher" : "Bioinformatics (Oxford, England)",
#     "url" : "http://www.ncbi.nlm.nih.gov/pubmed/21636591",
#     "_id" : 1
# },

