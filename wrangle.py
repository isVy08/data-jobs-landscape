#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 21:34:54 2020

@author: vyvo
"""

from dependency import *

#read translated data - remember to change directory 
data = pd.read_csv('dsjob_trans.csv',converters={'industry_v2': ast.literal_eval,'job_func_v2': ast.literal_eval})

#Standardize values for EXP LEVEL / JOB TYPE 

from datainfo import get_unique
get_unique(data[['exp_level_v2','job_type_v2']])

exp_level = {
    'internship':['stage','trainee','practices','internship','practice'],
    'associate':['associate','medium level','intermediate','some responsibility','confirmed','collaborator','coworker','assistant manager','staff level'],
    'mid-senior level':['mid-senior level','high-level','medium-high level','intermediate control','manager','senior level','senior employee'],
    'director':['director','director / supervisor','managing director','president / ceo','executive level','upper manager','manager level'],
    'n/a':['not applicable','non pertinent','unlimited']
    }

job_type = {
    'contract':['contract','contract for work'],
    'internship':['internship','stage','practice','practices','intern / alternating'],
    'temporary':['temporary','temporary employment','volunteer','CDD or one-off mission','temporary work','temporary worker'],
    'part-time':['part-time','part time'],
    'others':['others','other']
    }


def stdize(x,default_result,valueDict):
    result = default_result
    for level in list(valueDict.keys()):
        if x.lower() in valueDict[level]:
            result = level
            break
    return result 


data['exp_level_v2'] = data['exp_level_v2'].map(lambda x: stdize(x,'Entry level',exp_level)) 
data['job_type_v2'] = data['job_type_v2'].map(lambda x: stdize(x,'Full-time',job_type)) 



#Standardize values for INDUSTRY

#original     
data['industry_v2'] = data['industry_v2'].map(lambda x: list(map(lambda i: remove_special_characters(i.lower()),x)) if isinstance(x,list) else x)
original = list(data['industry_v2'].dropna())
original = pd.Series(chain(*original)).unique()

#industry
ind = pd.read_csv('industry.csv')
ind['Industry_clean'] = ind['Industry'].apply(remove_special_characters).str.lower()
check_list = ind['Industry_clean'].map(lambda x: remove_stopwords(x,return_str=False)) #list-like 



# =============================================================================
# # map potentially similar industries by check frequency of words mapped 
# def unique_list(list1):     
#     # insert the list to the set 
#     list_set = set(list1) 
#     # convert the set to the list 
#     unique_list = (list(list_set)) 
#     return unique_list
# 
# group = {}
# for value in original:
#     group[value] = {}
#     s = set(value.split(' '))
#     for i in range(len(check_list)): 
#         common = len(s.intersection(check_list[i]))
#         if common > 0: 
#             group[value][i] = common
#             
#     unq = unique_list(group[value].values()) #if multi matches, get the 'most' similar value
#     if len(unq) > 1: 
#         maxi = max(unq)
#         group[value] = [list(group[value].keys())[list(group[value].values()).index(maxi)]]
#     else: 
#         group[value] = list(group[value].keys())
#         
# 
# new_group = group.copy()
# for k,v in new_group.items():
#     new_group[k] = list(map(lambda x:ind['Industry_clean'][x],v))
# 
# pd.DataFrame({'original':list(new_group.keys()),'industry':list(new_group.values())}).to_csv('industry_v2.csv',index=False)
# #manually map multi-matched industry
# =============================================================================


result = pd.read_csv('industry_v2.csv',converters={"industry": ast.literal_eval})

final = []
for row in range(result.shape[0]):
    if len(result.industry[row]) == 0:
        final.append('Others')
    else: 
        index = result['true_industry'][row]
        final.append(result.industry[row][index])

result['final_industry'] = final 

# Industry --> Industry clean 
ref = pd.Series(ind.set_index('Industry_clean')['Industry']).to_dict()
result['key_industry'] = result['final_industry'].map(ref)
result['key_industry'].fillna('Others',inplace=True)

industry_map = pd.Series(result.set_index('original')['key_industry']).to_dict()

data['industry_v2'] = data['industry_v2'].map(lambda x: x if x is np.nan else list(map(lambda i: industry_map[i],x)))

#read new dataset
data.to_csv('dsjob_wrangle.csv',index=False)
