import requests
import sys

input_microbial_biom = sys.argv[1]
input_metabolomics_biom = sys.argv[2]

"""Calling remote server to do the calculation"""
SERVER_BASE = "http://localhost:5025"
files = {'microbial_biom': open(input_microbial_biom, 'rb'), \
'metabolite_biom': open(input_metabolomics_biom, 'rb')}

r_post = requests.post(SERVER_BASE + "/mmvec", files=files)
response_dict = r_post.json()

