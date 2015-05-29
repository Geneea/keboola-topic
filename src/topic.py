# coding=utf-8

import sys
import argparse
import json
import csv

import requests
import yaml

URL = 'https://api.geneea.com/keboola/topic'

try:
    from requests.packages import urllib3
    urllib3.disable_warnings()
except ImportError:
    pass

def main(args):
    with open(args.dataDir + '/config.yml', 'r') as config_file:
        config = yaml.load(config_file)

        input_path = args.dataDir + '/in/tables/' + config['storage']['input']['tables'][0]['source']
        output_path = args.dataDir + '/out/tables/' + config['storage']['output']['tables'][0]['source']
        user_key = config['parameters']['user_key']
        customer_id = config['parameters']['customer_id']
        id_col = config['parameters']['id_column']
        data_col = config['parameters']['data_column']
        language = config['parameters']['language'] if hasattr(config['parameters'], 'language') else None

    with open(input_path, 'rb') as input_file, open(output_path, 'wb') as output_file:
        reader = csv.DictReader(input_file)
        rows = list(reader)
        documents = map(lambda row: {'id': row[id_col], 'text': row[data_col]}, rows)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'user_key ' + user_key
        }
        data = {
            'customerId': customer_id,
            'language': language,
            'documents': documents
        }

        print >> sys.stdout, "sending {n} documents for topic detection".format(n=len(documents))
        response = requests.post(URL, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            response.raise_for_status()

        results = response.json()

        writer = csv.DictWriter(output_file, fieldnames=[id_col, 'topic', 'confidence'])
        writer.writeheader()

        for doc in results:
            writer.writerow({
                id_col: doc['id'].encode('utf-8'),
                'topic': doc['topic'].encode('utf-8'),
                'confidence': str(doc['confidence'])
            })

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-d', '--data', dest='dataDir', required=True)
    args = argparser.parse_args()

    try:
        main(args)
        print >> sys.stdout, "successfully finished"
        sys.exit(0)
    except (LookupError, IOError, csv.Error) as e:
        print >> sys.stderr, "{type}: {e}".format(type=type(e).__name__, e=e)
        sys.exit(1)
    except Exception as e:
        print >> sys.stderr, "{type}: {e}".format(type=type(e).__name__, e=e)
        sys.exit(2)
