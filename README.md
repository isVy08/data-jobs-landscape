# About this project 
Wanna break into Data industry but don't know where to begin? Check out my data analysis on what the world of "Data Analytics" is all about. 

# What I did 
1. Scraping and collecting 10,000 + data job postings on LinkedIn - worldwide and multilingual !   
2. Various pre-processing steps for textual data, including language translation  
3. Visualizing data statically and interactively
4. Writing up a detailed report 

# What's in this repo  
I used `Python` for data processing and `R` for visualization

**py-processor**
1. `cleantext`: text cleaning snippets 
2. `scraper`: web driver to automatically crawl data on LinkedIn public domain. No need to login !
3. `translator`: web driver to automatically translate data to English using Google Translate 
4. `reqs_keywords.csv`, `resp_keywords.csv`: keywords to filter out sections on Job requirements and Job responsibilities 

**Shiny**

My interactive viz built upon `Shiny (R)` and `D3 (JavaScript)`

To view the viz on local host, an easy way is to 
(1) open your R console
(2) load `Shiny` directory
(3) run the following code

```
devtools::install_github("czxa/gwordtree")

packages = c("shiny","googleVis", "gwordtree", "wordcloud", "RColorBrewer", "ggplot2","plotly","r2d3")
lapply(packages, require, character.only = TRUE)

runApp()
```

Another way to run directly from GitHub, but make sure your R version is compatible. 
```
runGitHub("data-jobs-landscape", "isVy08", subdir = "Shiny/")
```


# What's in the report

Only interested in the findings? Feel free to skip the codes and head straight to my article
<a href="https://isvy08.github.io/blog/data-job-landscape.html">What does a Data Scientist do?</a>

It contains useful information on 
  
1. Where is the demand for Data Scientist the highest?
2. What is a typical Data Scientist expected to do?
3. What skills and qualifications are required for Data Scientist?
4. How is job description for this role different among experience levels?
5. How is job description for Data Scientist different from those for Data Analyst, Data Engineer
and Machine Learning Engineer?





