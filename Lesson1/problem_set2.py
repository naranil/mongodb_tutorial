# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.

import xlrd
import os
import csv
from zipfile import ZipFile

datafile = "./data/2013_ERCOT_Hourly_Load_Data.xls"
outfile = "./output/2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = None
    d = {}
    header_row=0
    headers = [sheet.cell_value(header_row, i) for i in xrange(sheet.ncols)]

    for i, header in enumerate(headers):
        d[header] = [sheet.cell_value(row, i) for row in xrange(1, sheet.nrows)]

    data = []
    for header in headers:
        if header in ['COAST', 'EAST', 'FAR_WEST', 'NORTH', 'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']:
            csvline = {}
            csvline['Station'] = header
            csvline['Max Load'] = max(d[header])
            max_index = d[header].index(max(d[header]))
            max_date = xlrd.xldate_as_tuple(d['Hour_End'][max_index], 0)
            csvline['Year'] = max_date[0]
            csvline['Month'] = max_date[1]
            csvline['Day'] = max_date[2]
            csvline['Hour'] = max_date[3]
            data.append(csvline)

    return data

def save_file(data, filename):
    with open(filename, 'wb') as output_file:
        keys = data[0].keys()
        dict_writer = csv.DictWriter(output_file, keys, delimiter="|")
        dict_writer.writeheader()
        dict_writer.writerows(data)
    
def test():
    #open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)

        
if __name__ == "__main__":
    test()
