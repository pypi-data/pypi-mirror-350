from flex.flex_api_client import FlexApiClient
from flex.flex_objects import AccountProperty
import requests

class AccountPropertyClient(FlexApiClient):
    def __init__(self, base_url, username, password):
        super().__init__(base_url, username, password)

    def get_account_properties(self):
        """Return all properties set on the account."""
        endpoint = f"/accountProperties"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            account_property_list = [AccountProperty(account_property) for account_property in response.json().get('accountProperties', [])]
            return account_property_list
        except requests.RequestException as e:
            raise Exception(e)

    def create_account_property(self, property_data):
        """Creates a new Account Property."""
        endpoint = f"/accountProperties"
        try:
            response = requests.post(self.base_url + endpoint, headers=self.headers, json=property_data)
            response.raise_for_status()
            account_property = AccountProperty(response.json())
            return account_property
        except requests.RequestException as e:
            raise Exception(e)

    def get_account_property(self, accountPropertyId):
        """Returns an Account Property by the given property ID."""
        endpoint = f"/accountProperties/{accountPropertyId}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            account_property = AccountProperty(response.json())
            return account_property
        except requests.RequestException as e:
            raise Exception(e)

    def update_account_property(self, accountPropertyId, property_data):
        """Updates an account property."""
        endpoint = f"/accountProperties/{accountPropertyId}"
        try:
            response = requests.put(self.base_url + endpoint, headers=self.headers, json=property_data)
            response.raise_for_status()
            return response.json()  # Assuming the successful response indicates the update was successful
        except requests.RequestException as e:
            raise Exception(e)

    def delete_account_property(self, objectId):
        """Delete an account property."""
        endpoint = f"/accountProperties/{objectId}"
        try:
            response = requests.delete(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()  # Assuming the successful response indicates the delete was successful
        except requests.RequestException as e:
            raise Exception(e)