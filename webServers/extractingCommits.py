#!/usr/bin/env python
import importlib
import logging
import sys, os, shutil
import json
import csv as csv
import scipy
import numpy as np
import time
import logging
import threading
import random
import extensionFiles as exts
import creatingExpertiseList as exps
import preparingRecommendationList as recList
import similarity as sim
from operator import itemgetter  
from collections import OrderedDict
from github import Github, GithubException
from datetime import datetime, timedelta, timezone
import calendar
import textdistance

__author__ = "Kattiana Constantino"
__copyright__ = ""
__credits__ = ["Kattiana Constantino"]
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = ""
__email__ = "kattiana@gmail.com"
__status__ = "Production"

#CHANGES_IN_FILE_APPROACH = False

SET_RANGE_OF_DAYS = False
INTERVAL_OF_DAYS = 365
CROSS_COMMITS = False

# https://realpython.com/python-logging/:
# https://docs.python.org/3/library/logging.html#logrecord-attributes

class Logger():

    def createLogger(self):
        
        # create logger
        self.logger = logging.getLogger('coopfinder')
        self.logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)

        # create formatter
        self.formatter = logging.Formatter('%(asctime)s-%(funcName)s-%(levelname)s-%(message)s')

        # add formatter to ch
        self.ch.setFormatter(self.formatter)

        # add ch to logger
        self.logger.addHandler(self.ch)

    def getLogger(self):
        return self.logger

class CreatePath(object):
    """
        Create path 
        @param repoPath 
        @param commitFilesDir
    """
    print(" Create path")
    def __init__(self, repoPath, commitFilesDir, excludedCommitFilesDir, repoDataDir, commitFilesInfoDir, changedStrgyResultsDir, changesStrgyResultsDir):
        self.repoPath = repoPath
        self.commitFilesDir = commitFilesDir
        self.excludedCommitFilesDir = excludedCommitFilesDir
        self.repoDataDir = repoDataDir
        self.commitFilesInfoDir = commitFilesInfoDir
        self.changedStrgyResultsDir = changedStrgyResultsDir
        self.changesStrgyResultsDir = changesStrgyResultsDir
        
    def createPaths(self):
        if not os.path.exists(self.repoPath):
            os.makedirs(self.repoPath)
        else: shutil.rmtree(self.repoPath, ignore_errors=True)    

        if not os.path.exists(self.commitFilesDir):
            os.makedirs(self.commitFilesDir)    

        if not os.path.exists(self.excludedCommitFilesDir):
            os.makedirs(self.excludedCommitFilesDir)

        if not os.path.exists(self.repoDataDir):
            os.makedirs(self.repoDataDir)

        if not os.path.exists(self.commitFilesInfoDir):
            os.makedirs(self.commitFilesInfoDir) 

        if not os.path.exists(self.changedStrgyResultsDir):
            os.makedirs(self.changedStrgyResultsDir) 

        if not os.path.exists(self.changesStrgyResultsDir):
            os.makedirs(self.changesStrgyResultsDir) 

class CheckToken(object):
    """ 
        Class .....
        @param int 
    """
    def __init__(self, logger, accessToken):

        self.RATE_LIMIT = 4990
        self.access_token = accessToken
        self.gh = Github(self.access_token, per_page=100)

        self.logger = logger
        self.logger.info("Check Token")
        self.currentIndexToken = 0

    def deleteConnectionGH(self):
        del self.gh

    def setConnectionGH(self, token):
        print("Create Connection with ", token)
        self.gh = Github(token, per_page=100)

    def getGHConnection(self):
        return self.gh

    def getListDir(self, pathFiles):
        return os.listdir(pathFiles)

    def check_rate_limited(self):
        changeTokenResult = self.changeToken()
        if changeTokenResult: #true changedToken 
            self.getGHConnection().rate_limiting_resettime
            strLogger = '{}{} {} {}'.format("ChangeToken (TRUE) - .........: ", self.getGHConnection().rate_limiting[0], self.getGHConnection().rate_limiting[1], self.access_token)
            self.logger.info(strLogger)

    def changeToken(self):
        #global current_index_token 

        changedToken = False
        rate_limit_remaining = self.getGHConnection().rate_limiting[0]

        if rate_limit_remaining <= 1:
            core_rate_limit = self.getGHConnection().get_rate_limit().core
            reset_timestamp = calendar.timegm(core_rate_limit.reset.timetuple())
            sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 5  # add 5 seconds to be sure the rate limit has been reset
            
            strLogger = '{}{} {} {} {}'.format("Rate_limit_remaining..............: ", rate_limit_remaining, core_rate_limit, calendar.timegm(time.gmtime()), time.ctime(calendar.timegm(time.gmtime()) + 5 + sleep_time))
            self.logger.warning(strLogger)
            time.sleep(sleep_time)
            
        return changedToken
        
