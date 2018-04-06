# Ron Johnson
# 4/5/2018
#
# Retrieve all Gracenote ProgramMappings and count by date to estimate volume.
# Shows how to work with Gracenote API paging.

import requests
import xmltodict

UpdateID = 0
Limit = 1000
API_key = '<your-key-here>'

URLbase = 'http://on-api.gracenote.com/v3/ProgramMappings?updateId={0}&limit={1}&api_key={2}'
ProgramMappingsCountByDate = {}

while True:
    # retrieve next page from Gracenote
    URLinstance = URLbase.format(UpdateID, Limit, API_key)
    print(URLinstance)  # show progress
    RequestReturnFull = requests.get(URLinstance)
    ReturnRequest = xmltodict.parse(RequestReturnFull.text)

    # parse out programMappings list
    if 'programMapping' in ReturnRequest['on']:
        programMappingList = ReturnRequest['on']['programMappings']['programMapping']
    else:
        programMappingList = []

    # process all programMapping in list
    for programMapping in programMappingList:
        updateDate = programMapping['@updateDate'][0:10]

        if updateDate in ProgramMappingsCountByDate:
            ProgramMappingsCountByDate[updateDate] += 1
        else:
            ProgramMappingsCountByDate[updateDate] = 0

    # Get next UpdateID OR break
    if 'nextUpdateId' in ReturnRequest['on']['header']['streamData']:
        UpdateID = ReturnRequest['on']['header']['streamData']['nextUpdateId']
    else:
        break

# print count by date
for CountDate in ProgramMappingsCountByDate:
    print(CountDate, ProgramMappingsCountByDate[CountDate])
