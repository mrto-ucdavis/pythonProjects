#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as pd
import numpy as np

studentInfo = '2020-08-02T0844_Grades-Aggie_Transfer_Scholars_Week.csv'
mentorMentee = 'Mentor Groups .xlsx'
print('Enter Your Name: ')
name = input()

#Open mentorMentee by name of SOA
#pd.read_excel(mentorMentee)[x+'(SOA)']
# Current version of mentorMentee won't work for Tommy or ALexis,
# Uncomment following code for user to access student information
# pd.read_excel(mentorMentee)['Alexis']
# pd.read_excel(mentorMentee)['Tommy']
mentees = pd.read_excel(mentorMentee)[name + '(SOA)']
mentees = [x for x in mentees if x == x]


# In[42]:


name2ID = pd.read_csv(studentInfo, usecols=['Student','ID'])
name2ID = name2ID.replace(',','',regex=True)
attendeeName = name2ID["Student"].tolist()
attendeeID = name2ID["ID"].tolist()
# Accounts for First, Last vs. Last, First mishap
def containsAll(str, set):
    """ Check whether sequence str contains ALL of the items in set. """
    return 0 not in [c in str for c in set]

getIndex = []
for j in range(len(mentees)):
    for i in range(len(attendeeName)):
        if containsAll(mentees[j],attendeeName[i]):
            getIndex.append(i)

getID = []
for i in range(len(attendeeID)):
    if i in getIndex:
        getID.append(attendeeID[i])

for i in range(len(getID)): # print so I can just copy and paste into gmail email
    print(int(getID[i]))

