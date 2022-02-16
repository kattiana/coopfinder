from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv as csv
import pandas as pd
import time

class Similarity():

    def __init__(self, fork_names, strategy, resultsPath, dicts):
        self.fork_names = fork_names

        if strategy: #True: Changes in File; False: Changed File
            self.dictCorpus = dicts.getDictCorpusChangesInFiles()
        else: self.dictCorpus = dicts.getDictCorpusChangedFiles()
        self.corpus = []
        self.forksInCorpus = []
        self.tfidf_matrix = []
        self.resultsPath = resultsPath
        self.dicts = dicts
        self.createCorpus()

    def createCorpus(self):
        for fork in self.fork_names: # developers who changed files (commitFilesDir)
            if fork in self.dictCorpus:
                self.forksInCorpus.append(fork)
                self.corpus.append(self.dictCorpus[fork]['changedFilesList'])

        df_corpus = pd.DataFrame(self.corpus, index = self.forksInCorpus)
        df_corpus.to_csv(self.resultsPath + "tfidf_corpus.csv")
        
    def runTFIDF(self):
        tfidfVectorizer = TfidfVectorizer(analyzer='word', lowercase = False, token_pattern = '[a-zA-Z0-9/.#+_-]+')
        # Apply the vectoriser to the training set
        self.tfidf_matrix = tfidfVectorizer.fit_transform(self.corpus)

        feature_names = tfidfVectorizer.get_feature_names()
        dense = self.tfidf_matrix.todense()
        denselist = dense.tolist()

        df_tfidf = pd.DataFrame(denselist, index = self.forksInCorpus, columns=feature_names)

        for forkName in self.forksInCorpus:

            new_df = df_tfidf.filter(like=forkName, axis=0)
            df_sorted = new_df.sort_values(by=forkName, axis=1, ascending=False)
            files = df_sorted.head()   
            filenames = list(files)  

            for filename in filenames:

                if files[filename][0]>0:
                    self.dicts.setDictDevRelevantFiles(forkName, filename, files[filename][0])
        df_tfidf.to_csv(self.resultsPath + "tfidf_matrix.csv")

    def runCosSim(self):

        cosSimResult = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        with open(self.resultsPath + "cosineSimilarity.csv","w") as outfile:
            outfile.write(str(cosSimResult)) 

        #convert into pandas dataframe
        cosine_sim_df = pd.DataFrame(cosSimResult, index = self.forksInCorpus, columns=self.forksInCorpus)
        cosine_sim_df.to_csv(self.resultsPath + "cosineSimResults.csv")

        for forkName in self.forksInCorpus:
                    
            new_df = cosine_sim_df.filter(like=forkName, axis=0)
            df_sorted = new_df.sort_values(by=forkName, axis=1, ascending=False)
            devs_top = df_sorted.head() 

            devRecList = []
            devRecList = devs_top.columns

            for devRec in df_sorted:
                if forkName != devRec:
                    if df_sorted[devRec].values[0] > 0:
                        print(forkName,devRec, df_sorted[devRec].values[0]) 
                        self.dicts.setDictDevRec(forkName,devRec,df_sorted[devRec].values[0])

            del new_df
            del df_sorted
            del devs_top
            del devRecList

            print ("similarity done!")
            print()
            print()
## Tutoriais:
#https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
#https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html?highlight=tfidfvectorizer#sklearn.feature_extraction.text.TfidfVectorizer
#https://stackoverflow.com/questions/57424183/how-to-force-sklearn-countvectorizer-to-not-remove-special-characters-i-e
