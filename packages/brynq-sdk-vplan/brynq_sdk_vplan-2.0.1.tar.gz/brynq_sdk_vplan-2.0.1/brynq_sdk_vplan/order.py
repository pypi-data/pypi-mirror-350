import requests
from typing import Union, List, Any
import warnings
import json
from .get_data import GetData


class Order:
    def __init__(self, vplan):
        """
        Initialize the GetData class.
        Args: vplan: contains the vplan object with the headers and base_url
        """
        self.vplan = vplan
        self.get_data = GetData(vplan)

    def get_order_list(self, filter: str = None, with_array: str = None, show: str = None, hide: str = None):
        """
        Get all the orders from vPlan: https://developer.vplan.com/documentation/#tag/Order/paths/~1order/get
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

                with_array (list, optional): object(s) included in the dataset, Possible options are: address, item, order_rows, collection, project, relation, warehouse, board, contact, user, activity, order, item, project, relation, warehouse, supplies_order_rows
                show (str, optional): On the list endpoints it is possible to select the fields that should be returned. To apply a show use the show query parameter with the format: field1,field2,field3
                hide (str, optional): On the list endpoints it is possible to hide the fields that should not be returned. To apply a hide use the hide query parameter with the format: field1,field2,field3

        Returns: pd.DataFrame: The fetched data as a pandas DataFrame.
        """
        df = self.get_data.get_data(endpoint='order', filter=filter, with_array=with_array, show=show, hide=hide)
        return df

    def post_order(self, data: dict) -> requests.Response:
        """
        Create a new order in vPlan: https://developer.vplan.com/documentation/#tag/order/paths/~1order/post

        This method constructs a request URL based on the endpoint and sends a POST request
        to the vPlan API with the provided data.

        Args:   endpoint (str): The name of the endpoint to create a new order in.
                data (dict): The data to create the new order with.

        Returns: requests.Response: The response from the vPlan API.
        """
        required_fields = ['type', 'code', 'description']
        allowed_fields = ['quantity', 'external_url', 'sub_type', 'status', 'note', 'contact', 'relation_ref', 'date', 'desired_date', 'promised_date',
                          'delivered_date', 'collection_id', 'item_id', 'project_id', 'relation_id', 'warehouse_id', 'external_ref', 'board_id']
        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = f"{self.vplan.base_url}order"

        base_body = {
            "type": data['type'],
            "code": data['code'],
            "description": data['description']
        }
        # Add fields that you want to update a dict (adding to body itself is too much text)
        base_body.update({"quantity": data['quantity']}) if 'quantity' in data else base_body
        base_body.update({"external_url": data['external_url']}) if 'external_url' in data else base_body
        base_body.update({"sub_type": data['sub_type']}) if 'sub_type' in data else base_body
        base_body.update({"status": data['status']}) if 'status' in data else base_body
        base_body.update({"note": data['note']}) if 'note' in data else base_body
        base_body.update({"contact": data['contact']}) if 'contact' in data else base_body
        base_body.update({"relation_ref": data['relation_ref']}) if 'relation_ref' in data else base_body
        base_body.update({"date": data['date']}) if 'date' in data else base_body
        base_body.update({"desired_date": data['desired_date']}) if 'desired_date' in data else base_body
        base_body.update({"promised_date": data['promised_date']}) if 'promised_date' in data else base_body
        base_body.update({"delivered_date": data['delivered_date']}) if 'delivered_date' in data else base_body
        base_body.update({"collection_id": data['collection_id']}) if 'collection_id' in data else base_body
        base_body.update({"item_id": data['item_id']}) if 'item_id' in data else base_body
        base_body.update({"project_id": data['project_id']}) if 'project_id' in data else base_body
        base_body.update({"relation_id": data['relation_id']}) if 'relation_id' in data else base_body
        base_body.update({"warehouse_id": data['warehouse_id']}) if 'warehouse_id' in data else base_body
        base_body.update({"external_ref": data['external_ref']}) if 'external_ref' in data else base_body
        base_body.update({"board_id": data['board_id']}) if 'board_id' in data else base_body

        response = requests.request('POST', url, headers=self.vplan.post_headers, data=json.dumps(base_body), timeout=self.vplan.timeout)
        return response

    def update_order(self, order_id: str, data: dict) -> requests.Response:
        """
        Update an existing order in vPlan: https://developer.vplan.com/documentation/#tag/order/paths/~1order~1%7Border_id%7D/put

        This method constructs a request URL based on the endpoint and sends a POST request
        to the vPlan API with the provided data.

        Args:   endpoint (str): The name of the endpoint to create a new order in.
                data (dict): The data to create the new order with.

        Returns: requests.Response: The response from the vPlan API.
        """
        required_fields = []
        allowed_fields = ['description' 'type', 'code', 'quantity', 'external_url', 'sub_type', 'status', 'note', 'contact', 'relation_ref', 'date', 'desired_date',
                          'promised_date', 'delivered_date', 'collection_id', 'item_id', 'project_id', 'relation_id', 'warehouse_id', 'external_ref', 'board_id']
        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = f"{self.vplan.base_url}order/{order_id}"

        base_body = {
        }
        # Add fields that you want to update a dict (adding to body itself is too much text)
        base_body.update({"code": data['code']}) if 'code' in data else base_body
        base_body.update({"description": data['description']}) if 'description' in data else base_body
        base_body.update({"type": data['type']}) if 'type' in data else base_body
        base_body.update({"quantity": data['quantity']}) if 'quantity' in data else base_body
        base_body.update({"external_url": data['external_url']}) if 'external_url' in data else base_body
        base_body.update({"sub_type": data['sub_type']}) if 'sub_type' in data else base_body
        base_body.update({"status": data['status']}) if 'status' in data else base_body
        base_body.update({"note": data['note']}) if 'note' in data else base_body
        base_body.update({"contact": data['contact']}) if 'contact' in data else base_body
        base_body.update({"relation_ref": data['relation_ref']}) if 'relation_ref' in data else base_body
        base_body.update({"date": data['date']}) if 'date' in data else base_body
        base_body.update({"desired_date": data['desired_date']}) if 'desired_date' in data else base_body
        base_body.update({"promised_date": data['promised_date']}) if 'promised_date' in data else base_body
        base_body.update({"delivered_date": data['delivered_date']}) if 'delivered_date' in data else base_body
        base_body.update({"collection_id": data['collection_id']}) if 'collection_id' in data else base_body
        base_body.update({"item_id": data['item_id']}) if 'item_id' in data else base_body
        base_body.update({"project_id": data['project_id']}) if 'project_id' in data else base_body
        base_body.update({"relation_id": data['relation_id']}) if 'relation_id' in data else base_body
        base_body.update({"warehouse_id": data['warehouse_id']}) if 'warehouse_id' in data else base_body
        base_body.update({"external_ref": data['external_ref']}) if 'external_ref' in data else base_body
        base_body.update({"board_id": data['board_id']}) if 'board_id' in data else base_body

        response = requests.request('PUT', url, headers=self.vplan.post_headers, data=json.dumps(base_body), timeout=self.vplan.timeout)
        return response

    def delete_order(self, order_id):
        """
        Delete an existing order in vPlan: https://developer.vplan.com/documentation/#tag/order/paths/~1order~1%7Border_id%7D/delete
        This method constructs a request URL based on the endpoint and sends a DELETE request to the vPlan API.
        """
        url = f"{self.vplan.base_url}order/{order_id}"
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