import requests
import sys

input_microbial_qza = sys.argv[1]
input_metabolomics_qza = sys.argv[2]

input_microbial_metadata = sys.argv[3]
input_metabolomics_metadata = sys.argv[4]

"""Calling remote server to do the calculation"""
SERVER_BASE = "http://localhost:5025"
files = {'microbial_qza': open(input_microbial_qza, 'rb'), \
'metabolite_qza': open(input_metabolomics_qza, 'rb'), \
'microbial_metadata': open(input_microbial_metadata, 'rb'), \
'metabolite_metadata': open(input_metabolomics_metadata, 'rb'), \
}

r_post = requests.post(SERVER_BASE + "/mmvec", files=files)
open('rhapsody_results.tgz', 'wb').write(r_post.content)


