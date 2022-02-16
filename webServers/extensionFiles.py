
class ExtensionFiles():

    def __init__(self):

        self.setOfExtensions = (
            ".html",".htm",
            ".css",
            ".js",
            ".java",
            ".h",".c", 
            ".cc",".cpp",".cxx",".C",".c++",".h",".hh",".hpp",".hxx",".h++",   
            ".d",
            ".cs",
            ".fs",".fsi",".fsx",".fsscript",
            ".pl",".pm",".t",".pod",
            ".php",".phtml",".php3",".php4",".php5",".php7",".phps",
            ".dart",
            ".coffee",
            ".rb",
            ".st",
            ".go",
            ".pas",".pp",".inc",
            ".scm",".ss",
            ".scala",".sc",
            ".lua",
            ".clj",".cljs",".cljc",".edn",
            ".hs",".lhs",
            ".fan",".fwt",
            ".vala",".vapi",
            ".f",".for",".ftn",".f90",".f95",".f03",".f08",".f15",
            ".kt",".kts",
            ".jl",
            ".py",".pyx",".pxd",
            ".ipynb",
            ".ts",".tsx",
            ".swift",
            ".rs",".rlib",
            ".prg",".ch",
            ".cr",
            ".vue", 
            ".vim",
            ".jsonnet",
            ".sql",".sqlite",".sqlite3", ".sqlitedb",".db")

