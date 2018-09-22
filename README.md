# Logs-Analysis
This program used to connect to the database and fetch the data from it

## Code style
This project is written in python 3 and follow PEP-8 Guidelines,
Database system is postgreSQL

## Code design
The code depends on functions, so easy to read and to follow, there are three functions 
function called get_data to connect and fetch the data from the database, and function called 
display_data to print out the data, the last function called display_error to print out the errors

### Note this project depends on create view, and heres the create view command that used

articles_authors_view = '''create view atrtic_author as select slug, name from articles join authors on articles.author = authors.id'''
 
total_view = '''create view total_count as select date(time), count(*) as totl from log group by date(time) '''
 
 sum_view = '''create view addtion as select date(time), count(*) as sum from log where status != '200 OK' group by date(time) '''
 
## Run
All you have to do is just to type the name of file on linux terminal (Bash) like this: python reporting_tools.py
and the data will printed out
