import requests
from typing import Union, List, Any
import warnings
import json
from .get_data import GetData


class Leave:
    def __init__(self, vplan):
        """
        Initialize the GetData class.
        Args: vplan: contains the vplan object with the headers and base_url
        """
        self.vplan = vplan
        self.get_data = GetData(vplan)

    def get_leave(self, resource_id: str) -> requests.Response:
        """
        Get leave data for a specific resource.

        Args:
            resource_id (str): The id of the resource to get the leave from.

        Returns:
            requests.Response: The response from the vPlan API containing schedule deviations.
        """
        url = f"{self.vplan.base_url}resource/{resource_id}?with=schedule_deviations"
        response = requests.request('GET', url, headers=self.vplan.headers)
        return response

    def post_leave(self, resource_id: str, data: dict) -> requests.Response:
        """
        There is no documentation for this method available

        This method constructs a request URL based on the endpoint and sends a POST request
        to the vPlan API with the provided data.

        Args:   resource_id (str): The resource id of the employee to add the leave to
                data (dict): The data to create the new order with.

        Returns: requests.Response: The response from the vPlan API.
        """
        required_fields = ['type', 'time', 'description', 'start_date', 'end_date']
        allowed_fields = []
        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = f"{self.vplan.base_url}resource/{resource_id}/schedule_deviation"
        base_body = json.dumps({
            "type": data['type'],
            "time": data['time'],
            "description": data['description'],
            "start_date": data['start_date'],
            "end_date": data['end_date']
        })
        response = requests.request('POST', url, headers=self.vplan.post_headers, data=base_body, timeout=self.vplan.timeout)
        return response

    def update_leave(self, resource_id: str, leave_id: str, data: dict) -> requests.Response:
        """
        There is no documentation for this method available

        This method constructs a request URL based on the endpoint and sends a POST request
        to the vPlan API with the provided data.

        Args:   resource_id (str): The resource id of the employee to add the leave to
                leave_id (str): The id of the leave to update
                data (dict): The data to create the new order with.

        Returns: requests.Response: The response from the vPlan API.
        """
        required_fields = ['type', 'time', 'description', 'start_date', 'end_date']
        allowed_fields = []
        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = f"{self.vplan.base_url}resource/{resource_id}/schedule_deviation/{leave_id}"
        base_body = json.dumps({
            "type": data['type'],
            "time": data['time'],
            "description": data['description'],
            "start_date": data['start_date'],
            "end_date": data['end_date']
        })
        response = requests.request('PUT', url, headers=self.vplan.post_headers, data=base_body, timeout=self.vplan.timeout)
        return response

    def delete_leave(self, resource_id: str, leave_id: str):
        """
        There is no documentation for this method available
        This method constructs a request URL based on the endpoint and sends a DELETE request to the vPlan API.
        :param resource_id: The resource id of the employee to delete the the leave to
        :param leave_id: The id of the leave to delete
        """
        url = f"{self.vplan.base_url}resource/{resource_id}/schedule_deviation/{leave_id}"
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
