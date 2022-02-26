######################### Qui-quadrado de independência #########################

# Passo 1: Carregar os pacotes que serão usados

if(!require(dplyr)) install.packages("dplyr") 
library(dplyr)
if(!require(rstatix)) install.packages("rstatix") 
library(rstatix)
if(!require(psych)) install.packages("psych") 
library(psych)

# Passo 2: Carregamento do banco de dados e montagem do modelo

# Importante: selecionar o diretório de trabalho (working directory)
# Isso pode ser feito manualmente: Session > Set Working Directory > Choose Directory
# Ou usando a linha de código abaixo:
setwd("~/Qui2-twoStrategies")
 ############ Primeira opção: banco já no formato de tabela de contingência ############
 
 # Carregamento do Banco
 
 tabCont <- read.csv('qui2_twoStrategies_2x2_interestIn.csv', row.names=1, sep=",")
 #tabCont <- read.csv('qui2_twoStrategies_2x2_familiarity.csv', row.names=1, sep=",")
 #tabCont <- read.csv('qui2_twoStrategies_2x2_devRecommendations.csv', row.names=1, sep=",")
 
 View(tabCont)                               # Visualização dos dados em janela separada
 glimpse(tabCont)                            # Visualização de um resumo dos dados
 
 # Realização do teste de Qui-quadrado
 options(scipen = 999)
 #quiqua <- chisq.test(tabCont, simulate.p.value = TRUE)
 quiqua <- chisq.test(tabCont)
 quiqua
 
 # Passo 3: Análise das frequências esperadas
 ## Pressuposto: frequências esperadas > 5
 quiqua$expected

 # Passo 4: Análise dos resíduos padronizados ajustados
 ## Resíduo padronizado (SPSS) - resíduos de Pearson:
 quiqua1$residuals
 
 ## Resíduo padronizado ajustado (SPSS):
 quiqua1$stdres
 
 