#VERIFICAR E INCLUIR ESSAS DEMAIS EXTENSÕES PARA UM NOVO SURVEY/ANALISE - 31/03/21
#.as .asm .cshtml .ctp
#.d .ebuild .ejs .el .erb .erl .gradle .groovy
#.haml .i .jsp .less .m .mo .o
#.phpt .py .pyc .r .s .scala .scss .scssc
#.sh .smali .so .sql .tcl .vb .rkt


        self.setOfExcludedFile = ("Makefile", "Dockerfile")

    def checkExtFile(self, strFile):

        indexDot = strFile.rfind(".") # last occurrence of "."
        extFile = strFile[indexDot:len(strFile)]

        return (any([extFile in value for value in self.setOfExtensions])) 


    def checkExcludedFile(self, strFile):
        
        index = int()
        sFile = str()
        try:
            index = strFile.rindex("/") # last occurrence of "."
            sFile = strFile[index+1:len(strFile)]
        except Exception as e:
            sFile = strFile
        return (any([sFile in value for value in self.setOfExcludedFile])) 


    def checkExpertise(self, filename):

        index = 0
        extensionFile = str()

        try:
            index = filename.rindex(".") # last occurrence of "."
            extensionFile = filename[index:len(filename)]
            #print ("checkExpertise...:", filename, extensionFile)
        except Exception as e:
            return "Invalid"

        if index <= 0:
            return "NoExtension"

        if extensionFile in [".html", ".htm"]:
            # HTML          https://pt.wikipedia.org/wiki/HTML 
            #dictDevExpertise["HTML"]+=1
            return "HTML"
        elif extensionFile in [".css"]:
            # CSS           https://en.wikipedia.org/wiki/Cascading_Style_Sheets
            #dictDevExpertise["CSS"]+=1
            return "CSS"
        elif extensionFile in [".js"]:
            # JavaScript    https://pt.wikipedia.org/wiki/JavaScript
            #dictDevExpertise["JavaScript"]+=1
            return "JavaScript"
        elif extensionFile in [".java"]:
            # Java          https://pt.wikipedia.org/wiki/Java_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["Java"]+=1
            return "Java"
        elif extensionFile in [".h",".c"]:
            # C             https://pt.wikipedia.org/wiki/C_(linguagem_de_programa%C3%A7%C3%A3o) 
            #dictDevExpertise["C"]+=1
            return "C"
        elif extensionFile in [".cc",".cpp",".cxx",".C",".c++",".h",".hh",".hpp",".hxx",".h++"]:
            # C++           https://pt.wikipedia.org/wiki/C%2B%2B 
            #dictDevExpertise["C++"]+=1
            return "C++"
        elif extensionFile in [".cob",".cobol"]:
            # Cobol             https://www.filesuffix.com/pt/extension/cob 
            #dictDevExpertise["Cobol"]+=1
            return "Cobol"
        elif extensionFile in [".d"]:
            # D             https://pt.wikipedia.org/wiki/D_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["D"]+=1
            return "D"
        elif extensionFile in [".cs"]:
            # C#            https://pt.wikipedia.org/wiki/C_Sharp
            #dictDevExpertise["C#"]+=1
            return "C#"
        elif extensionFile in [".fs",".fsi",".fsx",".fsscript"]:
            # F#            https://pt.wikipedia.org/wiki/F_Sharp
            #dictDevExpertise["F#"]+=1
            return "F#"
        elif extensionFile in [".pl",".pm",".t",".pod"]:
            # Perl          https://pt.wikipedia.org/wiki/Perl
            #dictDevExpertise["Perl"]+=1
            return "Perl"
        elif extensionFile in [".php",".phtml",".php3",".php4",".php5",".php7",".phps"]:
            # PHP           https://pt.wikipedia.org/wiki/PHP 
            #dictDevExpertise["PHP"]+=1
            return "PHP"
        elif extensionFile in [".dart"]:
            # Dart          https://pt.wikipedia.org/wiki/Dart_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["Dart"]+=1
            return "Dart"
        elif extensionFile in [".coffee"]:
            # CoffeeScript  https://pt.wikipedia.org/wiki/CoffeeScript
            #dictDevExpertise["CoffeeScript"]+=1
            return "CoffeeScript"
        elif extensionFile in [".rb"]:
            # Ruby          https://pt.wikipedia.org/wiki/Ruby_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["Ruby"]+=1
            return "Ruby"
        elif extensionFile in [".st"]:
            # Smalltalk     https://pt.wikipedia.org/wiki/Smalltalk
            #dictDevExpertise["Smalltalk"]+=1
            return "Smalltalk"
        elif extensionFile in [".go"]:
            # GO            https://pt.wikipedia.org/wiki/Go_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["GO"]+=1
            return "GO"
        elif extensionFile in [".pas",".pp",".inc"]:
            # Pascal        https://pt.wikipedia.org/wiki/Pascal_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["Pascal"]+=1
            return "Pascal"
        elif extensionFile in [".scm",".ss"]:
            # Scheme        https://pt.wikipedia.org/wiki/Scheme
            #dictDevExpertise["Scheme"]+=1
            return "Scheme"
        elif extensionFile in [".scala",".sc"]:
            # Scala         https://pt.wikipedia.org/wiki/Scala_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["Scala"]+=1
            return "Scala"
        elif extensionFile in [".lua"]:
            # Lua           https://pt.wikipedia.org/wiki/Lua_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["Lua"]+=1
            return "Lua"
        elif extensionFile in [".clj",".cljs",".cljc",".edn"]:
            # Clojure       https://pt.wikipedia.org/wiki/Clojure
            #dictDevExpertise["Clojure"]+=1
            return "Clojure"
        elif extensionFile in [".hs",".lhs"]:
            # Haskell       https://pt.wikipedia.org/wiki/Haskell_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["Haskell"]+=1
            return "Haskell"
        elif extensionFile in [".fan",".fwt"]:
            # Fantom        https://pt.wikipedia.org/wiki/Fantom
            #dictDevExpertise["Fantom"]+=1
            return "Fantom"
        elif extensionFile in [".vala",".vapi"]:
            # Vala          https://pt.wikipedia.org/wiki/Vala_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["Vala"]+=1
            return "Vala"
        elif extensionFile in [".f",".for",".ftn",".f90",".f95",".f03",".f08",".f15"]:
            # Fortran           https://pt.wikipedia.org/wiki/Fortran
            #dictDevExpertise["Fortran"]+=1
            return "Fortran"
        elif extensionFile in [".kt",".kts"]:
            # Kotlin        https://pt.wikipedia.org/wiki/Kotlin
            #dictDevExpertise["Kotlin"]+=1
            return "Kotlin"
        elif extensionFile in [".jl"]:
            # Julia         https://pt.wikipedia.org/wiki/Julia_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["Julia"]+=1
            return "Julia"
        elif extensionFile in [".py",".pyx",".pxd",".ipynb"]:
            # Python        https://pt.wikipedia.org/wiki/Python   https://pt.stackoverflow.com/questions/185944/extens%C3%B5es-pyc-pyd-pyo-em-python
            #dictDevExpertise["Python"]+=1
            return "Python"
        elif extensionFile in [".ts",".tsx"]:
            # TypeScript    https://pt.wikipedia.org/wiki/TypeScript
            #dictDevExpertise["TypeScript"]+=1
            return "TypeScript"
        elif extensionFile in [".swift"]:
            # Swift         https://pt.wikipedia.org/wiki/Swift_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["Swift"]+=1
            return "Swift"
        elif extensionFile in [".rs",".rlib"]:
            # Rust          https://pt.wikipedia.org/wiki/Rust_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["Rust"]+=1
            return "Rust"
        elif extensionFile in [".prg",".ch"]:
            # Clipper       https://pt.wikipedia.org/wiki/Clipper_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["Clipper"]+=1
            return "Clipper"
        elif extensionFile in [".cr"]:
            # Crystal       https://pt.wikipedia.org/wiki/Crystal_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["Crystal"]+=1
            return "Crystal"
        elif extensionFile in [".vue"]:
            # Vue           https://br.vuejs.org/v2/guide/single-file-components.html
            #dictDevExpertise["Vue"]+=1
            return "Vue"
        elif extensionFile in [".vim"]:
            # Vim           https://en.wikipedia.org/wiki/Vim_(text_editor)
            #dictDevExpertise["Vim"]+=1
            return "Vim"
        elif extensionFile in [".jsonnet"]:
            # Jsonnet       https://jsonnet.org/
            #dictDevExpertise["Jsonnet"]+=1
            return "Jsonnet"
        elif extensionFile in [".json"]:
            return "JSon"
        elif extensionFile in [".sql",".sqlite",".sqlite3", ".sqlitedb",".db"]:
            return "SQL" #https://fileinfo.com/extension/sql
        elif extensionFile in [".erl", ".hrl"]:
            # Erlang https://pt.wikipedia.org/wiki/Erlang_(linguagem_de_programa%C3%A7%C3%A3o)
            #dictDevExpertise["Erlang"]+=1
            return "Erlang"
        else:
            #dictDevExpertise["others"]+=1
            #dictDevExpertise["other_extension"]=extensionFile #inicializar como array e usar o append ou push
            return "OtherExtension"

        # https://fileinfo.com
        # Essas linguagem usam extensões já mencionadas
        # Groovy        https://pt.wikipedia.org/wiki/Groovy 
        # Objective-C   https://pt.wikipedia.org/wiki/Objective-C
        # JRuby         https://pt.wikipedia.org/wiki/JRuby

        #VERIFICAR E INCLUIR ESSAS DEMAIS EXTENSÕES PARA UM NOVO SURVEY/ANALISE - 31/03/21
        #.as .asm .cshtml .ctp
        #.d .ebuild .ejs .el .erb .erl .gradle .groovy 
        #.haml .i .jsp .less .m .mo .o
        #.phpt .py .pyc .r .s .scala .scss .scssc
        #.sh .smali .so .sql .tcl .vb .rkt



