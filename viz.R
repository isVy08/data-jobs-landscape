library("tm")
library("SnowballC")
library("wordcloud")
library("RColorBrewer")

data = read_excel('desc_text.xlsx',sheet=3)
colnames(data)[1] = 'experience'

x = data$general[4]
text = Corpus(VectorSource(x))
tdm = TermDocumentMatrix(text)
m <- as.matrix(tdm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
# check the color palette name 
colorPalette="Dark2"
if(!colorPalette %in% rownames(brewer.pal.info)) colors = colorPalette else colors = brewer.pal(8, colorPalette) 

# Plot the word cloud
set.seed(1234)
wordcloud(d$word,d$freq, min.freq=3, max.words=100,
          random.order=FALSE, rot.per=0.35, 
          use.r.layout=FALSE, colors=colors)

