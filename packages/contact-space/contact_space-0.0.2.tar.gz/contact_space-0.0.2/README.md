# contact_space

An SDK to interact with the ContactSpace REST API

Documentation of API: https://documenter.getpostman.com/view/14510675/UVJhEabw#ab347a65-d28c-40f8-a0af-22647825318d 

GitHub: https://github.com/georgegburns/contactspace 

# How to install

Installed via pip:

    pip install contact_space


# Features
Handles authorisation check and batches requests to meet API requirements

Example authentication

    from contact_space import ContactSpace
    
    api_key = "EXAMPLE_API_KEY"
    url = "https://ukapithunder.makecontact.space/" # Update to region specific URL
    
    auth = ContactSpace(api_key, url)

Stable methods:

    - .create_call_api() 
        works with endpoints:
            - CreateDataSet
            - InsertRecord
            - InsertNextRecord
            - InsertRecordWithCallback

    - .get_call_api()
        works with endpoints:
            - GetUsers
            - GetAgentStatus
            - GetInitiatives
            - GetOutcome
            - GetData
            - GetDataWithAgent
            - GetCallIDs

    - .get_users()
        returns users and agents

    - .get_user_status()
        returns status of passed userid

    - .get_initiatives()
        returns initiatives

    - .get_outcomes()
        returns outcomes for a passed initiativeid

    - .get_data()
        returns record data across a given period for a provided invitiative, with or without agent

    - .create_datasets()
        creates a series of datasets to be uploaded into

    - .create_records()
        uploads records into a passed datasetid

    - .get_callids()
        gets callids across a given period

    - .get_records_from_callids()
        gets record data from passed callids

    - .get_records()
        gets records across a given period regardless of initiative
    

Upcoming methods:

    - update record/outcome/value

