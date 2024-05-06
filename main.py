# Import the Taipy Library and Packages
# (https://docs.taipy.io/en/release-2.2/manuals/reference/pkg_taipy.gui/)
from taipy.gui import Gui, notify, State, get_user_content_url, Markdown
import taipy.gui.builder as tgb

# Importing pandas Library
# (https://pandas.pydata.org/docs/)
import pandas as pd

# Importing calander module for temporal pocesses
# (https://docs.python.org/3/library/calendar.html)
import calendar

# Importing JSON module for GDPR compliance advisor
# (https://docs.python.org/3/library/json.html)
import json

# Importing Regular Expression module for GDPR compliance advisor
# (https://docs.python.org/3/library/re.html)
import re

# Importing MinMaxScaler Estimator provided by sklearn for the Risks calculations
# (https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html)
from sklearn.preprocessing import MinMaxScaler

# Importing IO module for the use of the buffer for the plotly sankey diagram
# (https://docs.python.org/3/library/io.html)
import io


##### Dataset file reading #####

# Importing the ICO Master Dataset
def get_data(path_to_csv: str):
    dataset = pd.read_csv(path_to_csv)
    return dataset
path_to_csv = "DataComplaintsMasterDoc.csv"
dataset = get_data(path_to_csv)

sankey = "sankey.png"

##### Temporal Data #####

# Converting Date Recieved column to datetime format using pandas library 
dataset['Date Received'] = pd.to_datetime(dataset['Date Received'], dayfirst=True, format='mixed')

# Converting Completed Date column to datetime format using pandas library 
dataset['Completed Date'] = pd.to_datetime(dataset['Completed Date'], dayfirst=True, format='mixed')

# Calculating the difference between Date Recieved and Completed Date to get the Time Delta
dataset["Time Delta"] = (dataset['Completed Date'] - dataset['Date Received']).dt.days


##### Temporal Chart Data ######

# Aggregating the Date Recieved column by Years for the Difference in decisions chart
dataset['YearFilter'] = ((dataset['Date Received']).dt.year).apply(str)

# Linking the complaints to days of the week for the Number of complaints by day for each sector heatmap chart
dataset['DayName'] = ((dataset['Date Received']).dt.day_name())

# Linking the complaints to months of the year for the Number of complaints by day for each sector heatmap chart
dataset['MonthName'] = ((dataset['Date Received']).dt.month_name())


##### GDPR Compliance Advisor #####

# Open JSON file for the GDPR compliance advisor recommendations page
jsonFile = open ('recommendations.json')
recommendations = json.load(jsonFile)
recommendationsList = recommendations['recommendations']['article'] 

# Group the dataset by sector and sub sector and get the most common primary reason for each
# Lambda counts the number of each primary reason and selects the three most common ones
common_decisions = dataset.groupby(['Sector', 'Sub Sector'])['Decision Primary Reason'].agg(lambda x: x.value_counts().nlargest(3).index.tolist()).reset_index()

# Convert the processed data into a suitable format for the GUI (e.g., nested dictionaries)
decision_dict = {row['Sector']: {} for index, row in common_decisions.iterrows()}
for index, row in common_decisions.iterrows():
    decision_dict[row['Sector']][row['Sub Sector']] = row['Decision Primary Reason']

# Initial values
sector_list = list(decision_dict.keys())
initial_sector = sector_list[0]
initial_sub_sector = list(decision_dict[initial_sector].keys())[0]

# Class that provides sectors with a constructor that initialises sectorName attribute
class Sector:
    def __init__(self,sectorName): 
        self.sectorName = sectorName
sectors = []

# Iterate over the list of sectors and adds them to the sectors list
for sector in sector_list:
    sectors.append(Sector(sector))
sector_sel = sectors [0]

# Class that provides subsectors with a constructor that initialises subsectorName attribute
class SubSector:
    def __init__(self, subSectorName, decisionPrimaryReason, reason2=None, reason3=None): 
        self.subSectorName = subSectorName
        self.decisionPrimaryReason = decisionPrimaryReason
        self.reason2 = reason2
        self.reason3 = reason3
# Initialise the list to store the subSector objects.
subSectors = []

# Sets initial sector and subsector
sector = "Central Government"
subSectors_list = decision_dict [sector].items()

# Loop through the subsector list and append them to the subSectors list
for subSectorName, reasons in subSectors_list:
    primaryReason = reasons[0] if len(reasons) > 0 else None
    reason2 = reasons[1] if len(reasons) > 1 else None
    reason3 = reasons[2] if len(reasons) > 2 else None
    subSectors.append(SubSector(subSectorName, primaryReason, reason2, reason3))
