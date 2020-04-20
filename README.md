# About this project 
As a wanna-be Data Scientist, many time I find myself drowning in an endless pool of stuff I am expected to have a hang of to be qualified to become one. And, my periodic existential crisis in which I cannot help from wondering what I am doing with my life and why I never seem good enough, definitely bolsters things up. So, I decided to crawl data on job postings for Data Scientist role on LinkedIn to understand what a Data Scientist is actually expected to do and what it takes to become one. I could have just googled and found tons of articles. Well it occurs to me that the writers were either not serious about it (they just wanted good SEO) or trying to prove why I suck! 

# What's interesting about this project (at least to me) 
- I scraped data from public Linkedn job search page. No need to Login!  
- The whole data is textual 
- Some job postings are in foreign languages as I also scraped jobs from non-English speaking countries 
- Play around Python NLTK packages and Word cloud visualization 

# What I did 
1. Scrape and collect data 
2. Wrange and clean text (the whole data is textual) 
3. Explore the data by create static visualizations (mostly word cloud) 
4. Write up an analysis report 

# What's in this repo  
Codes to perform major steps of the data preparation process 
1. Dependency 
2. Scraper
3. Translator: Translate data to English using Google Translate website 
4. Cleantext: Commonly used text cleaning functions 
5. Classifier: Job descriptions contain different kinds of information, besides Job Responsibilities and Requirements. I only need to extract and analyze those two pieces of information separately. So, I want to design a small algorithm to do this. 
- Naive version (Done): I classifiy a block of text based on keywords in its heading 
- Hero version: Advanced ML text classification model 
6. Data: raw dataset, clean & full-stack dataset, keywords

Still don't understand what I am doing? Read my report please. 

# What's next 
- Develop Hero classifier 
- Build interactive visualizations 
- Real-time job alert? 

