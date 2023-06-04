#!/usr/bin/env python
# coding: utf-8

# <img src=https://i.imgur.com/WKQ0nH2.jpg height=350>
# 
# # Setup and Context
# 

# ### Introduction
# 
# Welcome to Boston Massachusetts in the 1970s! Imagine you're working for a real estate development company. Your company wants to value any residential project before they start. You are tasked with building a model that can provide a price estimate based on a home's characteristics like:
# * The number of rooms
# * The distance to employment centres
# * How rich or poor the area is
# * How many students there are per teacher in local schools etc
# 
# <img src=https://i.imgur.com/WfUSSP7.png height=350>
# 
# To accomplish your task you will:
# 
# 1. Analyse and explore the Boston house price data
# 2. Split your data for training and testing
# 3. Run a Multivariable Regression
# 4. Evaluate how your model's coefficients and residuals
# 5. Use data transformation to improve your model performance
# 6. Use your model to estimate a property price

# ### Upgrade plotly (only Google Colab Notebook)
# 
# Google Colab may not be running the latest version of plotly. If you're working in Google Colab, uncomment the line below, run the cell, and restart your notebook server. 

# In[2]:


#%pip install --upgrade plotly


# ###  Import Statements
# 

# In[121]:


import pandas as pd
import numpy as np

import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
# TODO: Add missing import statements
from sklearn.model_selection import train_test_split


# ### Notebook Presentation

# In[4]:


pd.options.display.float_format = '{:,.2f}'.format


# # Load the Data
# 
# The first column in the .csv file just has the row numbers, so it will be used as the index. 

# In[5]:


data = pd.read_csv('boston.csv', index_col=0)


# ### Understand the Boston House Price Dataset
# 
# ---------------------------
# 
# **Characteristics:**  
# 
#     :Number of Instances: 506 
# 
#     :Number of Attributes: 13 numeric/categorical predictive. The Median Value (attribute 14) is the target.
# 
#     :Attribute Information (in order):
#         1. CRIM     per capita crime rate by town
#         2. ZN       proportion of residential land zoned for lots over 25,000 sq.ft.
#         3. INDUS    proportion of non-retail business acres per town
#         4. CHAS     Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
#         5. NOX      nitric oxides concentration (parts per 10 million)
#         6. RM       average number of rooms per dwelling
#         7. AGE      proportion of owner-occupied units built prior to 1940
#         8. DIS      weighted distances to five Boston employment centres
#         9. RAD      index of accessibility to radial highways
#         10. TAX      full-value property-tax rate per $10,000
#         11. PTRATIO  pupil-teacher ratio by town
#         12. B        1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
#         13. LSTAT    % lower status of the population
#         14. PRICE     Median value of owner-occupied homes in $1000's
#         
#     :Missing Attribute Values: None
# 
#     :Creator: Harrison, D. and Rubinfeld, D.L.
# 
# This is a copy of [UCI ML housing dataset](https://archive.ics.uci.edu/ml/machine-learning-databases/housing/). This dataset was taken from the StatLib library which is maintained at Carnegie Mellon University. You can find the [original research paper here](https://deepblue.lib.umich.edu/bitstream/handle/2027.42/22636/0000186.pdf?sequence=1&isAllowed=y). 
# 

# # Preliminary Data Exploration 🔎
# 
# **Challenge**
# 
# * What is the shape of `data`? 
# * How many rows and columns does it have?
# * What are the column names?
# * Are there any NaN values or duplicates?

# In[6]:


data.shape


# In[18]:


data.count()


# In[16]:


data.columns


# In[11]:


data.head()


# In[10]:


data.isna().values.any()


# ## Data Cleaning - Check for Missing Values and Duplicates

# In[12]:


data.duplicated().values.any() # no duplicates


# In[14]:


data.isna().values.any() # no null values


# In[20]:


data.info()


# In[ ]:





# ## Descriptive Statistics
# 
# **Challenge**
# 
# * How many students are there per teacher on average?
# * What is the average price of a home in the dataset?
# * What is the `CHAS` feature? 
# * What are the minimum and the maximum value of the `CHAS` and why?
# * What is the maximum and the minimum number of rooms per dwelling in the dataset?

# In[21]:


data.PTRATIO.mean()


# PTRATIO for students for teacher
# 
# CHAS     Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
# 
# RM for rooms per dwelling

# In[23]:


data.describe()


