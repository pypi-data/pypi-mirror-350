import requests

class Database:
    def __init__(self, base_url, api_key = None):
        self.api_key = api_key
        self.base_url = base_url
        if api_key:
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
        else:
            self.headers = {"Content-Type": "application/json"}
            
    def insert(self, data):
        """
        Inserts a document into the database.
        
        Args:
            data (dict): The document to insert.
        
        Returns:
            dict: Response from the database service.
        """
       
        response = requests.post(
            f"{self.base_url}/insert",
            json=data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
