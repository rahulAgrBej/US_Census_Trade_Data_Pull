import requests
import json
import pprint
import helpers

# international import and export trade URLs
EXPORT_URL = 'https://api.census.gov/data/timeseries/intltrade/exports/hs'
IMPORT_URL = 'https://api.census.gov/data/timeseries/intltrade/imports/hs'

# read in API key
f = open('census_api_key.txt', 'r')
API_KEY = f.read()
f.close()

# make sure there are no extra characters in key
API_KEY = API_KEY.rstrip('\n')

tableHeadersExport = [
    'CTY_CODE',
    'CTY_NAME',
    'ALL_VAL_MO',
    'QTY_1_MO',
    'QTY_1_MO_FLAG',
    'UNIT_QY1',
    'QTY_2_MO',
    'QTY_2_MO_FLAG',
    'UNIT_QY2',
    #'UNIT_QY2',
    #'AIR_VAL_MO', # air value
    #'AIR_WGT_MO', # air weight value
    #'VES_VAL_MO', # vessel value
    #'CNT_VAL_MO', # containerized vessel value
    'MONTH',
    'SUMMARY_LVL',
    'DF'
]

tableHeadersImport = [
    'CTY_CODE',
    'CTY_NAME',
    'GEN_CHA_MO',
    'GEN_CIF_MO',
    'GEN_VAL_MO',
    'GEN_QY1_MO_FLAG',
    'UNIT_QY1',
    'GEN_QY2_MO',
    'GEN_QY2_MO_FLAG',
    'UNIT_QY2',
    #'AIR_VAL_MO', # air value
    #'AIR_WGT_MO', # air weight value
    #'VES_VAL_MO', # vessel value
    #'VES_WGT_MO', # vessel value weight
    #'CNT_VAL_MO', # containerized vessel value
    #'CNT_WGT_MO', # containerized vessel weight value
    'MONTH',
    'SUMMARY_LVL'
    #'DF'
]

years = [
    #2017,
    2018,
    2019
]

ctyCodes = [
]

hsLvl = 'HS10'

# Get all relevant HS Codes from files

inFilePath = 'seafoodLvl10Codes.csv'
inF = open(inFilePath, 'r')
lines = inF.readlines()
inF.close()

seafoodHScodes = []

for line in lines:
    line = line.rstrip('\n')
    seafoodHScodes.append(line)

#seafoodHScodes = ['0301110020']

for year in years:
    print(f'hs codes are being searched for {year}')

    for hsCode in seafoodHScodes:

        print(f'YEAR: {year} HS CODE: {hsCode}')
        # INTL and Domestic export trades
        exports = helpers.getTradeRecords('export', EXPORT_URL, tableHeadersExport, [hsCode], hsLvl, [year], ctyCodes, API_KEY)
        exportFile = ''
        if exports != None:
            exportFile = helpers.makeCSV(exports)
        print('retrieved exports')

        fOutName = f'Raw_Data/exports/{year}/{hsCode}_{str(year)}.csv'
        fOut = open(fOutName, 'w')
        fOut.write(exportFile)
        fOut.close()

        imports = helpers.getTradeRecords('import', IMPORT_URL, tableHeadersImport, [hsCode], hsLvl, [year], ctyCodes, API_KEY)
        importFile = ''
        if imports != None:
            importFile = helpers.makeCSV(imports)
        print('retrieved imports')

        importFilePath = f'Raw_Data/imports/{year}/{hsCode}_{str(year)}.csv'
        importF = open(importFilePath, 'w')
        importF.write(importFile)
        importF.close()