# Select the first subsector
subSector_sel = subSectors [0]

# Loads initial recommendation
for article in recommendationsList:

    # Loop through the recommendation list and match the subsector's reasons with the article identifiers.
    if article['articleIdentifier'] == subSectors[0].decisionPrimaryReason:
        found = True

        # Set variables for the first reason
        articleIdentifier = article['articleIdentifier']
        articleDescription = article['articleDescription']
        articleRecommendations = article['recommendations']
        articleRecommendations2 = article['recommendations2']
        articleRecommendations3 = article['recommendations3']
    elif article['articleIdentifier'] == subSectors[0].reason2:
        found = True
        # Set variables for the second reason
        article2Identifier = article['articleIdentifier']
        article2Description = article['articleDescription']
        article2Recommendations = article['recommendations']
        article2Recommendations2 = article['recommendations2']
        article2Recommendations3 = article['recommendations3']
    elif article['articleIdentifier'] == subSectors[0].reason3:
        found = True
        # Set variables for the third reason
        article3Identifier = article['articleIdentifier']
        article3Description = article['articleDescription']
        article3Recommendations = article['recommendations']
        article3Recommendations2 = article['recommendations2']
        article3Recommendations3 = article['recommendations3']

# Loads subsector into page
def startSubSectorSelection(state, var_value):
    subSectors = []
    sector = var_value.sectorName
    subSectors_list = decision_dict[sector].items()

    for subSector in subSectors_list:
        name = subSector[0]
        try:
            detail_1 = subSector[1][0]
            detail_2 = subSector[1][1]
            detail_3 = subSector[1][2]
        except IndexError as e:
            # If details are missing and set them to None
            if len(subSector[1]) == 0:
                detail_1 = None
                detail_2 = None
                detail_3 = None
            elif len(subSector[1]) == 1:
                detail_2 = None
                detail_3 = None
            elif len(subSector[1]) == 2:
                detail_3 = None

        # Append the SubSector with details handled by the try-except block
        subSectors.append(SubSector(name, detail_1, detail_2, detail_3))

    # Select the first subSector if the list is not empty, else None
    subSector_sel = subSectors[0] if subSectors else None
    state.subSectors = subSectors
    state.selectedSubSector = subSector_sel

#print (decision_dict)

# Default event handler from Taipy
def on_change(state, var_name, var_value):
    #print (var_name)

    # Starting company selection change
    if var_name == "selected_companyname":
        startCompanySelection(state, var_value)

    # Starting subsector selection change
    if var_name == "sector_sel":
        startSubSectorSelection (state, var_value)

    # Starting article change
    elif var_name == "subSector_sel":
        getArticleFromJson(state, var_value)

# Finds the company and updates the table for Risks Page
def startCompanySelection(state, var_value):
    updated = filter_df_by_company(var_value)
    state.data_merged_filtered = updated

# Finds the article and prints to page
def getArticleFromJson(state, var_value):
    print(var_value.decisionPrimaryReason)
    print(var_value.reason2)
    print(var_value.reason3)

    # Initialize all state variables related to articles
    state.articleIdentifier = state.articleRecommendations = state.articleRecommendations2 = state.articleRecommendations3 = ''
    state.articleDescription = 'Not Found'

    state.article2Identifier = state.article2Recommendations = state.article2Recommendations2 = state.article2Recommendations3 = ''
    state.article2Description = 'Not Found'

    state.article3Identifier = state.article3Recommendations = state.article3Recommendations2 = state.article3Recommendations3 = ''
    state.article3Description = 'Not Found'

    # Go through recommendations list to find the matching articles
    for article in recommendationsList:
        # First article
        if article['articleIdentifier'] == var_value.decisionPrimaryReason:
            state.articleIdentifier = article['articleIdentifier']
            state.articleDescription = article['articleDescription']
            state.articleRecommendations = article.get('recommendations', '')
            state.articleRecommendations2 = article.get('recommendations2', '')
            state.articleRecommendations3 = article.get('recommendations3', '')
        # Second article
        elif article['articleIdentifier'] == var_value.reason2:
            state.article2Identifier = article['articleIdentifier']
            state.article2Description = article['articleDescription']
            state.article2Recommendations = article.get('recommendations', '')
            state.article2Recommendations2 = article.get('recommendations2', '')
            state.article2Recommendations3 = article.get('recommendations3', '')
        # Third article
        elif article['articleIdentifier'] == var_value.reason3:
            state.article3Identifier = article['articleIdentifier']
            state.article3Description = article['articleDescription']
            state.article3Recommendations = article.get('recommendations', '')
            state.article3Recommendations2 = article.get('recommendations2', '')
            state.article3Recommendations3 = article.get('recommendations3', '')

    # Handle case when primary article is not found using regex
    if state.articleDescription == 'Not Found':
        match = re.search(r'Art \d+', var_value.decisionPrimaryReason)
        if match:
            for article in recommendationsList:
                if article['articleIdentifier'] == match.group(0):
                    state.articleIdentifier = article['articleIdentifier']
                    state.articleDescription = article['articleDescription']
                    state.articleRecommendations = article.get('recommendations', '')
                    state.articleRecommendations2 = article.get('recommendations2', '')
                    state.articleRecommendations3 = article.get('recommendations3', '')

    # Print an error message if no articles were found
    if state.articleDescription == 'Not Found' and state.article2Description == 'Not Found' and state.article3Description == 'Not Found':
        print("No articles were found matching the given criteria.")


