"""
Author: Don Shaw
Company: Esri
Division: Professional Services / Washington, D.C. Regional Services
Contact: d.shaw@esri.com
Purpose: Scrape University of Virginia / Harvard Public Line List Coronavirus (COVID-19) Data and import it to a FGDB
"""

import requests
import datetime
from datetime import date
import csv
import arcpy
from os import path
import logging
import sys
import configparser


def process_today(url, data_file, fieldnames):

    with open(data_file, 'w', newline='', encoding='utf-8') as csvfile:
        count = 0
        harvard_url = 'https://docs.google.com/spreadsheets/d/1itaohdPiAeniCXNlntNztZ_oRvjh0HsGuJXUJWET008'
        coronavirus_file = csv.DictWriter(csvfile, fieldnames=fieldnames)
        coronavirus_file.writeheader()
        # Make the request
        r = requests.get(url, verify=True)
        if r.status_code == 200:
            logging.info('Successfully connected to {0}'.format(url))
            # Iterate over the lines and decode them to utf-8
            lines = (line.decode('utf-8') for line in r.iter_lines())
            for record in lines:
                state = record.split(',')[0]
                country = record.split(',')[1]
                last_updated = record.split(',')[2]
                confirmed = record.split(',')[3]
                source = url
                if country == 'USA':
                    update_time = last_updated[:19]
                    idx = last_updated.find('*')
                    if idx == 0 or idx == -1:
                        pass
                    else:
                        bad_list = ['CNTY', 'CNTY:', 'CTY', 'CNTY', 'CNTY: ', 'Parish:']
                        for i in bad_list:
                            if i in last_updated:
                                last_updated = last_updated.replace(i, 'CTY: ')
                    cnty_idx = last_updated.find(': ')
                    state_county_list = last_updated[cnty_idx + 1:]
                    county_split = state_county_list.split(';')

                    for x in county_split:
                        if len(x) < 30:
                            x.split(' ')
                            c = x.rsplit(' ', 1)
                        else:
                            c = x.rsplit(' ', 2)
                        county_name = c[0]
                        cases = c[1]
                        if ':' in county_name:
                            county_name = county_name.replace(':', '')
                        full_county_name = county_name + ', ' + state
                        if ' ,' in full_county_name:
                            full_county_name = full_county_name.replace(' ,', ',')
                        if full_county_name.startswith(' '):
                            full_county_name = full_county_name.lstrip(' ')
                        if state in ['District of Columbia', 'Puerto Rico', 'Guam']:
                            cases = confirmed
                            full_county_name = state + ', ' + state
                        if state in ['US Virgin Islands', 'USVI', 'US Virgin Island']:
                            cases = confirmed
                            full_county_name = 'US Virgin Islands, US Virgin Islands'
                        if full_county_name in ['Kauai County, Hawaii', 'Maui County, Hawaii',
                                                'Kalawao County, Hawaii', 'Hawaii County, Hawaii']:
                            full_county_name = full_county_name.replace(' County,', ',')
                        if ':' in cases:
                            cases = cases.replace(':', '')
                        if cases.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9')):
                            case = cases
                            # print(Cases)
                            coronavirus_file.writerow({'State': str(state), 'Country': str(country),
                                                       'County_Name': str(county_name),
                                                       'Full_County_Name': str(full_county_name),
                                                       'Cases': int(case), 'Update_Time': str(update_time),
                                                       'UVA_URL': str(source),
                                                       'Harvard_URL': str(harvard_url)})
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
    arcpy.Append_management(data_file, coronavirus_table, "TEST")

    logging.info('Compacting fgdb')
    arcpy.Compact_management(fgdb)


if __name__ == '__main__':

    log_dir = path.dirname(path.realpath(__file__))
    log_name = path.join(log_dir,  'coronavirus_scraper.log')
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=log_name,
                        level=logging.INFO,
                        format=log_format,
                        filemode="a")
    logging.info("***** Start time:  {0}".format(datetime.datetime.now().strftime("%A %B %d %I:%M:%S %p %Y")))

    today = date.today()
    today = today.strftime("%m-%d-%Y")

    # Read the .ini file
    config = configparser.ConfigParser()
    config.read(path.join(sys.path[0], 'config.ini'))

    # Variables
    start_url_format = 'https://nssac.bii.virginia.edu/covid-19/dashboard/data/nssac-ncov-sd-'
    today_url = start_url_format + today + '.csv'
    fields = ['State', 'Country', 'County_Name', 'Full_County_Name', 'Cases', 'Update_Time', 'UVA_URL', 'Harvard_URL']

    output_file = config.get('ALL', 'output_path') + today + '.csv'
    coronavirus_fgdb = config.get('ALL', 'coronavirus_fgdb')
    coronavirus_table = config.get('ALL', 'coronavirus_table')

    logging.info('URL:  {0}'.format(today_url))
    logging.info('Output File:  {0}'.format(output_file))
    logging.info('FGDB:  {0}'.format(coronavirus_fgdb))

    process_today(today_url, output_file, fields)
    update_fgdb(coronavirus_fgdb, output_file, coronavirus_table)
    logging.info("***** Completed time:  {0}\n".format(datetime.datetime.now().strftime("%A %B %d %I:%M:%S %p %Y")))