class CreateDicts(object):
    def __init__(self):

        self.dictUserInfo = dict()
        self.dictDevFileChanges = dict()
        self.dictDevInfo = dict()
        self.dictDevRec = dict()
        self.dictDevelopers = dict()
        self.dictRecListChangedFiles = dict()
        self.dictRecListChangesInFiles = dict()
        self.dictCorpusChangedFiles = dict()
        self.dictCorpusChangesInFiles = dict()
        self.dictForksData = dict()
        self.dictDevFileChangesInfo = dict()
        self.dictDevRelevantFiles = dict()
        self.dictRecListResult = dict()
        self.devExpertiseList = dict()

        self.fork_names = []

    def setDictRecListResult(self, devLogin):
        if devLogin not in self.dictRecListResult.keys():
            devRecResult = dict()
            devRecResult['login'] = devLogin
            devRecResult['name'] = self.getDictDevInfo().get(devLogin).get('name')
            devRecResult['full_name'] = self.getDictDevInfo().get(devLogin).get('full_name')
            devRecResult['avatar_url'] = self.getUserDetailsByLogin(devLogin).get("avatar_url")
            devRecResult['html_url'] = self.getUserDetailsByLogin(devLogin).get("html_url")
            devRecResult['last_commit_date'] = self.getDictDevInfo().get(devLogin).get('last_commit_date')
            devRecResult['total_commits'] = self.getDictDevInfo().get(devLogin).get('total_commits')
            devRecResult['total_commits_unmerged'] = self.getDictDevInfo().get(devLogin).get('total_commits_ahead')
            if self.getUserDetailsByLogin(devLogin).get("followers")=='---':
                devRecResult['followers'] = 0
            else: devRecResult['followers'] = int(self.getUserDetailsByLogin(devLogin).get("followers"))
            if self.getUserDetailsByLogin(devLogin).get("following")=='---':
                devRecResult['following'] = 0
            else: devRecResult['following'] = int(self.getUserDetailsByLogin(devLogin).get("following"))
            devRecResult['rec_strategy_list'] = []
            self.dictRecListResult[devLogin] = devRecResult
        
    def setStrategyInDictRecListResult(self, devLogin, dictStrategy):
        if devLogin is not None:
            devRecResult = self.dictRecListResult.get(devLogin)
            devRecResult['rec_strategy_list'].append(dictStrategy)

    def getDictRecListResult(self):
        return self.dictRecListResult
    
    def getDictRecListResultByLogin(self, devLogin):
        return self.dictRecListResult[devLogin] 

    def setUserDetails(self, iduser, login, name, isFork, isActive, email, avatar_url, html_url, 
        followers, followers_url, following, following_url, organizations_url):
        # Insere dados no dictionario
        if login not in self.dictUserInfo:
            self.dictUserInfo[login] = {}
            self.dictUserInfo[login]['login'] = login
            self.dictUserInfo[login]['name'] = []  # list of names, or nicknames, and the author's login

        if iduser:
            self.dictUserInfo[login]['id'] = iduser
        else: self.dictUserInfo[login]['id'] = "00000"

        if name:
            self.dictUserInfo[login]['name'].append(name)
            if (name != login):
                self.dictUserInfo[login]['name'].append(login)
        else: self.dictUserInfo[login]['name'].append(login)

        self.dictUserInfo[login]['isFork'] = isFork
        self.dictUserInfo[login]['isActive'] = isActive
        
        if email:
            self.dictUserInfo[login]['email'] = email
        else: self.dictUserInfo[login]['email'] = "---"

        if avatar_url:
            self.dictUserInfo[login]['avatar_url'] = avatar_url
        else: self.dictUserInfo[login]['avatar_url'] = "---" 
        
        if html_url:
            self.dictUserInfo[login]['html_url'] = html_url
        else: self.dictUserInfo[login]['html_url'] = "---"
        
        if followers:
            self.dictUserInfo[login]['followers'] = followers
        else: self.dictUserInfo[login]['followers'] = "---"
        
        if followers_url:
            self.dictUserInfo[login]['followers_url'] = followers_url
        else: self.dictUserInfo[login]['followers_url'] = "---" 
        
        if following:
            self.dictUserInfo[login]['following'] = following
        else: self.dictUserInfo[login]['following'] = "---" 
        
        if following_url:
            self.dictUserInfo[login]['following_url'] = following_url
        else: self.dictUserInfo[login]['following_url'] = "---" 

        if organizations_url:
            self.dictUserInfo[login]['organizations_url']= organizations_url
        else: self.dictUserInfo[login]['organizations_url'] = "---" 

    def setUserDetailsByName(self, login, name):
        if name and (name not in self.dictUserInfo[login]['name']):
            print ("setUserDetailsByName...: ", login, name, self.dictUserInfo[login]['name'])
            self.dictUserInfo[login]['name'].append(name)

    def setUserDetailsByFullname(self, login, full_name):
        if full_name:
            self.dictUserInfo[login]['full_name'] = full_name
        else: self.dictUserInfo[login]['full_name'] = "---"

    def setUserDetailsByEmail(self, login, email):
        if email and (email ):
            if (self.dictUserInfo[login]['email'] == "---"):   
                self.dictUserInfo[login]['email'] = email

    def setUserDetailsByIsFork(self, login, isFork):
        self.dictUserInfo[login]['isFork'] = isFork
        
    def getLoginFromUserDetails(self,name):
        for key in self.dictUserInfo.keys():
            if name in self.dictUserInfo[key]['name']:
                print()
                print("getLoginFromUserDetails (name, key)..: ", name, key)
                return key
            else: pass
        return None

    def getUserDetailsByLogin(self, login):
        return self.dictUserInfo[login]  

    def getUserDetails(self):
        return self.dictUserInfo

    def setDictDevRelevantFiles(self, key, filename, tfidf):
        # Insere dados no dictionario
        if key not in self.dictDevRelevantFiles:
            self.dictDevRelevantFiles[key] = {}

        if filename is not None:
            self.dictDevRelevantFiles[key][filename] = tfidf

    def getDictDevRelevantFiles(self):
        return self.dictDevRelevantFiles

    def getDictDevRelevantFilesByOwner(self, key):
        return self.dictDevRelevantFiles.get(key)

    def setDictDevFileChangesInfo_LastURL(self, key, filename, last_fileChanges_url):
        print(key, filename, last_fileChanges_url)

    def setDictDevFileChangesInfo_LastDate(self, key, filename, last_fileChanges_date):
        print(key, filename, last_fileChanges_date)

    def setDictDevFileChangesInfo_HighestChangesURL(self, key, filename, highest_changes_url):
        print(key, filename, highest_changes_url) 

    def setDictDevFileChangesInfo_HighestChanges(self, key, filename, highest_changes):
        print(key, filename, highest_changes)

    def setDictDevFileChanges(self, author, filename, numberOfChanges):
        if author not in self.dictDevFileChanges:
            self.dictDevFileChanges[author] = {}

        if filename in self.dictDevFileChanges[author]:
            self.dictDevFileChanges[author][filename]+=numberOfChanges
        else: 
            self.dictDevFileChanges[author][filename]=numberOfChanges
    
    def getDictDevFileChanges(self):
        return self.dictDevFileChanges
    
    def getDictDevFileChangesByAuthor(self, author):
        return self.dictDevFileChanges[author]
    
    def setDictFilesInfo(self, key, commit_sha, commit_message, filename, numberOfChanges, fileChanges_url, fileChanges_date, committedByAuthor):
        # foi decidido considerar a url do commit pq a do arquivo estava quebrando para alguns casos

        if key not in self.dictDevFileChangesInfo.keys():
            dictFileInfo = dict()
            dictFileInfo['commit_sha'] = []
            dictFileInfo['commit_sha'].append(commit_sha)
            dictFileInfo['commit_message'] = []
            dictFileInfo['commit_message'].append(commit_message)
            dictFileInfo['highestChanges_commit_sha']=commit_sha
            dictFileInfo['highestChanges_commit_message']=commit_message
            dictFileInfo['last_commit_sha']=commit_sha
            dictFileInfo['last_commit_message']=commit_message

            dictFileInfo['filename']=filename
            dictFileInfo['fileChanges_url']=[]
            dictFileInfo['fileChanges_url'].append(fileChanges_url)
            dictFileInfo['highestChanges']=int(numberOfChanges) 
            dictFileInfo['highestChanges_url']=fileChanges_url
            dictFileInfo['last_fileChanges_date']=fileChanges_date
            dictFileInfo['last_fileChanges_url']=fileChanges_url
            dictFileInfo['best_commit_url']=fileChanges_url
            dictFileInfo['totalNumberOfChanges']=int(numberOfChanges)
            dictFileInfo['totalNumberOfChangedFile']=1

            self.dictDevFileChangesInfo[key] = [] 
            self.dictDevFileChangesInfo[key].append(dictFileInfo)

            del dictFileInfo

        else:
            
            #TUTORIAL: https://www.geeksforgeeks.org/python-get-values-of-particular-key-in-list-of-dictionaries/    
            #SOLUTION 1:
            # Using list comprehension 
            # Get values of particular key in list of dictionaries 
            #filename_list = [ sub['filename'] for sub in dictDevFileChangesInfo.get(key)]

            #SOLUTION 2:
            # Using map() + itemgetter() 
            # Get values of particular key in list of dictionaries 
            filename_list = list(map(itemgetter('filename'), self.dictDevFileChangesInfo.get(key)))
            dictFileInfoa = dict()
            
            #Adding new item in the list
            if filename not in filename_list:

                dictFileInfoa['commit_sha'] = []
                dictFileInfoa['commit_sha'].append(commit_sha)
                dictFileInfoa['commit_message'] = []
                dictFileInfoa['commit_message'].append(commit_message)
                dictFileInfoa['highestChanges_commit_sha']=commit_sha
                dictFileInfoa['highestChanges_commit_message']=commit_message
                dictFileInfoa['last_commit_sha']=commit_sha
                dictFileInfoa['last_commit_message']=commit_message

                dictFileInfoa['filename']=filename
                dictFileInfoa['fileChanges_url']=[]
                dictFileInfoa['fileChanges_url'].append(fileChanges_url)
                dictFileInfoa['highestChanges']=int(numberOfChanges) 
                dictFileInfoa['highestChanges_url']=fileChanges_url
                dictFileInfoa['last_fileChanges_date']=fileChanges_date
                dictFileInfoa['last_fileChanges_url']=fileChanges_url
                dictFileInfoa['best_commit_url']=fileChanges_url
                dictFileInfoa['totalNumberOfChanges']=int(numberOfChanges)
                dictFileInfoa['totalNumberOfChangedFile']=1
                
                self.dictDevFileChangesInfo[key].append(dictFileInfoa)

            else: # update item

                for dictFilename in self.dictDevFileChangesInfo.get(key):

                    if dictFilename['filename'] == str(filename):

                        dictFilename['commit_sha'].append(commit_sha)
                        dictFilename['commit_message'].append(commit_message)
                        dictFilename['fileChanges_url'].append(fileChanges_url)
                        dictFilename['totalNumberOfChanges']+=int(numberOfChanges) #update
                        dictFilename['totalNumberOfChangedFile']+=1 #update

                        if dictFilename['highestChanges'] < numberOfChanges: # the highest changes
                            dictFilename['highestChanges_url']=fileChanges_url
                            dictFilename['highestChanges']=int(numberOfChanges)
                            dictFilename['highestChanges_commit_sha']=commit_sha
                            dictFilename['highestChanges_commit_message']=commit_message

                        if dictFilename['last_fileChanges_date'] < fileChanges_date: # mais recente
                            dictFilename['last_fileChanges_date']=fileChanges_date
                            dictFilename['last_fileChanges_url']=fileChanges_url
                            dictFilename['last_commit_sha']=commit_sha
                            dictFilename['last_commit_message']=commit_message

    def getDictFilesInfo(self):
        return self.dictDevFileChangesInfo

    def getDictFilesInfoByOwner(self, key):
        return self.dictDevFileChangesInfo.get(key)

    def setDictDevInfo(self, key, owner_id, full_name, last_commit_date, name, email):     
        
        # Insere dados no dictionario
        if key not in self.dictDevInfo:
            self.dictDevInfo[key] = {}

        if not owner_id:
            self.dictDevInfo[key]['owner_id'] = random.randint(1,101)
        else: self.dictDevInfo[key]['owner_id'] = owner_id

        if full_name is not None:
            self.dictDevInfo[key]['full_name'] = full_name
        else: self.dictDevInfo[key]['full_name'] = "---"

        if last_commit_date is not None:
            self.dictDevInfo[key]['last_commit_date'] = last_commit_date
        else: self.dictDevInfo[key]['last_commit_date'] = "---"

        if name is not None:
            self.dictDevInfo[key]['name'] = name
        else: self.dictDevInfo[key]['name'] = "---"

        if email is not None:
            self.dictDevInfo[key]['email'] = email
        else: self.dictDevInfo[key]['email'] = "---"

    def setDictDevInfo_LastCommitDate(self, key, last_commit_date):
        self.dictDevInfo[key]['last_commit_date']=last_commit_date

    def setDictDevInfo_TotalCommits(self, key, total_commits):
        self.dictDevInfo[key]['total_commits']=total_commits
        
    def setDictDevInfo_CommitsAhead(self, key, total_commits_ahead):
        self.dictDevInfo[key]['total_commits_ahead']=total_commits_ahead

    def checkDictDevInfoCommits(self):
        print ("check Dict Dev Info Commits ")

        for key in self.dictDevInfo.keys():
            try: 
                if self.dictDevInfo[key]['total_commits'] is None:
                    self.setDictDevInfo_TotalCommits(key,0)
            except Exception:
                self.setDictDevInfo_TotalCommits(key,0)    
            try: 
                if self.dictDevInfo[key]['total_commits_ahead'] is None:
                    self.setDictDevInfo_CommitsAhead(key,0)
            except Exception:
                self.setDictDevInfo_CommitsAhead(key,0)    

    def setDictDevRec(self, key, devRec, devSim):
        if key not in self.dictDevRec:
            self.dictDevRec[key] = {}

        self.dictDevRec[key][devRec]=devSim

    def getDictDevRecByKey(self, key):
        return self.dictDevRec[key]

    def getDictDevRec(self):
        return self.dictDevRec

    def getDictDevInfo(self):
        return self.dictDevInfo

    def setDictDevelopers(self,commitFilesDir):
        self.dictDevelopers = self.ghCreateAuthorFileDict(commitFilesDir)

    def getDictDevelopers(self):
        return self.dictDevelopers

    def ghCreateAuthorFileDict(self, commitFilesDir):
        """"
            Create Dict Developer
        """
        files = os.listdir(commitFilesDir)
        files.sort()
        fork_names = []
        dictDev = {}
        #print()
        #print()
        for file in files:
            fork_name = file[0:file.find("_")]
            if self.getUserDetailsByLogin(fork_name).get('isActive'):
                fork_names.append(fork_name)
                if not fork_name in dictDev: 
                    dictDev[fork_name]={}
                with open(os.path.join(commitFilesDir,file),'r') as f:
                    commitFiles = json.load(f)

                for comfile in commitFiles:
                    filename =comfile['filename']
                    if filename in dictDev[fork_name]:
                        dictDev[fork_name][filename]+=1
                    else: 
                        dictDev[fork_name][filename]=1
        return dictDev

    def setRecListChangedFilesDict(self, key, value):
        if key not in self.dictRecListChangedFiles:
            self.dictRecListChangedFiles[key] = [ ]
        self.dictRecListChangedFiles[key].append(value) # esse é o segredo, aqui cria uma lista
                
    def getRecListChangedFilesDict(self):
        return self.dictRecListChangedFiles

    def setRecListChangesInFilesDict(self, key, value):
        if key not in self.dictRecListChangesInFiles:
            self.dictRecListChangesInFiles[key] = []

        self.dictRecListChangesInFiles[key].append(value) # esse é o segredo, aqui cria uma lista
                
    def getRecListChangesInFilesDict(self):
        return self.dictRecListChangesInFiles

    def setDevFilesDictCorpus(self, pathDir, changes):
        print("set Dev Files DictCorpus ") 
        listOfFiles = os.listdir(pathDir)
        listOfFiles.sort() 

        for fileIn in listOfFiles:
            #if os.path.isfile(fileIn):
            fork_name = fileIn[0:fileIn.find("_")]
            print()
            print ("fork_name...: ", fork_name)
            print()
            if fork_name not in self.fork_names:
                self.fork_names.append(fork_name)

            if (changes):
                if not fork_name in self.dictCorpusChangesInFiles:
                    self.dictCorpusChangesInFiles[fork_name]={}
            else:
                if not fork_name in self.dictCorpusChangedFiles:
                    self.dictCorpusChangedFiles[fork_name]={}

            filenames = []
            with open(os.path.join(pathDir,fileIn),'r') as f:
                commitFilesInfo = json.load(f)

            for infoFile in commitFilesInfo:
                filename = infoFile['filename']
                if (changes):
                    self.dictCorpusChangesInFiles[fork_name][filename]=filename
                    for i in range(infoFile['totalNumberOfChanges']): # volume de alterações no arquivo
                        filenames.append(filename)
                else:
                    self.dictCorpusChangedFiles[fork_name][filename]=filename
                    for i in range(infoFile['totalNumberOfChangedFile']): # numero de vezes que o arquivo foi alterado
                        filenames.append(filename)

            strFilenames = " ".join(str(item) for item in filenames)

            if (changes):
                self.dictCorpusChangesInFiles[fork_name]['changedFilesList'] = strFilenames
            else:
                self.dictCorpusChangedFiles[fork_name]['changedFilesList'] = strFilenames
                
    def getDictCorpusChangedFiles(self):
        return self.dictCorpusChangedFiles

    def getDictCorpusChangesInFiles(self):
        return self.dictCorpusChangesInFiles
   
    def getForkNames(self):
        return self.fork_names

    def setDictForksData(self, key, full_name, avatar_url, html_url, description, isFork, stargazers_count, watchers_count, forks_count, open_issues_count, created_at, updated_at, pushed_at, language):  
        
        if key not in self.dictForksData:
            self.dictForksData[key] = {}

        if full_name is not None:
            self.dictForksData[key]['full_name'] = full_name
        else: self.dictForksData[key]['full_name'] = "---"

        if avatar_url is not None:
            self.dictForksData[key]['avatar_url'] = avatar_url
        else: self.dictForksData[key]['avatar_url'] = "---"

        if html_url is not None:
            self.dictForksData[key]['html_url'] = html_url
        else: self.dictForksData[key]['html_url'] = "---"

        if description is not None:
            self.dictForksData[key]['description'] = description
        else: self.dictForksData[key]['description'] = "---"

        if created_at is not None:
            self.dictForksData[key]['created_at'] = created_at
        else: self.dictForksData[key]['created_at'] = "---"

        if updated_at is not None:
            self.dictForksData[key]['updated_at'] = updated_at
        else: self.dictForksData[key]['updated_at'] = "---"

        if pushed_at is not None:
            self.dictForksData[key]['pushed_at'] = pushed_at
        else: self.dictForksData[key]['pushed_at'] = "---"

        if language is not None:
            self.dictForksData[key]['language'] = language
        else: self.dictForksData[key]['language'] = "---"

        self.dictForksData[key]['fork']=isFork  # true/false
        self.dictForksData[key]['stargazers_count']=stargazers_count
        self.dictForksData[key]['watchers_count']=watchers_count
        self.dictForksData[key]['forks_count']=forks_count
        self.dictForksData[key]['open_issues_count']=open_issues_count

        self.dictForksData[key]['total_commits']=0
        self.dictForksData[key]['total_commits_ahead'] = 0
        self.dictForksData[key]['last_commit_date'] = "---" 
        self.dictForksData[key]['type_of_contributor'] = "---" # core, peripheral, one time contributor (otc), newcomer, inactive 
        self.dictForksData[key]['current_fork_status'] = "---" # active, inactive, deleted
        self.dictForksData[key]['current_fork_commits_status'] = "---" # ahead, behind, inactive  
        
    def setDictForksData_TotalCommits(self, key, total_commits):
        self.dictForksData[key]['total_commits']=total_commits
        
    def setDictForksData_CommitsAhead(self, key, total_commits_ahead):
        self.dictForksData[key]['total_commits_ahead']=total_commits_ahead

    def setDictForksData_LastCommitDate(self, key, last_commit_date):
        self.dictForksData[key]['last_commit_date']=last_commit_date

    def setDictForksData_TypeOfContributor(self, key, type_of_contributor):
        self.dictForksData[key]['type_of_contributor']=type_of_contributor

    def setDictForksData_CurrentForkStatus(self, key, current_fork_status):
        self.dictForksData[key]['current_fork_status']=current_fork_status

    def setDictForksData_CurrentForkCommitsStatus(self, key, current_fork_commits_status):
        self.dictForksData[key]['current_fork_commits_status']=current_fork_commits_status

    def getDictForksData(self):
        return self.dictForksData

    def getDictForksDataByKey(self, key):
        return self.dictForksData[key]

    def getDictDevFileChangesInfo(self):
        return self.dictDevFileChangesInfo

    def getDictDevFileChangesInfoByAuthor(self, key):
        return self.dictDevFileChangesInfo[key]


