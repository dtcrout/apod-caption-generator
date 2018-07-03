"""get_data_using_range.py"""

import argparse
import datetime
import json
import os
import requests
import sys
import time

parser = argparse.ArgumentParser(
    description='Download APOD metadata using APOD API service.'
)

parser.add_argument('conf',
                    type=argparse.FileType('r'),
                    default=sys.stdin,
                    help='path to configuration file')

parser.add_argument('-s',
                    '--start-date',
                    default='1995-06-16',
                    help='start date in YYYY-MM-DD format')

# Defaults to today's date
parser.add_argument('-e',
                    '--end-date',
                    default=datetime.datetime.today().strftime('%Y-%m-%d'),
                    help='end date in YYYY-MM-DD format')

def main():
    args = parser.parse_args()

    # Read the configuration file
    with open(args.conf.name, 'r') as conf_file:
        conf = json.load(conf_file)
    if not conf:
        raise SystemExit('Invalid Configuration File')

    # Read start and end dates
    earliest_day = args.start_date
    latest_day = args.end_date

    # Paths initialization
    src_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.dirname(src_dir)
    metadata_dir = os.path.join(app_dir, conf['metadata_dir'])

    # API key
    data_gov_api_key = os.environ.get('DATA_GOV_API_KEY')
    if not data_gov_api_key:
        raise ValueError('API key not found.\n`export DATA_GOV_API_KEY=<your_API_key>` before running this program')

    # API end-point
    api_endpoint = conf['apod_api_url']

    # Starting and ending years
    earliest_year = int(earliest_day[:4])
    latest_year = int(latest_day[:4])

    # Loop over yearly ranges
    for yyyy in range(earliest_year, latest_year+1):
        if yyyy == earliest_year:
            start_date = earliest_day
            end_date = '{}-12-31'.format(earliest_year)
        elif yyyy == latest_year:
            start_date = '{}-01-01'.format(latest_year)
            end_date = latest_day
        else:
            start_date = '{}-01-01'.format(yyyy)
            end_date = '{}-12-31'.format(yyyy)

        payload = {"api_key": data_gov_api_key,
                   "start_date": start_date,
                   "end_date": end_date}

        r = requests.get(api_endpoint, payload)

        if r.status_code != 200:
            print('Could not get data for year {}'.format(yyyy))
            continue

        response_json = r.json()
        outfile = os.path.join(metadata_dir, 'metadata_{}'.format(yyyy))

        print('Year: {} - Writing {} records to {}'\
            .format(yyyy, len(response_json), outfile))
        with open(outfile, 'w') as o:
            json.dump(response_json, o)
        time.sleep(1)

if __name__ == "__main__":
    raise SystemExit(main())
