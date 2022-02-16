import json

class JSonFiles():

    def __init__(self, strFilePath):
        self.repoData = ""
        self.userDataList = ""
        self.userExpertiseList = ""
        self.setUserDataList(strFilePath)
        self.setRepoData(strFilePath)
        self.setUserExpertiseList(strFilePath)

    def setUserDataList(self, strFilePath):
        self.userDataList = open(self.strFilePath + "/usersDetails.json","r")

    def setRepoData(self, strFilePath):
        self.repoData = open(self.strFilePath + "/repoDetails.json","r")
    
    def setUserExpertiseList(self, strFilePath):
        self.userDataList = open(self.strFilePath + "/repoDetails.json","r")

    def getUserDataList(self, strFilePath):
        return self.userDataList

    def getRepoData(self, strFilePath):
        return self.repoData

    def getUserExpertiseList(self, strFilePath):
        return self.userDataList


def main(GHUserName, repoName, repoPath, changedFilesStrategyPath, changesInFilesStrategyPath):

    strFilePath = "../data⁩/"+ GHUserName + "/"+  repoName + "/" 
    jsonFiles = JSonFiles(strFilePath)


if __name__ == "__main__":

    print(f"Arguments count: {len(sys.argv)}")

    print(f"PY File Name                    : {sys.argv[0]}")
    print(f"User Name                       : {sys.argv[1]}")
    print(f"Repository Name                 : {sys.argv[2]}")
    print(f"Repo Path                       : {sys.argv[3]}")
    print(f"ChangedFiles Strategy Path      : {sys.argv[4]}")
    print(f"changesInFiles Strategy Path    : {sys.argv[5]}")
    print()

    time.sleep(5)
    
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])