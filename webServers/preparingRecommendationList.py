from operator import itemgetter 
import extensionFiles as exts
from datetime import datetime, timedelta, timezone
import time
import json
import csv as csv
import sys, os, shutil

MIN_TOTAL_COMMITS = 1
INTERVAL_OF_DAYS = 365
MIN_MATCH_PERCENTAGE = 0 #0%
MAX_OF_RECOMMENDATIONS = 5

class DevRecommendationList(object):

    def __init__(self, logger, dicts, resultsPath, repoName, approach):
        
        self.logger = logger
        self.dicts = dicts
        self.resultsPath = resultsPath
        self.CHANGES_IN_FILE_APPROACH = bool(approach)
        self.repoName = repoName

        self.strStrategy = str
        if self.CHANGES_IN_FILE_APPROACH:  #recommendation strategy
            self.strStrategy = "strategy2"
        else: self.strStrategy = "strategy1"

        self.since = datetime.now() - timedelta(days=INTERVAL_OF_DAYS)

    def setDevRecommendationList(self):
        self.logger.info(" set Developer Recommendation List...", self.dicts.getDictDevRec().keys())

        try:
            for devFocus in self.dicts.getDictDevRec().keys():

                self.dicts.setDictRecListResult(devFocus)
                
                strategyResult = dict()
                strategyResult['strategy'] = self.strStrategy
                strategyResult['devRecList'] = []

                devRecList = sorted(self.dicts.getDictDevRec()[devFocus].items(), key = itemgetter(1), reverse = True)

                self.logger.info(" set Developer Recommendation List - devRecList...", devRecList)

                count=0
                for recDevItem in devRecList:

                    if count < MAX_OF_RECOMMENDATIONS: 

                        recommendedDev = recDevItem[0] #login

                        recDev = dict()

                        recDev['login'] = recommendedDev
                        recDev['name'] = self.dicts.getDictDevInfo().get(recommendedDev).get('name')
                        recDev['full_name'] = self.dicts.getDictDevInfo().get(recommendedDev).get('full_name')
                        recDev['avatar_url'] = self.dicts.getUserDetailsByLogin(recommendedDev).get("avatar_url")
                        recDev['html_url'] = self.dicts.getUserDetailsByLogin(recommendedDev).get("html_url")
                        recDev['last_commit_date'] = self.dicts.getDictDevInfo().get(recommendedDev).get('last_commit_date')
                        recDev['total_commits'] = self.dicts.getDictDevInfo().get(recommendedDev).get('total_commits')
                        recDev['total_commits_unmerged'] = self.dicts.getDictDevInfo().get(recommendedDev).get('total_commits_ahead')
                        if self.dicts.getUserDetailsByLogin(recommendedDev).get("followers")=='---':
                            recDev['followers'] = 0
                        else: recDev['followers'] = int(self.dicts.getUserDetailsByLogin(recommendedDev).get("followers"))
                        if self.dicts.getUserDetailsByLogin(recommendedDev).get("following")=='---':
                            recDev['following'] = 0
                        else: recDev['following'] = int(self.dicts.getUserDetailsByLogin(recommendedDev).get("following"))

                        recDev['match_percentage'] = recDevItem[1] #similarity
                        recDev['recDev_relevant_file_list'] = []
                        recDev['devFocus_relevant_file_list'] = []


                        devFocusFileList = sorted(self.dicts.getDictDevRelevantFiles()[devFocus].items(), key = itemgetter(1), reverse = True)
                        self.logger.info(" set Developer Recommendation List - devFocusFileList...", devFocusFileList)

                        topDevFileList   = sorted(self.dicts.getDictDevRelevantFiles()[recommendedDev].items(), key = itemgetter(1), reverse = True)
                        self.logger.info(" set Developer Recommendation List - topDevFileList...", topDevFileList)

                        for devFocus_filename in devFocusFileList:
                            for devTop_filename in topDevFileList:
                                if devFocus_filename[0]==devTop_filename[0]:

                                    commonFile = devFocus_filename[0]

                                    for devFocus_infoFile in self.dicts.getDictFilesInfoByOwner(devFocus):
                                        if (commonFile == devFocus_infoFile['filename']):
                                            devFocus_relevantFile = dict()
                                            devFocus_relevantFile['filename'] = devFocus_infoFile['filename']
                                            devFocus_relevantFile['fileChanges_url'] = devFocus_infoFile['fileChanges_url']
                                            devFocus_relevantFile['totalNumberOfChanges'] = devFocus_infoFile['totalNumberOfChanges']
                                            devFocus_relevantFile['totalNumberOfChangedFile'] = devFocus_infoFile['totalNumberOfChangedFile']
                                            
                                            recDev['devFocus_relevant_file_list'].append(devFocus_relevantFile) 
                                            del devFocus_relevantFile    

                                    for devTop_infoFile in self.dicts.getDictFilesInfoByOwner(recommendedDev):
                                        if (commonFile == devTop_infoFile['filename']):
                                            devTop_relevantFile  = dict()
                                            devTop_relevantFile['filename'] = devTop_infoFile['filename']
                                            devTop_relevantFile['fileChanges_url'] = devTop_infoFile['fileChanges_url']
                                            devTop_relevantFile['totalNumberOfChanges'] = devTop_infoFile['totalNumberOfChanges']
                                            devTop_relevantFile['totalNumberOfChangedFile'] = devTop_infoFile['totalNumberOfChangedFile']
                                            
                                            recDev['recDev_relevant_file_list'].append(devTop_relevantFile)
                                            del devTop_relevantFile

                        strategyResult['devRecList'].append(recDev)
                        del recDev
                        count+=1

                self.dicts.setStrategyInDictRecListResult(devFocus, strategyResult)

            print ("recListResult ..: ", self.dicts.getDictRecListResult())
            print()
        except Exception:
            self.logger.error("Exception occurred...: ", exc_info=True)



def main(logger, dicts, resultsPath, repoName, strategy):

    recList = DevRecommendationList(logger, dicts, resultsPath, repoName, strategy)
    recList.setDevRecommendationList()


if __name__ == "__main__":

    print(f"Arguments count: {len(sys.argv)}")

    print(f"File name       : {sys.argv[0]}")
    print(f"logger          : {sys.argv[1]}")
    print(f"dict objects    : {sys.argv[2]}")
    print(f"resultsPath     : {sys.argv[3]}")
    print(f"repoName        : {sys.argv[4]}")
    print(f"strategy        : {sys.argv[5]}")

    print()
    time.sleep(5)

    if (sys.argv[4]=="True"):
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True)
    else: main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], False)