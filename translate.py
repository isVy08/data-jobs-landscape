#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 14:50:04 2020

@author: vyvo
"""
from dependency import * 

pd.set_option('display.max_columns',100)
pd.set_option('display.max_rows',500)


#1. READ DATASET
data = pd.read_csv('dsjob_final.csv',converters={'industry_v2': ast.literal_eval,'job_func_v2': ast.literal_eval})

#----------------------------------------------------------------------

#2.UNUSUAL VALUES: Remove records where description = 0  & set other '0' as null values  
data = data[data.description!='0'].reset_index(drop=True)

for col in ['exp_level','job_func','industry','job_type']: 
    data[col] = data[col].map(lambda x: np.nan if x=='0' else x)
        
#3. LOCATION: get Country & Area --------------------------------------

#extract Country from Link 
data['country'] = data['link'].str.extract(r'https://([a-z]+)')
data['country'] = data['country'].map(lambda x: 'us' if x=='www' else x)

def to_country(x):
    if x == 'us':
        return 'United States'
    elif x == 'uk':
        return 'United Kingdom'
    else: 
        return (pcy.countries.get(alpha_2=x.upper()).name)

data['country'] = data['country'].apply(to_country)

#extract Area (State / City)  from Location 

nrow = data.shape[0]
loc = data['location'].str.split(', ') #split into list

for i in range(nrow): 
    #print(loc[i])
    if data['country'][i] in loc[i] and len(loc[i])>1:
        loc[i].remove(data['country'][i]) #remove 'Country' from the value

us_state = {
    'CA':'California','OR':'Oregon','GA':'Georgia','NY':'New York','MA':'Massachusetts',
    'PA':'Pennsylvania','AZ':'Arizona','TX':'Texas', 'IL':'Illinois','MN':'Minnesota'
    }
#normalize values of area 
def to_area(x): 
    if len(x) == 2:
        return us_state[x]
    elif 'Metropolitan' in x: 
        p = re.compile(r'(.*) Metropolitan') 
        return p.findall(x)[0]
    else: 
        return x
  
loc = loc.map(lambda x: x[-1])   
data['area'] = loc.apply(to_area)
#-----------------------------------------------------------------------------

# 4. TRANSLATE TEXT ATTRIBUTE: JOB FUNC / INDUSTRY / EXP LEVEL / JOB TYPE / JOB DESCRIPTION / TITLE

#Transform JOB FUNC / INDUSTRY into simple attribute of unique values


data['job_func'] = data['job_func'].map(lambda x: ast.literal_eval(x) if x is not np.nan else x)
data['industry'] = data['industry'].map(lambda x: ast.literal_eval(x) if x is not np.nan else x)

fucins = {}

for i in range(nrow):
    try:
        country = data['Country'][i]
        if country in fucins.keys():        
            fl = list(filter(lambda x: x not in fucins[country],data['job_func'][i]))
            il = list(filter(lambda x: x not in fucins[country],data['industry'][i]))
            fl.extend(il)
            fucins[data['Country'][i]].extend(fl)
        else: 
            fucins[country] = []
    except: 
        pass            


# extract file to be translated 
        
foreign = ['China','Japan','France','Germany','Italy','Netherlands','Spain','Sweden','Switzerland']

# =============================================================================
# for country in foreign: 
#     subset = data[data['Country']==country]
#     attrs = ['description','title','job_type','exp_level','fucins']
#     df = pd.DataFrame()
#     for a in attrs: 
#         if a == 'description': 
#             df = pd.concat([df,subset[a].reset_index(drop=True)],axis=1,ignore_index=True)
#         elif a == 'fucins':
#             df = pd.concat([df,pd.Series(fucins[country])],axis=1,ignore_index=True)
#         else: 
#             df = pd.concat([df,pd.Series(subset[a].unique())],axis=1,ignore_index=True) 
#     df.columns = attrs 
#     filename = '~/raw text/'+country+'.xlsx'
#     get_file(df,filename)            
#     
# =============================================================================

#5. GET TRANSLATED RESULT

#load file
trans = pd.read_excel('translated.xlsx',index_col=0)

#create dictionary for Title / Job type / Exp level / Job func / Industry
dictionary = {}

for country in foreign: 
    file = pd.read_excel('~/raw text/'+country+'.xlsx')
    for a in ['title','job_type','exp_level','fucins']:
        s = trans.loc[country,a].dropna()
        s.index = list(file[a].dropna())
        dictionary.update(s.to_dict())


#update translated attributes      
        
def translate(x):
    if x in dictionary.keys():
        return dictionary[x]
    else: 
        return x 

for a in ['description','title','exp_level','job_type','job_func','industry']:
    name = a+'_v2'
    if a == 'description': 
        data[name] = data['description']
        for country in foreign: 
            data.loc[data['country']==country,name] = list(trans.loc[country,'description'])
    elif a in ['title','job_type','exp_level']:
        data[name] = data[a].map(lambda x: translate(x))
    else: 
        data[name] = data[a].map(lambda x: [translate(i) for i in x] if isinstance(x,list) else x)
        
newdata = data[['id','link','company','list_time','country','area','description_v2','exp_level_v2','job_type_v2','industry_v2','job_func_v2']]
newdata.to_csv('~/Documents/GitHub/LinkedIn_dsjob/dsjob_trans.csv',index=False)