##### Stacked barchart settings #####

def taken(row):
    if (row["Decision"].title() == "Informal Action Taken"):
        return 1
    else:
        return 0
    return 0

def not_taken(row):
    if (row["Decision"].title() == "No Further Action"):
        return 1
    else:
        return 0
    return 0

dataset['Decision (Action Taken)'] = dataset.apply(taken, axis=1)
dataset['Decision (No Action Taken)'] = dataset.apply(not_taken, axis=1)
layout={ "barmode": "stack" }


##### Risk Factor data #####

# Group the dataset by sector and calculate the sum of action taken and no action taken decisions
temp_data_1 = dataset.groupby(['Sector']).agg({'Decision (Action Taken)':'sum', 'Decision (No Action Taken)':'sum'}).reset_index()
temp_data_1["Total Decisions"] = temp_data_1['Decision (Action Taken)'] + temp_data_1['Decision (No Action Taken)']
temp_data_1["Sector Risk Factor"] = (temp_data_1['Decision (Action Taken)'] / (temp_data_1['Decision (Action Taken)'] + temp_data_1['Decision (No Action Taken)']))

# Group the dataset by decision articles and calculate the sum of action taken and no action taken decisions
temp_data_2 = dataset.groupby(['Decision Articles']).agg({'Decision (Action Taken)':'sum', 'Decision (No Action Taken)':'sum'}).reset_index()
temp_data_2["Total Decisions"] = temp_data_2['Decision (Action Taken)'] + temp_data_2['Decision (No Action Taken)']
temp_data_2["Article Risk Factor"] = (temp_data_2['Decision (Action Taken)'] / (temp_data_2['Decision (Action Taken)'] + temp_data_2['Decision (No Action Taken)']))

# Group the dataset by subsector and calculate the sum of action taken and no action taken decisions
temp_data_3 = dataset.groupby(['Sub Sector']).agg({'Decision (Action Taken)':'sum', 'Decision (No Action Taken)':'sum'}).reset_index()
temp_data_3["Total Decisions"] = temp_data_3['Decision (Action Taken)'] + temp_data_3['Decision (No Action Taken)']
temp_data_3["Sub Sector Risk Factor"] = (temp_data_3['Decision (Action Taken)'] / (temp_data_3['Decision (Action Taken)'] + temp_data_3['Decision (No Action Taken)']))

# Group the dataset by number of times a complaint is submitted against a specific organisation and calculate the sum of action taken and no action taken decisions
temp_data_4 = dataset.groupby(['Submitted About Account']).agg({'Decision (Action Taken)':'sum', 'Decision (No Action Taken)':'sum'}).reset_index()
temp_data_4["Total Decisions"] = temp_data_4['Decision (Action Taken)'] + temp_data_4['Decision (No Action Taken)']
temp_data_4["Account Risk Factor"] = (temp_data_4['Decision (Action Taken)'] / (temp_data_4['Decision (Action Taken)'] + temp_data_4['Decision (No Action Taken)']))

# Setting the risk factor for each group
temp_data_1 = temp_data_1[['Sector', 'Sector Risk Factor']]
temp_data_2 = temp_data_2[['Decision Articles', 'Article Risk Factor']]
temp_data_3 = temp_data_3[['Sub Sector', 'Sub Sector Risk Factor']]
temp_data_4 = temp_data_4[['Submitted About Account', 'Account Risk Factor']]
company_data = dataset