class CollectGHData(object):

    def __init__(self, checkToken, logger, repository, repoPath, commitFilesDir, excludedCommitFilesDir, repoDataDir, commitFilesInfoDir, changedStrgyResultsDir, changesStrgyResultsDir, dicts, extFiles, expDevs):
        self.checkToken = checkToken
        self.logger = logger
        self.all_present_forks_name_list = []
        self.all_present_forks_list = []
        self.all_merged_fork_name_list = []
        self.all_forks_committed_into_range_of_days= []
        self.all_changed_files = []
        self.all_forks_committed = []
        self.listOfCommitAuthors = []
        self.contributors_name_list = []
        self.inactive_contributors = []
        self.fork_names = []
        self.forks_merged = []   # all present forks that has merged commit
        self.forks_unmerged = []  # all present forks that has unmerged commit
        self.repository = repository
        self.commitFilesDir = commitFilesDir
        self.excludedCommitFilesDir = excludedCommitFilesDir
        self.repoDataDir = repoDataDir
        self.commitFilesInfoDir = commitFilesInfoDir
        self.changedStrgyResultsDir = changedStrgyResultsDir
        self.changesStrgyResultsDir = changesStrgyResultsDir

        self.dicts = dicts
        self.repoPath = repoPath
        self.extFiles = extFiles
        self.expDevs = expDevs

        self.createPaths = CreatePath(self.repoPath, self.commitFilesDir, self.excludedCommitFilesDir, repoDataDir, commitFilesInfoDir, self.changedStrgyResultsDir, self.changesStrgyResultsDir)
        self.createPaths.createPaths()
        self.repo = self.checkToken.getGHConnection().get_repo(self.repository)

        self.repoDataFile = open(self.repoDataDir + "/repo_" + self.repo.name + ".json","w+")
        self.repoDataFile.write(json.dumps(self.repo.raw_data))
        self.repoDataFile.close()
        
        #Getting repository owner's commits
        self.repo_owner_login = self.repo.owner.login
        #Getting all forks from repository
        self.forks = self.repo.get_forks()
        self.repo_owner_name = ""

    def getCommitsFromRepoByForks(self):

        for fork in self.forks:
            self.checkToken.check_rate_limited()
            comm_count = self.repo.get_commits(author=fork.owner.login)
        
    def setForksData(self, repo_owner):

        self.repo
        self.dicts.setDictForksData(self.repo.owner.login, self.repo.full_name, self.repo.owner.avatar_url, self.repo.html_url, self.repo.description, self.repo.fork, 
        self.repo.stargazers_count, self.repo.watchers_count, self.repo.forks_count, self.repo.open_issues_count,(self.repo.created_at).isoformat(), (self.repo.updated_at).isoformat(), (self.repo.pushed_at).isoformat(), self.repo.language)
        
        for fork in self.forks:
            self.dicts.setDictForksData(fork.owner.login, fork.full_name, fork.owner.avatar_url, fork.html_url, fork.description, 
            fork.fork, fork.stargazers_count, fork.watchers_count, fork.forks_count, fork.open_issues_count,
            (fork.created_at).isoformat(), (fork.updated_at).isoformat(), (fork.pushed_at).isoformat(), fork.language)
        
    def findLastCommitDate(self, forkAuthorName, commitList):

        mergedCommitCount = 0
        for commit in commitList:
            if len(commit.parents) == 1: #significa que não é apenas um commit de build
                commitAuthor = str
                try:
                    commitAuthor = commit.author.login
                    print("commit.author..............: ", commitAuthor)
                except Exception as e:
                    commitAuthor = commit.commit.author.name
                    print("commit.commit.author.name..: ", commitAuthor) 
                    print("Exception occurred...: ", commitAuthor, e)  
                if commitAuthor == forkAuthorName:
                    print("Name...: ", commitAuthor) 
                    print("Date...: ", commit.commit.author.date)
                    return commit.commit.author.date
            else: 
                mergedCommitCount += 1 
        return "---"    

    def findFirstCommitDate(self, forkAuthorName, commitList):

        mergedCommitCount = 0
        for commit in commitList:
            if len(commit.parents) == 1:
                commitAuthor = str
                try:
                    commitAuthor = commit.author.login
                except Exception as e:
                    commitAuthor = commit.commit.author.name
                if commitAuthor == forkAuthorName:
                    return commit.commit.author.date
            else: 
                mergedCommitCount += 1 
        return "---"    

    def getCommitURLFromFork(self, login, sha):
        if login:
            for fork in self.forks:
                try:
                    if fork.owner.login == login:
                        self.checkToken.check_rate_limited()     
                        commit = fork.get_commit(sha=sha)
                        if commit is not None:
                            return commit.html_url
                except GithubException:
                    self.logger.error("GithubException occurred", exc_info=True)
                except Exception:
                    self.logger.error("Exception occurred", exc_info=True)
            return "---"
        else: return "---"

    def getMergedCommitsByRangeOfDays(self,fork):
        self.checkToken.check_rate_limited()
        commits_tmp=[]
        if SET_RANGE_OF_DAYS:
            since = datetime.now() - timedelta(days=INTERVAL_OF_DAYS)
            commits_tmp = fork.get_commits(author=fork.owner.login, since=since)
            if commits_tmp.totalCount > 0:
                self.all_forks_committed.append(fork.owner.login)
                self.forks_merged.append(fork)
                self.all_merged_fork_name_list.append(fork.full_name[:fork.full_name.find("/")])
                self.dicts.setDictForksData_TotalCommits(fork.owner.login, commits_tmp.totalCount)
                self.dicts.setDictForksData_LastCommitDate(fork.owner.login, self.findLastCommitDate(fork.owner.login, commits_tmp))
            else: pass  
        else: 
            commits_tmp = fork.get_commits(author=fork.owner.login) # list commits on a repository
            if commits_tmp.totalCount > 0:
                self.all_forks_committed.append(fork.owner.login)
                self.forks_merged.append(fork)
                self.all_merged_fork_name_list.append(fork.full_name[:fork.full_name.find("/")])
                self.dicts.setDictForksData_TotalCommits(fork.owner.login, commits_tmp.totalCount)
                self.dicts.setDictForksData_LastCommitDate(fork.owner.login, self.findLastCommitDate(fork.owner.login, commits_tmp))
            else: pass
        print ("SET_RANGE_OF_DAYS: ", SET_RANGE_OF_DAYS, " getMergedCommitsByRangeOfDays - self.forks_merged..: ", fork.owner.login, commits_tmp.totalCount)    
        return commits_tmp


    def getRepoCommitsByAuthor(self, authorName):
        self.checkToken.check_rate_limited() 
        commitList = self.repo.get_commits(author=authorName)
        if commitList and (commitList.totalCount > 0):
            self.all_forks_committed.append(self.repo_owner_name)
            self.collectMergedCommitsByAuthor(authorName, self.dicts.getUserDetailsByLogin(authorName).get("id"), self.dicts.getUserDetailsByLogin(authorName).get("full_name"), commitList) 
        del (commitList)


    def setRepoOwnerData(self,possible_owners_repo_list):
        self.possible_owners_repo_list = possible_owners_repo_list
        self.list_mergedCommit_files = []
        try:
            max=0
            repo_owner=""
            for contributor_name in self.possible_owners_repo_list:
                try:
                    contr_commits=[]
                    self.checkToken.check_rate_limited()
                    contr_commits = self.repo.get_commits(author=contributor_name)
                    if contr_commits.totalCount > max:
                        max = contr_commits.totalCount
                        del repo_owner
                        repo_owner = contributor_name
                    del (contr_commits)
                except GithubException:
                    self.logger.error("GithubException occurred", exc_info=True)
                except Exception:
                    self.logger.error("Exception occurred", exc_info=True)
            self.repo_owner_name = repo_owner
            self.checkToken.check_rate_limited()
            contr_commits = self.getOwnerRepoCommits(self.repo_owner_name)
            if contr_commits and (contr_commits.totalCount > 0):
                self.all_forks_committed.append(self.repo_owner_name)
                self.collectMergedCommitsByAuthor(self.repo_owner_name, self.repo.owner.id, self.repo.full_name, contr_commits) 
        except GithubException:
            self.logger.error("GithubException occurred", exc_info=True)
        except Exception:
            self.logger.error("Exception occurred", exc_info=True)

    #Getting repository's contributors
    def setContributorsNameList(self):
        self.logger.info(" Set Contributors Name List")
        self.checkToken.check_rate_limited()
        contributors = self.repo.get_contributors()
        for contributor in contributors:
            try:
                self.checkToken.check_rate_limited()
                print(contributor.login,contributor.type,contributor.contributions, contributor)
                self.contributors_name_list.append(contributor.login)
            except GithubException:
                self.logger.error("GithubException occurred", exc_info=True)
            except Exception:
                self.logger.error("Exception occurred", exc_info=True)
    
    def createUserDetails(self):
        self.logger.info("Getting Users Information (details)")
        self.setContributorsNameList()
        # getting all repository's contributors name
        contributors_name_list = self.getContributorsNameList()  

        self.setAllPresentForkNameList()
        # getting all fork names
        present_forks_list = self.getAllPresentForkNameList()

        # setting inactive contributors and contributor that is not a fork (problably owner of repository)
        self.inactive_contributors = (set(contributors_name_list)).difference(set(present_forks_list))
    
        count=1
        maintainer=str
        self.checkToken.check_rate_limited()
        contributors = self.repo.get_contributors()
        for contributor in contributors:
            try:
                self.checkToken.check_rate_limited()
                user = self.checkToken.getGHConnection().get_user(contributor.login)

                if (user.login in self.inactive_contributors):
                    if count == 1:
                        self.dicts.setUserDetails(user.id, user.login, user.name, self.repo.fork, True, user.email, user.avatar_url, user.html_url, user.followers, user.followers_url, user.following, user.following_url, user.organizations_url)
                        self.dicts.setUserDetailsByFullname(user.login, self.repo.full_name)
                        maintainer=user.login
                    else:
                        self.dicts.setUserDetails(user.id, user.login, user.name, True, False, user.email, user.avatar_url, user.html_url, user.followers, user.followers_url, user.following, user.following_url, user.organizations_url)
                        self.contributors_name_list.remove(user.login)
                else:
                    self.dicts.setUserDetails(user.id, user.login, user.name, self.repo.fork, True, user.email, user.avatar_url, user.html_url, user.followers, user.followers_url, user.following, user.following_url, user.organizations_url)
                count +=1

                del(user)
            except GithubException:
                self.logger.error("GithubException occurred", exc_info=True)
            except Exception:
                self.logger.error("Exception occurred", exc_info=True)

        for fork in self.forks:
            try:
                self.checkToken.check_rate_limited()
                if fork.owner.login not in self.contributors_name_list:
                    user = self.checkToken.getGHConnection().get_user(fork.owner.login)
                    self.dicts.setUserDetails(user.id, user.login, user.name, fork.fork, True, user.email, user.avatar_url, 
                    user.html_url, user.followers, user.followers_url, user.following, user.following_url, user.organizations_url)
                    self.dicts.setUserDetailsByFullname(user.login, fork.full_name)
                    del(user) 
                else: 
                    #forks --- already added
                    user = self.checkToken.getGHConnection().get_user(fork.owner.login)
                    self.dicts.setUserDetailsByFullname(user.login, fork.full_name)
                    self.dicts.setUserDetailsByIsFork(user.login,fork.fork)
                    del (user)
            except GithubException:
                self.logger.error("GithubException occurred", exc_info=True)
            except Exception:
                self.logger.error("Exception occurred", exc_info=True)

        with open(self.repoDataDir + self.repo.owner.login + "_usersDetails.json", 'w') as f:
            f.write(json.dumps(self.dicts.getUserDetails()))

    def getOwnerRepoCommits(self, repo_owner_name):
        self.logger.info("Get Owner Repo Commits")
        self.checkToken.check_rate_limited()
        repoOwnerCommits=[]
        try:
            if SET_RANGE_OF_DAYS:
                since = datetime.now() - timedelta(days=INTERVAL_OF_DAYS)
                repoOwnerCommits = self.repo.get_commits(author=repo_owner_name, since=since)
            else: repoOwnerCommits = self.repo.get_commits(author=repo_owner_name) #All commits
            return repoOwnerCommits
        except GithubException:
            self.logger.error("GithubException occurred", exc_info=True)
            return repoOwnerCommits
        except Exception:
            self.logger.error("Exception occurred", exc_info=True)
            return repoOwnerCommits

    def setAllPresentForkNameList(self):
        self.checkToken.check_rate_limited()
        for fork in self.forks:
            try:
                self.all_present_forks_name_list.append(fork.owner.login)
            except GithubException:
                self.logger.error("GithubException occurred", exc_info=True)
            except Exception:
                self.logger.error("Exception occurred", exc_info=True)

    def getAllPresentForkNameList(self):
        return self.all_present_forks_name_list

    def getAllPresentForksList(self):
        return self.all_present_forks_list
    
    def getAllMergedForkNameList(self):
        return self.all_merged_fork_name_list

    def getAllChangeFiles(self):
        return self.all_changed_files

    def getContributorsNameList(self):
        return self.contributors_name_list
    
    # getting all present forks that has merged commit
    def getAllForkMerged(self):
        return self.forks_merged 

    # getting all present forks that has unmerged commit
    def getAllForkUnMerged(self):
        return self.forks_unmerged 

    def getRepoOwnerData(self):
        return self.repo_owner_name

    def setMergedForkList(self):
        self.logger.info("set Merged Fork List.")
        for fork in self.forks:
            try:             
                self.getMergedCommitsByRangeOfDays(fork)
            except Exception:
                self.logger.error("Exception occurred", exc_info=True)

    def collectMergedCommitsByAuthor(self, login, id, full_name, listOfcommits):

        self.fork_owner_login = login
        self.fork_full_name = full_name
        self.fork_owner_id = id
        self.commits = listOfcommits
            
        setLastCommit = False
        indexLastCommit = 0
        mergeCommitCount = 0
        commitcount = 0
        for commit in self.commits:
            try:
                commitAuthor = str
                commitCommitter = str
                commit_html_url = str
                if len(commit.parents) == 1:
                    commitAuthor = self.getLoginByCommitAuthor(self.fork_owner_login, commit)
                    commitCommitter = self.getLoginByCommitCommitter(self.fork_owner_login, commit)
                    committedByAuthor = bool
                    if commitAuthor:
                        if commitAuthor == commitCommitter:
                            committedByAuthor = True
                        else: committedByAuthor = False
                        if CROSS_COMMITS:
                            commitcount +=1   
                            if self.dicts.getUserDetailsByLogin(self.fork_owner_login).get("isFork"):  
                                commit_html_url = self.getCommitURLFromFork(self.fork_owner_login, commit.sha)
                                if (commit_html_url is None) or (commit_html_url == "---"):
                                    commit_html_url = commit.html_url
                            else: 
                                commit_html_url = commit.html_url    
                            #Get files in a commit
                            self.checkToken.check_rate_limited()
                            #countFiles = commit.files
                            files = commit.files
                            for cfile in files:
                                try:    
                                    if self.extFiles.checkExtFile(cfile.filename) and (cfile.changes > 0) and (not self.extFiles.checkExcludedFile(cfile.filename)):
                                        if not setLastCommit:
                                            lastCommit = self.commits[indexLastCommit]
                                            self.dicts.setDictDevInfo(commitAuthor, self.dicts.getUserDetailsByLogin(commitAuthor).get('id'), self.dicts.getUserDetailsByLogin(commitAuthor).get('full_name'), lastCommit.commit.author.date, lastCommit.commit.author.name, lastCommit.commit.author.email)                            
                                            self.dicts.setDictDevInfo_TotalCommits(commitAuthor, self.commits.totalCount)
                                            setLastCommit = True
                                        if cfile.filename not in self.all_changed_files:
                                            self.all_changed_files.append(cfile.filename)
                                        self.dicts.setDictDevFileChanges(commitAuthor, cfile.filename, cfile.changes)#, cfile.raw_data)
                                        self.expDevs.setDictDevExpertise(commitAuthor, cfile.filename)
                                        self.dicts.setDictFilesInfo(commitAuthor, commit.sha, commit.commit.message, cfile.filename, cfile.changes, commit_html_url, (commit.commit.author.date).isoformat(), committedByAuthor)  

                                        if commitAuthor not in self.listOfCommitAuthors:
                                            self.listOfCommitAuthors.append(commitAuthor)
                                            print(commitAuthor, "was added in the list: ", self.listOfCommitAuthors)
                                            print()
                                    else: pass
                                except GithubException:
                                    self.logger.error("GithubException occurred", exc_info=True)
                                except Exception:
                                    self.logger.error("Exception occurred", exc_info=True)
                        else: # NOT CROSS_COMMITS:
                            if commitAuthor == self.fork_owner_login:
                                commitcount +=1 

                                if self.dicts.getUserDetailsByLogin(self.fork_owner_login).get("isFork"):  
                                    commit_html_url = self.getCommitURLFromFork(self.fork_owner_login, commit.sha)
                                    if (commit_html_url is None) or (commit_html_url == "---"):
                                        commit_html_url = commit.html_url
                                else: 
                                    commit_html_url = commit.html_url    
                                #Get files in a commit
                                self.checkToken.check_rate_limited()
                                #countFiles = commit.files
                                files = commit.files
                                for cfile in files:
                                    try:
                                        if self.extFiles.checkExtFile(cfile.filename) and (cfile.changes > 0) and (not self.extFiles.checkExcludedFile(cfile.filename)):
                                            if not setLastCommit:
                                                lastCommit = self.commits[indexLastCommit]
                                                self.dicts.setDictDevInfo(commitAuthor, self.dicts.getUserDetailsByLogin(commitAuthor).get('id'), self.dicts.getUserDetailsByLogin(commitAuthor).get('full_name'), lastCommit.commit.author.date, lastCommit.commit.author.name, lastCommit.commit.author.email)                            
                                                self.dicts.setDictDevInfo_TotalCommits(commitAuthor, self.commits.totalCount)
                                                setLastCommit = True
                                            if cfile.filename not in self.all_changed_files:
                                                self.all_changed_files.append(cfile.filename)
                                            self.dicts.setDictDevFileChanges(commitAuthor, cfile.filename, cfile.changes)#, cfile.raw_data)
                                            self.dicts.setDictFilesInfo(commitAuthor, commit.sha, commit.commit.message, cfile.filename, cfile.changes, commit_html_url, (commit.commit.author.date).isoformat(), committedByAuthor)  
                                            self.expDevs.setDictDevExpertise(commitAuthor, cfile.filename)
                                            if commitAuthor not in self.listOfCommitAuthors:
                                                self.listOfCommitAuthors.append(commitAuthor)
                                        else: pass
                                    except GithubException:
                                        self.logger.error("GithubException occurred", exc_info=True)
                                    except Exception:
                                        self.logger.error("Exception occurred", exc_info=True)    
                            else: 
                                print("CollectMergedCommitsByAuthor (rejected) ..: ", commit.sha, login, commitAuthor, commitCommitter, commit.commit.author.date, commit.commit.committer.date, " parent count  ", len(commit.parents))
                else: 
                    mergeCommitCount += 1
                indexLastCommit += 1
                del(commitAuthor)
                del(commitCommitter)
                del(commit_html_url)
            except GithubException:
                self.logger.error("GithubException occurred", exc_info=True)
            except Exception:
                self.logger.error("Exception occurred", exc_info=True)
        del(self.fork_owner_login)
        del(self.fork_full_name)
        del(self.fork_owner_id)
        del(self.commits)

    def getMergedCommits(self):
        self.logger.info("Get Merged Commits.")
        for fork in self.forks:
            try:   
                if fork.owner.login:          
                    self.checkToken.check_rate_limited()
                    #returned commits in a paginated list
                    mergedCommits  = fork.get_commits(author=fork.owner.login) #self.repo.get_commits(author=contributor_name)
                    if mergedCommits and (mergedCommits.totalCount > 0):
                        self.collectMergedCommitsByAuthor(fork.owner.login, fork.owner.id ,fork.full_name, mergedCommits)
                    del (mergedCommits)
            except GithubException:
                self.logger.error("GithubException occurred", exc_info=True)
            except Exception:
                self.logger.error("Exception occurred", exc_info=True)

    def getLoginByCommitAuthor(self, fork_owner_login, commit):
        try:
            if commit.author.login:
                if fork_owner_login == commit.author.login:
                    return fork_owner_login
                elif (textdistance.levenshtein.normalized_similarity(fork_owner_login, commit.author.login) > 0.7):
                    self.dicts.setUserDetailsByName(fork_owner_login, commit.author.login)
                    return fork_owner_login
                else: 
                    return self.dicts.getLoginFromUserDetails(commit.author.login)
        except Exception:
            print("Exception")
            if fork_owner_login == commit.commit.author.name:
                return fork_owner_login
            elif (textdistance.levenshtein.normalized_similarity(fork_owner_login, commit.commit.author.name) > 0.7):
                self.dicts.setUserDetailsByName(fork_owner_login, commit.commit.author.name)
                return fork_owner_login
            else:
                return self.dicts.getLoginFromUserDetails(commit.commit.author.name)
            return None


    def getLoginByCommitCommitter(self, fork_owner_login, commit):
        try:
            if commit.committer.login:
                if fork_owner_login == commit.committer.login:
                    return fork_owner_login
                elif (textdistance.levenshtein.normalized_similarity(fork_owner_login, commit.committer.login) > 0.7):
                    self.dicts.setUserDetailsByName(fork_owner_login, commit.committer.login)
                    return fork_owner_login
                else: 
                    return self.dicts.getLoginFromUserDetails(commit.committer.login)
        except Exception:
            print("Exception")
            if fork_owner_login == commit.commit.committer.name:
                return fork_owner_login
            elif (textdistance.levenshtein.normalized_similarity(fork_owner_login, commit.commit.committer.name) > 0.7):
                self.dicts.setUserDetailsByName(fork_owner_login, commit.commit.committer.name)
                return fork_owner_login
            else:
                return self.dicts.getLoginFromUserDetails(commit.commit.committer.name)
            return None

    # getting diff branches
    def compareForks(self):
        self.logger.info("Compare Forks.")
        branch_fork_name = "HEAD"

        count=1

        for fork in self.forks:
            try:         
                self.checkToken.check_rate_limited()
                self.fork_name = fork.full_name[0:fork.full_name.find("/")]
                diff = self.repo.compare(self.repo.get_branch(branch="master").name,self.fork_name +":"+branch_fork_name)
                if diff.ahead_by > 0:
                    self.all_forks_committed.append(fork.owner.login)
                    self.forks_unmerged.append(fork)
                    
                    count +=1
                    # getting all commits for a interval of days
                    since = datetime.now() - timedelta(days=INTERVAL_OF_DAYS)
                    indexLastCommit = 0
                    mergeCommitCount = 0
                    for commit in diff.commits:
                        commitAuthor = str
                        commitCommitter = str
                        commit_html_url = str
                        if len(commit.parents) == 1:
                            commitAuthor = self.getLoginByCommitAuthor(fork.owner.login, commit)
                            commitCommitter = self.getLoginByCommitCommitter(fork.owner.login, commit)
                            
                            if commitAuthor:
                                if CROSS_COMMITS:    
                                    commit_html_url = self.getCommitURLFromFork(fork.owner.login, commit.sha)
                                    if (commit_html_url is None) or (commit_html_url == "---"):
                                        commit_html_url = commit.html_url
                                    
                                    # flag usado posteriormente para escolher a melhor URL dos commits do author
                                    committedByAuthor = bool
                                    #if fork.owner.login == commitAuthor:
                                    if commitAuthor == commitCommitter:
                                        committedByAuthor = True
                                    else: committedByAuthor = False
                                
                                    if SET_RANGE_OF_DAYS:
                                        if since < commit.commit.author.date: #author-date:YYYY-MM-DD
                                            #Get files in a commit
                                            files = commit.files
                                            for cfile in files:
                                                if self.extFiles.checkExtFile(cfile.filename) and (cfile.changes > 0) and (not self.extFiles.checkExcludedFile(cfile.filename)):
                                                    last_commit = diff.commits[indexLastCommit]

                                                    if self.fork_name not in self.dicts.getDictDevInfo().keys():
                                                        self.dicts.setDictDevInfo(commitAuthor, self.dicts.getUserDetailsByLogin(commitAuthor).get('id'), self.dicts.getUserDetailsByLogin(commitAuthor).get('full_name'), last_commit.commit.author.date, last_commit.commit.author.name, last_commit.commit.author.email)
                                                        self.dicts.setDictDevInfo_CommitsAhead(commitAuthor, diff.ahead_by)
                                                        self.dicts.setDictDevInfo_TotalCommits(commitAuthor, 0)
                                                    else:   
                                                        if self.dicts.getDictDevInfo().get(commitAuthor).get('last_commit_date') < last_commit.commit.author.date:
                                                            self.dicts.setDictDevInfo_LastCommitDate(commitAuthor, last_commit.commit.author.date)
                                                        self.dicts.setDictDevInfo_CommitsAhead(commitAuthor, diff.ahead_by)
                                                    
                                                    if cfile.filename not in self.all_changed_files:
                                                        self.all_changed_files.append(cfile.filename)

                                                    self.dicts.setDictDevFileChanges(commitAuthor, cfile.filename, cfile.changes)#, cfile.raw_data)
                                                    self.dicts.setDictFilesInfo(commitAuthor, commit.sha, commit.commit.message, cfile.filename, cfile.changes, commit_html_url, (commit.commit.author.date).isoformat(), committedByAuthor)    
                                                    self.expDevs.setDictDevExpertise(commitAuthor, cfile.filename)
                                                    if commitAuthor not in self.listOfCommitAuthors:
                                                        self.listOfCommitAuthors.append(commitAuthor)
                                    else: # all commits  
                                        files = commit.files
                                        for cfile in files:
                                            if self.extFiles.checkExtFile(cfile.filename) and (cfile.changes > 0) and (not self.extFiles.checkExcludedFile(cfile.filename)):
                                                last_commit = diff.commits[indexLastCommit]

                                                if self.fork_name not in self.dicts.getDictDevInfo().keys():
                                                    self.dicts.setDictDevInfo(commitAuthor, self.dicts.getUserDetailsByLogin(commitAuthor).get('id'), self.dicts.getUserDetailsByLogin(commitAuthor).get('full_name'), last_commit.commit.author.date, last_commit.commit.author.name, last_commit.commit.author.email)
                                                    self.dicts.setDictDevInfo_CommitsAhead(commitAuthor, diff.ahead_by)
                                                    self.dicts.setDictDevInfo_TotalCommits(commitAuthor, 0)
                                                else:  
                                                    if self.dicts.getDictDevInfo().get(commitAuthor).get('last_commit_date') < last_commit.commit.author.date:
                                                        self.dicts.setDictDevInfo_LastCommitDate(commitAuthor, last_commit.commit.author.date)
                                                    self.dicts.setDictDevInfo_CommitsAhead(commitAuthor, diff.ahead_by)

                                                if cfile.filename not in self.all_changed_files:
                                                    self.all_changed_files.append(cfile.filename)
                                                
                                                self.dicts.setDictDevFileChanges(commitAuthor, cfile.filename, cfile.changes)#, cfile.raw_data)
                                                self.dicts.setDictFilesInfo(commitAuthor, commit.sha, commit.commit.message, cfile.filename, cfile.changes, commit_html_url, (commit.commit.author.date).isoformat(), committedByAuthor)   
                                                self.expDevs.setDictDevExpertise(commitAuthor, cfile.filename)
                                                if commitAuthor not in self.listOfCommitAuthors:
                                                    self.listOfCommitAuthors.append(commitAuthor)
                                        
                                else: # NOT CROSS_COMMITS
                                    if commitAuthor == fork.owner.login:
                                        commit_html_url = self.getCommitURLFromFork(fork.owner.login, commit.sha)
                                        if (commit_html_url is None) or (commit_html_url == "---"):
                                            commit_html_url = commit.html_url
                                    
                                        committedByAuthor = bool
                                        if commitAuthor == commitCommitter:
                                            committedByAuthor = True
                                        else: committedByAuthor = False
                                        if SET_RANGE_OF_DAYS:
                                            if since < commit.commit.author.date: #author-date:YYYY-MM-DD
                                                #Get files in a commit
                                                files = commit.files
                                                for cfile in files:
                                                    if self.extFiles.checkExtFile(cfile.filename) and (cfile.changes > 0) and (not self.extFiles.checkExcludedFile(cfile.filename)):
                                                        
                                                        last_commit = diff.commits[indexLastCommit]
                                                        if self.fork_name not in self.dicts.getDictDevInfo().keys():
                                                            self.dicts.setDictDevInfo(commitAuthor, self.dicts.getUserDetailsByLogin(commitAuthor).get('id'), self.dicts.getUserDetailsByLogin(commitAuthor).get('full_name'), last_commit.commit.author.date, last_commit.commit.author.name, last_commit.commit.author.email)
                                                            self.dicts.setDictDevInfo_CommitsAhead(commitAuthor, diff.ahead_by)
                                                            self.dicts.setDictDevInfo_TotalCommits(commitAuthor, 0)
                                                        else:   
                                                            if self.dicts.getDictDevInfo().get(commitAuthor).get('last_commit_date') < last_commit.commit.author.date:
                                                                self.dicts.setDictDevInfo_LastCommitDate(commitAuthor, last_commit.commit.author.date)
                                                            self.dicts.setDictDevInfo_CommitsAhead(commitAuthor, diff.ahead_by)
                                                        if cfile.filename not in self.all_changed_files:
                                                            self.all_changed_files.append(cfile.filename)
                                                        self.dicts.setDictDevFileChanges(commitAuthor, cfile.filename, cfile.changes)#, cfile.raw_data)
                                                        self.dicts.setDictFilesInfo(commitAuthor, commit.sha, commit.commit.message, cfile.filename, cfile.changes, commit_html_url, (commit.commit.author.date).isoformat(), committedByAuthor)    
                                                        self.expDevs.setDictDevExpertise(commitAuthor, cfile.filename)
                                                        if commitAuthor not in self.listOfCommitAuthors:
                                                            self.listOfCommitAuthors.append(commitAuthor)
                                        else: # all commits  
                                            files = commit.files
                                            for cfile in files:
                                                if self.extFiles.checkExtFile(cfile.filename) and (cfile.changes > 0) and (not self.extFiles.checkExcludedFile(cfile.filename)):
                                                    last_commit = diff.commits[indexLastCommit]
                                                    if self.fork_name not in self.dicts.getDictDevInfo().keys():
                                                        self.dicts.setDictDevInfo(commitAuthor, self.dicts.getUserDetailsByLogin(commitAuthor).get('id'), self.dicts.getUserDetailsByLogin(commitAuthor).get('full_name'), last_commit.commit.author.date, last_commit.commit.author.name, last_commit.commit.author.email)
                                                        self.dicts.setDictDevInfo_CommitsAhead(commitAuthor, diff.ahead_by)
                                                        self.dicts.setDictDevInfo_TotalCommits(commitAuthor, 0)
                                                    else:  
                                                        if self.dicts.getDictDevInfo().get(commitAuthor).get('last_commit_date') < last_commit.commit.author.date:
                                                            self.dicts.setDictDevInfo_LastCommitDate(commitAuthor, last_commit.commit.author.date)
                                                        self.dicts.setDictDevInfo_CommitsAhead(commitAuthor, diff.ahead_by)
                                                    if cfile.filename not in self.all_changed_files:
                                                        self.all_changed_files.append(cfile.filename)
                                                    
                                                    self.dicts.setDictDevFileChanges(commitAuthor, cfile.filename, cfile.changes)#, cfile.raw_data)
                                                    self.dicts.setDictFilesInfo(commitAuthor, commit.sha, commit.commit.message, cfile.filename, cfile.changes, commit_html_url, (commit.commit.author.date).isoformat(), committedByAuthor)   
                                                    self.expDevs.setDictDevExpertise(commitAuthor, cfile.filename)
                                                    if commitAuthor not in self.listOfCommitAuthors:
                                                        self.listOfCommitAuthors.append(commitAuthor)
                                    else:
                                        print ("Comparing Forks ( rejected ) ......: ", commit.sha, fork.owner.login, commitAuthor, commitCommitter)
                            del(commitAuthor)
                            del(commitCommitter)
                            del(commit_html_url)
                        else: 
                            mergeCommitCount+=1
            except GithubException:
                self.logger.error("GithubException occurred", exc_info=True)
            except Exception:
                self.logger.error("Exception occurred", exc_info=True)

    def printAuthorFilesDir(self):
        for authorName in self.listOfCommitAuthors:
            if (self.dicts.getUserDetailsByLogin(authorName).get('isActive')) and (len(self.dicts.getDictDevFileChangesInfoByAuthor(authorName))>0):
                with open(self.commitFilesInfoDir + authorName + "_changedFilesInfo.json","w+") as outfile:
                    outfile.write(json.dumps(self.dicts.getDictDevFileChangesInfoByAuthor(authorName)))   

        for commitAuthor in self.dicts.dictDevFileChanges:
            if self.dicts.getUserDetailsByLogin(commitAuthor).get('isActive'):
                with open(self.commitFilesDir + commitAuthor + "_commitFiles.json", 'w', encoding='utf-8') as outfile:
                    outfile.write(json.dumps(self.dicts.getDictDevFileChangesByAuthor(commitAuthor).get('cfile_raw_data')))  

    def printRecListResult(self):
        with open(self.repoDataDir + self.repo.name + "_recListResult.json","w+") as outfile:
            outfile.write(json.dumps(self.dicts.getDictRecListResult(), indent = 4, sort_keys = True, default = str)) 