# ## Visualise the Features
# 
# **Challenge**: Having looked at some descriptive statistics, visualise the data for your model. Use [Seaborn's `.displot()`](https://seaborn.pydata.org/generated/seaborn.displot.html#seaborn.displot) to create a bar chart and superimpose the Kernel Density Estimate (KDE) for the following variables: 
# * PRICE: The home price in thousands.
# * RM: the average number of rooms per owner unit.
# * DIS: the weighted distance to the 5 Boston employment centres i.e., the estimated length of the commute.
# * RAD: the index of accessibility to highways. 
# 
# Try setting the `aspect` parameter to `2` for a better picture. 
# 
# What do you notice in the distributions of the data? 

# #### House Prices 💰

# In[37]:


data.head()


# In[44]:


sns.displot(data=data.PRICE,
            aspect=2,
            bins=50,
            kde=True,
            color='green'
           )
plt.xlabel("Price in $1000\'s")
plt.ylabel("Number of Homes")
plt.title("1970\'s Home Values in Boston")
plt.show()


# #### Distance to Employment - Length of Commute 🚗

# In[48]:


sns.displot(data=data.DIS,
            aspect=2,
            bins=50,
            kde=True,
            color='red'
           )
plt.xlabel("Distance to Employment Centres.")
plt.ylabel("Number of Homes")
plt.title("1970\'s Home Values in Boston")
plt.show()


# #### Number of Rooms

# In[55]:


sns.displot(data=data.RM,
            aspect=2,
            bins=20,
            kde=True,
            color='purple'
           )
plt.xlabel("Distribution of Rooms")
plt.ylabel("Number of Homes")
plt.title("Average nunber of rooms in 1970(Boston)")
plt.show()


# #### Access to Highways 🛣

# In[64]:


sns.displot(data.RAD, 
         bins=50, 
         ec='black', 
         color='#7b1fa2')

plt.xlabel('Accessibility to Highways')
plt.ylabel('Number of Houses')
plt.title("Access to Radial Highway in 1970's(Boston)")
plt.show()


# #### Next to the River? ⛵️
# 
# **Challenge**
# 
# Create a bar chart with plotly for CHAS to show many more homes are away from the river versus next to it. The bar chart should look something like this:
# 
# <img src=https://i.imgur.com/AHwoQ6l.png height=350>
# 
# You can make your life easier by providing a list of values for the x-axis (e.g., `x=['No', 'Yes']`)

# In[85]:


chas = data.CHAS.value_counts()
bar_chart = px.bar(x=['No', 'Yes'],
                   y=chas.values,
                   title='Next to Charles River?',
                   color=chas.values,
                  )

bar_chart.update_layout(xaxis_title='Property Located Next to the River?', 
                  yaxis_title='Number of Homes',
                  coloraxis_showscale=False)
bar_chart.show()


# <img src=https://i.imgur.com/b5UaBal.jpg height=350>

# # Understand the Relationships in the Data

# ### Run a Pair Plot
# 
# **Challenge**
# 
# There might be some relationships in the data that we should know about. Before you run the code, make some predictions:
# 
# * What would you expect the relationship to be between pollution (NOX) and the distance to employment (DIS)? 
# * What kind of relationship do you expect between the number of rooms (RM) and the home value (PRICE)?
# * What about the amount of poverty in an area (LSTAT) and home prices? 
# 
# Run a [Seaborn `.pairplot()`](https://seaborn.pydata.org/generated/seaborn.pairplot.html?highlight=pairplot#seaborn.pairplot) to visualise all the relationships at the same time. Note, this is a big task and can take 1-2 minutes! After it's finished check your intuition regarding the questions above on the `pairplot`. 

# In[91]:


sns.pairplot(data)
plt.show()


# **Challenge**
# 
# Use [Seaborn's `.jointplot()`](https://seaborn.pydata.org/generated/seaborn.jointplot.html) to look at some of the relationships in more detail. Create a jointplot for:
# 
# * DIS and NOX
# * INDUS vs NOX
# * LSTAT vs RM
# * LSTAT vs PRICE
# * RM vs PRICE
# 
# Try adding some opacity or `alpha` to the scatter plots using keyword arguments under `joint_kws`.

# #### Distance from Employment vs. Pollution
# 
# **Challenge**: 
# 
# Compare DIS (Distance from employment) with NOX (Nitric Oxide Pollution) using Seaborn's `.jointplot()`. Does pollution go up or down as the distance increases? 

# In[108]:


