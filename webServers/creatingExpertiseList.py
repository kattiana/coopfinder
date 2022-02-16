import json
import time
from operator import itemgetter
from collections import defaultdict

class ExpertiseList(object):
    def __init__(self):
        self.devExpertiseList = {}

    def checkExtension(self, filename):
        index = 0
        extensionFile = str()

        try:
            index = filename.rindex(".") # last occurrence of "."
            extensionFile = filename[index:len(filename)]
            #print ("checkExpertise...:", filename, extensionFile)
        except Exception as e:
            return "noExtension"

        if extensionFile in [".html", ".htm"]:
            # HTML          https://pt.wikipedia.org/wiki/HTML 
            return "HTML"
        elif extensionFile in [".css"]:
            # CSS           https://en.wikipedia.org/wiki/Cascading_Style_Sheets
            return "CSS"
        elif extensionFile in [".js"]:
            # JavaScript    https://pt.wikipedia.org/wiki/JavaScript
            return "JavaScript"
        elif extensionFile in [".java"]:
            # Java          https://pt.wikipedia.org/wiki/Java_(linguagem_de_programa%C3%A7%C3%A3o)
            return "Java"
        elif extensionFile in [".h",".c"]:
            # C             https://pt.wikipedia.org/wiki/C_(linguagem_de_programa%C3%A7%C3%A3o) 
            return "C"
        elif extensionFile in [".cc",".cpp",".cxx",".C",".c++",".h",".hh",".hpp",".hxx",".h++"]:
            # C++           https://pt.wikipedia.org/wiki/C%2B%2B 
            return "C++"
        elif extensionFile in [".cob",".cobol"]:
            # Cobol             https://www.filesuffix.com/pt/extension/cob 
            return "Cobol"
        elif extensionFile in [".d"]:
            # D             https://pt.wikipedia.org/wiki/D_(linguagem_de_programa%C3%A7%C3%A3o)
            return "D"
        elif extensionFile in [".cs"]:
            # C#            https://pt.wikipedia.org/wiki/C_Sharp
            return "C#"
        elif extensionFile in [".fs",".fsi",".fsx",".fsscript"]:
            # F#            https://pt.wikipedia.org/wiki/F_Sharp
            return "F#"
        elif extensionFile in [".pl",".pm",".t",".pod"]:
            # Perl          https://pt.wikipedia.org/wiki/Perl
            return "Perl"
        elif extensionFile in [".php",".phtml",".php3",".php4",".php5",".php7",".phps"]:
            # PHP           https://pt.wikipedia.org/wiki/PHP 
            return "PHP"
        elif extensionFile in [".dart"]:
            # Dart          https://pt.wikipedia.org/wiki/Dart_(linguagem_de_programa%C3%A7%C3%A3o)
            return "Dart"
        elif extensionFile in [".coffee"]:
            # CoffeeScript  https://pt.wikipedia.org/wiki/CoffeeScript
            return "CoffeeScript"
        elif extensionFile in [".rb"]:
            # Ruby          https://pt.wikipedia.org/wiki/Ruby_(linguagem_de_programa%C3%A7%C3%A3o)
            return "Ruby"
        elif extensionFile in [".st"]:
            # Smalltalk     https://pt.wikipedia.org/wiki/Smalltalk
            return "Smalltalk"
        elif extensionFile in [".go"]:
            # GO            https://pt.wikipedia.org/wiki/Go_(linguagem_de_programa%C3%A7%C3%A3o)
            return "GO"
        elif extensionFile in [".pas",".pp",".inc"]:
            # Pascal        https://pt.wikipedia.org/wiki/Pascal_(linguagem_de_programa%C3%A7%C3%A3o)
            return "Pascal"
        elif extensionFile in [".scm",".ss"]:
            # Scheme        https://pt.wikipedia.org/wiki/Scheme
            return "Scheme"
        elif extensionFile in [".scala",".sc"]:
            # Scala         https://pt.wikipedia.org/wiki/Scala_(linguagem_de_programa%C3%A7%C3%A3o)
            return "Scala"
        elif extensionFile in [".lua"]:
            # Lua           https://pt.wikipedia.org/wiki/Lua_(linguagem_de_programa%C3%A7%C3%A3o)
            return "Lua"
        elif extensionFile in [".clj",".cljs",".cljc",".edn"]:
            # Clojure       https://pt.wikipedia.org/wiki/Clojure
            return "Clojure"
        elif extensionFile in [".hs",".lhs"]:
            # Haskell       https://pt.wikipedia.org/wiki/Haskell_(linguagem_de_programa%C3%A7%C3%A3o)
            return "Haskell"
        elif extensionFile in [".fan",".fwt"]:
            # Fantom        https://pt.wikipedia.org/wiki/Fantom
            return "Fantom"
        elif extensionFile in [".vala",".vapi"]:
            # Vala          https://pt.wikipedia.org/wiki/Vala_(linguagem_de_programa%C3%A7%C3%A3o)
            return "Vala"
        elif extensionFile in [".f",".for",".ftn",".f90",".f95",".f03",".f08",".f15"]:
            # Fortran           https://pt.wikipedia.org/wiki/Fortran
            return "Fortran"
        elif extensionFile in [".kt",".kts"]:
            # Kotlin        https://pt.wikipedia.org/wiki/Kotlin
            return "Kotlin"
        elif extensionFile in [".jl"]:
            # Julia         https://pt.wikipedia.org/wiki/Julia_(linguagem_de_programa%C3%A7%C3%A3o)
            return "Julia"
        elif extensionFile in [".py",".pyx",".pxd",".ipynb"]:
            # Python        https://pt.wikipedia.org/wiki/Python   https://pt.stackoverflow.com/questions/185944/extens%C3%B5es-pyc-pyd-pyo-em-python
            return "Python"
        elif extensionFile in [".ts",".tsx"]:
            # TypeScript    https://pt.wikipedia.org/wiki/TypeScript
            return "TypeScript"
        elif extensionFile in [".swift"]:
            # Swift         https://pt.wikipedia.org/wiki/Swift_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["Swift"]+=1
            return "Swift"
        elif extensionFile in [".rs",".rlib"]:
            # Rust          https://pt.wikipedia.org/wiki/Rust_(linguagem_de_programa%C3%A7%C3%A3o)
            return "Rust"
        elif extensionFile in [".prg",".ch"]:
            # Clipper       https://pt.wikipedia.org/wiki/Clipper_(linguagem_de_programa%C3%A7%C3%A3o)
            return "Clipper"
        elif extensionFile in [".cr"]:
            # Crystal       https://pt.wikipedia.org/wiki/Crystal_(linguagem_de_programa%C3%A7%C3%A3o)
            return "Crystal"
        elif extensionFile in [".vue"]:
            # Vue           https://br.vuejs.org/v2/guide/single-file-components.html
            return "Vue"
        elif extensionFile in [".vim"]:
            # Vim           https://en.wikipedia.org/wiki/Vim_(text_editor)
            return "Vim"
        elif extensionFile in [".jsonnet"]:
            # Jsonnet       https://jsonnet.org/
            return "Jsonnet"
        elif extensionFile in [".json"]:
            return "JSon"
        elif extensionFile in [".erl", ".hrl"]:
            # Erlang https://pt.wikipedia.org/wiki/Erlang_(linguagem_de_programa%C3%A7%C3%A3o)
            return "Erlang"
        else:
            return "otherExtension"
    
    def setDictDevExpertise(self, author, filename):

        progLanguage = str()
        progLanguage = self.checkExtension(filename)
    
        index = 0
        extensionFile = str()

        if progLanguage != 'noExtension':
            try:
                index = filename.rindex(".") # last occurrence of "."
                extensionFile = filename[index:len(filename)]
            except Exception as e:
                print ("Extensão inexistente ...:", filename, extensionFile)
                pass
        
        if author not in self.devExpertiseList.keys():
            
            devExpertise = dict()
            expertise = dict()
            otherExt = dict()
            
            devExpertise['fork_name'] = author
            devExpertise['expertiseList'] = []
            
            otherExt['otherExtensions'] = [] 
            otherExt['noExtension'] = []

            if progLanguage == "otherExtension":
                otherExt['otherExtensions'].append(extensionFile)
            elif progLanguage == "noExtension":
                otherExt['noExtension'].append(filename)
            else:
                devExpertise['expertiseList']= [{'language': progLanguage, 'count':1}]

            devExpertise['others'] = otherExt

            self.devExpertiseList[author]=devExpertise

            del otherExt
            del expertise
            del devExpertise

        else: 

            for devKey in self.devExpertiseList.keys():

                if devKey == str(author):
                    devExpertise = self.devExpertiseList.get(devKey)
                    otherExt=devExpertise['others']

                    if progLanguage == "otherExtension":
                        if extensionFile not in otherExt['otherExtensions']:
                            otherExt['otherExtensions'].append(extensionFile)
                    elif progLanguage == "noExtension":
                        if filename not in otherExt['noExtension']:
                            otherExt['noExtension'].append(filename)
                    else:

                        languageList = list(map(itemgetter('language'), devExpertise['expertiseList']))

                        if progLanguage in languageList:
                            for expertise in devExpertise['expertiseList']:
                                if expertise['language']== progLanguage:
                                    expertise['count'] +=1
                        else: 
                            devExpertise['expertiseList'].append(dict({'language': progLanguage, 'count':1}))

    def getDevExpertiseList(self):
        return self.devExpertiseList
    
    def printDevExpertiseData(self, repoDataDir):
        with open(repoDataDir + "devExpertiseInfo.json","w+") as outfile:
            outfile.write(json.dumps(self.getDevExpertiseList())) 

