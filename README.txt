############################### SIMPLE FAMILY TREE PROJECT IN PYTHON DJANGO ##########################

################ Querstion #####################

>>>> Define a family tree:
    Design a command line tool (family-tree) that has the following options:
> family-tree add person <name>
    eg: family-tree add Amit Dhakad
> family-tree add relationship <name>
    eg: family-tree add relationship father
    eg: family-tree add relationship son
>family-tree connect <name 1> as <relationship> of <name 2>
    eg: family-tree connect Amit Dhakad as son of KK Dhakad

>>>> Queries:
    Based on relations created, we should be able to make following queries
>family-tree count sons of <name>
    This should count sons
>family-tree count daughters of <name>
    This should count of all daughters
>family-tree count wives of <name>
    This should count wives
>family-tree father of <name>
    This should return father name
>>>> Our Family Tree:
    Please ignore the DoB
    Pink = Females

>>>>For Family tree Diagram please check question.pdf

################################################

######################## Runnning Instruction ########################

Note:
    using default database sqlite3, so if wanted fresh data then delete file named db.sqlite3 and then run below code to setup new database.
    >> python manage.py migrate
    above code will crete all tables

For running server plese follow below code:
    >> python manage.py runserver 0.0.0.0:8000
    Above code will start the server and then we can visit http://localhost:8000/ which will have UI for manuplating data and querying data

IMPORTANT:
    For Example i have already added sample data for a diagram which is shown in question.pdf file, If someone wants then they can delete data 
    and add there own data and check the working of code.

######################################################################