with sns.axes_style('darkgrid'):
        sns.jointplot(x=data['DIS'],
                      y=data['NOX'],
                      kind='hex',
                      joint_kws={'alpha':0.5})


# #### Proportion of Non-Retail Industry 🏭🏭🏭 versus Pollution 
# 
# **Challenge**: 
# 
# Compare INDUS (the proportion of non-retail industry i.e., factories) with NOX (Nitric Oxide Pollution) using Seaborn's `.jointplot()`. Does pollution go up or down as there is a higher proportion of industry?

# In[112]:


with sns.axes_style('darkgrid'):
    
    sns.jointplot(x=data['NOX'], 
                  y=data['INDUS'], 
                  height=6,
                  color='darkblue',
                  kind='hex',
                  joint_kws={'alpha':0.5})
plt.show()


# #### % of Lower Income Population vs Average Number of Rooms
# 
# **Challenge** 
# 
# Compare LSTAT (proportion of lower-income population) with RM (number of rooms) using Seaborn's `.jointplot()`. How does the number of rooms per dwelling vary with the poverty of area? Do homes have more or fewer rooms when LSTAT is low?

# In[118]:


with sns.axes_style('darkgrid'):
    sns.jointplot(x=data.LSTAT, 
                  y=data.RM, 
                  kind='hex', 
                  height=7, 
                  color='purple',
                  joint_kws={'alpha':0.5})
plt.show()


# #### % of Lower Income Population versus Home Price
# 
# **Challenge**
# 
# Compare LSTAT with PRICE using Seaborn's `.jointplot()`. How does the proportion of the lower-income population in an area affect home prices?

# In[116]:


with sns.axes_style('darkgrid'):
    sns.jointplot(x=data.LSTAT, 
                  y=data.PRICE, 
                  kind='hex', 
                  height=7, 
                  color='crimson',
                  joint_kws={'alpha':0.5})
plt.show()


# #### Number of Rooms versus Home Value
# 
# **Challenge** 
# 
# Compare RM (number of rooms) with PRICE using Seaborn's `.jointplot()`. You can probably guess how the number of rooms affects home prices. 😊 

# In[119]:


with sns.axes_style('whitegrid'):
  sns.jointplot(x=data.RM, 
                y=data.PRICE, 
                height=7,
                kind='hex',
                color='darkblue',
                joint_kws={'alpha':0.5})
plt.show()


# # Split Training & Test Dataset
# 
# We *can't* use all 506 entries in our dataset to train our model. The reason is that we want to evaluate our model on data that it hasn't seen yet (i.e., out-of-sample data). That way we can get a better idea of its performance in the real world. 
# 
# **Challenge**
# 
# * Import the [`train_test_split()` function](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) from sklearn
# * Create 4 subsets: X_train, X_test, y_train, y_test
# * Split the training and testing data roughly 80/20. 
# * To get the same random split every time you run your notebook use `random_state=10`. This helps us get the same results every time and avoid confusion while we're learning. 
# 
# 
# Hint: Remember, your **target** is your home PRICE, and your **features** are all the other columns you'll use to predict the price. 
# 

# In[126]:


target = data['PRICE']
features = data.drop('PRICE', axis=1)

X_train, X_test, y_train, y_test = train_test_split(features, 
                                                    target, 
                                                    test_size=0.2, 
                                                    random_state=10)


# In[123]:


# % of training set
train_pct = 100*len(X_train)/len(features)
print(f'Training data is {train_pct:.3}% of the total data.')

# % of test data set
test_pct = 100*X_test.shape[0]/features.shape[0]
print(f'Test data makes up the remaining {test_pct:0.3}%.')


# # Multivariable Regression
# 
# In a previous lesson, we had a linear model with only a single feature (our movie budgets). This time we have a total of 13 features. Therefore, our Linear Regression model will have the following form:
# 
# $$ PR \hat ICE = \theta _0 + \theta _1 RM + \theta _2 NOX + \theta _3 DIS + \theta _4 CHAS ... + \theta _{13} LSTAT$$

# ### Run Your First Regression
# 
# **Challenge**
# 
# Use sklearn to run the regression on the training dataset. How high is the r-squared for the regression on the training data?

# In[127]:


regression = LinearRegression()


# In[135]:


regression.fit(X_train, y_train)
rsquared = regression.score(X_train, y_train)
rsquared


