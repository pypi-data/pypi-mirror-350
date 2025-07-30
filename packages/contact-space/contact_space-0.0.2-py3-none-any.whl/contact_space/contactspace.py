import requests as reqs
import time
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import math
from contact_space.checks import Checks

class ContactSpace():

    # ContactSpace API Rules
    # 1,000,000 calls per month
    # Maximum of 50 requests per second
    # Maximum of 1 poll per minute

    def __init__(self, key : str, url : str = "https://ukapithunder.makecontact.space/") -> None:
        """Initialise ContactSpace instance.

        Args:
            key (str) : the apikey to access ContactSpace
            url (str) : the base url for the api, defaults to the UK url
        
        Returns:
            None
        """
        Checks._type_check(ContactSpace.__init__, locals())
        self.auth = {"x-api-key" : key,
                     "Accept" : "application/json"
                    }
        self.base_url = url
        self.timeout = 10
        self.call_limit = 50 # 50 Requests per second limit
        self.call_time = 1.5
        Checks._auth_check(self.auth, self.base_url, self.timeout)

    def create_call_api(self, func : str, params : list = [{}]) -> dict:
        """Call provided endpoint with provided parameters

        Endpoints that are supported:
            - CreateDataSet
            - InsertRecord
            - InsertNextRecord
            - InsertRecordWithCallback
        Args:
            func (str) : the endpoint of the API to call
            params (list) : a list of dictionaries of the parameters to be passed to the call

        Returns:
            dictionary of the returned json
            {"response" : response_data,
             "count" : expected_count,
             "returned_count" : returned_count,
             "errors" : identified_errors}
        
        """
        Checks._type_check(ContactSpace.create_call_api, locals())
        session = reqs.Session()
        successes = []
        errors = []

        url = self.base_url + func
        header = self.auth.copy()

        total_count = len(params)
        
        response = session.post(url, headers=header, params=params[0], timeout=self.timeout).json()
        if response is None:
            return {"No Data" : {func : params}}
        elif "error" in response:
            return response
        elif total_count == 1:
            return {"response" : response.get("info"),
                    "count" : 1,
                    "returned_count" : 1,
                    "errors" : []}
        successes.extend([response.get("info")])

        params.pop(0)

        def _handle_calls(param : dict) -> dict:
            """Handle batching multiple callids

            Args:
                param (dict) : the params to pass to request

            Returns:
                the records key value pair from the json
            """
            Checks._type_check(_handle_calls, locals())
            local_params = param.copy()
            res = session.post(url, headers=header, params=param).json()
            responses = res.get("info", {"Error" : 
                                        f"{str(local_params)} - {str(res)}"})
            return responses

        rate = self.call_limit

        for i in range(0, len(params)+1, rate):
            batch = params[i:i + rate]
            with ThreadPoolExecutor() as executor:
                results = list(executor.map(_handle_calls, batch))
                successes.extend([response for response in results if "Error" not in response])
                errors.extend([response for response in results if "Error" in response])
                time.sleep(self.call_time)
        return {"response" : successes,
                "count" : total_count,
                "returned_count" : len(successes),
                "errors" : errors}

    def get_call_api(self, func : str, params : dict = {}) -> dict:
        """Call provided endpoint with provided parameters

        Endpoints that are supported:
            - GetUsers
            - GetAgentStatus
            - GetInitiatives
            - GetOutcome
            - GetData
            - GetDataWithAgent
            - GetCallIDs

        Args:
            func (str) : the endpoint of the API to call
            params (dict) : the parameters to be passed to the call

        Returns:
            dictionary of the returned json
            {"response" : response_data,
             "count" : expected_count,
             "returned_count" : returned_count,
             "errors" : identified_errors}
        """
        Checks._type_check(ContactSpace.get_call_api, locals())
        session = reqs.Session()

        url = self.base_url + func
        header = self.auth.copy()
        
        # Initial call to obtain the first page
        response = session.post(url, headers=header, params=params, timeout=self.timeout).json()
        if response is None:
            return {"No Data" : {func : params}}
        elif "error" in response:
            return response
        
        # key after info is returned data but different key values
        data_key = next(k for k in response if k != "info")
        all_data = response.get(data_key, [])

        # obtaining counts for handling pagination
        page_count = int(response.get("info", {}).get("per_page", 1))
        total_count = int(response.get("info", {}).get("count", 1))
        data_left = total_count-page_count 
        more_records = response.get("info", {}).get("more_records", 0)

        # exit if only 1 page
        if int(more_records) == 0:
            return {"response" : all_data,
                    "count" : total_count,
                    "returned_count" : len(all_data)}
        
        # data_left will be the total data - returned date (from first call)
        # total_pages is data_left / page_count rounded up
        # +2 as is used as a range 
        # i.e. if 200 records are returned
        # 631 records in total
        # 431 records remain
        # math.ceil(431/200) = 3 more pages (4 pages in total)
        # start loop on page 2, so need to end on page 5 to get page 4
        # 5 = 3 + 2

        total_pages = math.ceil(data_left/page_count)
        total_pages += 2
        
        def _handle_pagination(page_num : int) -> dict:
            """Handle pagination in response data
            
                Args:
                    page_num (int) : the page to call next

                Returns:
                    dictionary of the returned json
                    {"response" : response_data,
                    "count" : expected_count,
                    "returned_count" : returned_count,
                    "errors" : identified_errors}
            """
            Checks._type_check(_handle_pagination, locals())
            local_params = params.copy()
            local_params["page"] = str(page_num)
            res = session.post(url, headers=header, params=local_params).json()
            
            return res.get(data_key, {"Error" : res, "params" : local_params})
            
        
        def _batches(start : int, end : int, batch_size : int) -> list:
            """Process provided pages into batches

            Args: 
                start (int) : the first page
                end (int) : the last page
                batch_size : the maximum size of the batches

            Returns:
                a list of ranges starting at the start and going to the end,
                either in batch_size steps or where the difference between
                start and end is less, just the start to end
            """
            if end > batch_size:
                return [range(x, min(x + batch_size, end)) for x in range(start, end, batch_size)]
            else:
                return [range(start, end)]
        
        successes = []
        errors = []

        batch_params = {"start" : 2,
                        "end" : total_pages,
                        "batch_size" : self.call_limit
                        }
        batches = _batches(**batch_params)

        for batch in batches:
            with ThreadPoolExecutor() as executor:
                results = list(executor.map(lambda page: _handle_pagination(page), batch))
                successes.extend([response for response in results if "Error" not in response])
                errors.extend([response for response in results if "Error" in response])
                time.sleep(self.call_time)
        for page_data in successes:
            all_data.extend(page_data)

        return {"response" : all_data,
                "count" : total_count,
                "returned_count" : len(all_data),
                "errors" : errors}

    def get_users(self) -> dict:
        """Get users information
        
        Returns:
            a dictionary of the returned json
            {"response" : response_data,
             "count" : expected_count,
             "returned_count" : returned_count,
             "errors" : identified_errors}
        """
        func = "GetUsers"
        return self.get_call_api(func=func)

    def get_user_status(self, user_id : int) -> dict:
        """Get users logged on status

        Args:
            user_id (int) : the id of the user

        Returns:
            a dictionary of the returned json
            {"response" : response_data,
             "count" : expected_count,
             "returned_count" : returned_count,
             "errors" : identified_errors}
        """
        Checks._type_check(ContactSpace.get_user_status, locals())
        try:
            kwargs = {"func" : "GetAgentStatus",
                    "params" : {"userid" : int(user_id)}
                    }
        except TypeError:
            raise
        return self.get_call_api(**kwargs)


    def get_initiatives(self) -> dict:
        """Get initiative information

        Returns:
            a dictionary of the returned json
        """
        func = "GetInitiatives"
        return self.get_call_api(func=func)

    def get_outcomes(self, initiative_id : int) -> dict:
        """Get outcome information for an initiative

        Args:
            initiative_id (int) : the id of the initiative

        Returns:
            a dictionary of the returned json
            {"response" : response_data,
             "count" : expected_count,
             "returned_count" : returned_count,
             "errors" : identified_errors}
        
        """
        Checks._type_check(ContactSpace.get_outcomes, locals())
        try:
            kwargs = {"func" : "GetOutcome",
                    "params" : {"module" : "data",
                                "initiativeid" : int(initiative_id)}
                    }
        except TypeError:
            raise
        return self.get_call_api(**kwargs)


    def get_data(self, fromdate : str, todate : str, initiative_id : int, with_agent : bool = False) -> dict:
        """ Get data from an initiative across a period of time

        Args:
            fromdate (str) : date to start from (inclusive),
                             date must be in "%Y-%m-%d" or "%Y-%m-%d %H:%M:%S" format
            todate (str) : date to end at (inclusive),
                           date must be in "%Y-%m-%d" or "%Y-%m-%d %H:%M:%S" format
            initiative_id (int) : the id of the initiative
            with_agent (bool) : whether to include info on the agent who called, defaults to False

        Returns:
            a dictionary of the returned json
            {"response" : response_data,
             "count" : expected_count,
             "returned_count" : returned_count,
             "errors" : identified_errors}
        
        """
        Checks._type_check(ContactSpace.get_data, locals())
        func = "GetData"
        if with_agent:
            func = "GetDataWithAgent"
        
        Checks._date_format_check(fromdate)
        Checks._date_format_check(todate)
        Checks._date_order_check(str(fromdate), str(todate))
        try:
            kwargs = {"func" : func,
                      "params" : {"module" : "data",
                                  "moduleid" : int(initiative_id),
                                  "fromdate" : str(fromdate),
                                  "todate" : str(todate)
                                  }
            }
        except TypeError:
            raise
        return self.get_call_api(**kwargs)

    def create_datasets(self, names : list, initiative_ids : list, status : int = 0) -> dict:
        """Create datasets to upload data into

        Args: 
            names (list) : a list of dataset names,
                           must be same size as initiative_ids
            initiative_ids (list) : a list of initiative ids to upload to,
                                    must be same size as names
            status (int) : the status of the created dataset,
                            0 = inactive, 1 = active
        
        Returns:
            a dictionary of the returned json
            {"response" : response_data,
             "count" : expected_count,
             "returned_count" : returned_count,
             "errors" : identified_errors}

        """
        Checks._type_check(ContactSpace.create_datasets, locals())
        Checks._equal_check(names, initiative_ids)
        if int(status) not in [0, 1]:
            raise ValueError(f"Unsupported status param (must be either 0 or 1): {status}")
        params = [{"initiativeid" : int(initiative_ids[index]),
                    "datasetname" : str(names[index]),
                    "status" : int(status)} for index in range(0, len(names))]
        func = "CreateDataSet"
        return self.create_call_api(func=func, params=params)

    def create_records(self, data : pd.DataFrame, datasetid : str, userid : str = "", callback : str = "") -> dict:
        """Uploads records into a dataset

        Args: 
            data (pd.DataFrame) : a pandas df of data to be uploaded,
                                  the column names must be equal to the field names on ContactSpace
            datasetid (str) : the datasetid to upload to
            userid (str) : the userid to assign the data to
            callback (str) : date to return the record to the agent at,
                             date must be in "%Y-%m-%d" or "%Y-%m-%d %H:%M:%S" format
        
        Returns:
            a dictionary of the returned json
            {"response" : response_data,
             "count" : expected_count,
             "returned_count" : returned_count,
             "errors" : identified_errors}

        """
        Checks._type_check(ContactSpace.create_records, locals())
        func = "InsertRecord"
        if bool(userid):
            func = "InsertNextRecord"
        if bool(callback) and bool(userid):
            func = "InsertRecordWithCallback"
            Checks._date_format_check(callback)
                
        records = data.to_dict(orient='records')

        try:
            json_list = [{"datasetid" : str(datasetid),
                          "jsondata" : json.dumps(record),
                          **({"userid":  str(userid)} if bool(userid) else {}),
                          **({"callbackdatetime":  str(callback)} if bool(callback) else {})
                         } for record in records]
        except (TypeError, ValueError) as ex:
            raise("Invalid JSON:", ex)

        return self.create_call_api(func=func, params=json_list)

    def get_callids(self, fromdate : str, todate : str, initiativeid : int = 0, predictive : int = 0) -> dict:
        """Get call ids across a period

        Args:
            fromdate (str) : date to start from (inclusive),
                             date must be in "%Y-%m-%d" or "%Y-%m-%d %H:%M:%S" format
            todate (str) : date to end at (inclusive),
                           date must be in "%Y-%m-%d" or "%Y-%m-%d %H:%M:%S" format
            initiative_id (int) : the id of the initiative, defaults to 0 (all initiatives)
            predictive (int) : whether to include manually added call ids, 0 : no, 1 : yes, defaults to 0

        Returns:
            a dictionary of the returned json
            {"response" : response_data,
             "count" : expected_count,
             "returned_count" : returned_count,
             "errors" : identified_errors}
        
        """
        Checks._type_check(ContactSpace.get_callids, locals())
        if predictive not in [0, 1]:
            raise ValueError(f"Unsupported predictive param (must be either 0 or 1): {predictive}")
        Checks._date_format_check(fromdate)
        Checks._date_format_check(todate)
        Checks._date_order_check(str(fromdate), str(todate))
        try:
            kwargs = {
                "func" : "GetCallIDs",
                "params" : {
                        "initiativeid" : int(initiativeid),
                        "fromdate" : str(fromdate),
                        "todate" : str(todate),
                        "predictive" : int(predictive)
                    }
            }
        except TypeError:
                raise
        return self.get_call_api(**kwargs)

    def get_records_from_callids(self, callids : list) -> dict:
        """Get record data from call ids

        Args:
            callids (list) : a list of callids
        
        Returns:
            a dictionary of the returned data
            {"response" : response_data,
             "count" : expected_count,
             "returned_count" : returned_count,
             "errors" : identified_errors}
        
        """
        Checks._type_check(ContactSpace.get_records_from_callids, locals())

        if len(callids) == 0:
            raise IndexError("Length of callid list must be greater than 0")
        elif not isinstance(callids, list):
            raise TypeError("callids must be in a list")

        session = reqs.Session()
        url = self.base_url + "GetRecord"
        header = self.auth
        params = {"callid" : "",
                  "module" : "data"}
        total_count = len(callids)

        def _handle_multiplerecords(callid : int) -> dict:
            """Handle batching multiple callids

            Args:
                callid (int) : the call id to request

            Returns:
                the records key value pair from the json
            """
            Checks._type_check(_handle_multiplerecords, locals())
            params["callid"] = str(callid)
            res = session.post(url, headers=header, params=params).json()
            records = res.get("records", {"Error" : str(callid)})
            return records

        rate = self.call_limit
        successes = []
        errors = []

        for i in range(0, len(callids)+1, rate):
            batch = callids[i:i + rate]
            with ThreadPoolExecutor() as executor:
                results = list(executor.map(_handle_multiplerecords, batch))
                successes.extend([response for response in results if "Error" not in response])
                errors.extend([response for response in results if "Error" in response])
                time.sleep(self.call_time)
        return {"response" : successes,
                "count" : total_count,
                "returned_count" : len(successes),
                "errors" : errors}

    def get_records(self, fromdate : str, todate : str, initiativeid : int = 0) -> dict:
        """Get record information across a period

        Args:
            fromdate (str) : date to start from (inclusive), 
                             date must be in "%Y-%m-%d" or "%Y-%m-%d %H:%M:%S" format
            todate (str) : date to end at (inclusive), 
                           date must be in "%Y-%m-%d" or "%Y-%m-%d %H:%M:%S" format
            initiative_id (int) : the id of the initiative, defaults to 0 (all initiatives)

        Returns:
            a dictionary of the returned json
            {"response" : response_data,
             "count" : expected_count,
             "returned_count" : returned_count,
             "errors" : identified_errors}
        """
        Checks._type_check(ContactSpace.get_records, locals())
        no_pred_ids = self.get_callids(fromdate, todate, predictive=0).get("response")
        pred_ids = self.get_callids(fromdate, todate, predictive=1).get("response")
        list_predictive = [rep_dict.get("Id") for rep_dict in no_pred_ids if "Id" in rep_dict]
        list_non_predictive = [rep_dict.get("Id") for rep_dict in pred_ids if "Id" in rep_dict]
        list_predictive.extend(list_non_predictive)
        all_ids = list(set(list_predictive))

        return self.get_records_from_callids(all_ids)