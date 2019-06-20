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
    metabolite_metadata_file = request.files['metabolite_metadata']
    microbial_metadata_file = request.files['microbial_metadata']

    uuid_prefix = str(uuid.uuid4())
    
    
    local_metabolite_metadata_filename = os.path.join(app.config['UPLOAD_FOLDER'], uuid_prefix + "_metabolite.metadata")
    local_microbial_metadata_filename = os.path.join(app.config['UPLOAD_FOLDER'], uuid_prefix + "_microbial.metadata")

    


    metabolite_metadata_file.save(local_metabolite_metadata_filename)
    microbial_metadata_file.save(local_microbial_metadata_filename)

    #Running the code
    all_cmd = []

    #Importing
    metabolite_qza = os.path.join(app.config['UPLOAD_FOLDER'], uuid_prefix + "_metabolite.qza")
    microbiome_qza = os.path.join(app.config['UPLOAD_FOLDER'], uuid_prefix + "_microbiom.qza")

    if "metabolite_biom" in request.files:
        metabolite_biom_file = request.files['metabolite_biom']
        microbial_biom_file = request.files['microbial_biom']
        local_metabolite_biom_filename = os.path.join(app.config['UPLOAD_FOLDER'], uuid_prefix + "_metabolite.biom")
        local_microbial_biom_filename = os.path.join(app.config['UPLOAD_FOLDER'], uuid_prefix + "_microbial.biom")
        metabolite_biom_file.save(local_metabolite_biom_filename)
        microbial_biom_file.save(local_microbial_biom_filename)

        all_cmd.append("qiime tools import --input-path %s --output-path %s --type FeatureTable[Frequency]" % (local_metabolite_biom_filename, metabolite_qza) )
        all_cmd.append("qiime tools import --input-path %s --output-path %s --type FeatureTable[Frequency]" % (local_microbial_biom_filename, microbiome_qza) )
    elif "metabolite_qza" in request.files:
        metabolite_qza_file = request.files['metabolite_qza']
        microbial_qza_file = request.files['microbial_qza']

        metabolite_qza_file.save(metabolite_qza)
        microbial_qza_file.save(microbiome_qza)

    #Running mmvec
    mmvec_output_directory = os.path.join(app.config['UPLOAD_FOLDER'], uuid_prefix + "_results")

    LATENT_DIM = 5
    LEARNING_RATE = 0.001
    EPOCHS = 10
    
    cmd = "qiime rhapsody mmvec \
    --p-latent-dim %d \
    --p-learning-rate %f \
    --p-epochs %d \
	--i-microbes %s \
	--i-metabolites %s \
	--output-dir %s" % (LATENT_DIM, LEARNING_RATE, EPOCHS, microbiome_qza, metabolite_qza, mmvec_output_directory)
    all_cmd.append(cmd)

    #Outputting to qzv
    conditional_biplot = os.path.join(mmvec_output_directory, "conditional_biplot.qza")
    output_emperor = os.path.join(mmvec_output_directory, "emperor.qzv")

    all_cmd.append("qiime emperor biplot \
	--i-biplot %s \
    --m-sample-metadata-file %s \
	--m-feature-metadata-file %s \
	--o-visualization %s \
    --p-ignore-missing-samples" % (conditional_biplot, local_metabolite_metadata_filename, local_microbial_metadata_filename, output_emperor))

    for cmd in all_cmd:
        print(cmd)

    for cmd in all_cmd:
        os.system(cmd)

    #zipping up results
    results_zip_filename = microbiome_qza = os.path.join(app.config['UPLOAD_FOLDER'], uuid_prefix + "_results.tgz")
    os.system("tar -czvf %s %s" % (results_zip_filename, mmvec_output_directory))

    return send_file(results_zip_filename, as_attachment=True, attachment_filename="rhapsody.tgz", cache_timeout=5)
    
"""Custom way to send files back to client"""
@app.route('/cdn/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/heartbeat', methods=['GET'])
def testapi():
    return_obj = {}
    return_obj["status"] = "success"
    return json.dumps(return_obj)
