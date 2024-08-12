#!/usr/bin/env python3
'''Module to provide statistics about Nginx logs stored in MongoDB.
'''
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    '''Prints statistics about Nginx request logs.

    Args:
        nginx_collection (pymongo.collection.Collection): MongoDB collection
        containing the Nginx logs.
    '''
    total_logs = nginx_collection.count_documents({})
    print(f'{total_logs} logs')
    print('Methods:')

    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        method_count = nginx_collection.count_documents({'method': method})
        print(f'\tmethod {method}: {method_count}')

    status_check_count = nginx_collection.count_documents({
        'method': 'GET', 'path': '/status'
    })
    print(f'{status_check_count} status check')


def run():
    '''Connects MongoDB n prints stats abt Nginx logs stored in collection'''
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    print_nginx_request_logs(nginx_collection)


if __name__ == '__main__':
    run()
