import requests
from datetime import date
import csv
import arcpy

def process_today(url, data_file, fieldnames):
    #last_url = 'http://nssac.bii.virginia.edu/covid-19/dashboard/data/nssac-ncov-sd-03-12-2020.csv'
    with open(data_file, 'w', newline='') as csvfile:
        count = 0
        coronavirus_file = csv.DictWriter(csvfile, fieldnames=fieldnames)
        coronavirus_file.writeheader()
        # Make the request
        r = requests.get(url)
        if r.status_code == 200:
            # Iterate over the lines and decode them to utf-8
            lines = (line.decode('utf-8') for line in r.iter_lines())
            for record in lines:
                State = record.split(',')[0]
                Country = record.split(',')[1]
                Last_Updated = record.split(',')[2]
                Confirmed = record.split(',')[3]
                Deaths = record.split(',')[4]
                Recovered = record.split(',')[5]
                if Country == 'USA':
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
                        if State in ['Hawaii', 'District of Columbia']:
                            Full_County_Name = State
                            Cases = Confirmed
                        if State in ['Vermon', 'Vermont']:
                            State = 'Vermont'
                        if ':' in Cases:
                            Cases = Cases.replace(':', '')
                        if Cases.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9')):
                            Cases = Cases
                           # print(Cases)
                            coronavirus_file.writerow({'State': str(State), 'Country': str(Country), 'County Name': str(County_Name),
                                                  'Full County Name': str(Full_County_Name), 'Cases': int(Cases)})

                    count += 1
            print("Wrote {0} records to {1}".format(count, output_file))
        else:
            print("The latest file is not available")


def update_fgdb(fgdb, data_file, table):
    arcpy.env.workspace = fgdb
    print('Truncating table')
    arcpy.TruncateTable_management(table)
    print('Appending records')

    arcpy.Append_management(data_file, table, "NO_TEST",
                            'State "State" true true false 8000 Text 0 0,First,#,data_file,State,0,8000;Country "Country" true true false 8000 Text 0 0,First,#,data_file,Country,0,8000;County_Name '
                            '"County Name" true true false 50 Text 0 0,First,#,data_file,County Name,0,8000;Full_County_Name "Full County Name" true true false 8000 Text 0 0,First,#,data_file,'
                            'Full County Name,0,8000;Cases "Cases" true true false 4 Long 0 0,First,#,data_file,Cases,-1,-1',
                            '', '')
    print('Compacting fgdb')
    arcpy.Compact_management(fgdb)


if __name__ == '__main__':

    today = date.today()
    today = today.strftime("%m-%d-%Y")

    start_url_format = 'http://nssac.bii.virginia.edu/covid-19/dashboard/data/nssac-ncov-sd-'
    today_url = start_url_format + today + '.csv'
    output_file = 'C:/Data/coronavirus/' + today + '.csv'
    fields = ['State', 'Country', 'County Name', 'Full County Name', 'Cases']
    coronavirus_fgdb = "C:/Data/coronavirus/Coronavirus.gdb"
    coronavirus_table = "C:/Data/coronavirus/Coronavirus.gdb/Coronavirus_Cases"

    process_today(today_url, output_file, fields)

    update_fgdb(coronavirus_fgdb, output_file, coronavirus_table)