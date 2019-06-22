# Multi-Omics Integration with GNPS and Rhapsody

To co-analyze metabolomics and microbiome data with Rhapsody, there are several key things to keep in mind:

1. Sample Identifier Consistency - The sample identifiers in the microbiome data and metabolomics data must intersect and match
2. Microbiome Abundances and Taxonomy - Microbiome Data must be processed (or at least available as qiime2 artifacts) with taxonomy assignment performed
3. Metabolomics Abundances and Identifications - Metabolomics molecule abundance/qualitative abundance must be available as qiime2 artifacts. Identifications of the molecules 

This may seem daunting but this guide will make it way more straight-forward. 

## Sample Identifier Consistency

To make sure sample identifiers are consistent between the metabolomics and microbiome data, we must agree on a common name for each sample. This common name can be completely arbitrary, but here we will describe to mechanism to achieve this result. 

Microbiome analysis - In order to assign a particular sample to a sample identifier, we recommend importing the reads into qiime2 with the qiime import command where a manifest is provided. This will enable mapping a fastq file to a given sample name.

TODO: provide link

Metabolomics analysis - When metabolomics analysis is performed at GNPS (either feature based molecular networking or classic molecular networking), a metadata file can be provided. A key column header (sample_name) will allow the renaming of mass spectrometry files (.mzXML or .mzML) to this sample identifier when GNPS automatically outputs the data as a qiime2 qza file. 

TODO: provide link

## Microbiome Abundances and Taxonomy

Rhapsody requires two inputs from the microbiome analysis. 

1. Abundances of microbes across all samples
2. Taxonomic assignments for all OTUs

To produce these files, we recommend processing microbiome data through qiime2 in the conventional way to call OTUs and assign taxonomy. The inputs will simply be a biom table (in qza format) for the microbial abundances and a taxonomy qza to denote the taxa. 

## Metabolomics Abundances and Identifications

Rhapsody requires two inputs from metabolomics analysis. 

1. Abundances of molecules across all samples
2. Identifications of molecules in the study

To produce these files, there are two methods: Feature Based Molecular Networking and Classic Molecular Networking. 

In Feature Based Molecular Networking, feature detection will need to be performed in a tool like MZmine2 (link to documentaiton) and then a molecular network will be run at GNPS. This workflow will provide all the required materials for Rhapsody (provided you corrected entered the metadata file).

In Classic Molecular Networking, simply uploading your mzXML/mzML mass spectrometry files and metadata file (to rename the sample names), it will provide for you the required files for Rhapsody. 

