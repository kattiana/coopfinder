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
        #self.userName = self.gh.get_user()

    def getGHConnection(self):
        return self.gh

    def setConnectionGH(self, token):
        print("Create Connection with ", token)
        self.gh = Github(token, per_page=100)

    def getReposUser(self):
        return self.gh.get_user().get_repos()

    def saveReposUser(self, repos):
        print(self.userName)
        reposData = {}
        reposData [self.userName] = []
        for repo in repos:
            print(repo.name)
            reposData [self.userName].append({
                'name': repo.name,
                'full_name': repo.full_name
            })
        with open(self.userName+'/repos_'+self.userName+'.json', 'w') as outfile:
            json.dump(reposData, outfile)
    
    def getSpecificUser(self, userList):

        INTERVAL_OF_DAYS = (3*365  + 180) # three years
        #print("specific User..: ", specificUser)

        with open("./surveyParticipantsBackground.csv","w") as surveyParticipantOutFile:
                
            surveyPartWriter = csv.writer(surveyParticipantOutFile)

            surveyPartWriter.writerow(["Fork","Type","Company","Location","Followers","Following",
                                        "Public Repos","Contributions Last Year","Contributions Last Three Years", "HTML_URL", "Bio"])

            i = 1
            for user in userList:
                ghUser = user[:user.find("/")]
                print(i, " GH User...............: ", ghUser, user)
                userNamed = self.gh.get_user(ghUser)
                surveyPartWriter.writerow([user, userNamed.type,userNamed.company,userNamed.location, userNamed.followers, userNamed.following, 
                userNamed.public_repos, userNamed.get_events().totalCount, 0, userNamed.html_url, userNamed.bio])
                i += 1
        exit()
        

def main(userName):

    cPaths = CreatePaths(userName)
    cPaths.setRootPath()
    userPath =  cPaths.getRootPath()

    access_token = ""
    gh = GHConnection(userName, access_token)
    #gh = GHConnection(access_token)
    gh.getGHConnection()

    #repos = gh.getReposUser()
    #gh.saveReposUser(repos)

    userList = ["fnlctrl/vue-next","KeiLongW/RSSHub","yangmingshan/vue-next","lankas/mongo","Eric-Arellano/pants","jsirois/pants","lydiastepanek/mongo",
    "tajila/openj9","dsouzai/openj9","fjeremic/openj9","XxAdi101xX/openj9","hi-rustin/vue-next","KomachiSion/nacos","printomi/deeplearning4j","lidaoyang/nacos",
    "GuillemGSubies/pytorch-transformers","gerhardberger/electron","illicitonion/pants","shahidhk/graphql-engine","Qiyu8/numpy","r-devulap/numpy","groszewn/seldon-core",
    "takanori-pskq/numpy","realprogrammer5000/sherlock","CloseChoice/numpy","sturlamolden/numpy","bashtage/numpy","eric-wieser/numpy","LameLemon/sherlock",
    "adriangonz/seldon-core","Mistercrunch/superset","rusackas/incubator-superset","mmaybeno/transformers","lastephey/numpy","Luidiblu/sherlock","mrocklin/dask",
    "ryandawsonuk/seldon-core","loiacon/vue-next","blcksrx/incubator-superset","newville/matplotlib","rushabh-v/cupy","siddhesh/scipy","Iamsoto/astropy",
    "Dahlia-Chehata/cupy","vkWeb/freeCodeCamp","pmli/scipy","peterjc/astropy","johnnyEmpires/matplotlib","jjerphan/scipy","stargaser/astropy","story645/matplotlib",
    "mpirvu/openj9","cifkao/magenta","LinHu2016/openj9","edobranov/mongo","VermaSh/openj9","ShaunSHamilton/freeCodeCamp","fangchenli/pandas","quangngd/pandas",
    "vaibhavhrt/pandas","proost/pandas","kernc/pandas","Dr-Irv/pandas","tswast/pandas","blorente/pants","roopeshvs/sherlock","OliverHofkens/dask","rossbar/numpy",
    "betodealmeida/incubator-superset","AshNaz87/freeCodeCamp","dsaxton/pandas-dev","mdhaber/scipy","rhshadrach/pandas","UmashankarTriforce/cupy",
    "DCtheTall/matplotlib","phobson/matplotlib","brunobeltran/matplotlib","mruffalo/scipy","janvle/scipy","chrisb83/scipy","tomdonaldson/astropy","jonchang/brew",
    "rafaelss95/components","pierrechevalier83/pants","renatocaval/akka","fujiaxiang/pandas","AlexKirko/pandas","kiendang/brew","pdebuyl/numpy","peterpanmj/pandas",
    "MarkEWaite/jenkins","admshao/obs-studio","Rosuav/obs-studio","swilly22/redis","odd/akka","halfninja/playframework","fredfp/akka","itamarhaber/redis",
    "pjdarton/jenkins","katre/bazel","alexjski/bazel","slide/jenkins","mbehrlich/components","ggreif/wasmtime","multun/bevy","justinhorvitz/bazel","acfoltzer/wasmtime",
    "StefanSpieker/jenkins","nikola-sh/bazel","mrowqa/wasmtime","dmatveev/opencv","Cancerberosgx/opencv","l-bat/opencv","ePirat/obs-studio","YashasSamaga/opencv",
    "guybe7/redis","ioangogo/obs-studio","mkg33/scipy"]
    
    gh.getSpecificUser(userList)


if __name__ == "__main__":

    print(f"Arguments count: {len(sys.argv)}")
    print(f"userName    : {sys.argv[0]}")
    print(f"userName    : {sys.argv[1]}")
    print()
    #time.sleep(2)

    main(sys.argv[1])