def main(repository, access_token):
    
    repoName = repository[repository.find("/")+1:len(repository)]
    repoPath = "./" +  repoName
    commitFilesDir =  repoPath + "/commitFiles/"
    excludedCommitFilesDir =  repoPath + "/excludedCommitFiles/"
    repoDataDir  =  repoPath + "/resultData/"
    commitFilesInfoDir = repoPath + "/commitFilesInfoDir/"
    changedFileStrategyResultsPath = repoPath + "/changedFilesStrategyResults/"
    changesInFilesStrategyResultsPath = repoPath + "/changesInFilesStrategyResults/"

    # Create Obj Logger
    objLogger = Logger()
    objLogger.createLogger()
    setLogger = objLogger.getLogger()
    checkToken = CheckToken(setLogger, access_token)

    extFiles = exts.ExtensionFiles() # to check the extension files

    expDevs = exps.ExpertiseList()

    dicts = CreateDicts()
    
    # Class  CollectGHData  (constructor)
    collectGHData = CollectGHData(checkToken, setLogger, repository, repoPath, commitFilesDir, excludedCommitFilesDir, repoDataDir, commitFilesInfoDir, changedFileStrategyResultsPath, changesInFilesStrategyResultsPath, dicts, extFiles, expDevs)

    collectGHData.createUserDetails()

    contributors_name_list = collectGHData.getContributorsNameList()

    # getting all commits for all contributors
    for contributor_name in contributors_name_list:
        collectGHData.getRepoCommitsByAuthor(contributor_name)
    
    #non-merged commits by forks 
    collectGHData.compareForks()           
    #preparing input data
    collectGHData.printAuthorFilesDir()
    # set zero if total commits or commit ahead is none
    dicts.checkDictDevInfoCommits()

    #### Strategy 1: number of commits ####
    dicts.setDevFilesDictCorpus(commitFilesInfoDir, False) # False = # of changed files;  True: changes in file (# of deletes + # of additions) 
    dictCorpus_changedFilesStrategy = dicts.getDictCorpusChangedFiles()
    forkNames = dicts.getForkNames()
    expDevs.printDevExpertiseData(repoDataDir)
    changedFilesStrategySimilarity = sim.Similarity(forkNames, False, changedFileStrategyResultsPath,dicts)
    changedFilesStrategySimilarity.runTFIDF()
    changedFilesStrategySimilarity.runCosSim()
    changedFilesStrategyRecList = recList.DevRecommendationList(setLogger, dicts, changedFileStrategyResultsPath, repoName, False)
    changedFilesStrategyRecList.setDevRecommendationList()

    #### Strategy 2: number of changed LoC ####
    dicts.setDevFilesDictCorpus(commitFilesInfoDir, True) # False = # of changed files;  True: changes in file (# of deletes + # of additions) 
    dictCorpus_changesInFilesStrategy = dicts.getDictCorpusChangesInFiles()
    changesInFilesStrategySimilarity = sim.Similarity(forkNames,True,changesInFilesStrategyResultsPath,dicts)
    changesInFilesStrategySimilarity.runTFIDF()
    changesInFilesStrategySimilarity.runCosSim()
    changesInFilesStrategyRecList = recList.DevRecommendationList(setLogger, dicts, changesInFilesStrategyResultsPath, repoName, True)
    changesInFilesStrategyRecList.setDevRecommendationList()

    collectGHData.printRecListResult()
    print("done!")

if __name__ == "__main__":

    print(f"Arguments count: {len(sys.argv)}")

    print(f"File name       : {sys.argv[0]}")
    print(f"Repository Name : {sys.argv[1]}")
    print(f"AccessToken     : {sys.argv[2]}")
    
    main(sys.argv[1], sys.argv[2])
