# CSGO_DataBase_Project
Python project that analyses CS:GO data
There are several files that make this project work. Their purposes (and order of use) are outlined below. Please follow the instructions provided in this document to set up the application
so that it can be used/tested succesfully. 

---- Installing PostgreSQL ----

Postgress can be downloaded from the following location: https://www.postgresql.org/download/
It is free and works on most OS. I personally set this up on Windows, so to help me visualize the tables I was making, I also installed PgAdmin4 (https://www.pgadmin.org/download/pgadmin-4-windows/).
You don't need PgAdmin4 for this project to work, but it came in handy when trouble-shooting. The only thing that is important when setting up PostgreSQL is to make note of the name of the server and the
password for that server. I chose the default server name for this process. 

---- Obtaining the Data ----

The data used in this project can be obtained from: https://www.kaggle.com/skihikingkevin/csgo-matchmaking-damage
To make it play nicely with my code however, I had to clean the data and create a cleaned version of each of the CSV files provided. 
There is a folder called "Cleaned Data" but it only contains the file needed to clean the data properly. As I do not own the original
data, I did not feel confortable re-uploading it here. 

---- Data Structure ----

The data itself is comprised of 11 files from the orignial site along with an additional file "ratio_data.csv" which helps in the construction of the database and in loading the data into said
database. Specifically, this extra file serves a purpose similar to a dictionary, but as it needs to store multiple values per "key" it was easier to construct a table instead. It should also be noted
that outside of the data folder there is a similar ratio_data file, but this file contain significantly more information and thus the two are not interchangable. 

Addtionally, with regard to my own personal meta-files, there are a series of .txt files which allow the program to run and should be included.

Finally, the actuall data provided by the website/source mostly contains information about player interactions (mostly kills) over a several week period. Team, side, weapon used, bomb site,
as well as additional information like location of the player and damage delt were obtained for each kill/interaction. The data also containes information related to specific maps and game types played,
and uses both round number and second as means of keeping time. In my cleaning process, I converted some vatriables (like bombsite) to binary options in order to simplify the matter at hand. 
Most variables however are either stored as either bigint type data or varchar type based on the values they contain. Post cleaning there was some issues with NULL values by setting them to False 
when appropriate or simply excluding the data when necessary. I unforntunitly do not have an exact number for those values, but the original source estimates that for most variables it was between 
1 and 5%. Considering some of these values were extrapolated from the rest of the data (and some were simply not necessary) I would estimate I lost about 2-3% of the data in total due to missing values.
The total size of the data is about 3-4GB and thus could not be loaded in active memory. This accounts for about 10538180 samples in the largest table and only about 6 in the smallest.
A more detailed decsription is provided in the Ppt, but in short the data acts as a small subset of the type of data Valve (tm) generate every time two players engage eachother in CS:GO.


---- Loading the Data into the Data Base ----

Once you have sucessfully conected to the database the file "CSGO_data_builder.py" can (and should) be used first to create the data tables which will house the data for the reast of this project.
This is a rather quick process and should only take a few seconds to run. The following file "CSGO_data_loader.py" needs to be ruin next and will take a rather lengthy amount of time to run.
Based on my tests, I predict that it should take between 4-6 hrs to run to completion. There is a variable related to chunk size within the file which is currently set to 20. I have tried adjusting it to
a lower value and this has increased the spead some, but setting it too low, increased the time once again. Adjust at your discression. 

---- Running the Application ----

Once the data is loaded the application can be sucessfully run. The following files will need the paths of related files changed:
- stats_2.py --> Groups statistics defined in stats_1.py into categories for use by the main application.
- graphs.py --> Creates a series of graphs for the user.
- questions.py --> Provides a series of prompts for the user as well as code to handle user responce in relation to the data.
- window.pw --> Creates a window with the user requested graph.
- main.py --> Is the main "interface" of the code. 

Running the application can be accomplished by running the "main.py" file. This file (assuming all paths have been corrected for) will call all other subsequent files inorder to prompt the user
regarding the possible analysis that can be run on the given data set. These include:
- Running the user's own test.
- Running a single or all test(s) used in the presentation.
- Running a single or all test(s) throught up by the programer, but cut from the presentation due to time.

The user will also be given the option of creating a graph for each test they perform and looping back through the prompts to examine different variables. 

---- Cleaning Up ----

To remove the data from the database run the "clean_up.py" file. This file should connect to the database and not only delete the data but also remove the data tables as well. This does mean
that if one wishes to put the data back into the database and/or run the application again, the "CSGO_data_builder.py" file will likewise need to be run in addition to the "CSGO_data_loader.py"
file. Once the data has been removed from the database, you can uninstall PostgreSQL and PgAdmin4. 
