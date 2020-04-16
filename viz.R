library("SnowballC")
library("wordcloud")
library("RColorBrewer")
library("readxl")

# check the color palette name 
colorPalette="Dark2"
if(!colorPalette %in% rownames(brewer.pal.info)) colors = colorPalette else colors = brewer.pal(8, colorPalette) 

# general words
gword = as.vector(read.csv('gword.csv')$word)

# tools 
tool = as.vector(read.csv('technical.csv')$tools)

# plot word cloud 
wc = function(filepath1,filepath2,sheetname,gword,tool,maxword=300) {
  d = read_excel(filepath1,sheet = sheetname) # read job description file 
  r = read_excel(filepath2,sheet = sheetname) # read job requirement file 
  colnames(d)[1] = "word"
  colnames(r)[1] = "word"
  d = d[(nchar(d$word)>3) & (!d$word %in% gword) & (!d$word %in% tool),] 
  r = r[is.na(as.numeric(r$word)) & (!r$word %in% letters[-c(18)]),] #exclude numbers & letters, except R
  r = r[(!r$word %in% d$word) & (!r$word %in% gword),]
  # plot 
  set.seed(18)
  wordcloud(d$word,d$freq, min.freq=3, max.words=maxword, scale = c(2.5,.5), random.order=FALSE, rot.per=0.35, use.r.layout=FALSE, colors=colors)
  title(main = paste("Responsibilities of",sheetname)) 
  wordcloud(r$word,r$freq, min.freq=3, max.words=maxword, scale = c(2.5,.5), random.order=FALSE, rot.per=0.35, use.r.layout=FALSE, colors=colors)
  title(main = paste("Requirement for",sheetname)) 
}

# Plot by attribute

choice = function(attr,gword,tool,maxword=300) {
  if (attr=='t') {
    level = c('Data Scientist','Data Analyst','Data Engineer','Machine Learning Engineer')
  } else {level = c('Entry level','Senior','Associate')
    }
  filepath1 = paste(attr,'_desc.xlsx',sep="")
  filepath2 = paste(attr,'_reqr.xlsx',sep="")
  for (sheetname in level) {
   wc(filepath1,filepath2,sheetname,gword,tool,maxword=maxword)  
  }
}
  
choice("e",gword,tool,maxword=25)



