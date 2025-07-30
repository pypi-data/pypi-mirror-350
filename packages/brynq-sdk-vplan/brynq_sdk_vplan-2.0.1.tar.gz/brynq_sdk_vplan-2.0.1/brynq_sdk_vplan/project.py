import requests
from typing import Union, List
import warnings
import json
from .get_data import GetData


class Project:
    def __init__(self, vplan):
        """
        Initialize the GetData class.
        Args: vplan: contains the vplan object with the headers and base_url
        """
        self.vplan = vplan
        self.get_data = GetData(vplan)

    def get_project_list(self, filter: str = None, show: str = None, hide: str = None):
        """
        Get all the projects from vPlan: https://developer.vplan.com/documentation/#tag/Project/paths/~1project/get
        Args:   filter (str, optional): On the list endpoints it is possible to filter the result set given. To apply a filter use the filter query parameter with the format: field:operator:value
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
        df = self.get_data.get_data(endpoint='project', filter=filter, show=show, hide=hide)
        return df

    def post_project(self, data: dict) -> requests.Response:
        """
        Create a new project in vPlan: https://developer.vplan.com/documentation/#tag/Project/paths/~1project/post

        This method constructs a request URL based on the endpoint and sends a POST request
        to the vPlan API with the provided data.

        Args:   endpoint (str): The name of the endpoint to create a new project in.
                data (dict): The data to create the new project with.

        Returns: requests.Response: The response from the vPlan API.
        """
        required_fields = ['name']
        allowed_fields = ['code', 'description', 'external_ref']
        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = f"{self.vplan.base_url}project"

        base_body = {
            "name": data['name']
        }

        # Add fields that you want to update a dict (adding to body itself is too much text)
        base_body.update({"code": data['code']}) if 'code' in data else base_body
        base_body.update({"description": data['description']}) if 'description' in data else base_body
        base_body.update({"external_ref": data['external_ref']}) if 'external_ref' in data else base_body

        response = requests.request('POST', url, headers=self.vplan.post_headers, data=json.dumps(base_body), timeout=self.vplan.timeout)
        return response

    def update_project(self, project_id: str, data: dict) -> requests.Response:
        """
        Update an existing project in vPlan: https://developer.vplan.com/documentation/#tag/Project/paths/~1project~1%7Bproject_id%7D/put

        This method constructs a request URL based on the endpoint and sends a POST request
        to the vPlan API with the provided data.

        Args:   endpoint (str): The name of the endpoint to create a new project in.
                data (dict): The data to create the new project with.

        Returns: requests.Response: The response from the vPlan API.
        """
        required_fields = ['name']
        allowed_fields = ['code', 'description', 'external_ref']
        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = f"{self.vplan.base_url}project/{project_id}"

        base_body = {
            "name": data['name']
        }
        # Add fields that you want to update a dict (adding to body itself is too much text)
        base_body.update({"code": data['code']}) if 'code' in data else base_body
        base_body.update({"description": data['description']}) if 'description' in data else base_body
        base_body.update({"external_ref": data['external_ref']}) if 'external_ref' in data else base_body

        response = requests.request('PUT', url, headers=self.vplan.post_headers, data=json.dumps(base_body), timeout=self.vplan.timeout)
        return response

    def delete_project(self, project_id):
        """
        Delete an existing project in vPlan: https://developer.vplan.com/documentation/#tag/Project/paths/~1project~1%7Bproject_id%7D/delete
        This method constructs a request URL based on the endpoint and sends a DELETE request to the vPlan API.
        """
        url = f"{self.vplan.base_url}project/{project_id}"
        response = requests.request('DELETE', url, headers=self.vplan.headers, timeout=self.vplan.timeout)
        return response

    @staticmethod
    def __check_fields(data: Union[dict, List], required_fields: List, allowed_fields: List):
        if isinstance(data, dict):
            data = data.keys()

        for field in data:
            if field not in allowed_fields and field not in required_fields:
                warnings.warn('Field {field} is not implemented. Optional fields are: {allowed_fields}'.format(field=field, allowed_fields=tuple(allowed_fields)))

        for field in required_fields:
            if field not in data:
                raise ValueError('Field {field} is required. Required fields are: {required_fields}'.format(field=field, required_fields=tuple(required_fields)))