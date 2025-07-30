"""
Terrakio Admin API Client

A Python client for administrators to access Terrakio's administrative API.
"""

__version__ = "0.1.0"

from terrakio_core.client import BaseClient

class Client(BaseClient):
    # Expose admin methods as public
    def get_user_by_id(self, user_id: str):
        return self._get_user_by_id(user_id)

    def get_user_by_email(self, email: str):
        return self._get_user_by_email(email)

    def list_users(self, substring: str = None, uid: bool = False):
        return self._list_users(substring, uid)

    def edit_user(self, user_id: str, uid: str = None, email: str = None, role: str = None, apiKey: str = None, groups: list = None, quota: int = None):
        return self._edit_user(user_id, uid, email, role, apiKey, groups, quota)

    def reset_quota(self, email: str, quota: int = None):
        return self._reset_quota(email, quota)

    def delete_user(self, uid: str):
        return self._delete_user(uid)
    
    # Expose dataset management methods as public
    def get_dataset(self, name: str, collection: str = "terrakio-datasets"):
        return self._get_dataset(name, collection)
    
    def list_datasets(self, substring: str = None, collection: str = "terrakio-datasets"):
        return self._list_datasets(substring, collection)
    
    def create_dataset(self, name: str, collection: str = "terrakio-datasets", **kwargs):
        return self._create_dataset(name, collection, **kwargs)
    
    def update_dataset(self, name: str, append: bool = True, collection: str = "terrakio-datasets", **kwargs):
        return self._update_dataset(name, append, collection, **kwargs)
    
    def overwrite_dataset(self, name: str, collection: str = "terrakio-datasets", **kwargs):
        return self._overwrite_dataset(name, collection, **kwargs)
    
    def delete_dataset(self, name: str, collection: str = "terrakio-datasets"):
        return self._delete_dataset(name, collection)

__all__ = [
    'Client'
]
    