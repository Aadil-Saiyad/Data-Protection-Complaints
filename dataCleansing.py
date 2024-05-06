# importing pandas package
import pandas as pd
 
# making data frame from csv file
data = pd.read_csv("C:/Users/Aadil/Documents/Uni Year 4/INM450 Individual Project/Data Complaints Master Doc - Test.csv")

# Making the Values Camel Case
data["Decision"]= data["Decision"].str.title()
 
# Converting Date Recieved column to datetime format
data['Date Received'] = pd.to_datetime(data['Date Received'])

# Converting Completed Date column to datetime format
data['Completed Date'] = pd.to_datetime(data['Completed Date'])

# Calculating time delta using the difference of Completed Date and Date Recieved
data["Time Delta"] = data['Completed Date'] - data['Date Received']

data

# Save the changes back to the same CSV file
data.to_csv("C:/Users/Aadil/Documents/Uni Year 4/INM450 Individual Project/Data Complaints Master Doc - Test.csv", index=False)