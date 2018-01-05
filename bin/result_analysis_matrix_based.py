#!/usr/bin/python
import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
import math
import os
import time
import scimpute

# read cmd
print('reads H.hd5 and M.hd5, then analysis the result')
print('usage: python -u result_analysis.py H.hd5 gene_row/cell_row M.hd5 gene_row/cell_row')
print('H means prediction, M means ground truth')

if len(sys.argv) != 5:
    raise Exception('cmd err')
else:
    print('cmd: ', sys.argv)
    
file_h = str(sys.argv[1]).strip()
file_h_ori = str(sys.argv[2]).strip()
file_m = str(sys.argv[3]).strip()
file_m_ori = str(sys.argv[4]).strip()

# read data
if file_h_ori == 'gene_row':
    H = pd.read_hdf(file_h).transpose()
elif file_h_ori == 'cell_row':
    H = pd.read_hdf(file_h)
else:
    raise Exception('parameter err: h_orientation not correctly spelled')

if file_m_ori == 'gene_row':
    M = pd.read_hdf(file_m).transpose()
elif file_m_ori == 'cell_row':
    M = pd.read_hdf(file_m)
else:
    raise Exception('parameter err: m_orientation not correctly spelled')

# Test mode or not
test_flag = 1
m = 100
n = 200
if test_flag > 0:
    print('in test mode')
    H = H.ix[0:m, 0:n]
    M = M.ix[0:m, 0:n]

# input summary
print('inside this code, matrices are supposed to be cell_row')
print('H:', H.ix[0:3, 0:2])
print('M:', M.ix[0:3, 0:2])
print('H.shape', H.shape)
print('M.shape', M.shape)

# Hist of H
scimpute.hist_df(H, title='H({})'.format(file_h))
scimpute.hist_df(M, title='M({})'.format(file_m))


# Hist Cell/Gene corr
hist = scimpute.gene_corr_hist(H.values, M.values,
                               title="Hist Gene-Corr (H vs M)\n"+file_h+'\n'+file_m,
                               dir='plots'
                               )
hist = scimpute.cell_corr_hist(H.values, M.values,
                               title="Hist Cell-Corr (H vs M)\n"+file_h+'\n'+file_m,
                               dir='plots'
                               )


# Visualization of dfs
print('> Visualization of dfs')
max, min = scimpute.max_min_element_in_arrs([H.values, M.values])
mse2 = ((H.values - M.values) ** 2).mean()
mse2 = round(mse2, 5)
scimpute.heatmap_vis(H.values,
                     title='H: {}'.format(file_h),
                     xlab='genes\nMSE2(H vs M)={}'.format(mse2),
                     ylab='cells', vmax=max, vmin=min,
                     dir='plots')
scimpute.heatmap_vis(M.values,
                     title='M: {}'.format(file_m),
                     xlab='genes',
                     ylab='cells', vmax=max, vmin=min,
                     dir='plots')


# Factors Affecting Gene Prediction
print('Mean and Var are calculated from H')
gene_corr = scimpute.gene_corr_list(M.values, H.values)
gene_mse = scimpute.gene_mse_list(M.values, H.values)
gene_mean_expression = H.sum(axis=0).values / H.shape[1]  # sum for each column
gene_nz_rate = scimpute.gene_nz_rate_list(H.values)
gene_var = scimpute.gene_var_list(H.values)
gene_nzvar = scimpute.gene_nzvar_list(H.values)

scimpute.density_plot(gene_mean_expression, gene_mse,
                      title='Factors, expression vs mse, {}'.format('test'),
                      dir='plots',
                      xlab='gene mean expression',
                      ylab='gene mse')

scimpute.density_plot(gene_mean_expression, gene_corr,
                      title='Factors, expression vs corr, {}'.format('test'),
                      dir='plots',
                      xlab='gene mean expression',
                      ylab='gene corr (NA: -1.1)')

scimpute.density_plot(gene_nz_rate, gene_mse,
                      title='Factors, nz_rate vs mse, {}'.format('test'),
                      dir='plots',
                      xlab='gene nz_rate',
                      ylab='gene mse')

scimpute.density_plot(gene_nz_rate, gene_corr,
                      title='Factors, nz_rate vs corr, {}'.format('test'),
                      dir='plots',
                      xlab='gene nz_rate',
                      ylab='gene corr (NA: -1.1)')

scimpute.density_plot(gene_var, gene_mse,
                      title='Factors, var vs mse, {}'.format('test'),
                      dir='plots',
                      xlab='gene variation',
                      ylab='gene mse')

scimpute.density_plot(gene_var, gene_corr,
                      title='Factors, var vs corr, {}'.format('test'),
                      dir='plots',
                      xlab='gene variation',
                      ylab='gene corr (NA: -1.1)')

scimpute.density_plot(gene_nzvar, gene_mse,
                      title='Factors, nz_var vs mse, {}'.format('test'),
                      dir='plots',
                      xlab='gene nz_variation',
                      ylab='gene mse')

scimpute.density_plot(gene_nzvar, gene_corr,
                      title='Factors, nz_var vs corr, {}'.format('test'),
                      dir='plots',
                      xlab='gene nz_variation',
                      ylab='gene corr (NA: -1.1)')


# # gene MSE
# j = 0
# input_j = H.ix[:, j:j+1].values
# pred_j = h.ix[:, j:j+1].values
# groundTruth_j = M.ix[:, j:j+1].values
#
# mse_j_input = ((pred_j - input_j) ** 2).mean()
# mse_j_groundTruth = ((pred_j - groundTruth_j) ** 2).mean()
#
# matrix MSE

# Clustmap of weights, bottle-neck-activations (slow on GPU, moved to CPU)
# os.system('for file in ./{}/*npy; do python -u weight_visualization.py $file {}; done'.format(p.stage, p.stage))
