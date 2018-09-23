#!/usr/bin/env python3
import psycopg2
import sys

DBNAME = 'news'

# Query for most popular articles
popular_articles = ''' select articles.title, count(*)
 as num from articles join log on
 where log.path = '/article/' || articles.slug
 group by articles.title order by num desc limit 3
'''

# Query for most popular authors
articles_authors_view = '''create view atrtic_author as
 select slug, name from articles join authors
 on articles.author = authors.id'''

popular_authors = ''' select atrtic_author.name , count(*)
 as num from atrtic_author join log
 on log.path like '%'|| atrtic_author.slug || '%'
 group by atrtic_author.name order by num desc;
'''

# Query for most requstes lead to error
# Create table with date with total requstes
total_view = '''create view total_count as select date(time), count(*) as totl
 from log group by date(time) '''

# Create table with date with faulty requstes
sum_view = '''create view addtion as select date(time), count(*) as sum
  from log where status != '200 OK' group by date(time) '''

# Get the final result for each day and get the ones that more than 1%
error_requests = '''select to_char(date, 'Mon dd, yyyy'), c from
 (select total_count.date as date,
 (cast(sum as float) / cast(totl as float)) * 100 as c
 from total_count join addtion on total_count.date = addtion.date)
 as result where c > 1'''


def get_data(*qureies):
    ''' This function used to connect to the database'''
    try:
        pg = psycopg2.connect(dbname=DBNAME)
    except psycopg2.Error as e:
        print ("Unable to connect!")
        print (e.pgerror)
        print (e.diag.message_detail)
        sys.exit(1)
    else:
        c = pg.cursor()
        for qurey in qureies:
            c.execute(qurey)
        d = c.fetchall()
        pg.close()
    return d


def display_data():
    ''' This function used to display the data to we get from database'''
    print(" The most popular three articles of all time: ")

    for article in get_data(popular_articles):
        print("-{} - {} views".format(article[0], article[1]))
    print('\n')
    print(" The most popular article authors of all time: ")
    for author in get_data(articles_authors_view, popular_authors):
        print("-{} - {} views".format(author[0], author[1]))
    print('\n')


def display_error():
    errors = get_data(total_view, sum_view, error_requests)
    if errors:
        print(" Days did more than 1% of requests lead to errors: ")
        for error in errors:
            print("-{0} - {1:.2f}% errors".format(error[0], error[1]))
    else:
        print("We have no errors :)")

if __name__ == '__main__':
    display_data()
    display_error()
