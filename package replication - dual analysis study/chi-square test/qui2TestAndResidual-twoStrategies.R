######################### Qui-quadrado de independência #########################

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
 
 #tabCont <- read.csv('qui2_twoStrategies_2x2_interestIn.csv', row.names=1, sep=",")
 #tabCont <- read.csv('qui2_twoStrategies_2x3_interestIn.csv', row.names=1, sep=",")
 #tabCont <- read.csv('qui2_twoStrategies_2x2_familiarity.csv', row.names=1, sep=",")
 tabCont <- read.csv('qui2_twoStrategies_2x3_familiarity.csv', row.names=1, sep=",")
 #tabCont <- read.csv('qui2_twoStrategies_2x2_devRecommendations.csv', row.names=1, sep=",")
 
 #View(tabCont)                               # Visualização dos dados em janela separada
 glimpse(tabCont)                             # Visualização de um resumo dos dados
 
 # Realização do teste de Qui-quadrado
 
 options(scipen = 999)
 #quiqua <- chisq.test(tabCont, simulate.p.value = TRUE)
 quiqua <- chisq.test(tabCont)
 quiqua
 
 fishertest <- fisher.test(tabCont)
 fishertest
 

 # Passo 3: Análise das frequências esperadas
 ## Pressuposto: frequências esperadas > 5
 quiqua$expected

 # Passo 4: Análise dos resíduos padronizados ajustados
 
 ## Resíduo padronizado (SPSS) - resíduos de Pearson:
 quiqua1$residuals
 
 ## Resíduo padronizado ajustado (SPSS):
 quiqua1$stdres
 
 ## Resíduo padronizado ajustado > 1,96 ou < -1,96 -- alfa de 5%
 # Passo 5: Cálculo do ponto de corte para os resíduos padronizados
 
 ## Calcular o novo alfa:
 ### Sendo "l" o número de linhas e "c" o número de colunas
 ### Dividiremos o 0,05 pelo produto c*l (número de células)
 
 novoalfa <- 0.05/(nrow(tabCont)*ncol(tabCont))
 novoalfa
 
 
 ## Calcular o ponto de corte, com base no novo alfa:
 ### A divisão por dois é por ser bicaudal
 
 qnorm(novoalfa/2)
 
 ### Resíduos significativos: > 2,64 ou < -2,64 -- novo alfa: 0,008
 
 
 # Passo 6 (opcional): Cálculo do p para os resíduos
 
 round(2*(1-pnorm(abs(quiqua$stdres))),6)
 
 ## Devem ser comparados com o novo alfa: 0,008
 
 
 # Passo 7: Tamanho de efeito - V de Cramer
 
 cramer_v(tabCont)
 
 ## A interpretação depende dos graus de liberdade:
 ## gl = (linhas-1) * (colunas-1)
 ## Nesse caso: gl = 2 e o V de Cramer corresponde a um tamanho de efeito pequeno (Cohen, 1988)
 
 
 ### Para tabelas 2 x 2:
 # phi(tabela)
 
 
 
 # Passo 8: Representação visual dos resíduos ajustados
 
 corrplot(quiqua1$stdres, is.cor = FALSE,
          method = "color",
          tl.col = "black", tl.srt = 0)
 
 
 