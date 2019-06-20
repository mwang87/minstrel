# views.py
from flask import abort, jsonify, render_template, request, redirect, url_for, send_file, make_response, send_from_directory

from app import app

import os
import csv
import json
import uuid
import requests

@app.route('/', methods=['GET'])
def renderhomepage():
    return render_template('index.html')

@app.route('/mmvec', methods=['POST'])
def process_mmvec():
    #metadata_file = request.files['metadata']

    metabolite_biom_file = request.files['metabolite_biom']
    microbial_biom_file = request.files['microbial_biom']

    uuid_prefix = str(uuid.uuid4())
    
    local_metabolite_biom_filename = os.path.join(app.config['UPLOAD_FOLDER'], uuid_prefix + "_metabolite.biom")
    local_microbial_biom_filename = os.path.join(app.config['UPLOAD_FOLDER'], uuid_prefix + "_microbial.biom")

    metabolite_biom_file.save(local_metabolite_biom_filename)
    microbial_biom_file.save(local_microbial_biom_filename)

    #Running the code
    all_cmd = []

    #Importing
    metabolite_qza = os.path.join(app.config['UPLOAD_FOLDER'], uuid_prefix + "_metabolite.qza")
    microbiome_qza = os.path.join(app.config['UPLOAD_FOLDER'], uuid_prefix + "_microbiom.qza")

    all_cmd.append("qiime tools import --input-path %s --output-path %s --type FeatureTable[Frequency]" % (local_metabolite_biom_filename, metabolite_qza) )
    all_cmd.append("qiime tools import --input-path %s --output-path %s --type FeatureTable[Frequency]" % (local_microbial_biom_filename, microbiome_qza) )

    #Running mmvec
    mmvec_output_directory = os.path.join(app.config['UPLOAD_FOLDER'], uuid_prefix + "_results")

    cmd = "qiime rhapsody mmvec \
	--i-microbes %s \
	--i-metabolites %s \
	--output-dir %s" % (microbiome_qza, metabolite_qza, mmvec_output_directory)
    all_cmd.append(cmd)

    #Outputting to qzv
    conditional_biplot = os.path.join(mmvec_output_directory, "conditional_biplot.qza")
    output_emperor = os.path.join(mmvec_output_directory, "emperor.qzv")

    all_cmd.append("qiime emperor biplot \
	--i-biplot %s \
    --m-sample-metadata-file data/metabolite-metadata.txt \
	--o-visualization %s" % (conditional_biplot, output_emperor))

    for cmd in all_cmd:
        print(cmd)

    for cmd in all_cmd:
        os.system(cmd)

    response_dict = {}

    return json.dumps(response_dict)

"""Custom way to send files back to client"""
@app.route('/cdn/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/heartbeat', methods=['GET'])
def testapi():
    return_obj = {}
    return_obj["status"] = "success"
    return json.dumps(return_obj)
