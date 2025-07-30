[![Downloads](https://pepy.tech/badge/veevatools)](https://pepy.tech/project/veevatools)

# Introduction

This python package is a set of Salesforce.com, Veeva Network, Veeva Vault, and Veeva Nitro libraries, scripts, and functions used to help expedite the development of Veeva Tools.
<br/>
<br/>

# Installation / Requirements

Ensure you have **at least Python version 3.10** installed.
To Check your installation version, type the following commands in the terminal (MacOs) / command prompt (Windows):
```
python --version
```
To install python, go to https://www.python.org/ then navigate to the download page of your Operating System.

![Screenshot 2022-06-24 140724](https://user-images.githubusercontent.com/59848012/175649491-0eafdef7-acd2-4631-85cb-f9dee8630b04.png)

You will need to have Packager Installer for Python (pip) installed. To install pip, run the following command in the terminal (MacOs) / command prompt (Windows):

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```
To install the Veeva Tools library:

```
pip install veevatools
```
To upgrade to the latest version of Veeva Tools library:
```
pip install veevatools --upgrade
```

# Overview

The Veeva Tools package currently contains 3 major components:
## Salesforce library

### Authentication:

```python
from salesforce import Sf
from pandas import pd
sf = Sf()
sf.authenticate(
    sfUsername='yourname@salesforce.com',
    sfPassword='password123',
    sfOrgId='00D2C0000008jIK',
    isSandbox= false
    )
```
> Sidenote on Pandas DataFrames: <br/>
Pandas DataFrame (pd) is used to prepare the data for import (i.e. create, update methods) and additional export methods such as pd.to_excel() in order to save the output into an Excel file.<br/>
Additionally, Complex data manipuation (joins, merges, groupbys, filters)and data analytics (describe, statistical analysis) can all be performed using Pandas. <br />
To learn more about Pandas DataFrames, go to the [Pandas documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
<br \>
> Or just Google tutorials on Pandas DataFrames. 
[This YouTube playlist by Corey Schafer](https://www.youtube.com/watch?v=ZyhVh-qRZPA&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&ab_channel=CoreySchafer)
provides an excellent starting point into the world of Pandas!

<br/>

### Data methods:
The salesforce class (Sf) contains methods that can help you interact with data and metadata components:
<br/>
#### **Query**

```python
account_recordtypes = sf.query("SELECT Id, Name, SobjectType from RecordType WHERE SobjectType = 'Account'")]

account_recordtypes
```

`Return -> pd.DataFrame():`
|    |                 Id |                      Name | SobjectType |
|---:|-------------------:|--------------------------:|------------:|
|  0 | 012f4000001ArT3AAK |          Professional_vod |     Account |
|  1 | 012f4000001ArT4AAK |           Institution_vod |     Account |
|  2 | 012f4000001ArT5AAK |                   MCO_vod |     Account |
|  3 | 012f4000001ArT6AAK |          Organization_vod |     Account |
|  4 | 012f4000001ArWzAAK |              Hospital_vod |     Account |

> Sidenote: <br />
You can use any Pandas (pd) methods on the return value of the query output. For example <br/>```account_recordtypes.to_excel("Account RecordTypes.xlsx")``` <br/>
Will save the results of the DataFrame into an Excel file.

<br/>

### **Create**
```python
## Takes a DataFrame of CRM records and creates records in CRM

account_records = pd.DataFrame([{'FirstName': 'Test', 'LastName': 'Account'}, {'FirstName': 'Test2', 'LastName': 'Account2'}])

result = sf.create('Account', account_records)

result
```
`Return -> pd.DataFrame():`
|   | success | created |                 Id |
|--:|--------:|--------:|-------------------:|
| 0 |    True |    True | 0010r00000tF7L1AAK |
| 1 |    True |    True | 0010r00000tF7L2AAK |

<br/>

### Update
```python
### Takes a dataframe that contains at least the Id column
### and any other column to be updated, for example, FirstName
update_account_name = pd.DataFrame(
    [{'FirstName': 'Updated', 'Id': '0010r00000tF7L1AAK'},
     {'FirstName': 'Name', 'Id': '0010r00000tF7L2AAK'}]
    )

result = sf.update('Account', update_account_name)

result
```
`Return -> pd.DataFrame()`
|   | success | created |                 Id |
|--:|--------:|--------:|-------------------:|
| 0 |    True |   False | 0010r00000tF7L1AAK |
| 1 |    True |   False | 0010r00000tF7L2AAK |
<br/>

### Upsert
```python
### Takes a dataframe that contains an external ID column
### and any other column to be updated, for example, Name
### if the external ID matches an existing record,
### the account is updated, otherwise, a new record is created

upsert_account = pd.DataFrame(
    [{'NET_External_Id__c': '242977178138969088', 'Name': 'Updated Hospital Name'},
     {'NET_External_Id__c': '555579769212255555', 'Name': 'Create New Hospital'}]
    )

result = sf.upsert(object_api='Account', external_id_field_api='NET_External_Id__c', record_dataframe=upsert_account)

result
```
`Return -> pd.DataFrame()`
|   | success | created |                 id |
|--:|--------:|--------:|-------------------:|
| 0 |    True |   False | 001f400000PKOrwAAH |
| 1 |    True |    True | 0010r00000tF7stAAC |

<br/>

### Delete
```python
### Takes a dataframe that contains the Id column
### deletes records listed based on their SFID.

delete_account = pd.DataFrame([{'Id': '0010r00000tF7stAAC'}, {'Id': '001f400000PKOrwAAH'}])

result = sf.delete(object_api='Account', record_dataframe=delete_account)

result
```
`Return -> pd.DataFrame()`

|   | success | created |                 Id |
|--:|--------:|--------:|-------------------:|
| 0 |    True |   False | 0010r00000tF7stAAC |
| 1 |    True |   False | 001f400000PKOrwAAH |

<br/>

### Read Metadata
```python
###

```
<br/>

### Create Metadata
```python
###

```
<br/>

### Update Metadata
```python
###

```
<br/>

### Rename Metadata
```python
###

```
<br/>

### Delete Metadata
```python
###

```
<br/>

### List MetaData
```python
###

```
