import json
import gspread
import math
from oauth2client.service_account import ServiceAccountCredentials


def load_spreadsheet():
    print 'Load Google credentials'
    json_key = json.load(open('credentials.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

    gc = gspread.authorize(credentials)
    sh = gc.open_by_key('1PgxD5wx6qrWtIfnJ89fdczpS6yKK5BOZZHcRQeZCnD4')

    # delete worksheet
    sh.del_worksheet(sh.worksheet('BC105'))

    # make worksheet
    wks = sh.add_worksheet(title="BC105", rows='100', cols='10')
    #wks = sh.worksheet('105_cart')
    
    header = wks.range('A1:G1')
    #header[0].value = 'besteller'
    #header[1].value = 'artikel'
    #header[2].value = 'type'
    header[3].value = 'Per stuk'
    header[4].value = '#'
    header[5].value = 'Totaal'
    header[6].value = '5%'
    wks.update_cells(header)

    return wks

def add_to_spreadsheet(wks, orders):
    row_number = 2

    for user, products in orders.iteritems():
        print user
        wks.update_cell(row_number, 2, user)
        row_number += 1
        first_row = row_number
        for product in products:
            row = wks.range('A' + str(row_number) + ':G' + str(row_number))
            row[0].value, row[1].value = product['name'].split(' ', 1)
            row[2].value = product['type']
            row[3].value = product['price']
            row[4].value = product['qty']
            row[5].value = float(product['price']) * product['qty']
            row[6].value = math.ceil(float(row[5].value) * 0.95 * 100) / 100

            wks.update_cells(row)
            row_number += 1
        last_row = row_number - 1
        wks.update_cell(row_number, 6, '=SUM(F' + str(first_row) + ':F' + str(last_row) + ')')
        wks.update_cell(row_number, 7, '=CEILING(F' + str(row_number) + '*0.95, 0.01)')
        row_number += 2




    print 'Orders added to spreadsheet'

def write_summary():
    print 'write summary'


