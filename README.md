# mod3_project


* a. Listing project members

Tina Liu, Zaria Rankine


* b. Dataset

We will be using the BreezoMeter API with hourly Air Quality reports, and the London Borough Demographics Data CSV.
We also used MapBox API for latitude and longitude coordinates for our broughs. We explored the London Borough data first, to determine areas of interest in London, and formed hypotheses around these findings.

https://api.breezometer.com/air-quality/v2/historical/hourly?lat=48.857456&lon=2.354611&key=YOUR_API_KEY&datetime=2019-11-07T14:00:00
https://www.kaggle.com/marshald/london-boroughs#london-borough-profiles-2016%20Data%20set.csv
https://docs.mapbox.com/api/maps/


* c. Goals

We are looking to explore air quality data for different boroughs of London, in an aim to provide insights useful to potential house buyers. We decided our stakeholders would be property websites like Rightmove and Zoopla, as they often provide area guides for their customers being house buyers.

We define air quality using the Air Quality Index (AQI) score from BreezoMeter.

Hypothesis 1:

- H0: Air quality of boroughs in Inner London = Air quality of boroughs in Outer London
- H1: Air quality of boroughs in Inner London != Air quality of boroughs in Outer London

Inner London and Outer London is as defined by the borough dataset.

Hypothesis 2:

- H0: Air quality of borough of interest 1 = Air quality of borough of interest 2
- H1: Air quality of borough of interest 1 > Air quality of borough of interest 2

Areas of interest are defined as:
Boroughs with highest and lowest Greenspace - Havering and City of London

Hypothesis 3:

- H0: Air quality of borough of interest 1 = Air quality of borough of interest 2
- H1: Air quality of borough of interest 1 > Air quality of borough of interest 2

Areas of interest are defined as:
Boroughs with highest and lowest House Prices - 'Kensington and Chelsea' and 'Barking and Dagenham'

Hypothesis 4:

- H0: Air quality of Conservative boroughs = Air quality of Labour boroughs
- H1: Air quality of Conservative boroughs != Air quality of Labour boroughs

Consituency information is given in the borough dataset.


* d. Responsibilities

Tina
- London Borough Data - Load and Clean
- London Borough Data - EDA
- Refactoring Data Cleaning Code
- Refactoring API Call Code
- Mapbox API
- Generating Visualizations
- Hypothesis by group function
- Hypothesis 1, 4


Zaria
- BreezoMeter API check
- London Borough data - EDA
- Refactoring Hypothesis Code
- Generating Visualizations
- Refactoring Visualization Code
- Hypothesis 2, 3, 4

* e. Summary of the files in the repository

- api.py - Functions for calling API
- data_cleaning.py - Functions for cleaning data
- hypothesis_tests.py - Functions for hypothesis testing
- visualizations.py - Functions for visualizations
- hypotheses.ipynb - Hypotheses tests with code and explanations
- Hypothesis_Testing.pdf - Stakeholder presentation
