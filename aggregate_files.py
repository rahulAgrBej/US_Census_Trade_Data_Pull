import os
import json
import pandas as pd

def aggregate_files(folderPath):

    fileNames = os.listdir(folderPath)

    dfs = []

    for fileName in fileNames:
        if fileName != '.DS_Store':
            fp = os.path.join(folderPath, fileName)
            print(fp)
            fileSize = os.path.getsize(fp)
            if fileSize > 0:
                currDf = pd.read_csv(fp)
                dfs.append(currDf)

    aggregateDf = pd.concat(dfs)
    return aggregateDf

importFolder = 'Raw_Data/imports_all_files/'
exportFolder = 'Raw_Data/exports_all_files/'

print('Aggregating IMPORT files')
importDf = aggregate_files(importFolder)

print('Aggregating EXPORT files')
exportDf = aggregate_files(exportFolder)

outImportPath = 'Data_Pulls/imports.csv'
outExportPath = 'Data_Pulls/exports.csv'

print('Writing IMPORT records')
importDf.to_csv(outImportPath, index=False)

print('Writing EXPORT records')
exportDf.to_csv(outExportPath, index=False)