# Merging the groups
data_merged = pd.merge(company_data,temp_data_1,left_on='Sector',right_on='Sector')
data_merged = pd.merge(data_merged,temp_data_2,left_on='Decision Articles',right_on='Decision Articles')
data_merged = pd.merge(data_merged,temp_data_3,left_on='Sub Sector',right_on='Sub Sector')
data_merged = pd.merge(data_merged,temp_data_4,left_on='Submitted About Account',right_on='Submitted About Account')

# Calculates the total risk factor by averaging the risk factors from all categories and multiplying by 100 to get a percentage
data_merged["Total Risk Factor"] = ((data_merged["Account Risk Factor"] + data_merged["Sub Sector Risk Factor"] + data_merged["Sector Risk Factor"] + data_merged["Article Risk Factor"])/4)*100

# Function to capitalise the first letter of each word in company names to reduce duplicates
def process_string(string):
    return string.title()
data_merged['Submitted About Account'] = data_merged['Submitted About Account'].apply(process_string)

# Sort the dataframe by the 'Submitted About Account' column
data_merged = data_merged.sort_values(by='Submitted About Account')

# Selects the first company name
unique_companyname = data_merged['Submitted About Account'].unique().tolist()
selected_companyname = unique_companyname[0]

# Filter the DataFrame to include only data related to the selected company
data_merged_filtered = data_merged[data_merged["Submitted About Account"] == selected_companyname]

# Function to define the selected company name
def filter_df_by_company(selected_companyname):
    return data_merged[data_merged['Submitted About Account'] == selected_companyname]


##### MinMaxScaler Use ##### 

# Setting the range of normalisation
scaler = MinMaxScaler(feature_range=(1, 100))
data_merged['Scaled Risk Factor'] = scaler.fit_transform(data_merged['Total Risk Factor'].values.reshape(-1,1)) 
data_merged[["Scaled Risk Factor"]] = data_merged[["Scaled Risk Factor"]].round(2)
data_merged_filtered = data_merged[["Case Reference", "Submitted About Account" ,"Date Received", "Completed Date", "Sector", "Sub Sector", "Decision Primary Reason", "Decision", "Decision Detail2", "Scaled Risk Factor"]]

# Setting the colour depending on percentage
def risk_style(_1, value, _2, _3, _4):
    if value < 25:
        return "green-cell"
    elif value >= 25 and value < 50:
         return "yellow-cell"
    elif value >= 50 and value < 75:
         return "orange-cell"
    else:
        return "red-cell"


##### Barchart for complaints / sector #####
dataset_2 = dataset.groupby(['Sector']).size().reset_index(name='Count').sort_values(by=['Count'], ascending=False)


##### Piechart for overall decisions #####
dataset_3 = dataset.groupby(['Decision']).size().reset_index(name='Count')


##### Linechart for complaints submitted over time #####
dataset_6 = dataset.groupby(['Date Received']).size().reset_index(name='Count').sort_values(by=['Date Received'], ascending=True)


##### Calculating the average time for a complaint to be processed #####
dataset_12 = dataset.groupby(['Sector'])['Time Delta'].mean().reset_index(name='Time Delta').sort_values(by=['Time Delta'], ascending=False)
dataset_timedelta = dataset


##### Barchart for complaints / subsector #####
dataset_14 = dataset.groupby(['Sub Sector']).size().reset_index(name='Count').sort_values(by=['Count'], ascending=False)
dataset_14 = dataset_14[dataset_14['Sub Sector'] != 'Unassigned']
dataset_14 = dataset_14.query("Count > 2600")


##### Shortened Piechart of Decision Articles #####
dataset_4_temp = dataset.groupby(['Decision Articles']).size().reset_index(name='Count')
dataset_4_temp = dataset_4_temp[dataset_4_temp['Decision Articles'] != 'Unassigned']
small_values = dataset_4_temp.query("Count < 500")
small_values_sum = small_values['Count'].sum()
small_values_row = pd.DataFrame({'Decision Articles': 'Other','Count': [small_values_sum]})
dataset_15 = pd.concat([dataset_4_temp, small_values_row])
dataset_15 = dataset_15.query("Count > 500")

##### Shortened Piechart of Decision Primary Reason #####
decisonPrimaryReason_data = dataset.groupby(['Decision Primary Reason']).size().reset_index(name='Count')
decisonPrimaryReason_data = decisonPrimaryReason_data[decisonPrimaryReason_data['Decision Primary Reason'] != 'Unassigned']
small_values = decisonPrimaryReason_data.query("Count < 500")
small_values_sum = small_values['Count'].sum()
small_values_row = pd.DataFrame({'Decision Primary Reason': 'Other','Count': [small_values_sum]})
decisonPrimaryReason_pie = pd.concat([decisonPrimaryReason_data, small_values_row])
decisonPrimaryReason_pie = decisonPrimaryReason_pie.query("Count > 2000")


