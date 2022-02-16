import os
import sys
import shutil
import time
import json
from github import Github, GithubException
from datetime import datetime, timedelta, timezone
import calendar
import csv as csv

class CreatePaths(object):
    def __init__(self, rootName):
        self.rootName = rootName

    def setRootPath(self):
        self.create_paths(("./" + self.rootName))

    def getRootPath(self):
        return ("./" + self.rootName)

    def create_paths(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

class GHConnection(object):
    def __init__(self, userName, token):
        self.userName = userName
        self.access_token = token
        self.gh = Github(self.access_token, per_page=100)
        print("self.access_token..: ", self.access_token)
        print("self.gh............: ", self.gh)
        print("self.userName......: ", self.userName) 

    def getRepoInfo(self, repoName):
        return self.gh.get_repo(repoName)

    def getGHConnection(self):
        return self.gh

    def setConnectionGH(self, token):
        self.gh = Github(token, per_page=100)

    def getReposUser(self):
        return self.gh.get_user().get_repos()

    def saveReposUser(self, userPath, repos):
        reposData = {}
        reposData ['userName'] = self.userName
        reposData ['repoList'] = []
        for repo in repos:
            if repo.parent:
                if repo.parent.forks_count > 400:
                    reposData ['repoList'].append({
                        'parent_repo_full_name': repo.parent.full_name,
                        'language': repo.parent.language,
                        'created_at': str(repo.parent.created_at),
                        'forks_count': int(repo.parent.forks_count),
                        'open_issues_count': int(repo.parent.open_issues_count),
                        'stargazers_count': int(repo.parent.stargazers_count),
                        #'contributors_count': repo.parent.contributors_count,
                        'repo_name': repo.name,
                        'repo_full_name': repo.full_name
                    })

            else:
                if repo.forks_count > 100:
                    reposData ['repoList'].append({
                        'parent_repo_full_name': None,
                        'language': repo.language,
                        'created_at': str(repo.created_at),
                        'forks_count': int(repo.forks_count),
                        'open_issues_count': int(repo.open_issues_count),
                        'stargazers_count': int(repo.stargazers_count),
                        #'contributors_count': repo.contributors_count,
                        'repo_name': repo.name,
                        'repo_full_name': repo.full_name
                    })
        with open(userPath +'/repoListData.json', 'w') as outfile:
            json.dump(reposData, outfile)
    
    def getSpecificUser(self, userList):

        INTERVAL_OF_DAYS = (3*365  + 180) # three years

        with open("./surveyParticipantsBackground.csv","w") as surveyParticipantOutFile:
            surveyPartWriter = csv.writer(surveyParticipantOutFile)
            surveyPartWriter.writerow(["Fork","Type","Company","Location","Followers","Following",
                                        "Public Repos","Contributions Last Year","Contributions Last Three Years", "HTML_URL", "Bio"])
            i = 1
            for user in userList:
                ghUser = user[:user.find("/")]
                #print(i, " GH User...............: ", ghUser, user)
                userNamed = self.gh.get_user(ghUser)
                surveyPartWriter.writerow([user, userNamed.type,userNamed.company,userNamed.location, userNamed.followers, userNamed.following, 
                userNamed.public_repos, userNamed.get_events().totalCount, 0, userNamed.html_url, userNamed.bio])
                i += 1
        exit()


def main(userName):

    cPaths = CreatePaths('../data/'+ userName)
    cPaths.setRootPath()
    userPath =  cPaths.getRootPath()
    print("userPath", userPath)
    access_token = "" #including personal token access (github)
    gh = GHConnection(userName, access_token)
    gh.getGHConnection()
    repos = gh.getReposUser()
    print("repos", repos)
    gh.saveReposUser(userPath, repos)
    print("Done!")

if __name__ == "__main__":

    print(f"Arguments count: {len(sys.argv)}")
    print(f"fileName    : {sys.argv[0]}")
    print(f"userName    : {sys.argv[1]}")
    main(sys.argv[1])