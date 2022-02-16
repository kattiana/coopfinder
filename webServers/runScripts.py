import os
import sys
import shutil
import time

access_token_list = ["", ""]
repository = ""

repoName = repository[repository.find("/")+1:len(repository)]

strChanged = "_changed"
strChanges = "_changes"

repoPath = "./" +  repoName 
changedFileStrategyResultsPath = repoPath + "/changedFilesStrategyResults/"
changesInFilesStrategyResultsPath = repoPath + "/changesInFilesStrategyResults/"
resultDataPath = repoPath + "/resultData/"

changedFilesStrategyRecList     = "recList_" + repoName + strChanged + ".csv"
changesInFilesStrategyRecList   = "recList_" + repoName + strChanges + ".csv"

print("changedFilesStrategyRecList.....: ", changedFileStrategyResultsPath + changedFilesStrategyRecList)
print("changesInFilesStrategyRecList...: ", changesInFilesStrategyResultsPath + changesInFilesStrategyRecList)

os.system('python3 extractingCommits.py ' + repository + " " + access_token_list[1])
print("...extractingCommits.py ", repoPath, " Done!")
print("...runScripts Done!")