##### Stacked barchart for decision taken per sector over time #####
dataset_18 = dataset.groupby(['Sector']).agg({'Decision (Action Taken)':'sum', 'Decision (No Action Taken)':'sum'}).reset_index()
dataset_18["Total Decisions"] = dataset_18['Decision (Action Taken)'] + dataset_18['Decision (No Action Taken)']
dataset_18['Decision (Action Taken)'] = round((dataset_18['Decision (Action Taken)'] / dataset_18['Total Decisions'])*100)
dataset_18['Decision (No Action Taken)'] = round((dataset_18['Decision (No Action Taken)'] / dataset_18['Total Decisions'])*100)


##### Day Heatmap #####

# Sets the colour scale of the heatmap from (https://plotly.com/javascript/colorscales/) 
heatmap_options = {"colorscale": "Portland"}

# Mapping day names to numbers starting from 1 using calendar.day_name
day_to_num = {day: index for index, day in enumerate(calendar.day_name, start=1)}
dataset_19_temp = dataset
dataset_19_temp['DayNum'] = dataset_19_temp['DayName'].map(day_to_num)
dataset_19 = dataset_19_temp.groupby(['Sector', 'DayName', 'DayNum']).size().reset_index(name='Count').sort_values(by='DayNum')

# Removes the unknown column since it has partial data
dataset_19 = dataset_19.drop(dataset_19[dataset_19['Sector'] == 'Unknown'].index)


##### Month Heatmap #####

# Mapping month names to numbers starting from 1 using calendar.month_name
month_to_num = {month: index for index, month in enumerate(calendar.month_name) if month}
dataset_20_temp = dataset
dataset_20_temp['MonthNum'] = dataset_20_temp['MonthName'].map(month_to_num)
dataset_20 = dataset_20_temp.groupby(['Sector', 'MonthName', 'MonthNum']).size().reset_index(name='Count').sort_values(by='MonthNum')

# Removes the unknown column since it has partial data
dataset_20 = dataset_20.drop(dataset_20[dataset_20['Sector'] == 'Unknown'].index)


##### Stacked barchart buttons #####

# Updates the chart for all the years when pressed
def button_pressed(state):
    if (state.year_selected == "All"):
        dataset_18 = dataset.groupby(['Sector']).agg({'Decision (Action Taken)':'sum', 'Decision (No Action Taken)':'sum'}).reset_index()
        dataset_18["Total Decisions"] = dataset_18['Decision (Action Taken)'] + dataset_18['Decision (No Action Taken)']
        dataset_18['Decision (Action Taken)'] = round((dataset_18['Decision (Action Taken)'] / dataset_18['Total Decisions'])*100)
        dataset_18['Decision (No Action Taken)'] = round((dataset_18['Decision (No Action Taken)'] / dataset_18['Total Decisions'])*100)
        state.dataset_18=dataset_18
        notify(state, 's', 'Data has been updated!')

 # Updates the chart for the specific year selected       
    else:
        query ="YearFilter == '"+state.year_selected+"'"
        dataset_18_temp = dataset.query(query)
        dataset_18 = dataset_18_temp.groupby(['Sector']).agg({'Decision (Action Taken)':'sum', 'Decision (No Action Taken)':'sum'}).reset_index()
        dataset_18["Total Decisions"] = dataset_18['Decision (Action Taken)'] + dataset_18['Decision (No Action Taken)']
        dataset_18['Decision (Action Taken)'] = round((dataset_18['Decision (Action Taken)'] / dataset_18['Total Decisions'])*100)
        dataset_18['Decision (No Action Taken)'] = round((dataset_18['Decision (No Action Taken)'] / dataset_18['Total Decisions'])*100)
        state.dataset_18=dataset_18
        notify(state, 's', 'Data has been updated!')

# Sets the chart to be the stacked barchart
layout={ "barmode": "stack" }

# Sets the starting year selected to be all
year_selected = "All"


##### Contents of the Page #####

root = Markdown("pages/root.md")
dashboard = Markdown("pages/dashboard.md")
risks = Markdown("pages/risks.md")
advisor = Markdown("pages/advisor.md")
instructions = Markdown("pages/instructions.md")

pages = {
    '/': root,
    "Getting-Started":instructions,
    "Dashboard":dashboard,
    "Risks":risks,
    "GDPR-Compliance-Advisor":advisor,
}

Gui(pages = pages).run(title="ICO Complaints Dashboard", dark_mode = False, css_file = 'main.css')
