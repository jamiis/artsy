# python libs
import urllib

# 3rd party
import requests
from pymongo import MongoClient
# connect to mongoDB, get articles collection
client = MongoClient('mongodb://localhost')
db = client.artsy

# keep those keys hidden!
from keys import *

apiurl = 'https://api.artsy.net/api/'
headers = {
    #'Accept': 'application/vnd.artsy-v3+json',
    'X-XAPP-Token': token,
}

# get all artists, write into 'artists'
req = requests.get(apiurl + 'artists', headers=headers)
reqjson = req.json()

# while there are pages to be had
'''
while('next' in reqjson['_links']):
    # iterate through list of artist dictionaries
    for artist in reqjson['_embedded']['artists']:
        # save artist to mongo
        query = { 'id': artist['id'] }
        update = { '$set': artist }
        db.artists.update_one(query, update, upsert=True)
    print 'artist', artist['id'], artist['name']

    # get next page of artists
    req = requests.get(reqjson['_links']['next']['href'], headers=headers)
    reqjson = req.json()
'''

for artist in db.artists.find():
    import ipdb; ipdb.set_trace();
    req = requests.get(artist['_links']['artworks']['href'], headers=headers)
    query = { 'id': artist['id'] }
    update = { '$set': { 'artworks': req.json()['_embedded']['artworks'] }}
    db.artist.update_one(query, update)
    print 'artworks', artist['id'], artist['name']
