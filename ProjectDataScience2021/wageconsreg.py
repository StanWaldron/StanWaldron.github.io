import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
model = LinearRegression(fit_intercept=True)

# Take in the cleaned data

consumption = pd.read_csv(
    'https://raw.githubusercontent.com/StanWaldron/StanWaldron.github.io/main/h_consumption%20big.csv')

wages = pd.read_csv('https://raw.githubusercontent.com/StanWaldron/StanWaldron.github.io/main/Data/wages.csv')
# Set the axes from the data
x = consumption['Value']
y = wages['Value']

# Create the fit variables for the regression

model.fit(x[:, np.newaxis], y)

xfit = np.linspace(50000, 350000, 246)
yfit = model.predict(xfit[:, np.newaxis])

# Draw the figure, plot teh scatter and plot teh regression line

fig = plt.figure()
plt.scatter(x, y)
plt.plot(xfit, yfit)
plt.xlabel('Consumption', fontsize=10)
plt.ylabel('Wages', fontsize=10)

# Take the values necessary for statistical analysis
# The coefficients
print("Coefficients: \n", model.coef_)
# The mean squared error
print("Mean squared error: %.2f" % mean_squared_error(y, yfit))
# The coefficient of determination: 1 is perfect prediction
print("Coefficient of determination: %.2f" % r2_score(y, yfit))
plt.show()

#  [-2.83063067e-05]
# Mean squared error: 23.58
# Coefficient of determination: 0.12
