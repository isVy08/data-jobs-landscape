# About this project 
As a wanna-be Data Scientist, many time I find myself drowning in an endless pool of knowledge. And, my periodic existential crisis in which I cannot help from wondering what I am doing with my life and why I never seem good enough, definitely bolsters things up. So, I decided to crawl data on job postings for Data Scientist role on LinkedIn to understand what a Data Scientist is actually expected to do and what it takes to become one. I could have just googled and found tons of articles. Well it occurs to me that the writers were either not serious about it (they just wanted good SEO) or trying to prove why I suck! 

# What's interesting about this project
- Data scraped from public Linkedn job search page. No need to Login!  
- The whole data is textual 
- Some job postings are in foreign languages as I also scraped jobs from non-English speaking countries 
- Play around Python NLTK packages and Word cloud visualization 

# What I did 
1. Scrape and collect data 
2. Wrange and clean text (the whole data is textual) 
3. Explore the data through static visualizations (mostly word cloud) 
4. Write up an analysis report 

# What's in this repo  
Codes to perform major steps of the data preparation process 
1. Dependency 
2. Scraper
3. Translator: Translate data to English using Google Translate website 
4. Cleantext: Commonly used text cleaning functions 
5. Classifier: Job descriptions contain different kinds of information, besides Job Responsibilities and Requirements. I only need to extract and analyze those two pieces of information separately. So, I want to design a small algorithm to do this. 
- Naive version (Done): I classifiy a block of text based on keywords in its heading 
6. Data: raw dataset, clean dataset (with all attributes), keywords (for classifier)

Still don't understand what I am doing? Read my report please. 

# What's in the report
1. Where is the demand for Data Scientist the highest?
2. What is a typical Data Scientist expected to do?
3. What skills and qualifications are required for Data Scientist?
4. How is job description for this role different among experience levels?
5. How is job description for Data Scientist different from those for Data Analyst, Data Engineer
and Machine Learning Engineer?

# What's next 
- Build interactive visualizations (see below)

# About my interactive viz
Dependencies
```
shiny
googleVis
gwordtree
devtools::install_github("czxa/gwordtree")
wordcloud
RColorBrewer
ggplot2
plotly
r2d3
```
To view the viz, open your R console and run

```
runGitHub("LinkedIn_dsjob", "isVy08", subdir = "Shiny/")
```

