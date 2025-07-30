import requests
import jwt
import time
from typing import Optional, Literal
from urllib.parse import urlencode
import yaml
import uuid
import os
from typing import List, Dict, Any
import csv


class EizenSDK:
    def __init__(
        self,
        refresh_token: str,
        environment: str = None,
        base_url: str = None,
        client_id: str = None,
    ):
        if environment == "dev":
            base_url: str = "https://vip-dev-api.eizen.ai/analytics/v1"
            client_id: str = "analytics-service"
        elif environment == "ldev":
            base_url: str = "https://gateway.eizen.ai"
            client_id: str = "analytics-service"
        self.__refresh_token = refresh_token
        self.client_id = client_id
        self.base_url = base_url
        self.__tenant_id = 0
        self.__role = ""
        self.__access_token = None
        self.__fetch_access_token()
        self.__get_tenant_id()

    def __fetch_access_token(self):
        """Fetch a new access token using the refresh token."""
        if not self.__refresh_token or self.__is_token_expired(self.__refresh_token):
            raise Exception("Refresh token is expired. Please provide a new one.")

        url = f"{self.base_url}/realms/Analytics/protocol/openid-connect/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": self.__refresh_token,
        }

        response = requests.post(
            url,
            data=urlencode(data),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if response.status_code == 200:
            tokens = response.json()
            self.__access_token = tokens["access_token"]
            self.__refresh_token = tokens.get("refresh_token", self.__refresh_token)
        else:
            raise Exception(f"Failed to retrieve access token: {response.text}")

    def __refresh_access_token(self):
        """Refresh the access token using the refresh token."""
        if not self.__refresh_token or self.__is_token_expired(self.__refresh_token):
            self.__fetch_new_tokens()  # If refresh token expired, get new tokens
            return

        url = f"{self.base_url}/realms/Analytics/protocol/openid-connect/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": self.__refresh_token,
        }

        response = requests.post(
            url,
            data=urlencode(data),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if response.status_code == 200:
            tokens = response.json()
            self.__access_token = tokens["access_token"]
            self.__refresh_token = tokens.get("refresh_token", self.__refresh_token)
        else:
            self.__fetch_new_tokens()  # If refresh fails, fetch new tokens

    def get_access_token(self) -> str:
        """Get a valid access token, refreshing it if necessary."""
        if not self.__access_token or self.__is_token_expired(self.__access_token):
            self.__fetch_access_token()
        return self.__access_token

    def __is_token_expired(self, token: str) -> bool:
        """Check if a JWT token is expired."""
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload["exp"] < time.time()
        except Exception as e:
            print(e)
            return True  # If token is invalid, assume expired

    def __make_request(self, method: str, url: str, **kwargs):
        """Handles API requests and refreshes token if needed."""
        if self.__is_token_expired(self.__access_token):
            self.__refresh_access_token()

        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.__access_token}"
        kwargs["headers"] = headers

        response = requests.request(method, url, **kwargs)

        if response.status_code == 401:
            self.__refresh_access_token()
            headers["Authorization"] = f"Bearer {self.__access_token}"
            response = requests.request(method, url, **kwargs)

        if response.status_code // 100 != 2:
            raise Exception(f"Request failed ({response.status_code}): {response.text}")

        if response.status_code == 204:
            return {}

        if response.headers.get("Content-Type") == "application/json":
            return response.json()

        return response.text

    def __make_request_access_token(self, method: str, url: str, **kwargs):
        """Handles API requests and refreshes token if needed."""
        if self.__is_token_expired(self.__access_token):
            self.__refresh_access_token()

        headers = kwargs.get("headers", {})
        headers["access_token"] = self.__access_token
        headers["Authorization"] = f"Bearer {self.__access_token}"
        kwargs["headers"] = headers
        response = requests.request(method, url, **kwargs)

        if response.status_code == 401:
            self.__refresh_access_token()
            headers["access_token"] = self.__access_token  # Keep consistent lowercase
            response = requests.request(method, url, **kwargs)

        if response.status_code // 100 != 2:
            raise Exception(f"Request failed ({response.status_code}): {response.text}")

        if response.status_code == 204:
            return {}

        if response.headers.get("Content-Type") == "application/json":
            return response.json()

        return response.text

    def __get_tenant_id(self):

        payload = jwt.decode(self.__access_token, options={"verify_signature": False})
        self.username = payload["preferred_username"]

        url = f"{self.base_url}/user"
        response = self.__make_request("GET", url, params={"email": self.username})
        self.__tenant_id = response["tenantId"]
        self.__role = response["roles"][0] if response["roles"] else ""  

    def get_analytics(self):
        if (self.__role == "Eizen"):
            url = f"{self.base_url}/analytics"
            analytics = self.__make_request("GET", url)
            return analytics
        else:
            url = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url)
            return [{"id": i["id"], "name": i["name"]} for i in analytics]

    def get_analytic_zones(self, analytic_id: int):
        if self.__role in ["Administrator", "User"]:
            url_analytics = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url_analytics)
            valid_ids = {a["id"] for a in analytics}
            if analytic_id not in valid_ids:
                raise PermissionError("401 Unauthorized access: You are not authorized to view zones for this analytic.")
            url = f"{self.base_url}/zone/analytics/{analytic_id}"
            zones = self.__make_request("GET", url)
            return [{"id": i["id"], "name": i["name"]} for i in zones]
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to view analytic zones.")

    def get_zone_sources(self, zone_id: int):
        if self.__role in ["Administrator", "User"]:
            url_analytics = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url_analytics)
            valid_zone_ids = set()
            for analytic in analytics:
                analytic_id = analytic["id"]
                url_zones = f"{self.base_url}/zone/analytics/{analytic_id}"
                zones = self.__make_request("GET", url_zones)
                valid_zone_ids.update(zone["id"] for zone in zones)
            if zone_id not in valid_zone_ids:
                raise PermissionError("401 Unauthorized access: You are not authorized to view sources for this zone.")
            url = f"{self.base_url}/source/zone/{zone_id}"
            sources = self.__make_request("GET", url)
            return [{"id": i["id"], "name": i["name"]} for i in sources]
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to view zone sources.")

    def get_analytic_sources(self, analytic_id: int):
        if self.__role in ["Administrator", "User"]:
            url_analytics = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url_analytics)
            valid_ids = {a["id"] for a in analytics}
            if analytic_id not in valid_ids:
                raise PermissionError("401 Unauthorized access: You are not authorized to view sources for this analytic.")
            url = f"{self.base_url}/source/analytics/{analytic_id}"
            sources = self.__make_request("GET", url)
            return [{"id": i["id"], "name": i["name"]} for i in sources["sources"]]
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to view analytic sources.")

    def get_source_details(self, source_id: int):
        if self.__role in ["Administrator", "User"]:
            url_analytics = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url_analytics)
            valid_source_ids = set()
            for analytic in analytics:
                analytic_id = analytic["id"]
                url_sources = f"{self.base_url}/source/analytics/{analytic_id}"
                sources = self.__make_request("GET", url_sources)
                valid_source_ids.update(source["id"] for source in sources.get("sources", []))
            if source_id not in valid_source_ids:
                raise PermissionError("401 Unauthorized access: You are not authorized to view details for this source.")
            url = f"{self.base_url}/source/{source_id}"
            return self.__make_request("GET", url)
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to view source details.")

    def get_source_summary(self, source_id: int):
        if self.__role in ["Administrator", "User"]:
            url_analytics = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url_analytics)
            valid_source_ids = set()
            for analytic in analytics:
                analytic_id = analytic["id"]
                url_sources = f"{self.base_url}/source/analytics/{analytic_id}"
                sources = self.__make_request("GET", url_sources)
                valid_source_ids.update(source["id"] for source in sources.get("sources", []))
            if source_id not in valid_source_ids:
                raise PermissionError("401 Unauthorized access: You are not authorized to view summary for this source.")
            url = f"{self.base_url}/videos/summary/{source_id}"
            return self.__make_request("GET", url)
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to view source summary.")

    def get_models(self):
        if self.__role == "Eizen":
            url = f"{self.base_url}/model"
            models = self.__make_request("GET", url)
            return models
        else:
            url = f"{self.base_url}/model/tenant/{self.__tenant_id}"
            models = self.__make_request("GET", url)
            return [{"id": i["id"], "name": i["name"]} for i in models]

    def get_all_tenants(self):
        if self.__role == "Eizen":
            url = f"{self.base_url}/tenant"
            tenants = self.__make_request("GET", url)
            return tenants
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to view all tenants.")

    def get_all_analytics_list(self):
        if (self.__role == "Eizen"):
            url = f"{self.base_url}/analytics"
            analytics = self.__make_request("GET", url)
            return analytics
        else:
            url = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url)
            return analytics

    def add_tenant(self, name, iconUri="https://example.com/acme_logo.png"):
        if self.__role == "Eizen":
            payload = {"name": name, "iconUri": iconUri}
            url = f"{self.base_url}/tenant"
            tenant = self.__make_request("POST", url, json=payload)
            return tenant
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to add a tenant.")

    def add_analytics(
        self,
        name,
        description,
        tenant_id,
        analytics_type_id,
        analytics_category_id,
        iconUri="https://example.com/acme_logo.png",
    ):
        if self.__role == "Eizen":
            payload = {
                "name": name,
                "description": description,
                "iconUri": iconUri,
                "tenantId": tenant_id,
                "analyticsTypeId": analytics_type_id,
                "analyticsCategoryId": analytics_category_id,
            }
            url = f"{self.base_url}/analytics"
            analytics = self.__make_request("POST", url, json=payload)
            return analytics
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to add analytics.")

    def add_analytics_type(
        self, name, description, tenant_id, icon_uri="https://example.com/acme_logo.png"
    ):
        if self.__role == "Eizen":
            payload = {
                "name": name,
                "description": description,
                "iconUri": icon_uri,
                "tenantId": tenant_id,
            }
            url = f"{self.base_url}/analytics-type"
            analytics_type = self.__make_request("POST", url, json=payload)
            return analytics_type
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to add an analytics type.")

    def add_analytics_category(
        self,
        name,
        description,
        tenant_id,
        analytics_type_id,
        icon_uri="https://example.com/acme_logo.png",
    ):
        if self.__role == "Eizen":
            payload = {
                "name": name,
                "description": description,
                "iconUri": icon_uri,
                "tenantId": tenant_id,
                "analyticsTypeId": analytics_type_id,
            }
            url = f"{self.base_url}/analytics-category"
            analytics_category = self.__make_request("POST", url, json=payload)
            return analytics_category
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to add an analytics category.")

    def get_analytics_type(self, analytics_type_id):
        if self.__role == "Eizen":
            url = f"{self.base_url}/analytics-type/{analytics_type_id}"
            analytics_type = self.__make_request("GET", url)
            return analytics_type
        elif self.__role in ["Administrator", "User"]:
            url_all = f"{self.base_url}/analytics-type/tenant/{self.__tenant_id}"
            analytics_types = self.__make_request("GET", url_all)
            valid_ids = {atype["id"] for atype in analytics_types}
            if analytics_type_id not in valid_ids:
                raise PermissionError("401 Unauthorized access: You are not authorized to view this analytics type.")
            url = f"{self.base_url}/analytics-type/{analytics_type_id}"
            analytics_type = self.__make_request("GET", url)
            return analytics_type
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to view this analytics type.")

    def get_analytics_category(self, analytics_category_id):
        if self.__role == "Eizen":
            url = f"{self.base_url}/analytics-category/{analytics_category_id}"
            analytics_category = self.__make_request("GET", url)
            return analytics_category
        elif self.__role in ["Administrator", "User"]:
            url_types = f"{self.base_url}/analytics-type/tenant/{self.__tenant_id}"
            analytics_types = self.__make_request("GET", url_types)
            valid_category_ids = set()
            for atype in analytics_types:
                type_id = atype["id"]
                url_cats = f"{self.base_url}/analytics-category/analytics-type/{type_id}"
                categories = self.__make_request("GET", url_cats)
                valid_category_ids.update(cat["id"] for cat in categories)
            if analytics_category_id not in valid_category_ids:
                raise PermissionError("401 Unauthorized access: You are not authorized to view this analytics category.")
            url = f"{self.base_url}/analytics-category/{analytics_category_id}"
            analytics_category = self.__make_request("GET", url)
            return analytics_category
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to view this analytics category.")

    def get_analytics_categories_by_analytic_type(self, analytics_type_id):
        url = f"{self.base_url}/analytics-category/analytics-type/{analytics_type_id}"
        analytics_category = self.__make_request("GET", url)
        return analytics_category

    def get_all_analytics_types(self):
        if (self.__role == "Eizen"):
            url = f"{self.base_url}/analytics-type"
            analytics_types = self.__make_request("GET", url)
            return analytics_types
        else:
            url = f"{self.base_url}/analytics-type/tenant/{self.__tenant_id}"
            analytics_types = self.__make_request("GET", url)
            return analytics_types

    def get_all_analytics_categories(self):
        if self.__role == "Eizen":
            url = f"{self.base_url}/analytics-category"
            analytics_categories = self.__make_request("GET", url)
            return analytics_categories
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to view all analytics categories.")

    def get_all_zones(self):
        if self.__role in ["Administrator", "User"]:
            url_analytics = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url_analytics)
            tenant_zone_ids = set()
            zones_list = []
            for analytic in analytics:
                analytic_id = analytic["id"]
                url_zones = f"{self.base_url}/zone/analytics/{analytic_id}"
                zones = self.__make_request("GET", url_zones)
                for zone in zones:
                    if zone["id"] not in tenant_zone_ids:
                        tenant_zone_ids.add(zone["id"])
                        zones_list.append(zone)
            return zones_list
        else:
            raise PermissionError("You are not authorized to view all zones.")

    def get_zone(self, zone_id):
        if self.__role in ["Administrator", "User"]:
            url_analytics = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url_analytics)
            valid_zone_ids = set()
            for analytic in analytics:
                analytic_id = analytic["id"]
                url_zones = f"{self.base_url}/zone/analytics/{analytic_id}"
                zones = self.__make_request("GET", url_zones)
                valid_zone_ids.update(zone["id"] for zone in zones)
            if zone_id not in valid_zone_ids:
                raise PermissionError("401 Unauthorized access: You are not authorized to view this zone.")
            url = f"{self.base_url}/zone/{zone_id}"
            zone = self.__make_request("GET", url)
            return zone
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to view this zone.")

    def add_zone(self, name, analytics_id):
        if self.__role == "Administrator":
            url_analytics = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url_analytics)
            valid_ids = {a["id"] for a in analytics}
            if analytics_id not in valid_ids:
                raise PermissionError("401 Unauthorized access: You are not authorized to add a zone for this analytic.")
            payload = {"name": name, "analyticsId": analytics_id}
            url = f"{self.base_url}/zone"
            zone = self.__make_request("POST", url, json=payload)
            return zone
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to add a zone.")

    def get_model_by_id(self, model_id):
        if self.__role == "Eizen":
            url = f"{self.base_url}/model/{model_id}"
            model = self.__make_request("GET", url)
            return {"id": model.get("id"), "name": model.get("name")}
        else:
            url = f"{self.base_url}/model/tenant/{self.__tenant_id}"
            models = self.__make_request("GET", url)
            valid_ids = {m["id"] for m in models}
            if model_id not in valid_ids:
                raise PermissionError("401 Unauthorized access: You are not authorized to view this model.")
            url = f"{self.base_url}/model/{model_id}"
            model = self.__make_request("GET", url)
            return {"id": model.get("id"), "name": model.get("name")}

    def get_all_models(self):
        if self.__role == "Eizen":
            url = f"{self.base_url}/model"
            models = self.__make_request("GET", url)
            return models
        else:
            url = f"{self.base_url}/model/tenant/{self.__tenant_id}"
            models = self.__make_request("GET", url)
            return [{"id": i["id"], "name": i["name"]} for i in models]


    def add_model(
        self,
        name,
        description,
        model_type,
        system,
        model_cd,
        model_category,
        objects,
        events,
        activities,
        endpoint_url,
        tenants,
        use_cases,
        is_inference_active,
        image_url="https://example.com/acme_logo.png",
        anomalies=[],
    ):
        if self.__role in [ "Eizen","Administrator"]:
            payload = {
                "name": name, 
                "modelCd": model_cd, 
                "system": system,  
                "modelCategory": model_category,
                "anomalies": anomalies, 
                "description": description,  
                "modelType": model_type, 
                "objects": objects,  
                "events": events, 
                "activities": activities, 
                "imageUrl": image_url,  
                "endpointUrl": endpoint_url,
                "tenants": tenants, 
                "useCases": use_cases, 
                "isInferenceActive": is_inference_active, 
            }
            url = f"{self.base_url}/model"
            model = self.__make_request("POST", url, json=payload)
            return model
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to add a model.")


    def update_model(
        self,
        model_id: int,
        name: str,
        model_cd: str ,
        system: str,
        model_category: str,
        anomalies: list ,
        description: str ,
        objects: list ,
        events: list ,
        activities: list,
        tenants: list,
        use_cases: list,
        image_url: str ,
        weights_url: str ,
        endpoint_url: str ,
        is_inference_active: bool,
    ):
        """
        Updates a model by its ID.

        :param model_id: ID of the model to update.
        :param ...: (other fields to update)
        :return: The updated model object.
        """
        if self.__role in ["Administrator", "Eizen"]:
            payload = {
                "name": name,
                "modelCd": model_cd,
                "system": system,
                "modelCategory": model_category,
                "anomalies": anomalies,
                "description": description,
                "objects": objects,
                "events": events,
                "activities": activities,
                "tenants": tenants,
                "useCases": use_cases,
                "imageUrl": image_url,
                "weightsUrl": weights_url,
                "endpointUrl": endpoint_url,
                "isInferenceActive": is_inference_active,
            }
            payload = {k: v for k, v in payload.items() if v is not None}

            url = f"{self.base_url}/model/{model_id}"
            return self.__make_request("PUT", url, json=payload)
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to update a model.")


    def get_all_users(self):
        if self.__role == "Eizen":
            url = f"{self.base_url}/user/list"
            users = self.__make_request("GET", url)
            return users
        elif self.__role =="Administrator":
            url = f"{self.base_url}/user/list/{self.__tenant_id}"
            users = self.__make_request("GET", url)
            return users
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to view all users.")

    def create_user(
        self,
        user_name,
        email,
        password,
        first_name,
        last_name,
        roles,
        tenant_id,
        analytics_id,
    ):
        """
        Creates a new user via the API.

        Args:
            user_name (str): Username for the new user.
            email (str): Email address for the new user.
            password (str): Password for the new user.
            first_name (str): First name of the user.
            last_name (str): Last name of the user.
            roles (list[str]): List of role strings to assign.
            tenant_id (int): The ID of the tenant the user belongs to.
            analytics_id (list[int]): List of analytics IDs associated with the user.

        Returns:
            dict: The created user object returned by the API.
                  Raises an exception if the request fails.
        """

        if self.__role == "Eizen":
            payload = {
                "userName": user_name,
                "email": email,
                "password": password,
                "firstName": first_name,
                "lastName": last_name,
                "roles": roles,
                "tenantId": tenant_id,
                "analyticsId": analytics_id,
            }
            url = f"{self.base_url}/user"
            user = self.__make_request("POST", url, json=payload)
            return user
        elif self.__role == "Administrator":
            payload = {
                "userName": user_name,
                "email": email,
                "password": password,
                "firstName": first_name,
                "lastName": last_name,
                "roles": roles,
                "tenantId": self.__tenant_id,
                "analyticsId": analytics_id,
            }
            url = f"{self.base_url}/user"
            user = self.__make_request("POST", url, json=payload)
            return user
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to create a user.")

    def create_source(
            self,
            name: str,
            username: str,
            password: str,
            source_url: str,
            description: str,
            source_type: str,
            zone_id: int,
            mongo_host: str,
            mongo_db: str,
            models: list,
        ):
            if self.__role == "Administrator":
                url_analytics = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
                analytics = self.__make_request("GET", url_analytics)
                valid_zone_ids = set()
                for analytic in analytics:
                    analytic_id = analytic["id"]
                    url_zones = f"{self.base_url}/zone/analytics/{analytic_id}"
                    zones = self.__make_request("GET", url_zones)
                    valid_zone_ids.update(zone["id"] for zone in zones)
                if zone_id not in valid_zone_ids:
                    raise PermissionError("401 Unauthorized access: You are not authorized to add a source to this zone.")
                url = f"{self.base_url}/source"
                return self.__make_request(
                    "POST",
                    url,
                    json={
                        "name": name,
                        "userName": username,
                        "password": password,
                        "sourceUrl": source_url,
                        "description": description,
                        "sourceType": source_type,
                        "zoneId": zone_id,
                        "mongoHost": mongo_host,
                        "mongoDb": mongo_db,
                        "models": models,
                    },
                )
            else:
                raise PermissionError("401 Unauthorized access: You are not authorized to add a source.")

    def update_source(
        self,
        source_id: int,
        name: str = None,
        username: str = None,
        password: str = None,
        source_url: str = None,
        description: str = None,
        source_type: str = None,
        models: list = None,
        mongo_host: str = None,
        mongo_db: str = None,
        is_active: bool = True,
        is_local: bool = None,
        video_search_enabled: bool = False,
        is_inferred: bool = None,
    ):
        """
        Updates a source by its ID.

        :param source_id: ID of the source to update.
        :param ...: (other optional fields to update)
        :return: The updated source object.
        """
        if self.__role == "Administrator":
            payload = {
                "name": name,
                "userName": username,
                "password": password,
                "sourceUrl": source_url,
                "description": description,
                "sourceType": source_type,
                "models": models,
                "mongoHost": mongo_host,
                "mongoDb": mongo_db,
                "isActive": is_active,
                "isLocal": is_local,
                "videoSearchEnabled": video_search_enabled,
                "isInferred": is_inferred,
            }
            # Remove keys with None values to avoid overwriting with nulls
            payload = {k: v for k, v in payload.items() if v is not None}

            url = f"{self.base_url}/source/update"
            params = {"id": source_id}
            return self.__make_request("PUT", url, params=params, json=payload)
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to update a source.")

    def create_sources_from_yaml(self, yaml_file: str):
        """
        Reads a YAML file containing a list of sources and calls create_source for each entry.

        :param yaml_file: Path to the YAML file containing source definitions.
        """
        if self.__role == "Administrator":
            with open(yaml_file, "r") as file:
                sources = yaml.safe_load(file)

            if not isinstance(sources, list):
                raise ValueError("YAML file must contain a list of sources.")

            url_analytics = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url_analytics)
            valid_zone_ids = set()
            for analytic in analytics:
                analytic_id = analytic["id"]
                url_zones = f"{self.base_url}/zone/analytics/{analytic_id}"
                zones = self.__make_request("GET", url_zones)
                valid_zone_ids.update(zone["id"] for zone in zones)

            for source in sources:
                if source["zone_id"] not in valid_zone_ids:
                    raise PermissionError(f"401 Unauthorized access: You are not authorized to add a source to zone_id {source['zone_id']}.")

            response = []

            for source in sources:
                response.append(
                    self.create_source(
                        name=source["name"],
                        username=source["username"],
                        password=source["password"],
                        source_url=source["source_url"],
                        description=source["description"],
                        source_type=source["source_type"],
                        zone_id=source["zone_id"],
                        mongo_host=source["mongo_host"],
                        mongo_db=source["mongo_db"],
                        models=source.get(
                            "models", []
                        ),  # Default to empty list if models key is missing
                    )
                )

            return [i["id"] for i in response]
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to create sources from YAML.")

    def delete_source(self, source_id: int):
        if self.__role == "Administrator":
            url_analytics = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url_analytics)
            valid_source_ids = set()
            for analytic in analytics:
                analytic_id = analytic["id"]
                url_sources = f"{self.base_url}/source/analytics/{analytic_id}"
                sources = self.__make_request("GET", url_sources)
                valid_source_ids.update(source["id"] for source in sources.get("sources", []))
            if source_id not in valid_source_ids:
                raise PermissionError("401 Unauthorized access: You are not authorized to delete this source.")
            url = f"{self.base_url}/source/{source_id}"
            return self.__make_request("DELETE", url)
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to delete a source.")

    def yolo_inference(
        self,
        model_id: int,
        input_type: str,
        media_url: str,
        response_type: str,
        s3_bucket_name: str = None,
        s3_access_key: str = None,
        s3_secret_key: str = None,
    ):

        # Get model details first
        url = f"{self.base_url}/model/{model_id}"
        model = self.__make_request("GET", url)
        endpoint = model["endpointUrl"]
        inferenceUrl = f"{self.base_url}/ez_yolo_model_inference/"

        # Send inference data
        data = {
            "inferenceUrl": endpoint,
            "inputType": input_type,
            "media_url": media_url,
            "responseType": response_type,
            "s3AccessKey": s3_access_key,
            "s3Secretkey": s3_secret_key,
            "s3BucketName": s3_bucket_name,
        }
        headers = {"access_token": self.__access_token}
        return self.__make_request_access_token(
            "POST", inferenceUrl, json=data, headers=headers
        )

    def collect_data(
        self,
        source_id: int,
        time_interval: int = 10,
        number_of_frames_requested: int = None,
        skip_frame_count: int = None,
        s3_bucket_name: str = None,
        s3_access_key: str = None,
        s3_secret_key: str = None,
        s3_cloud_path: str = None,
    ):
        if self.__role in ["Administrator", "User"]:
            url = f"{self.base_url}/ez_collect-data-to-label-studio/"

            headers = {"access_token": self.__access_token}

            if number_of_frames_requested:
                time_interval = None
            data = {
                "id": source_id,
                "s3_access_key": s3_access_key,
                "s3_secret_key": s3_secret_key,
                "s3_bucket_name": s3_bucket_name,
                "s3_cloud_folder_path": s3_cloud_path,
                "time_interval": time_interval,
                "number_of_frames_requested": number_of_frames_requested,
                "skip_frame_count": skip_frame_count,
            }

            return self.__make_request_access_token("POST", url, json=data, headers=headers)
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to collect data.")

    def model_building(
        self,
        modelName: Optional[str] = None,
        modelCategory: Optional[str] = None,
        modelType: Optional[str] = "private",
        modelWeightsPath: Optional[str] = "",
        dataPath: Optional[str] = "",
        numberOfEpochs: Optional[int] = 50,
        useWeights: Optional[bool] = False,
        yaml_file: Optional[str] = None,
    ):
        try:
            url = f"{self.base_url}/ez_model_training/"

            if yaml_file:
                with open(yaml_file, "r") as file:
                    modelData = yaml.safe_load(file)

                if not isinstance(modelData, list):
                    raise ValueError("YAML file must contain a list of sources.")

                if modelData:
                    data = modelData[0]
                    modelName = data.get("modelName")
                    modelCategory = data.get("modelCategory")
                    modelWeightsPath = data.get("modelWeightsPath", "")
                    dataPath = data.get("dataPath", "")
                    useWeights = data.get("useWeights", False)
                    numberOfEpochs = data.get("numberOfEpochs", 10)

            data = {
                "modelName": modelName,
                "modelType": modelType,
                "modelCategory": modelCategory,
                "dataPath": dataPath,
                "modelWeightsPath": modelWeightsPath,
                "numberOfEpochs": numberOfEpochs,
                "useWeights": useWeights,
                "tenantId": self.__tenant_id,
            }

            headers = {"access_token": self.__access_token}
            model_building = self.__make_request_access_token(
                "POST", url, json=data, headers=headers
            )
            return model_building

        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
        except ValueError as e:
            print(f"Value error: {e}")
        except FileNotFoundError:
            print(f"File not found: {yaml_file}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def model_retraining(
        self,
        id: Optional[int] = None,
        modelType: Optional[str] = "private",
        dataPath: Optional[str] = None,
        useWeights: Optional[bool] = True,
        numberOfEpochs: Optional[int] = 50,
        yaml_file: Optional[str] = None,
    ):
        try:
            url = f"{self.base_url}/ez_model_retraining/"

            if yaml_file:
                with open(yaml_file, "r") as file:
                    modelData = yaml.safe_load(file)

                if not isinstance(modelData, list):
                    raise ValueError("YAML file must contain a list of sources.")

                if modelData:
                    data = modelData[0]
                    id = data.get("id")
                    modelType = data.get("modelType", "private")
                    dataPath = data.get("dataPath", "")
                    useWeights = data.get("useWeights", True)
                    numberOfEpochs = data.get("numberOfEpochs", 10)

            headers = {"access_token": self.__access_token}
            model_retraining_data = {
                "id": id,
                "modelType": modelType,
                "dataPath": dataPath,
                "numberOfEpochs": numberOfEpochs,
                "useWeights": useWeights,
            }

            model_retraining = self.__make_request_access_token(
                "POST", url, json=model_retraining_data, headers=headers
            )
            return model_retraining

        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
        except ValueError as e:
            print(f"Value error: {e}")
        except FileNotFoundError:
            print(f"File not found: {yaml_file}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def video_process_llava(
        self,
        videoUrl: str,
        instruction: str,
        version: Optional[str] = None,
        modelID: Optional[str] = "EZA_MDL_FOUN_LLAV_NEXT_VIDEO",
    ):
        url = f"{self.base_url}/ez_video_process_llava_video/"
        print("Video Process Strated .....")
        data = {
            "videoFile": videoUrl,
            "instruction": instruction,
            "version": version,
            "modelID": modelID,
        }
        headers = {"access_token": self.__access_token}
        video_process = self.__make_request_access_token(
            "POST", url, json=data, headers=headers
        )
        return video_process

    def video_chat(self, source_id: int, question: str):
        if self.__role in ["Administrator", "User"]:
            url = f"{self.base_url}/video-inference/ask-elina"
            data = {
                "sourceId": source_id,
                "question": question,
            }
            return self.__make_request("POST", url, json=data)
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to use video chat.")

    def get_raw_analytics(
        self, source_id: int, start_time: int | None = None, end_time: int | None = None
    ):
        if self.__role in ["Administrator", "User"]:
            url_analytics = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url_analytics)
            valid_source_ids = set()
            for analytic in analytics:
                analytic_id = analytic["id"]
                url_sources = f"{self.base_url}/source/analytics/{analytic_id}"
                sources = self.__make_request("GET", url_sources)
                valid_source_ids.update(source["id"] for source in sources.get("sources", []))
            if source_id not in valid_source_ids:
                raise PermissionError("401 Unauthorized access: You are not authorized to view raw analytics for this source.")
            url = f"{self.base_url}/raw-analytics/raw-analytics"
            data = {
                "sourceId": source_id,
                "startTime": start_time,
                "endTime": end_time,
            }
            return self.__make_request("GET", url, params=data)
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to view raw analytics.")

    def get_analytics_report(
        self, source_id: int, start_time: int | None = None, end_time: int | None = None
    ):
        if self.__role in ["Administrator", "User"]:
            url_analytics = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url_analytics)
            valid_source_ids = set()
            for analytic in analytics:
                analytic_id = analytic["id"]
                url_sources = f"{self.base_url}/source/analytics/{analytic_id}"
                sources = self.__make_request("GET", url_sources)
                valid_source_ids.update(source["id"] for source in sources.get("sources", []))
            if source_id not in valid_source_ids:
                raise PermissionError("401 Unauthorized access: You are not authorized to get analytics report for this source.")
            data = self.get_raw_analytics(source_id, start_time, end_time)
            return self.convert_objects_to_csv(data)
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to get analytics report.")

    def get_analytics_report_list(
        self,
        source_ids: List[int],
        start_time: int | None = None,
        end_time: int | None = None,
    ):
        """
        Fetches analytics reports for a list of source IDs and returns a list of CSV file paths.
        :param source_ids: List of source IDs.
        :param start_time: Start time for the analytics report.
        :param end_time: End time for the analytics report.
        :return: List of file paths to the generated CSV files.
        """
        if self.__role in ["Administrator", "User"]:
            url_analytics = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url_analytics)
            valid_source_ids = set()
            for analytic in analytics:
                analytic_id = analytic["id"]
                url_sources = f"{self.base_url}/source/analytics/{analytic_id}"
                sources = self.__make_request("GET", url_sources)
                valid_source_ids.update(source["id"] for source in sources.get("sources", []))
            for source_id in source_ids:
                if source_id not in valid_source_ids:
                    raise PermissionError(f"401 Unauthorized access: You are not authorized to get analytics report for source_id {source_id}.")
            csv_files = {}
            for source_id in source_ids:
                data = self.get_raw_analytics(source_id, start_time, end_time)
                csv_file = self.convert_objects_to_csv(data)
                csv_files[source_id] = csv_file
            return csv_files
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to get analytics report list.")

    def convert_objects_to_csv(
        self, data: List[Dict[str, Any]], output_dir: str = "."
    ) -> str:
        """
        Converts a list of dictionaries to a CSV file and returns the file path.

        :param data: List of dictionary objects.
        :param output_dir: Directory where the CSV file will be saved.
        :return: Path to the generated CSV file.
        """
        if self.__role in ["Administrator", "User"]:
            if not data:
                return "Data is not available."
            # Flatten function for list values
            def flatten(item):
                if isinstance(item, list):
                    return ";".join(str(i) for i in item)
                return item

            # Collect all keys
            all_keys = sorted({key for obj in data for key in obj.keys()}) 
            # Unique filename
            filename = f"export_{uuid.uuid4().hex[:8]}.csv"
            file_path = os.path.join(output_dir, filename)

            # Write to CSV
            with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=all_keys)
                writer.writeheader()
                for obj in data:
                    flat_row = {k: flatten(obj.get(k, "")) for k in all_keys}
                    writer.writerow(flat_row) 
            return file_path
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to convert objects to CSV.")

    def search_in_video(self, source_id: int, search_text: str):
        if self.__role in ["Administrator", "User"]:
            url_analytics = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url_analytics)
            valid_source_ids = set()
            for analytic in analytics:
                analytic_id = analytic["id"]
                url_sources = f"{self.base_url}/source/analytics/{analytic_id}"
                sources = self.__make_request("GET", url_sources)
                valid_source_ids.update(source["id"] for source in sources.get("sources", []))
            if source_id not in valid_source_ids:
                raise PermissionError("401 Unauthorized access: You are not authorized to search in this video source.")
            url = f"{self.base_url}/videos/search/{source_id}"
            data = {
                "event": search_text,
            }
            return self.__make_request("GET", url, params=data)
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to search in video.")

    def video_library(
        self,
        analytic_ids: List[int],
        zone_id: int | None = None,
        source_id: int | None = None,
        page_number: int = 0,
        page_size: int = 6,
    ):
        if self.__role in ["Administrator", "User"]:
            url_analytics = f"{self.base_url}/analytics/tenant/{self.__tenant_id}"
            analytics = self.__make_request("GET", url_analytics)
            valid_analytic_ids = {a["id"] for a in analytics}
            for aid in analytic_ids:
                if aid not in valid_analytic_ids:
                    raise PermissionError(f"401 Unauthorized access: You are not authorized to view analytic {aid}.")
            valid_zone_ids = set()
            for analytic in analytics:
                analytic_id = analytic["id"]
                url_zones = f"{self.base_url}/zone/analytics/{analytic_id}"
                zones = self.__make_request("GET", url_zones)
                valid_zone_ids.update(zone["id"] for zone in zones)
            if zone_id is not None and zone_id not in valid_zone_ids:
                raise PermissionError(f"401 Unauthorized access: You are not authorized to view zone {zone_id}.")
            valid_source_ids = set()
            for analytic in analytics:
                analytic_id = analytic["id"]
                url_sources = f"{self.base_url}/source/analytics/{analytic_id}"
                sources = self.__make_request("GET", url_sources)
                valid_source_ids.update(source["id"] for source in sources.get("sources", []))
            if source_id is not None and source_id not in valid_source_ids:
                raise PermissionError(f"401 Unauthorized access: You are not authorized to view source {source_id}.")
                
            url = f"{self.base_url}/event"
            params = {
                "analyticIds": analytic_ids,
                "zoneId": zone_id,
                "sourceId": source_id,
                "pageNumber": page_number,
                "itemsPerPage": page_size,
            }
            return self.__make_request("GET", url, params=params)
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to view the video library.")

    def get_avatar_list(self):
        if self.__role in ["Administrator", "User"]:
            url = f"{self.base_url}/avatar/tenant/{self.__tenant_id}"
            return self.__make_request("GET", url)
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to view avatar list.")

    def generate_video(
        self,
        name: str,
        gender: Literal["male", "female"],
        language: Literal[
            "English",
            "Hindi",
            "Japanese",
            "Chinese",
            "Korean",
            "French",
            "German",
            "Italian",
            "Spanish",
            "Russian",
        ],
        text: str,
        avatar_url: str,
    ):
        if self.__role in ["Administrator", "User"]:
            url = f"{self.base_url}/video-generation/video"
            data = {
                "name": name,
                "gender": gender,
                "language": language,
                "text": text,
                "avatarUri": avatar_url,
                "tenantId": self.__tenant_id,
            }
            return self.__make_request("POST", url, json=data)
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to generate video.")
    
    def check_generation_video_status(self, video_id: int):
        if self.__role in ["Administrator", "User"]:
            url = f"{self.base_url}/video-generation/video/{video_id}"
            return self.__make_request("GET", url).get("status")
        else:
            raise PermissionError("401 Unauthorized access: You are not authorized to check video generation status.")
    
    def grant_access(self, user_email: str):
        url = f"{self.base_url}/user-access/{user_email}"
        return self.__make_request("POST", url)
    
    def check_access(self, user_email: str):
        url = f"{self.base_url}/user-access/{user_email}"
        result = self.__make_request("GET", url)
        return len(result) > 0
    
    def get_token(self, user_email: str, password: str):
        url = f"{self.base_url}/realms/Analytics/protocol/openid-connect/token"
        data = {
            "grant_type": "password",
            "client_id": "analytics-service",
            "username": user_email,
            "password": password,
            "scope": "offline_access"
        }
        return self.__make_request("POST", url, data=data).get("refresh_token")