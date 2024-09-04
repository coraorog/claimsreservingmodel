"""Simple claims reserving model to predict future claims liabilities based on historical claims data. """
import pandas as pd
import random
import numpy as np


#Generating random insurance data

num_years: int = int(input("Type amount of years for the model."))
first_year: int = int(input("Enter start year."))
years: list[int] = []
start_year = first_year
st_year = first_year

#Generating column labels

for i in range(num_years):
    years.append(i)
    start_year += 1

data: dict[str:list[int]] = {"Accident Year": years}
count: int = num_years

#Organizing insurance data into triangle

for i in range(num_years):
    total: float = 0
    yearly_claim_data: list[float] = []
    for j in range(count):
        total += random.randrange(50,300)
        yearly_claim_data.append(total)
    while len(yearly_claim_data) < num_years:
        yearly_claim_data.append(0)
    data[first_year+1] = yearly_claim_data
    count -= 1
    first_year += 1

claims_df = pd.DataFrame(data)

#transpose table to have data oriented correct way

claims_df = claims_df.transpose()
print(claims_df)

#Calculate development factors for each year
#These factors show how much claims grow from one development period to the next, and they are key to estimating future claims.


devfacs: dict[int: float] = {}
for i in range(1, num_years):
    dev_factor = 0
    for j in range(num_years-i):
        if claims_df.iloc[j, i - 1] != 0:
            dev_factor += claims_df.iloc[j,i]/claims_df.iloc[j,i-1]

    dev_factor = dev_factor / (num_years - i)
    devfacs[i] = dev_factor


#using development factors to project future claims
    
for i in range(num_years+1):
    for j in range(1, num_years):
        if claims_df.iloc[i, j - 1] != 0 and claims_df.iloc[i, j] == 0:
            claims_df.iloc[i,j] = claims_df.iloc[i, j - 1]*devfacs[j]

# Print the updated claims data with projected values
print(claims_df)

# Print development factors to explain how the claims were projected
for year, factor in devfacs.items():
    print(f"Development Factor for Year {year} to {year + 1}: {factor:.2f}")

#Calculate reserves
reserves = {}
for i in range(2,num_years+1):
    x:int = num_years-1
    sums: float = 0
    for j in range(x,num_years):
        sums += claims_df.iloc[i,j]
    x -= 1
    reserves[st_year+ i] = sums
for year, reserve in reserves.items():
    print(f"Accident Year: {year}, Reserve Amount: ${reserve:,.2f}")

    #challenge: how to calculate reserves: before or after filling in table

#Next step: make model stochastic, run monte carlo simulations with variables for interest rates, inflation rates