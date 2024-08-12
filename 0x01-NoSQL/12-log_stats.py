#!/usr/bin/env python3
'''Task 12's module.
This module provides functionality to print statistics about Nginx request logs 
stored in a MongoDB collection.
'''
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    '''Prints stats about Nginx request logs.

    Args:
        nginx_collection (pymongo.collection.Collection): The MongoDB collection 
        containing the Nginx logs.

    Prints:
        The number of logs and the count of each HTTP method found in the logs.
    '''
    print('{} logs'.format(nginx_collection.count_documents({})))
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = nginx_collection.count_documents({'method': method})
        print('\tmethod {}: {}'.format(method, req_count))
    status_checks_count = nginx_collection.count_documents({
        'method': 'GET', 'path': '/status'
    })
    print('{} status check'.format(status_checks_count))


def run():
    '''Provides some stats about Nginx logs stored in MongoDB.'''
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)


if __name__ == '__main__':
    run()