def main():

    extFiles = ExtensionFiles()

    print("A extensão '.doc' é válida (False)...........: ", extFiles.checkExtFile("test.doc"))
    print("A extensão '.java' é válida (True)...........: ", extFiles.checkExtFile("test.java"))
    print("A extensão '.txt' é válida (False)...........: ", extFiles.checkExtFile("test.txt"))
    print("A extensão '.c++' é válida (True)............: ", extFiles.checkExtFile("test.c++"))
    print("A extensão '.py' é válida (True).............: ", extFiles.checkExtFile("test.py"))
    print("A extensão '.gitignore' é válida (False).....: ", extFiles.checkExtFile(".gitignore"))
    print("A extensão '.cpp' é válida (True)............: ", extFiles.checkExtFile("test.cpp"))
    print("A extensão '.md' é válida (False)............: ", extFiles.checkExtFile("README.md"))
    print("README é um arquivo excluido (True) .........: ", extFiles.checkExcludedFile("README"))
    print("Makefile é um arquivo excluido (True) .......: ", extFiles.checkExcludedFile("doc/Makefile"))
    print("Makefile é um arquivo excluido (True) .......: ", extFiles.checkExcludedFile("Makefile"))
    print("Dockerfile é um arquivo excluido (True) .....: ", extFiles.checkExcludedFile("Dockerfile"))


    
    print("done!")

