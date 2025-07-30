import pandas as pd
from typing import List, Any
import requests


class GetData:
    def __init__(self, vplan):
        """
        Initialize the GetData class.
        Args: vplan: contains the vplan object with the headers and base_url
        """
        self.vplan = vplan

    def get_data(self, endpoint: str, limit: int = 1000, filter: str = None, with_array: str = None, show: str = None, hide: str = None, archived: bool = False) -> pd.DataFrame:
        """
        Fetch data from a specified table from vPlan

        This method constructs a request URL based on the table name and optional filter,
        sends a request to the vPlan API, parses the JSON response, and converts it
        to a pandas DataFrame. The DataFrame columns are cleaned to remove unnecessary
        characters and duplicate columns are handled.

        Args:   endpoint (str): The name of the endpoint to fetch data from.
                filter (str, optional): On the list endpoints it is possible to filter the result set given. To apply a filter use the filter query parameter with the format: field:operator:value
                                        Example: ?filter=created_at:gt:2020-09-26,and,(id:not:starts_with:0000,or,id:contains:FFFF)

                                        Colon : is the separator between the field, operator(s) and value.
                                        Comma , can be used to combine filter statements by using ,and, or ,or,.
                                        Braces (...) can be used to group filter statements.

                                        The following operators are supported

                                        operator	description
                                        eq	        equal to the given value
                                        gt	        greater than the given value
                                        gte	        greater than or equal to the given value
                                        lt	        lesser than the given value
                                        lte	        lesser than or equal to the given value
                                        not	        negation of the operator that follows it
                                        contains	has occurrence of the given value
                                        starts_with	starts with the given value
                                        end_with	ends with the given value

                                        warning: Currently the comma , and colon : are not supported within the filter value

                show (str, optional): On the list endpoints it is possible to select the fields that should be returned. To apply a show use the show query parameter with the format: field1,field2,field3
                hide (str, optional): On the list endpoints it is possible to hide the fields that should not be returned. To apply a hide use the hide query parameter with the format: field1,field2,field3

        Returns: pd.DataFrame: The fetched data as a pandas DataFrame.
        """
        # Initial URL with subscription-key
        url = f"{self.vplan.base_url}{endpoint}?"
        if limit:
            url += f'limit={limit}&'
        if filter:
            url += f'filter={filter}&'
        if with_array:
            url += f'with={with_array}&'
        if show:
            url += f'show={show}&'
        if hide:
            url += f'hide={hide}&'
        if archived:
            url += f'archived={archived}&'

        all_data = []
        offset = 0
        received = 0
        while True:
            final_url = f'{url}offset={offset}'
            response = requests.get(url=final_url, headers=self.vplan.headers)
            response.raise_for_status()
            result = response.json()
            data = result.get('data', result)
            all_data.extend(data)

            # Determine if we need to continue fetching data
            count = result.get('count', 0)
            received += len(data)
            offset += limit
            if received >= count:
                break


        df = pd.DataFrame(all_data)
        return df
