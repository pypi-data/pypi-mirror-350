from flex.flex_api_client import FlexApiClient
import requests
from flex.flex_objects import Account, Workspace

class AccountClient(FlexApiClient):
    def __init__(self, base_url, username, password):
        super().__init__(base_url, username, password)

    def get_accounts(self):
        """Returns all accounts matching the specified parameters."""
        endpoint = f"/accounts"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            account_list = [Account(account) for account in response.json().get('accounts', [])]
            return account_list
        except requests.RequestException as e:
            raise Exception(e)

    def create_account(self, account_data):
        """Creates a new account."""
        endpoint = f"/accounts"
        try:
            response = requests.post(self.base_url + endpoint, headers=self.headers, json=account_data)
            response.raise_for_status()
            account = Account(response.json())
            return account
        except requests.RequestException as e:
            raise Exception(e)

    def get_account(self, accountId):
        """Returns the specified account."""
        endpoint = f"/accounts/{accountId}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            account = Account(response.json())
            return account
        except requests.RequestException as e:
            raise Exception(e)

    def update_account(self, baseMatrixParam, accountId, account_data):
        """Updates the account details."""
        endpoint = f"/accounts{baseMatrixParam}/{accountId}"
        try:
            response = requests.put(self.base_url + endpoint, headers=self.headers, json=account_data)
            response.raise_for_status()
            account = Account(response.json())
            return account
        except requests.RequestException as e:
            raise Exception(e)

    def get_account_workspace(self, accountId):
        """Returns the default workspace for the given account."""
        endpoint = f"/accounts/{accountId}/accountWorkspace"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            workspace = Workspace(response.json())
            return workspace
        except requests.RequestException as e:
            raise Exception(e)

    def get_account_configuration(self, accountId):
        """Returns the configuration metadata for a given account."""
        endpoint = f"/accounts/{accountId}/configuration"
        headers = self.headers.copy()
        try:
            response = requests.get(self.base_url + endpoint, headers=headers)
            response.raise_for_status()
            return response.json()  # Assuming successful response contains configuration metadata
        except requests.RequestException as e:
            raise Exception(e)

    def get_account_icon(self, baseMatrixParam, accountId, iconName):
        """Returns the icon for the account with the given id."""
        endpoint = f"/accounts{baseMatrixParam}/{accountId}/icons/{iconName}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            return response.content  # Assuming successful response contains the icon data
        except requests.RequestException as e:
            raise Exception(e)

    def update_account_icon(self, baseMatrixParam, accountId, iconName, icon_data):
        """Sets the icon for the account with the given id."""
        endpoint = f"/accounts{baseMatrixParam}/{accountId}/icons/{iconName}"
        try:
            response = requests.post(self.base_url + endpoint, headers=self.headers, files=icon_data)
            response.raise_for_status()
            return response.json()  # Assuming successful response indicates icon update was successful
        except requests.RequestException as e:
            raise Exception(e)