# ### Evaluate the Coefficients of the Model
# 
# Here we do a sense check on our regression coefficients. The first thing to look for is if the coefficients have the expected sign (positive or negative). 
# 
# **Challenge** Print out the coefficients (the thetas in the equation above) for the features. Hint: You'll see a nice table if you stick the coefficients in a DataFrame. 
# 
# * We already saw that RM on its own had a positive relation to PRICE based on the scatter plot. Is RM's coefficient also positive?
# * What is the sign on the LSAT coefficient? Does it match your intuition and the scatter plot above?
# * Check the other coefficients. Do they have the expected sign?
# * Based on the coefficients, how much more expensive is a room with 6 rooms compared to a room with 5 rooms? According to the model, what is the premium you would have to pay for an extra room? 

# In[137]:


coef = pd.DataFrame(data=regression.coef_, index=X_train.columns, columns=['Coefficient'])
coef


# In[140]:


coef.loc['RM'].values[0] * 1000 # the price premium is in $


# ### Analyse the Estimated Values & Regression Residuals
# 
# The next step is to evaluate our regression. How good our regression is depends not only on the r-squared. It also depends on the **residuals** - the difference between the model's predictions ($\hat y_i$) and the true values ($y_i$) inside `y_train`. 
# 
# ```
# predicted_values = regr.predict(X_train)
# residuals = (y_train - predicted_values)
# ```
# 
# **Challenge**: Create two scatter plots.
# 
# The first plot should be actual values (`y_train`) against the predicted value values: 
# 
# <img src=https://i.imgur.com/YMttBNV.png height=350>
# 
# The cyan line in the middle shows `y_train` against `y_train`. If the predictions had been 100% accurate then all the dots would be on this line. The further away the dots are from the line, the worse the prediction was. That makes the distance to the cyan line, you guessed it, our residuals 😊
# 
# 
# The second plot should be the residuals against the predicted prices. Here's what we're looking for: 
# 
# <img src=https://i.imgur.com/HphsBsj.png height=350>
# 
# 

# In[142]:


predicted_vals = regression.predict(X_train)
residuals = (y_train - predicted_vals)


# In[146]:


# Original Regression of Actual vs. Predicted Prices
plt.figure(dpi=100)
plt.scatter(x=y_train, y=predicted_vals, c='lightblue', alpha=0.6)
plt.plot(y_train, y_train, color='red')
plt.title(f'Actual vs Predicted Prices: $y _i$ vs $\hat y_i$', fontsize=17)
plt.xlabel('Actual prices 000s $y _i$', fontsize=14)
plt.ylabel('Prediced prices 000s $\hat y _i$', fontsize=14)
plt.show()

# Residuals vs Predicted values
plt.figure(dpi=100)
plt.scatter(x=predicted_vals, y=residuals, c='lightblue', alpha=0.6)
plt.title('Residuals vs Predicted Values', fontsize=17)
plt.xlabel('Predicted Prices $\hat y _i$', fontsize=14)
plt.ylabel('Residuals', fontsize=14)
plt.show()


# Why do we want to look at the residuals? We want to check that they look random. Why? The residuals represent the errors of our model. If there's a pattern in our errors, then our model has a systematic bias.
# 
# We can analyse the distribution of the residuals. In particular, we're interested in the **skew** and the **mean**.
# 
# In an ideal case, what we want is something close to a normal distribution. A normal distribution has a skewness of 0 and a mean of 0. A skew of 0 means that the distribution is symmetrical - the bell curve is not lopsided or biased to one side. Here's what a normal distribution looks like: 
# 
# <img src=https://i.imgur.com/7QBqDtO.png height=400>
# 
# **Challenge**
# 
# * Calculate the mean and the skewness of the residuals. 
# * Again, use Seaborn's `.displot()` to create a histogram and superimpose the Kernel Density Estimate (KDE)
# * Is the skewness different from zero? If so, by how much? 
# * Is the mean different from zero?

# In[150]:


res_mean = round(residuals.mean(), 2)
res_skew = round(residuals.skew(), 2)


# In[153]:


sns.displot(residuals, kde=True, color='blue')
plt.title(f'Residuals Skew ({res_skew}) Mean ({res_mean})')
plt.show()


# ### Data Transformations for a Better Fit
# 
# We have two options at this point: 
# 
# 1. Change our model entirely. Perhaps a linear model is not appropriate. 
# 2. Transform our data to make it fit better with our linear model. 
# 
# Let's try a data transformation approach. 
# 
# **Challenge**
# 
# Investigate if the target `data['PRICE']` could be a suitable candidate for a log transformation. 
# 
# * Use Seaborn's `.displot()` to show a histogram and KDE of the price data. 
# * Calculate the skew of that distribution.
# * Use [NumPy's `log()` function](https://numpy.org/doc/stable/reference/generated/numpy.log.html) to create a Series that has the log prices
# * Plot the log prices using Seaborn's `.displot()` and calculate the skew. 
# * Which distribution has a skew that's closer to zero? 
# 

