[comment]: <> (Title of the page)
<h1><span style="color:#Ff5000">Data Protection Complaints</span> <span style="color:black">Dashboard</span></h1>


[comment]: <> (Setting the first pane of the dashboard)
<|layout|columns = 2 2 2 2 2|gap=25px|

[comment]: <> (Total number of cases statistic)
<|card card-bg|
Total Number of Cases
<|{len(dataset.index)}|text|class_name=h3|>
|>

[comment]: <> (Average time statistic)
<|card card-bg|
Average Time to Process a Complaint
<|{round(dataset_timedelta .loc[:, 'Time Delta'].mean())} Days|text|class_name=h3|>
|>

[comment]: <> (Total number of re-opened cases)
<|card card-bg|
Total Number of Re-Opened Cases
<|{len(dataset[dataset.duplicated(['Case Reference'], keep=False)].index) //2 }|text|class_name=h3|>
|>
|>


<br/>


[comment]: <> (Setting the second pane of the dashboard)
<|layout|columns = 2 1|gap=25px|

[comment]: <> (Bar chart: complaints / sector)
<| {dataset_2}|chart|type=bar|labels=Sector|values=Count|color=#Ff5000|title=Number of Complaints / Sector|>

[comment]: <> (Pie chart: decision on complaints)
<| {dataset_3}|chart|type=pie|labels=Decision|values=Count|title=Overall Decision on Complaints|>
|>


<br/>


[comment]: <> (Setting the third pane of the dashboard)
<|layout|columns = 1 2|gap=25px|

[comment]: <> (Pie chart: decision article distribution)
<| {dataset_15}|chart|type=pie|labels=Decision Articles|values=Count|title=Distribution of GDPR Article Breach of Complaints|>

[comment]: <> (Line chart: cases submitted over time)
<| {dataset_6}|chart|mode=lines|y=Count|x=Date Received|title=Timeline of Cases Submitted|color=#Ff5000|>
|>


<br/>


[comment]: <> (Buttons: stacked bar chart years)
<| {year_selected}|toggle|lov=2018;2019;2020;2021;2022;2023;All|on_change=button_pressed|>

[comment]: <> (Setting the fourth pane of the dashboard)
<|layout|columns = 2 2|gap=25px|

[comment]: <> (Stacked bar chart: action or no action taken / sector)
<| {dataset_18}|chart|type=bar|x=Sector|y[1]=Decision (Action Taken)|y[2]=Decision (No Action Taken)|layout={layout}|title=Distribution 'Action Taken' VS 'No Action Taken' / Sector|>

[comment]: <> (Heatmap: complaints per month)
<| {dataset_20}|chart|type=heatmap|x=Sector|y=MonthName|z=Count|options={heatmap_options}|title=Distribution of Complaints / Month within each Sector|>
|>


<br/>


[comment]: <> (Setting the fith pane of the dashboard)
<|layout|columns = 2 2|gap=25px|

[comment]: <> (Bar chart: complaints / subsector)
<| {dataset_14}|chart|type=bar|labels=Sub Sector|values=Count|color=#Ff5000|title=Number of Complaints / Sub Sector|>

[comment]: <> (Pie chart: complaints / sector)
<| {decisonPrimaryReason_pie}|chart|type=pie|labels=Decision Primary Reason|values=Count|title=Distribution of Specific GDPR Breach of Complaints|>
|>


<br/>

<|card card-bg|

[comment]: <> (Sankey diagram: decision to decision detail2)
<|{sankey}|image|width=100%|height=50%|>

|>

