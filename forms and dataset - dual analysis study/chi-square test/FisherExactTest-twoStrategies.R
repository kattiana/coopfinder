######################### Fisher's Exact Test #########################

# Passo 1: Carregar os pacotes que serão usados

if(!require(dplyr)) install.packages("dplyr") 
library(dplyr)
if(!require(rstatix)) install.packages("rstatix") 
library(rstatix)
if(!require(psych)) install.packages("psych") 
library(psych)
if(!require(corrplot)) install.packages("corrplot") 
library(corrplot)

# Passo 2: Carregamento do banco de dados e montagem do modelo

# Importante: selecionar o diretório de trabalho (working directory)
# Isso pode ser feito manualmente: Session > Set Working Directory > Choose Directory
# Ou usando a linha de código abaixo:
 setwd("~/Qui2-twoStrategies")
 ############ Primeira opção: banco já no formato de tabela de contingência ############
 
 # Carregamento do Banco
 
 #tabCont <- read.csv('qui2_twoStrategies_2x3_interestIn.csv', row.names=1, sep=",")
 tabCont <- read.csv('qui2_twoStrategies_2x3_familiarity.csv', row.names=1, sep=",")
 
 #View(tabCont)                               # Visualização dos dados em janela separada
 glimpse(tabCont)                             # Visualização de um resumo dos dados
 
 # Realização do teste Exato
 
 options(scipen = 999)
 fishertest <- fisher.test(tabCont)
 fishertest
 