#!/usr/bin/env python
# coding: utf-8

# In[1]:


### 
#   CREATED BY THOMAS TO
#   JULY 27, 2020
#   THE PURPOSE OF THIS SCRIPT WAS TO ACCESS THE CANVAS DISCUSSION RESPONSES THROUGH A (BACKDOOR) API 
#   THAT UTILIZES JSON IN ORDER TO SEARCH FOR THE KEYWORDS: "ENGINEER" AND "COMPUTER" FOR THOSE MAJORING IN
#   THE RELEVANT FIELDS OF ENGINEERING AND COMPUTER SCIENCE (& ENGINEERING) TO SEND A GREETING EMAIL
#
###

### Ref:
# https://stackoverflow.com/questions/16129652/accessing-json-elements
# https://jsonlint.com/
# backdoorUrl = https://canvas.{INSTITUTION}.edu/api/v1/courses/{COURSENUMBER}/discussion_topics/{DISCUSSIONNUMBER}/view?include_new_entries=1&include_enrollment_state=1
# Purposefully removed actual discussion link to preserve data security 
# Remove while(1); then pass through jsonlint for formatting; nice GUI too
###

### Workflow
#   1. sort messages and keep track of user_id in messages (working backwords)
#   1.1 store in [[],[]], search through for key words then use boolean to make true/false sorting
#   2. in the "participants" key word, match the "user_id" to "id" value (in participants) and get their name "display_name"
#   3. From their name, open the grades worksheet and cross reference with email
#   4. Then send email 
###

import urllib, json, numpy as np
storemessages = [[],[]] #userid, message
isEngineer = []

with open("canvasDiscussion.txt") as canvas: #.txt obtained from backdoorUrl
    data = json.loads(canvas.read())
    
for i in range(len(data["participants"])):
    storemessages[0].append(data["view"][i]["user_id"])
    storemessages[1].append(str.upper(data["view"][i]["message"])) # Make all caps to search keywords easier
    if ("ENGINEER" in storemessages[1][i]) | ("COMPUTER" in storemessages[1][i]): # Creates true/false list to sort
        isEngineer.append(True)
    else:
        isEngineer.append(False)

# Cheeky way of implementing boolean sorting
userID = np.array(isEngineer) * np.array(storemessages[0])
userID = userID[userID > 0].tolist()

userInfoIndex = []
names = []
for i in range(len(data["participants"])): # for each participant id, check if in valid userID
    for j in range(len(userID)):
        if data["participants"][i]["id"] == userID[j]:
            names.append(data["participants"][i]["display_name"])

#userInfoIndex
names # im going to trust that all the names are here, I checekd a few and it seemed to work


# In[3]:


storemessages[1].append(str.upper(data["view"][i]["message"])) # Make all caps to search keywords easier
if ("ENGINEER" in storemessages[1][i]) | ("COMPUTER" in storemessages[1][i]): # Creates true/false list to sort
    isEngineer.append(True)
else:
    isEngineer.append(False)

# Cheeky way of implementing boolean sorting
userID = np.array(isEngineer) * np.array(storemessages[0])
userID = userID[userID > 0].tolist()

userInfoIndex = []
names = []
for i in range(len(data["participants"])): # for each participant id, check if in valid userID
for j in range(len(userID)):
    if data["participants"][i]["id"] == userID[j]:
        names.append(data["participants"][i]["display_name"])

#userInfoIndex
names # im going to trust that all the names are here, I checekd a few and it seemed to work


# In[ ]:


# Accounts for First, Last vs. Last, First mishap
def containsAll(str, set):
    """ Check whether sequence str contains ALL of the items in set. """
    return 0 not in [c in str for c in set]


# In[ ]:


import pandas as pd
contactInfo = pd.DataFrame(pd.read_csv("Aug4ATSWContantInfo.csv", usecols=["Student","SIS Login ID"]))
contactInfo = contactInfo.replace(',','',regex=True) # Removes commas in Last, First names for use in containsAll
attendeeName = contactInfo["Student"].tolist()
attendeeEmail = contactInfo["SIS Login ID"].tolist()

getEmailIndex = []
for j in range(len(names)):
    for i in range(len(attendeeName)):
        if containsAll(names[j],attendeeName[i]):
            getEmailIndex.append(i)

            getEmail = []
for i in range(len(attendeeEmail)):# Go through email list, if i == getEmailIndex, append email
    if i in getEmailIndex:
        getEmail.append(attendeeEmail[i])
        
for i in range(len(getEmail)): # print so I can just copy and paste into gmail email
    print(getEmail[i]+',')


# In[ ]:




