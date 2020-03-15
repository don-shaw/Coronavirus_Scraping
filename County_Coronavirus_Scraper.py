'''
Author: Don Shaw
Company: Esri
Division: Professional Services / Washington, D.C. Regional Services
Contact: d.shaw@esri.com
Purpose: Scrape University of Virginia Coronavirus (COVID-19) Data and import it to a FGDB
'''


import requests
import datetime
from datetime import date
import csv
import arcpy
from os import path
import logging
import sys


def process_today(url, data_file, fieldnames):
    with open(data_file, 'w', newline='') as csvfile:
        count = 0
        coronavirus_file = csv.DictWriter(csvfile, fieldnames=fieldnames)
        coronavirus_file.writeheader()
        # Make the request
        r = requests.get(url)
        if r.status_code == 200:
            logging.info('Successfully connected to {0}'.format(url))
            # Iterate over the lines and decode them to utf-8
            lines = (line.decode('utf-8') for line in r.iter_lines())
            for record in lines:
                State = record.split(',')[0]
                Country = record.split(',')[1]
                Last_Updated = record.split(',')[2]
                Confirmed = record.split(',')[3]
                Deaths = record.split(',')[4]
                Recovered = record.split(',')[5]
                Source = url
                if Country == 'USA':
                    update_time = Last_Updated[:19]
                    idx = Last_Updated.find('*')
                    if idx == 0 or idx == -1:
                        pass
                    else:
                        bad_list = ['CNTY', 'CNTY:', 'CTY', 'CNTY', 'CNTY: ', 'Parish:']
                        for i in bad_list:
                            if i in Last_Updated:
                                 Last_Updated = Last_Updated.replace(i, 'CTY: ')
                    cnty_idx = Last_Updated.find(': ')
                    state_county_list = Last_Updated[cnty_idx + 1:]
                    county_split = state_county_list.split(';')

                    for x in county_split:
                        if len(x) < 30:
                            x.split(' ')
                            c = x.rsplit(' ', 1)
                        else:
                            c = x.rsplit(' ', 2)
                        County_Name = c[0]
                        Cases = c[1]
                        if ':' in County_Name:
                            County_Name = County_Name.replace(':', '')
                        Full_County_Name = County_Name + ', ' + State
                        if Full_County_Name.startswith(' '):
                            Full_County_Name = Full_County_Name.lstrip(' ')
                        #print('{0} has {1} cases'.format(Full_County_Name, Cases))
                        if State in ['District of Columbia']:
                            Cases = Confirmed
                            Full_County_Name = 'District of Columbia, District of Columbia'
                        if State in ['Vermon', 'Vermont']:
                            State = 'Vermont'
                        if State in ['USVI']:
                            County_Name = 'USVI'
                            Full_County_Name = 'USVI'
                        if Full_County_Name in ['Kauai County, Hawaii', 'Maui County, Hawaii', 'Kalawao County, Hawaii', 'Hawaii County, Hawaii']:
                            Full_County_Name = Full_County_Name.replace(' County,', ',')
                        if ':' in Cases:
                            Cases = Cases.replace(':', '')
                        if Cases.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9')):
                            Cases = Cases
                           # print(Cases)
                            coronavirus_file.writerow({'State': str(State), 'Country': str(Country),
                                                       'County Name': str(County_Name), 'Full County Name': str(Full_County_Name),
                                                       'Cases': int(Cases), 'Update Time': str(update_time),
                                                       'Source': str(Source)})

                            count += 1
            logging.info("Wrote {0} records to {1}".format(count, output_file))
        else:
            logging.error("The latest file is not available")
            sys.exit('File not available')



def update_fgdb(fgdb, data_file, table):
    arcpy.env.workspace = fgdb
    logging.info('Truncating {0}'.format(table))
    arcpy.TruncateTable_management(table)
    logging.info('Appending records')

    arcpy.Append_management(data_file, table, "NO_TEST",
                            r'State "State" true true false 8000 Text 0 0,First,#,'
                            r'data_file,State,0,8000;Country "Country" true true false 8000 Text 0 0,'
                            r'First,#,data_file,Country,0,8000;County_Name "County Name" true true false 50 Text 0 0,'
                            r'First,#,data_file,County Name,0,8000;Full_County_Name "Full County Name" true true false'
                            r' 8000 Text 0 0,First,#,data_file,Full County Name,0,8000;Cases "Cases" true true false'
                            r' 4 Long 0 0,First,#,data_file,Cases,-1,-1;Update_Time "Update_Time" true true false 8 Date'
                            r' 0 0,First,#,data_file,Update Time,-1,-1;Source "Source" true true false 255 Text 0 0,'
                            r'First,#,data_file,Source,0,8000', '', '')
    logging.info('Compacting fgdb')
    arcpy.Compact_management(fgdb)


if __name__ == '__main__':

    log_dir = path.dirname(path.realpath(__file__))
    log_name = path.join(log_dir, 'coronavirus_scraper.log')
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=log_name,
                        level=logging.INFO,
                        format=log_format,
                        filemode="a")
    logging.info("***** Start time:  {0}".format(datetime.datetime.now().strftime("%A %B %d %I:%M:%S %p %Y")))

    today = date.today()
    today = today.strftime("%m-%d-%Y")

    # Variables
    start_url_format = 'http://nssac.bii.virginia.edu/covid-19/dashboard/data/nssac-ncov-sd-'
    today_url = start_url_format + today + '.csv'
    output_file = 'C:/Data/coronavirus/' + today + '.csv'
    fields = ['State', 'Country', 'County Name', 'Full County Name', 'Cases', 'Update Time', 'Source']
    coronavirus_fgdb = "C:/Data/coronavirus/Coronavirus.gdb"
    coronavirus_table = "C:/Data/coronavirus/Coronavirus.gdb/Coronavirus_Cases"

    logging.info('URL:  {0}'.format(today_url))
    logging.info('Output File:  {0}'.format(output_file))
    logging.info('FGDB:  {0}'.format(coronavirus_fgdb))

    process_today(today_url, output_file, fields)
    update_fgdb(coronavirus_fgdb, output_file, coronavirus_table)
    logging.info("***** Completed time:  {0}\n".format(datetime.datetime.now().strftime("%A %B %d %I:%M:%S %p %Y")))