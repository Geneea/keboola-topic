# coding=utf-8

import argparse
import json
import csv

import requests
import yaml


URL = 'https://api.geneea.com/s1/topic'

def main(args):
    config = yaml.load(open(args.dataDir + '/config.yml', 'r'))
    input_file = open(args.dataDir + '/' + config['storage']['input']['tables'][0]['source'], 'rb')
    output_file = open(args.dataDir + '/' + config['storage']['output']['tables'][0]['source'], 'wb')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'user_key ' + config['parameters']['user_key']
    }

    id_col = config['parameters']['primary_key_column']
    text_col = config['parameters']['data_column']
    reader = csv.DictReader(input_file)

    writer = csv.DictWriter(output_file, fieldnames=['id', 'topic', 'confidence'])
    writer.writeheader()

    for row in reader:
        data = {
            'text': row[text_col]
        }
        response = requests.post(URL, headers=headers, data=json.dumps(data)).json()
        writer.writerow({
            'id': row[id_col].encode('utf-8'),
            'topic': response['topic'].encode('utf-8'),
            'confidence': str(response['confidence'])
        })

    input_file.close()
    output_file.close()

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-d', '--data', dest='dataDir')
    args = argparser.parse_args()

    main(args)
