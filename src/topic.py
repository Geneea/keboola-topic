# coding=utf-8

import argparse

URL = 'https://api.geneea.com/s1/topic'

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-d", "--data", dest="dataDir")
    args = argparser.parse_args()
    
    print args.dataDir, "/config.yml"


