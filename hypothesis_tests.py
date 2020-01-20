"""
This module is for your final hypothesis tests.
Each hypothesis test should tie to a specific analysis question.

Each test should print out the results in a legible sentence
return either "Reject the null hypothesis" or "Fail to reject the null hypothesis" depending on the specified alpha
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import norm
import math

import api
import data_cleaning as dc
import visualizations as vis
import api

import scipy.stats as stats
from statsmodels.stats.power import TTestIndPower, TTestPower



def generate_datapoints(borough):
    cleaned_data = dc.full_clean()
    call = api.get_place_aqi(cleaned_data, borough,120)
    borough_data = np.asarray(call)
    return borough_data

def sample_mu_std_var(sample):
    mean = np.mean(sample)
    std = np.std(sample)
    var = np.var(sample)
    return mean, std, var

def Cohen_d(sample1, sample2):
    #Calculate Difference
    diff = sample1.mean() - sample2.mean()
    #Calulate shape of arrays
    n1, n2 = len(sample1), len(sample2)
    var1 = sample1.var()
    var2 = sample2.var()
    # Calculate the pooled threshold as shown earlier
    pooled_var = (n1 * var1 + n2 * var2) / (n1 + n2)
    # Calculate Cohen's d statistic
    d = diff / np.sqrt(pooled_var)
    return d

def twosample_tstatistic(sample1, sample2):
    statt = stats.ttest_ind(sample1, sample2, equal_var = False)
    return statt

def print_stats(stat):
    t_stat = stat.statistic
    p_val = stat.pvalue
    print('T-Stat: ',t_stat, ' P-Val: ',p_val)


def normals(mean, std):
    return norm(mean, std)

def evaluate_PDF(rv, x=4):
    # Identify the mean and standard deviation of random variable
    mean = rv.mean()
    std = rv.std()
    # Use numpy to calculate evenly spaced numbers over the specified interval (4 sd) and generate 100 samples.
    xs = np.linspace(mean - x*std, mean + x*std, 100)
    # Calculate the peak of normal distribution i.e. probability density.
    ys = rv.pdf(xs)
    return xs, ys

def compare_pval_alpha(p_val, alpha):
    status = ''
    if p_val > alpha:
        status = "Fail to reject"
    else:
        status = 'Reject'
    return status

def read_aqi24_data():
  """
  This method reads the aqi_24 data (air quality data from last 24hours) from
  csv file in /data folder and return a dataframe

  """

  # RUN THIS ONLY ONCE, afterwards, read_csv
  # dc.aqi_data(borough_data, 24)
  aqi = pd.read_csv('./data/borough_data_cleaned_aqi.csv',index_col=0)

  # after reading the saved aqi data, turn it into a list and calcualte mean and average
  aqi.aqi_24 = aqi.aqi_24.map(lambda x: [int(i) for i in x[1:-1].split(', ')])

  return aqi


def aqi_by_group(aqi,col,group1, group2):
  group1_raw = aqi[aqi[col]==group1].aqi_24.tolist()
  group1_aqi = api.flatten_list(group1_raw)

  group2_raw = aqi[aqi[col]==group2].aqi_24.tolist()
  group2_aqi = api.flatten_list(group2_raw)

  return np.array(group1_aqi), np.array(group2_aqi)


def create_sample_means(data, num = 1000):
  """
  Create a sample mean distribution from given data (np.array format).
  """
  sample_mean = []

  for x in range(num):
    ele = np.random.choice(data, size=50).mean()
    sample_mean.append(ele)

  return np.array(sample_mean)


def welch_t(a, b):

    """ Calculate Welch's t-statistic for two samples. """

    numerator = a.mean() - b.mean()
    denominator = np.sqrt(a.var(ddof=1)/a.size + b.var(ddof=1)/b.size)

    return np.abs(numerator/denominator)

def welch_df(a, b):

    """ Calculate the effective degrees of freedom for two samples. """

    s1 = a.var(ddof=1)
    s2 = b.var(ddof=1)
    n1 = a.size
    n2 = b.size

    numerator = (s1/n1 + s2/n2)**2
    denominator = (s1/ n1)**2/(n1 - 1) + (s2/ n2)**2/(n2 - 1)

    return numerator/denominator


def p_value(a, b, two_sided=False):

    t = welch_t(a, b)
    df = welch_df(a, b)

    p = 1- stats.t.cdf(np.abs(t), df)

    if two_sided:
      return 2*p
    else:
      return p




# ADDTIONAL THINGS THERE ->

def hypothesis_test_group(groupby, group_one, group_two, two_sided = True, alpha = None,
                          sampling = True, sample_size = 1000):
  """
  Use Welch t-test for hypothesis testing with set data but user given col to
  group the data by.

  :param alpha: the critical value of choice
  :return: status, cohen's d
  """
  # Get data by groups for tests
  aqi = read_aqi24_data()
  one, two = aqi_by_group(aqi,groupby,group_one,group_two)
  num = (len(one)+len(two))/2

  # get sample mean if sampling
  if sampling:
    one = create_sample_means(one, sample_size)
    two = create_sample_means(two, sample_size)
    num = sample_size

  print('size of',group_one,len(one))
  print('size of',group_two,len(two))

  # looking at the mean, standard deviation and variance of Inner London vs. Outer London
  print(group_one,' mean, std, var are: ', sample_mu_std_var(one))
  print(group_two,' mean, std, var are: ', sample_mu_std_var(two))

  vis.distplots(one, two)

  t = welch_t(one, two)
  df = welch_df(one, two)
  print('Welch t-stat is', round(t,3),'degree of freedom is', round(df,3))

  p = p_value(one, two, two_sided)
  print('p-value is: ', p)

  status = compare_pval_alpha(p, alpha)

  power_analysis = TTestIndPower()

  coh_d = Cohen_d(one, two)
  power = power_analysis.solve_power(alpha=.01, effect_size=coh_d,
                                      nobs1=num, alternative='two-sided')

  assertion = ''
  if status == 'Fail to reject':
      assertion = 'cannot'
  else:
      assertion = "can"
      # calculations for effect size, power, etc here as well

  print(f'\nBased on the p value of {p} and our aplha of {alpha} we {status.lower()}  the null hypothesis.'
        f'\nDue to these results, we  {assertion} state that there is a difference between {group_one}'
        f'\nand {group_two}')

  if assertion == 'can':
      print(f"with an effect size, cohen's d, of {str(round(coh_d,3))} and power of {power}.")
  else:
      print(".")

  return status, coh_d





