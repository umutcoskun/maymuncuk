import os
from datetime import datetime, timedelta
from optparse import OptionParser

from prettytable import PrettyTable

from . import Maymuncuk


print('\nMaymuncuk v1.0\n')

parser = OptionParser()

parser.add_option(
    '-p',
    '--property',
    dest='prop',
    help='URL of the property.',
)

(options, args) = parser.parse_args()

if not options.prop:
    options.prop = input('Property URL: ')

app = Maymuncuk(options.prop)
app.create_engine('maymuncuk.db')
app.create_session()
table = PrettyTable()

table.field_names = ["Date", "Queries"]

startDate = datetime.strptime('2017-09-19', Maymuncuk.date_format)
session_entry_count = 0

while startDate < datetime.now():
    endDate = startDate + timedelta(days=1)

    entries = app.get_entry_count_by_date(startDate.strftime(Maymuncuk.date_format))

    if entries > 0:
        table.add_row([startDate, 'Passed'])
    else:
        created_entry_count = app.query({
            'startDate': startDate.strftime(Maymuncuk.date_format),
            'endDate': endDate.strftime(Maymuncuk.date_format),
            'dimensions': ['query'],
            'rowLimit': 5000,
        })
        app.save()
        table.add_row([startDate, created_entry_count])
        session_entry_count += created_entry_count

    startDate = endDate

    os.system('clear')
    print('\nMaymuncuk v1.0\n')
    print(table)
    print('\nFetching data for {} ...'.format(startDate.strftime(Maymuncuk.date_format)))
    print('\nCreated {} entries in this session.'.format(session_entry_count))