# In[156]:


price_skew = data['PRICE'].skew()
sns.displot(data['PRICE'], kde='kde', color='green')
plt.title(f'Normal Prices. Skew is {price_skew:.3}')
plt.show()


# In[158]:


y_log = np.log(data['PRICE'])
sns.displot(y_log, kde=True, color='green')
plt.title(f'Log Prices. Skew is {y_log.skew():.3}')
plt.show()


# In[ ]:





# #### How does the log transformation work?
# 
# Using a log transformation does not affect every price equally. Large prices are affected more than smaller prices in the dataset. Here's how the prices are "compressed" by the log transformation:
# 
# <img src=https://i.imgur.com/TH8sK1Q.png height=200>
# 
# We can see this when we plot the actual prices against the (transformed) log prices. 

# In[160]:


plt.figure(dpi=150)
plt.scatter(data.PRICE, np.log(data.PRICE))

plt.title('Mapping the Original Price to a Log Price')
plt.ylabel('Log Price')
plt.xlabel('Actual $ Price in 000s')
plt.show()


# ## Regression using Log Prices
# 
# Using log prices instead, our model has changed to:
# 
# $$ \log (PR \hat ICE) = \theta _0 + \theta _1 RM + \theta _2 NOX + \theta_3 DIS + \theta _4 CHAS + ... + \theta _{13} LSTAT $$
# 
# **Challenge**: 
# 
# * Use `train_test_split()` with the same random state as before to make the results comparable. 
# * Run a second regression, but this time use the transformed target data. 
# * What is the r-squared of the regression on the training data? 
# * Have we improved the fit of our model compared to before based on this measure?
# 

# In[163]:


new_target = np.log(data['PRICE'])
features = data.drop('PRICE', axis=1)
X_train, X_test, log_y_train, log_y_test = train_test_split(features, 
                                                            new_target, 
                                                            test_size=0.2, 
                                                            random_state=10)


# In[164]:


log_regr = LinearRegression()
log_regr.fit(X_train, log_y_train)
log_rsquared = log_regr.score(X_train, log_y_train)

log_predictions = log_regr.predict(X_train)
log_residuals = (log_y_train - log_predictions)

print(f'Training data r-squared: {log_rsquared:.2}')


# In[165]:


# 79 compared to 75


# ## Evaluating Coefficients with Log Prices
# 
# **Challenge**: Print out the coefficients of the new regression model. 
# 
# * Do the coefficients still have the expected sign? 
# * Is being next to the river a positive based on the data?
# * How does the quality of the schools affect property prices? What happens to prices as there are more students per teacher? 
# 
# Hint: Use a DataFrame to make the output look pretty. 

# In[166]:


df_coef = pd.DataFrame(data=log_regr.coef_, index=X_train.columns, columns=['coef'])
df_coef


# In[167]:


# vs coef
coef


# ## Regression with Log Prices & Residual Plots
# 
# **Challenge**: 
# 
# * Copy-paste the cell where you've created scatter plots of the actual versus the predicted home prices as well as the residuals versus the predicted values. 
# * Add 2 more plots to the cell so that you can compare the regression outcomes with the log prices side by side. 
# * Use `indigo` as the colour for the original regression and `navy` for the color using log prices.

# In[168]:


# Graph of Actual vs. Predicted Log Prices
plt.scatter(x=log_y_train, y=log_predictions, c='navy', alpha=0.6)
plt.plot(log_y_train, log_y_train, color='cyan')
plt.title(f'Actual vs Predicted Log Prices: $y _i$ vs $\hat y_i$ (R-Squared {log_rsquared:.2})', fontsize=17)
plt.xlabel('Actual Log Prices $y _i$', fontsize=14)
plt.ylabel('Prediced Log Prices $\hat y _i$', fontsize=14)
plt.show()

# Original Regression of Actual vs. Predicted Prices
plt.scatter(x=y_train, y=predicted_vals, c='indigo', alpha=0.6)
plt.plot(y_train, y_train, color='cyan')
plt.title(f'Original Actual vs Predicted Prices: $y _i$ vs $\hat y_i$ (R-Squared {rsquared:.3})', fontsize=17)
plt.xlabel('Actual prices 000s $y _i$', fontsize=14)
plt.ylabel('Prediced prices 000s $\hat y _i$', fontsize=14)
plt.show()

