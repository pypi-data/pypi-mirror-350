# qdesc - Quick and Easy Descriptive Analysis
![Package Version](https://img.shields.io/badge/version-0.1.9.2-pink)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License: GPL v3.0](https://img.shields.io/badge/license-GPL%20v3.0-blue)

## Installation
```sh
pip install qdesc
```

## Overview
Qdesc is a package for quick and easy descriptive analysis. It is a powerful Python package designed for quick and easy descriptive analysis of quantitative data. It provides essential statistics like mean and standard deviation for normal distribution and median and raw median absolute deviation for skewed data. With built-in functions for frequency distributions, users can effortlessly analyze categorical variables and export results to a spreadsheet. The package also includes a normality check dashboard, featuring Anderson-Darling statistics and visualizations like histograms and Q-Q plots. Whether you're handling structured datasets or exploring statistical trends, qdesc streamlines the process with efficiency and clarity.

## Creating a sample dataframe
```python
import pandas as pd
import numpy as np

# Create sample data
data = {
    "Age": np.random.randint(18, 60, size=15),  # Continuous variable
    "Salary": np.random.randint(30000, 120000, size=15),  # Continuous variable
    "Department": np.random.choice(["HR", "Finance", "IT", "Marketing"], size=15),  # Categorical variable
    "Gender": np.random.choice(["Male", "Female"], size=15),  # Categorical variable
}
# Create DataFrame
df = pd.DataFrame(data)
```

## qd.desc Function
The function qd.desc(df) generates the following statistics:
* count - number of observations
* mean - measure of central tendency for normal distribution	
* std - measure of spread for normal distribution
* median - measure of central tendency for skewed distributions or those with outliers
* MAD - measure of spread for skewed distributions or those with outliers; this is manual Median Absolute Deviation (MAD) which is more robust when dealing with non-normal distributions.
* min - lowest observed value
* max - highest observed value	
* AD_stat	- Anderson - Darling Statistic
* 5% crit_value - critical value for a 5% Significance Level	
* 1% crit_value - critical value for a 1% Significance Level

```python
import qdesc as qd
qd.desc(df)

| Variable | Count | Mean  | Std Dev | Median | MAD   | Min   | Max    | AD Stat | 5% Crit Value |
|----------|-------|-------|---------|--------|-------|-------|--------|---------|---------------|
| Age      | 15.0  | 37.87 | 13.51   | 38.0   | 12.0  | 20.0  | 59.0   | 0.41    | 0.68          |
| Salary   | 15.0  | 72724 | 29483   | 67660  | 26311 | 34168 | 119590 | 0.40    | 0.68          |
```



## qd.grp_desc Function
This function, qd.grp_desc(df, "Continuous Var", "Group Var") creates a table for descriptive statistics similar to the qd.desc function but has the measures
presented for each level of the grouping variable. It allows one to check whether these measures, for each group, are approximately normal or not. Combining it
with qd.normcheck_dashboard allows one to decide on the appropriate measure of central tendency and spread.

```python
import qdesc as qd
qd.grp_desc(df, "Salary", "Gender")

| Gender  | Count | Mean  -   | Std Dev   | Median   | MAD      | Min    | Max     | AD Stat | 5% Crit Value |
|---------|-------|-----------|-----------|----------|----------|--------|---------|---------|---------------|
| Female  | 7     | 84,871.14 | 32,350.37 | 93,971.0 | 25,619.0 | 40,476 | 119,590 | 0.36    | 0.74          |
| Male    | 8     | 62,096.12 | 23,766.82 | 60,347.0 | 14,278.5 | 34,168 | 106,281 | 0.24    | 0.71          |
```


## qd.freqdist Function
Run the function qd.freqdist(df, "Variable Name") to easily create a frequency distribution for your chosen categorical variable with the following:
* Variable Levels (i.e., for Sex Variable: Male and Female)
* Counts - the number of observations
* Percentage - percentage of observations from total.

```python
import qdesc as qd
qd.freqdist(df, "Department")

| Department | Count | Percentage |
|------------|-------|------------|
| IT         | 5     | 33.33     |
| HR         | 5     | 33.33     |
| Marketing  | 3     | 20.00     |
| Finance    | 2     | 13.33     |
```



## qd.freqdist_a Function
Run the function qd.freqdist_a(df, ascending = FALSE) to easily create frequency distribution tables, arranged in descending manner (default) or ascending (TRUE), for all the categorical variables in your data frame. The resulting table will include columns such as:
* Variable levels (i.e., for Satisfaction: Very Low, Low, Moderate, High, Very High) 
* Counts - the number of observations
* Percentage - percentage of observations from total.

```python
import qdesc as qd
qd.freqdist_a(df)

| Column     | Value     | Count | Percentage |
|------------|----------|-------|------------|
| Department | IT       | 5     | 33.33%     |
| Department | HR       | 5     | 33.33%     |
| Department | Marketing| 3     | 20.00%     |
| Department | Finance  | 2     | 13.33%     |
| Gender     | Male     | 8     | 53.33%     |
| Gender     | Female   | 7     | 46.67%     |
```



## qd.freqdist_to_excel Function
Run the function qd.freqdist_to_excel(df, "Filename.xlsx", ascending = FALSE ) to easily create frequency distribution tables, arranged in descending manner (default) or ascending (TRUE), for all  the categorical variables in your data frame and SAVED as separate sheets in the .xlsx File. The resulting table will include columns such as:
* Variable levels (i.e., for Satisfaction: Very Low, Low, Moderate, High, Very High) 
* Counts - the number of observations
* Percentage - percentage of observations from total.

```python
import qdesc as qd
qd.freqdist_to_excel(df, "Results.xlsx")

Frequency distributions written to Results.xlsx
```

## qd.normcheck_dashboard Function
Run the function qd.normcheck_dashboard(df) to efficiently check each numeric variable for normality of its distribution. It will compute the Anderson-Darling statistic and create visualizations (i.e., qq-plot, histogram, and boxplots) for checking whether the distribution is approximately normal.

```python
import qdesc as qd
qd.normcheck_dashboard(df)
```
![Descriptive Statistics](https://raw.githubusercontent.com/Dcroix/qdesc/refs/heads/main/qd.normcheck_dashboard.png)


## License
This project is licensed under the GPL-3 License. See the LICENSE file for more details.

## Acknowledgements
Acknowledgement of the libraries used by this package...

### Pandas
Pandas is distributed under the BSD 3-Clause License, pandas is developed by Pandas contributors. Copyright (c) 2008-2024, the pandas development team All rights reserved.
### NumPy
NumPy is distributed under the BSD 3-Clause License, numpy is developed by NumPy contributors. Copyright (c) 2005-2024, NumPy Developers. All rights reserved.
### SciPy
SciPy is distributed under the BSD License, scipy is developed by SciPy contributors. Copyright (c) 2001-2024, SciPy Developers. All rights reserved.





