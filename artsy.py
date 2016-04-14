# python libs
import urllib, argparse

# 3rd party
import requests
from pymongo import MongoClient

# keep those keys hidden!
from keys import *

if __name__ == '__main__':
    # C M D L I N E   A R G U M E N T S
    parser = argparse.ArgumentParser(description='pull artist and associated artwork information from artsy api and store in mongo.')
    parser.add_argument('--ops', nargs='+', type=str, default=['artists','artworks'], help='operations to perform. presently avail: artists, artworks.')
    parser.add_argument('--host', default='localhost', type=str, help='host where mongo is running.')
    arg = parser.parse_args()

    # D B   &   S E T U P
    # connect to mongoDB on default port
    client = MongoClient('mongodb://{host}'.format(**vars(arg)))
    db = client.artsy

    # api url setup
    apiurl = 'https://api.artsy.net/api/'
    headers = { 'X-XAPP-Token': token }

    # A R T I S T S
    # hit artists endpoint
    if 'artists' in arg.ops:
        # get first page of artists
        req = requests.get(apiurl + 'artists', headers=headers)
        reqjson = req.json()

        # while there are pages to be had
        while('next' in reqjson['_links']):

            # iterate through list of artist dictionaries
            for artist in reqjson['_embedded']['artists']:
                # store artist in mongo
                query = { 'id': artist['id'] }
                update = { '$set': artist }
                db.artists.update_one(query, update, upsert=True)
            print 'artist', artist['id'], artist['name']

            # get next page of artists
            req = requests.get(reqjson['_links']['next']['href'], headers=headers)
            reqjson = req.json()

    # A R T W O R K S
    if 'artworks' in arg.ops:
        for artist in db.artists.find():
            req = requests.get(artist['_links']['artworks']['href'], headers=headers)
            query = { 'id': artist['id'] }
            update = { '$set': { 'artworks': req.json()['_embedded']['artworks'] }}
            db.artists.update_one(query, update)
            print 'artworks', artist['id'], artist['name']
