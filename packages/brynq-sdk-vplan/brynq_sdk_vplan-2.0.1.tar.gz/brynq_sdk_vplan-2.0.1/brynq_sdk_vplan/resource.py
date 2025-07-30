import requests
from typing import Union, List
import warnings
import json
from .get_data import GetData


class Resource:
    def __init__(self, vplan):
        """
        Initialize the GetData class.
        Args: vplan: contains the vplan object with the headers and base_url
        """
        self.vplan = vplan
        self.get_data = GetData(vplan)

    def get_resource_list(self, filter: str = None, show: str = None, hide: str = None, archived: bool = False):
        """
        Get all the resources from vPlan: https://developer.vplan.com/documentation/#tag/Resource/paths/~1resource/get.
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
        df = self.get_data.get_data(endpoint='resource', filter=filter, show=show, hide=hide, archived=archived)
        return df

    def post_resource(self, data: dict) -> requests.Response:
        """
        Create a new resource in vPlan: https://developer.vplan.com/documentation/#tag/Resource/paths/~1resource/post

        This method constructs a request URL based on the endpoint and sends a POST request
        to the vPlan API with the provided data.

        Args:   endpoint (str): The name of the endpoint to create a new resource in.
                data (dict): The data to create the new resource with.

        Returns: requests.Response: The response from the vPlan API.
        """
        required_fields = ['name']
        allowed_fields = ['type', 'start_date', 'workdays', 'description', 'end_date', 'integration_schedule', 'avatar', 'color_hex', 'external_ref', 'archive']
        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = f"{self.vplan.base_url}resource"

        base_body = {
            "name": data['name']
        }
        # Add fields that you want to update a dict (adding to body itself is too much text)
        base_body.update({"type": data['type']}) if 'type' in data else base_body
        base_body.update({"start_date": data['start_date']}) if 'start_date' in data else base_body
        base_body.update({"workdays": eval(data['workdays'])}) if 'workdays' in data else base_body
        base_body.update({"description": data['description']}) if 'description' in data else base_body
        base_body.update({"end_date": data['end_date']}) if 'end_date' in data else base_body
        base_body.update({"integration_schedule": data['integration_schedule']}) if 'integration_schedule' in data else base_body
        base_body.update({"avatar": data['avatar']}) if 'avatar' in data else base_body
        base_body.update({"color_hex": data['color_hex']}) if 'color_hex' in data else base_body
        base_body.update({"external_ref": data['external_ref']}) if 'external_ref' in data else base_body
        base_body.update({"archive": data['archive']}) if 'archive' in data else base_body

        response = requests.request('POST', url, headers=self.vplan.post_headers, data=json.dumps(base_body), timeout=self.vplan.timeout)
        return response

    def update_resource(self, resource_id: str, data: dict) -> requests.Response:
        """
        Update an existing resource in vPlan: https://developer.vplan.com/documentation/#tag/Resource/paths/~1resource/put

        This method constructs a request URL based on the endpoint and sends a POST request
        to the vPlan API with the provided data.

        Args:   endpoint (str): The name of the endpoint to create a new resource in.
                data (dict): The data to create the new resource with.

        Returns: requests.Response: The response from the vPlan API.
        """
        required_fields = []
        allowed_fields = ['name', 'type', 'start_date', 'workdays', 'description', 'end_date', 'integration_schedule', 'avatar', 'color_hex', 'external_ref', 'archive']
        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = f"{self.vplan.base_url}resource/{resource_id}"

        base_body = {}

        # Add fields that you want to update a dict (adding to body itself is too much text)
        base_body.update({"name": data['name']}) if 'name' in data else base_body
        base_body.update({"type": data['type']}) if 'type' in data else base_body
        base_body.update({"start_date": data['start_date']}) if 'start_date' in data else base_body
        base_body.update({"workdays": eval(data['workdays'])}) if 'workdays' in data else base_body
        base_body.update({"description": data['description']}) if 'description' in data else base_body
        base_body.update({"end_date": data['end_date']}) if 'end_date' in data else base_body
        base_body.update({"integration_schedule": data['integration_schedule']}) if 'integration_schedule' in data else base_body
        base_body.update({"avatar": data['avatar']}) if 'avatar' in data else base_body
        base_body.update({"color_hex": data['color_hex']}) if 'color_hex' in data else base_body
        base_body.update({"external_ref": data['external_ref']}) if 'external_ref' in data else base_body
        base_body.update({"archive": data['archive']}) if 'archive' in data else base_body

        response = requests.request('PUT', url, headers=self.vplan.post_headers, data=json.dumps(base_body), timeout=self.vplan.timeout)
        return response

    def delete_resource(self, resource_id):
        """
        Delete an existing resource in vPlan: https://developer.vplan.com/documentation/#tag/Resource/paths/~1resource~1%7Bresource_id%7D/delete
        This method constructs a request URL based on the endpoint and sends a DELETE request to the vPlan API.
        """
        url = f"{self.vplan.base_url}resource/{resource_id}"
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