README FILE

Analysing Data Protection Complaints: 
Data Analytics, Visualisations, Risk Assessment and Mitigation Strategies for ICO's Data Protection Complaints

AADIL SAIYAD

Supervisor: Nikos Kominos, Department of Computer Science.

Master’s Dissertation Project 2024
Department of Computer Science
City University of London
Northampton Square
London EC1V 0HB

###################################################################

THE PROJECT PACKAGE INCLUDES THE PROJECT APPLICATION WHICH CONTAINS:

The code:
- One main.py file which contains the main code of the project.
- 5x Markdown files containing the markdown code needed to display items on the page.
	root.md - Contains the markdown for displaying the navbar over all pages.
	dashboard.md - Contains markdown for visualising the charts on the main dashboard.
	risks.md - Contains the markdown for displaying the table and dropdown for organisations.
	advisor.md - Contains the markdown for displaying the Sectors and subsectors columns and GDPR recommednations.
	instructions.md - Contains the markdown for displaying the instructions on how to use the site.
- One CSS file required for the colouring of the Risks table.
- One JSON file required for the GDPR Compliance avisor page which contains the GDPR articles, description and recommendations.
- One dataCleansing.py file not needed to run but showcases parts of the data preperation stage.

The dataset:
- One CSV dataset containing the Data Protection Complaints data needed to visualise the data.

Images:
- One Image of the Sankey Diagram.

Cloud File:
- One requirements text file used to host the project on Taipy Cloud and help the system get the necessary modules.


###################################################################

REQUIREMENTS FOR THE PROJECT:

- IDE: The IDE used during this project was Visual Studio Code Windows 64bit so the same would be ideal.
	https://code.visualstudio.com/

- Python: The Python version used in development was 3.12.2 64bit for Windows so the same would be ideal.
	https://www.python.org/downloads/

- Pip: Pip is included by default if you use Python 3.4 or later. Otherwise, you can follow the official installation page of pip to install it.
	https://pip.pypa.io/en/stable/installation/

- Taipy: The preferred method to install Taipy is by using pip. "pip install taipy". If this does not work, I implemented it using "py -m pip install taipy". However there are multiple ways to install using this tutorial depending on setup.
	https://docs.taipy.io/en/release-3.1/installation/

- Scikit learn: Scikit learn is required to implement the MinMaxScaler normalisation for the risks table. This is done using the command "pip install -U scikit-learn". If this does not work, I implemented it using "py -m pip install scikit-learn".
Further information can be found on their webpage.
	https://scikit-learn.org/stable/install.html

- Pandas: Data maipulation and analysis tool within Python used for data cleansing, preperation, and visualisation. This is installed using the command "pip install pandas".
Further information can be found on their webpage.
	https://pandas.pydata.org/docs/index.html 

- Taipy Cloud Account: In order to host the site on the Taipy cloud, a free account must be created which gives you access to host an application on a machine for 6 hours a day. 
- Creating a Machine: Once the account is created, you can set up your machine with the details you desire, however, ensuring the Python version is set to 3.11.
- Adding the Application: Once the machine is ready, you can add the application to it, ensuring that the project is within a ZIP file and the entry point of the file is set to "main.py". Furthermore, the requirements file should be set to "requirements.txt".

Running this application should then successfully host the Data Protection Complaints Dashboard on the Taipy Cloud URL you set for anyone who has the link to use. 



