def main():

    expList = ExpertiseList()
    
    expList.setDictDevExpertise("fulano", "README")
    expList.setDictDevExpertise("fulano", "test.c++")
    expList.setDictDevExpertise("fulano", "test1.cpp")
    expList.setDictDevExpertise("fulano", "test.py")
    expList.setDictDevExpertise("fulano", "test2.py")
    expList.setDictDevExpertise("fulano", "test.java")
    expList.setDictDevExpertise("fulano", "test.txt")
    expList.setDictDevExpertise("fulano", "test2.txt")
    expList.setDictDevExpertise("fulano", ".gitignore")
    expList.setDictDevExpertise("fulano", "README.md")
    expList.setDictDevExpertise("fulano", "README")
    expList.setDictDevExpertise("fulano", "doc/Makefile")
    expList.setDictDevExpertise("fulano", "Makefile")
    expList.setDictDevExpertise("fulano", "Dockerfile")
    expList.setDictDevExpertise("fulano", "test.doc")
    expList.setDictDevExpertise("fulano", "test.doc")

    expList.setDictDevExpertise("beltrano", "README")
    expList.setDictDevExpertise("beltrano", "doc/Makefile")
    expList.setDictDevExpertise("beltrano", "Makefile")
    expList.setDictDevExpertise("beltrano", "Dockerfile")
    expList.setDictDevExpertise("beltrano", "test.doc")
    expList.setDictDevExpertise("beltrano", "test.doc")
    expList.setDictDevExpertise("beltrano", "test.java")
    expList.setDictDevExpertise("beltrano", "test.rs")
    expList.setDictDevExpertise("beltrano", "test.go")
    expList.setDictDevExpertise("beltrano", "test.c++")
    expList.setDictDevExpertise("beltrano", "test.py")
    expList.setDictDevExpertise("beltrano", ".gitignore")
    expList.setDictDevExpertise("beltrano", "test.cpp")
    expList.setDictDevExpertise("beltrano", "README.md")
    expList.setDictDevExpertise("beltrano", "README")
    expList.setDictDevExpertise("beltrano", "doc/Makefile")
    expList.setDictDevExpertise("beltrano", "Makefile")
    expList.setDictDevExpertise("beltrano", "Dockerfile")

    expList.printDevExpertiseData()
    print()    
    print("done!")

if __name__ == "__main__":
    main()