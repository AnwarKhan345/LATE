# Learning with AuToEncoder (LATE) and TRANSfer Learning with AuToEncoder (TRANSLATE)
Due to dropout and other technical limitations in single cell sequencing technologies. Single-cell RNA-seq 
(scRNA-seq) gene expression profile is
highly sparse 
with many zero expression values (typically above 80%, or even 95%). With an Autoencoder traind on 
nonzero values of the data, LATE leverages information of dependence between genes/cells, and recovers the missing values (zeros). With TRANSLATE that allows for transfer learning, the user can train the autoencoder on a reference 
gene expression dataset and then use the weights and biases as initial values for imputing the dataset of interest.

Reference:

Md. Bahadur Badsha, Rui Li, Boxiang Liu, Yang I. Li, Min Xian, Nicholas E. Banovich, Audrey Qiuyan Fu (2020) 
Imputation of single-cell gene expression with an autoencoder neural network. Quantitative Biology 8(1):78-94. https://doi.org/10.1007/s40484-019-0192-7.

Data sets:

Data sets analyzed in the paper are here: https://drive.google.com/drive/folders/1K8JIFLQBT89Z6jp97YojkXBMiluU7WS6.

## Installation
This implementation is written in Python (3.5+) and builds on TensorFlow (1.0-1.4). Additional Python modules needed are:
numpy, pandas, matplotlib, scipy, seaborn, tables, sklearn, MulticoreTSNE

For example, one may use conda or pip to install these modules:
`conda install numpy` or `pip install numpy`

Install `tensorflow` to use CPUs and `tensorflow-gpu` to use GPUs.

## Usage
Note: In the current version of LATE, code described below needs to run where it is stored on your computer.  To do so, go to the folder 'scripts/'
`cd scripts/`
Imputation and analysis will generate folders in the same directory.  Datasets used for imputation or analysis (e.g., the input, the reference, or the ground truth) may be stored elsewhere.
The examples below use two sets of scRNA-seq data, both generated by 10x Genomics.
- Set 1 from human PBMCs.
  - `example.hd5`: 10,000 genes and 10,000 cells.  
  - `example.msk90.hd5`: 10,000 genes and 10,000 cells.  This is generated from masking 90% of the data in `example.hd5`, and is referred to as `PBMC_G949_10K` in our paper.
  - `ref_example.mdk50.hd5`: 10,000 genes and 30,000 cells.  Together with `example.hd5`, they contain the 40,000 cells from 10x Genomics that have labels of cell types.  This data set is used as the reference data and is referred to as reference i) in our paper.
- Set 2 from the large mouse brain scRNA-seq data.  `example_mouse_brain_10x.h5` contains only a small subset of 10,000 genes and 10,000 cells.    
### Example 1: Running LATE
- Imputation: `python example_late.py -mode='late' -infile='../data/example.msk90.hd5'`
  - `example_late.py` reads in the input data, sets parameters and calls function `late_main` to perform imputation.  
  - Default values for imputation and analysis parameters are provided in `global_params.py`, and may be modified in `example_late.py` (for example, see how `example_late.py` specifies a short run).
### Example 2: Analyzing imputation results
- Following Example 1, after running imputation and generating the folder 'step2/', one may run analysis to summarize and visualize imputation results. 
    `python example_analysis.py -mode='analysis' -infile='../data/example.msk90.hd5'`
- In this analysis, the ground truth data exists in `example.hd5`, and is specified in `example_analysis.py`.
### Example 3: Running TRANSLATE
- Step 1: `python example_translate_step1.py -mode='pre-training' -infile='../data/ref_example.mdk50.hd5'`
  - This step runs LATE on the reference data `ref_example.mdk50.hd5`.
  - This step creates folder `step1/` and stores the output.
- Step 2: `python example_translate_step2.py -mode='translate' -infile='../data/example.msk90.hd5'`
  - This step runs LATE on the input data `example.msk90.hd5`.
  - This step creates folder `step2/` and stores the output.
- Note: `example_translate_step1.py` and `example_translate_step2.py` are identical in this example, although the parameters used for training may be specified differently.
### Example 4: Running LATE on the mouse brain data
- A small data set from mouse brain that contains 10,000 genes and 10,000 cells.
- Data in the h5 format and has genes in the rows and cells in the columns.
- Imputation with LATE: `python example_late_10x.py -mode='late' -infile='../data/example_mouse_brain_10x.h5'`
  - Note that the orientation of the input data needs to be specified.
- Result analysis: `python example_analysis_10x.py -mode='analysis' -infile='../data/example_mouse_brain_10x.h5'`
  - Note that the orientation of the input data needs to be specified.
  - Note also that there is no ground truth here, and that the ground truth is set to be the same as the input.

## Additional details
### Mode: 
- `late`:
  - Random initialization;
  - Trains the autoencoder on the input dataset (no reference data);
  - Generates folder `step2/`.
- `pre-training`:
  - Step 1 of TRANSLATE;
  - Random initialization;
  - Trains the autoencoder on the reference dataset.
  - Generates folder `step1/`.
- `translate`:
  - Step 2 of TRANSLATE;
  - Uses the results from `pre-training` as initialization;
  - Trains the autoencoder on the input dataset.
  - Generates folder `step2/`.
- `impute`:
  - Uses results from LATE or TRANSLATE (results that are currently stored in the folder `step2/`);
  - Calculates imputed values for the input dataset without training.
- `analysis`:
  - Uses imputation results in `step2` for summary and visualization;
  - Generates folder `Eval/`.
  
### Input data
- A data matrix of sequencing read counts, with row names (cell IDs) and column names (gene IDs) in one of the following formats:
    - csv: comma seperated values.
    - tsv: tab seperated values.
    - h5: 10x Genomics sparse matrix:
        - https://support.10xgenomics.com/single-cell-gene-expression/datasets
        - https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/advanced/h5_matrices

- The format of input files:
  
  empty|gene1|gene2
  ---|---|---
  cell1|0.392652|0.127627
  cell2|0.377387|0.213198

  In *.csv files, tabs are replaced by commas.
    
- The input data will be transformed with log10(count+1) for imputation.

### Output files

- Imputed data matrix is in the hd5 format and stored in `step2/imputation.step2.hd5`.  
- Values in this matrix have the same layout as the input, and are on the log10(count+1) scale.

### Ground truth
- The ground truth data should also be a matrix of read counts with the same format as the input.  
- When the ground truth does not exist, set it to be the same as the input.  See Example 4.

### Parameters
Default parameters are specified in `global_params.py`.  They may be modified in `example*.py`.  



