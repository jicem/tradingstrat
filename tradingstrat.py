# -*- coding: utf-8 -*-
"""
File: tradingstrat.py

Author: John Manigo

This Python code represents my trading strategy, where I buy shares of five stocks
as well as gold and an ETF of gold mining compnaies and print the total cost of
this group of stocks each year, also generating a plot that visualizes the
performance of the group of stocks compared to SPY over the time period the data
is gathered from
"""

import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv("tr_eikon_eod_data.csv")

# Convert 'Date' column to datetime type
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

# Set 'Date' column as index
df.set_index('Date', inplace=True)

# Extract relevant columns
selected_stocks = ['AAPL.O', 'MSFT.O', 'INTC.O', 'AMZN.O', 'GS.N', 'GDX', 'GLD']
stocks = df[selected_stocks]

# Initialize variables to store the sums
sums = []

# Loop through the data to calculate sums at every 261 rows starting with the third one
for i, (index, row) in enumerate(stocks.iterrows()):
    if i == 2 or (i >= 263 and (i - 2) % 261 == 0):
        # Calculate the sum of prices for selected stocks
        row_sum = row.sum()
        sums.append((index, row_sum))
        print(f"At {index.strftime('%Y-%m-%d')}, the sum of prices for selected stocks is: {row_sum}")

# Print the sum in the final row
final_sum = stocks.iloc[2215].sum()
sums.append((df.index[2215], final_sum))
print(f"At {df.index[2215].strftime('%Y-%m-%d')}, the sum of prices for selected stocks is: {final_sum}")

# Calculate the average price of selected stocks
stocks['Average'] = stocks.mean(axis=1)

# Plot the comparison between the SPY price and the average price of selected stocks
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['SPY'], label='SPY')
plt.plot(df.index, stocks['Average'], label='Average of Selected Stocks')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Comparison of SPY and Average Price of Selected Stocks')
plt.ylim(0, 400)
plt.legend()
plt.show()

# Print the sums at specific rows
for date, row_sum in sums:
    print(f"At {date.strftime('%Y-%m-%d')}, the sum of prices for selected stocks is: {row_sum}")