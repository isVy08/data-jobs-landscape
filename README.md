# LinkednIn_dsjob
1. Scrape job postings for Data Scientist role on LinkedIn
2. Wrangle data into tabular format with html tags removed (except Job Description feature)  
3. Build ML model to detect which sections in Job Description refer to Responsibilities or Qualifications
  3.1. Split train & test dataset (train data contains texts with bold titles) 
  3.2. Label train data from current dataset based on bold titles (group it first)  #1: Responsibility / 2: Requirement / 3 Others
  3.2. Preprocess text data in test dataset 
  3.3. Build & test ML models 
  3.4. Assign predicted labels to test dataset 
 4. Create 2 new features based on train / test labels: Job Responsibility & Job Description
 5. Explore dataset & report insights 
 6. Build real-time visualizations updating job demand for Data Scientists around the world 
 7. Collect more data from other job sites e.g., Glassdoor, Seek 
