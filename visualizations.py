"""
This module is for your final visualization code.
One visualization per hypothesis question is required.
A framework for each type of visualization is provided.
"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import data_cleaning as dc
import api
import hypothesis_tests as ht
import visualizations as vis

from scipy import stats
from scipy.stats import norm
from statsmodels.stats.power import TTestIndPower, TTestPower


sns.set_style('whitegrid')

def distplots(sample1, sample2):
    sns.distplot(sample1), sns.distplot(sample2)


def pdf_plot(borough1, borough2, normal_d1, normal_d2):
    #Var 1
    xs, ys = ht.evaluate_PDF(normal_d1)
    plt.plot(xs, ys, label=borough1, linewidth=4, color='#beaed4')
    #Var2
    xs, ys = ht.evaluate_PDF(normal_d2)
    plt.plot(xs, ys, label=borough2, linewidth=4, color='#fdc086')

    plt.xlabel('PDF of AQI in borough1 and borough2')


def power_n_plot(subplots, alpha_arr, e_sizes, axis_limit, marker_size):

  power_analysis = TTestIndPower()
  sns.set_style('darkgrid')

  fig, axes = plt.subplots(ncols=1, nrows=subplots, figsize=(8,5*subplots))
  for n, alpha in enumerate(alpha_arr):
    ax = axes[n]
    power_analysis.plot_power(dep_var="nobs",
                              nobs = np.array(range(2,axis_limit)),
                              effect_size=e_sizes,
                              alpha=alpha,
                              ax=ax)
    ax.set_title('Power of Test for alpha = {}'.format(alpha))
    ax.set_xticks(list(range(0,axis_limit,marker_size)))
    ax.set_yticks(np.linspace(0,1,11))

  return None