if __name__ == "__main__":
    main()
    

#   Linguagens supportada:

# HTML          https://pt.wikipedia.org/wiki/HTML
# CSS           https://en.wikipedia.org/wiki/Cascading_Style_Sheets
# JavaScript    https://pt.wikipedia.org/wiki/JavaScript
# Java          https://pt.wikipedia.org/wiki/Java_(linguagem_de_programa%C3%A7%C3%A3o)
# C             https://pt.wikipedia.org/wiki/C_(linguagem_de_programa%C3%A7%C3%A3o)
# C++           https://pt.wikipedia.org/wiki/C%2B%2B 
# D             https://pt.wikipedia.org/wiki/D_(linguagem_de_programa%C3%A7%C3%A3o)
# C#            https://pt.wikipedia.org/wiki/C_Sharp
# F#            https://pt.wikipedia.org/wiki/F_Sharp
# Perl          https://pt.wikipedia.org/wiki/Perl
# PHP           https://pt.wikipedia.org/wiki/PHP
# Dart          https://pt.wikipedia.org/wiki/Dart_(linguagem_de_programa%C3%A7%C3%A3o)
# CoffeeScript  https://pt.wikipedia.org/wiki/CoffeeScript
# Ruby          https://pt.wikipedia.org/wiki/Ruby_(linguagem_de_programa%C3%A7%C3%A3o)
# Smalltalk     https://pt.wikipedia.org/wiki/Smalltalk
# GO            https://pt.wikipedia.org/wiki/Go_(linguagem_de_programa%C3%A7%C3%A3o)
# Pascal        https://pt.wikipedia.org/wiki/Pascal_(linguagem_de_programa%C3%A7%C3%A3o)
# Scheme        https://pt.wikipedia.org/wiki/Scheme
# Scala         https://pt.wikipedia.org/wiki/Scala_(linguagem_de_programa%C3%A7%C3%A3o)
# Lua           https://pt.wikipedia.org/wiki/Lua_(linguagem_de_programa%C3%A7%C3%A3o)
# Clojure       https://pt.wikipedia.org/wiki/Clojure
# Haskell       https://pt.wikipedia.org/wiki/Haskell_(linguagem_de_programa%C3%A7%C3%A3o)
# Fantom        https://pt.wikipedia.org/wiki/Fantom
# Vala          https://pt.wikipedia.org/wiki/Vala_(linguagem_de_programa%C3%A7%C3%A3o)
# Fortran       https://pt.wikipedia.org/wiki/Fortran
# Kotlin        https://pt.wikipedia.org/wiki/Kotlin
# Julia         https://pt.wikipedia.org/wiki/Julia_(linguagem_de_programa%C3%A7%C3%A3o)
# Python        https://pt.wikipedia.org/wiki/Python   https://pt.stackoverflow.com/questions/185944/extens%C3%B5es-pyc-pyd-pyo-em-python
# Jupiter Notebook
# TypeScript    https://pt.wikipedia.org/wiki/TypeScript
# Swift         https://pt.wikipedia.org/wiki/Swift_(linguagem_de_programa%C3%A7%C3%A3o)
# Rust          https://pt.wikipedia.org/wiki/Rust_(linguagem_de_programa%C3%A7%C3%A3o)
# Clipper       https://pt.wikipedia.org/wiki/Clipper_(linguagem_de_programa%C3%A7%C3%A3o)
# Crystal       https://pt.wikipedia.org/wiki/Crystal_(linguagem_de_programa%C3%A7%C3%A3o)
# Vue           https://br.vuejs.org/v2/guide/single-file-components.html
# Vim           https://en.wikipedia.org/wiki/Vim_(text_editor)
# Jsonnet       https://jsonnet.org/




# Essas linguagem usam extensões já mencionadas
# Groovy        https://pt.wikipedia.org/wiki/Groovy 
# Objective-C   https://pt.wikipedia.org/wiki/Objective-C
# JRuby         https://pt.wikipedia.org/wiki/JRuby