# Residuals vs Predicted values (Log prices)
plt.scatter(x=log_predictions, y=log_residuals, c='navy', alpha=0.6)
plt.title('Residuals vs Fitted Values for Log Prices', fontsize=17)
plt.xlabel('Predicted Log Prices $\hat y _i$', fontsize=14)
plt.ylabel('Residuals', fontsize=14)
plt.show()

# Residuals vs Predicted values
plt.scatter(x=predicted_vals, y=residuals, c='indigo', alpha=0.6)
plt.title('Original Residuals vs Fitted Values', fontsize=17)
plt.xlabel('Predicted Prices $\hat y _i$', fontsize=14)
plt.ylabel('Residuals', fontsize=14)
plt.show()

# copied from solution :)


# **Challenge**: 
# 
# Calculate the mean and the skew for the residuals using log prices. Are the mean and skew closer to 0 for the regression using log prices?

# In[172]:


log_resid_mean = round(log_residuals.mean(), 2)
log_resid_skew = round(log_residuals.skew(), 2)

sns.displot(log_residuals, 
            kde=True, 
            color='green')
plt.title(f'Log price model: Residuals Skew ({log_resid_skew}) Mean ({log_resid_mean})')
plt.show()

sns.displot(residuals, 
            kde=True, 
            color='red')
plt.title(f'Original model: Residuals Skew ({resid_skew}) Mean ({resid_mean})')
plt.show()


# # Compare Out of Sample Performance
# 
# The *real* test is how our model performs on data that it has not "seen" yet. This is where our `X_test` comes in. 
# 
# **Challenge**
# 
# Compare the r-squared of the two models on the test dataset. Which model does better? Is the r-squared higher or lower than for the training dataset? Why?

# In[174]:


print(f'Original Model r-squared: {regression.score(X_test, y_test):.2}')
print(f'Log Model r-squared: {log_regr.score(X_test, log_y_test):.2}')


# # Predict a Property's Value using the Regression Coefficients
# 
# Our preferred model now has an equation that looks like this:
# 
# $$ \log (PR \hat ICE) = \theta _0 + \theta _1 RM + \theta _2 NOX + \theta_3 DIS + \theta _4 CHAS + ... + \theta _{13} LSTAT $$
# 
# The average property has the mean value for all its charactistics:

# In[175]:


# Starting Point: Average Values in the Dataset
features = data.drop(['PRICE'], axis=1)
average_vals = features.mean().values
property_stats = pd.DataFrame(data=average_vals.reshape(1, len(features.columns)), 
                              columns=features.columns)
property_stats


# **Challenge**
# 
# Predict how much the average property is worth using the stats above. What is the log price estimate and what is the dollar estimate? You'll have to [reverse the log transformation with `.exp()`](https://numpy.org/doc/stable/reference/generated/numpy.exp.html?highlight=exp#numpy.exp) to find the dollar value. 

# In[177]:


estimate_of_log = log_regr.predict(property_stats)[0]
print(f'The log price estimate is ${estimate_of_log:.3}')


# In[179]:


dollar_est = np.exp(estimate_of_log) * 1000
print(f'The property is estimated to be worth ${dollar_est:.6}')


# **Challenge**
# 
# Keeping the average values for CRIM, RAD, INDUS and others, value a property with the following characteristics:

# In[180]:


# Define Property Characteristics
next_to_river = True
nr_rooms = 8
students_per_classroom = 20 
distance_to_town = 5
pollution = data.NOX.quantile(q=0.75) # high
amount_of_poverty =  data.LSTAT.quantile(q=0.25) # low


# In[182]:


# Solution:
property_stats['RM'] = nr_rooms
property_stats['PTRATIO'] = students_per_classroom
property_stats['DIS'] = distance_to_town

if next_to_river:
    property_stats['CHAS'] = 1
else:
    property_stats['CHAS'] = 0

property_stats['NOX'] = pollution
property_stats['LSTAT'] = amount_of_poverty


# In[183]:


log_estimate = log_regr.predict(property_stats)[0]
print(f'The log price estimate is ${log_estimate:.3}')

dollar_est = np.e**log_estimate * 1000
print(f'The property is estimated to be worth ${dollar_est:.6}')


# In[ ]:




