#!/usr/bin/env python
# coding: utf-8

# In[1]:


print("Import Libs...")

import pandas as pd
import numpy as np
import random
import re
import copy


# In[2]:


def SelectTitle(selectedTag):
    title = []
    for i in range(len(titleDf.columns)):
        title.append(SelectRandomItemFromDataframeColumn('titleDf', titleDf.iloc[:, [i]], selectedTag))
    title = ' '.join([str(strElement) for strElement in title])
    return title
    
    
def SelectContext(selectedTag):
    Context = []
    for i in range(len(ContextDf.columns)):
        Context.append(SelectRandomItemFromDataframeColumn('ContextDf', ContextDf.iloc[:, [i]], selectedTag))
    Context = ' '.join([str(strElement) for strElement in Context])
    Context = Context.replace("{NEWLINE}", "\n")
    Context = Context.replace(".0", "") # Change float-string to int-string  -> for example 28.0 to 28
    return Context
    
    
def SelectKeyWord(selectedTag):
    Keywords = []
    for i in range(len(KeywordDf.columns)):
        Keywords.append(SelectRandomItemFromDataframeColumn('KeywordDf', KeywordDf.iloc[:, [i]], selectedTag))
    Keywords = ' '.join([str(strElement) for strElement in Keywords])
    return Keywords


# In[3]:


def IsConstraintcolumn(inputDataColumn):
    firstStringInColumn = str(inputDataColumn.iloc[1:2].values.tolist()[0][0])
    if(firstStringInColumn.find("{") >=0 and firstStringInColumn != "{NEWLINE}" and firstStringInColumn != "{}"):
        return True
    return False

def FilterInputDataFrameWithSelectedTag(inputDataColumn, selectedTag):
    if(IsConstraintcolumn(inputDataColumn) == True):
        inputDataColumnList = inputDataColumn.values.tolist()

        if(str(inputDataColumnList[0]).find("{MULTISELECT}") >= 0):
            MultiSelectHolder = inputDataColumnList[0][0]
            need_NOTIMPORTANT = False
        else:
            need_NOTIMPORTANT = True
            
        inputDataColumnList = [x for x in inputDataColumnList if str(x).find(selectedTag) > 0]
        
        if(need_NOTIMPORTANT == True):
            inputDataColumnList.insert(0,"[Not important]")
        else:
            inputDataColumnList.insert(0, MultiSelectHolder)
            
        inputDataColumn = pd.DataFrame(inputDataColumnList, columns = inputDataColumn.columns)        
    return inputDataColumn
    
def SelectRandomItemFromDataframeColumn(dataFrameName, inputDataFrame, selectedTag):
    inputDataFrame = FilterInputDataFrameWithSelectedTag(inputDataFrame, selectedTag)
    numOfRecordesInColumn = int(inputDataFrame.count())
    # Determine Min and Max Bounds in MULTISELECT column
    tmpList = inputDataFrame.values.tolist()
    numOfItemsMustBeSelected = 1
    if(str(tmpList[0][0]).find("{MULTISELECT}") >= 0):
        numOfRecordesInColumn -= 1
        minMaxStr = tmpList[0][0].replace("{MULTISELECT}", "")
        minMaxStr = minMaxStr.replace("{", "");
        minMaxStr = minMaxStr.replace("}", "");
        minMaxArr = minMaxStr.split(',')
        minBound = int(minMaxArr[0])
        maxBound = int(minMaxArr[1])
        numOfItemsMustBeSelected = random.randint(minBound, maxBound)

    # Select Items
    allSelectedItems = []
    try:
        randomIndexList = random.sample(range(1, numOfRecordesInColumn), numOfItemsMustBeSelected)
    except Exception as ex:
        print("Error: " + "numOfRecordesInColumn: "+ str(numOfRecordesInColumn) + " - numOfItemsMustBeSelected: " + str(numOfItemsMustBeSelected))
        print(ex)
        print(inputDataFrame)
        
    for i in range(len(randomIndexList)):
        try:
            selectedItem = inputDataFrame.iloc[randomIndexList[i]].values[0]
        except Exception as ex:
            print("Error: " + "numOfRecordesInColumn: "+ str(numOfRecordesInColumn) + " - numOfItemsMustBeSelected: " + str(numOfItemsMustBeSelected))
            print("Error:" + "randomIndexList:" + str(randomIndexList) + " - randomIndexList[i]: " + str(randomIndexList[i]) )
            print(inputDataFrame)
            print(ex)
        allSelectedItems.append(selectedItem)
        
    returnStr = ', '.join([str(strElement) for strElement in allSelectedItems])
    return returnStr


# In[4]:


def CleanTextList(inputList):
    for i in range(len(inputList)):
        inputList[i] = inputList[i].replace("'", "")
        inputList[i] = inputList[i].replace("[", "")
        inputList[i] = inputList[i].replace("]", "")
        inputList[i] = re.sub('{.*?}', '', inputList[i])

    return inputList


# In[5]:


#constraintList = []
def CreateNewPost(numberOfPost):
    allTitle = []
    allContext = []
    allKeyword = []
    for postCounter in range(numberOfPost):
        print("Create Post: " + str(postCounter))
        selectedTag = allCONST[random.randint(0, len(allCONST) - 1)]
        allTitle.append(SelectTitle(selectedTag))
        allContext.append(SelectContext(selectedTag))
        allKeyword.append(SelectKeyWord(selectedTag))
        
    allTitle = CleanTextList(allTitle)
    allContext = CleanTextList(allContext)
    allKeyword = CleanTextList(allKeyword)
    
    df = pd.DataFrame(list(zip(allTitle, allContext, allKeyword)),
           columns =['Title', 'Content', 'Keywords'])
    
    print("Writing to excel...")
    df.to_excel(r'GenerateContent_Output.xlsx', index = False)


# In[6]:


if __name__ == "__main__":
    print("Reading _Template.xlsx...")
    df = pd.read_excel('_Template.xlsx')

    constDf = df
    for col in df.columns:
        if(col.find('CONST') >= 0):
            pass
        else:
            constDf = constDf.drop(col, axis = 1)

    titleDf = df
    for col in df.columns:
        if(col.find('title') >= 0 or col.find('Title') >= 0):
            pass
        else:
            titleDf = titleDf.drop(col, axis = 1)

    ContextDf = df
    for col in df.columns:
        if(col.find('Context') >= 0 or col.find('context') >= 0):
            pass
        else:
            ContextDf = ContextDf.drop(col, axis = 1)

    KeywordDf = df
    for col in df.columns:
        if(col.find('keyword') >= 0 or col.find('Keyword') >= 0):
            pass
        else:
            KeywordDf = KeywordDf.drop(col, axis = 1)

    # Extract all tags from first column
    allCONST = constDf.iloc[:, [0]].values.tolist()
    allCONST = [x[0] for x in allCONST if str(x) != '[nan]']
    selectedTag = allCONST[random.randint(0, len(allCONST) - 1)]

    CreateNewPost(100)
    print("Done!")


# In[ ]:





# In[ ]:




