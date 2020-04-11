
data = read.csv('jrtest.csv',stringsAsFactors = F)

# remove rows with 0
data = data[data!='0',]
txt = paste(data,collapse = '')

source('http://www.sthda.com/upload/rquery_wordcloud.r')
res<-rquery.wordcloud(txt, max.words = 100, lang = "english")
