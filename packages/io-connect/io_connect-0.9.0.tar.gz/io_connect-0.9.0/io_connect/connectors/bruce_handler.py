# External Imports
import requests
from typeguard import typechecked
import io_connect.constants as c
from typing import Optional
import json
import logging
from io_connect.utilities.store import ERROR_MESSAGE, Logger


@typechecked
class BruceHandler:
    __version__ = c.VERSION

    def __init__(
        self,
        user_id: str,
        data_url: str,
        on_prem: Optional[bool] = False,
        logger: Optional[logging.Logger] = None,
    ):
        self.user_id = user_id
        self.data_url = data_url
        self.header = {"userID": user_id}
        self.on_prem = on_prem
        self.logger = Logger(logger)

    def get_insight_details(
        self,
        populate: list,
        sort: Optional[dict] = None,
        projection: Optional[dict] = None,
        on_prem: Optional[bool] = None,
    ) -> list:
        try:
            # If on_prem is not provided, use the default value from the class attribute
            if on_prem is None:
                on_prem = self.on_prem

            # Construct the URL based on the on_prem flag
            protocol = "http" if on_prem else "https"

            # Endpoint URL
            url = c.GET_INSIGHT_DETAILS.format(
                protocol=protocol,
                data_url=self.data_url,
            )

            # Prepare the request payload
            payload = {
                "pagination": {"page": 1, "count": 1000},
                "populate": populate,
                "sort": sort,
                "projection": projection,
                "user": {"id": self.user_id},
            }

            # Send the request via HTTP POST with headers
            response = requests.put(url, json=payload, headers=self.header)

            # Check the response status code
            response.raise_for_status()

            response_data = json.loads(response.text)

            if not response_data["success"]:
                raise ValueError(response_data)

            return response_data["data"]["data"]

        except requests.exceptions.RequestException as e:
            error_message = (
                ERROR_MESSAGE(response, url)
                if "response" in locals()
                else f"\n[URL] {url}\n[EXCEPTION] {e}"
            )
            self.logger.error(f"[EXCEPTION] {type(e).__name__}: {error_message}")
            return []

        except Exception as e:
            self.logger.error(f"[EXCEPTION] {e}")
            return []

    def add_insight_result(
        self,
        insight_id: str,
        workbench_id: str,
        result: list,
        devID: str,
        whitelisted_users: list,
        metadata: dict,
        tags: list,
        on_prem: Optional[bool] = None,
    ) -> bool:
        """
        Adds an insight result.

        This function adds an insight result using the specified parameters.

        Args:
            insight_id (str): The ID of the insight.
            workbench_id (str): The ID of the workbench.
            result (list): List of results.
            devID (str): Parameters related to the result.
            class_type (str): Metadata related to the result.
            tags (list): List of tags associated with the result.

        Returns:
            bool: True if the result was added successfully, False otherwise.
        Example:
            # Instantiate BruceHandler
            >>> bruce_handler = BruceHandler(data_url="example.com", user_id="userID")

            # Example: Adding an insight result
            >>> insight_added = bruce_handler.add_insight_result(
            ...     insight_id="insightID",
            ...     workbench_id="workbenchID",
            ...     result=["result1", "result2"],
            ...     devID="devID",
            ...     class_type="class type",
            ...     tags=['tags']
            ... )

        """
        try:
            # If on_prem is not provided, use the default value from the class attribute
            if on_prem is None:
                on_prem = self.on_prem

            # Construct the URL based on the on_prem flag
            protocol = "http" if on_prem else "https"

            # Endpoint URL
            url = c.ADD_INSIGHT_RESULT.format(
                protocol=protocol,
                data_url=self.data_url,
            )

            # Prepare the request payload
            payload = {
                "insightID": insight_id,
                "workbenchID": workbench_id,
                "result": result,
                "parameters": {"devID": devID},
                "metadata": metadata,
                "whitelistedUIsers": whitelisted_users,
                "tags": tags,
            }

            # Send the request via HTTP POST with headers
            response = requests.post(url, json=payload, headers=self.header)

            # Check the response status code
            response.raise_for_status()

            return True

        except requests.exceptions.RequestException as e:
            error_message = (
                ERROR_MESSAGE(response, url)
                if "response" in locals()
                else f"\n[URL] {url}\n[EXCEPTION] {e}"
            )
            self.logger.error(f"[EXCEPTION] {type(e).__name__}: {error_message}")
            return False

        except Exception as e:
            self.logger.error(f"[EXCEPTION] {e}")
            return False

    def get_insight_results(
        self, insight_id: str, count: int = 1000, on_prem: Optional[bool] = None
    ) -> list:
        """
        Fetches insights results.

        This function fetches insights results using the specified parameters.

        Args:
            insight_id (str): The ID of the insight.
            count (int): The number of results to fetch.

        Returns:
            dict: A dictionary containing the fetched insight results.

        Example:
            # Instantiate BruceHandler
            >>> bruce_handler = BruceHandler(data_url="example.com", user_id="userID")
            # Example
            >>> insight_id = "insightID"
            >>> fetched_results = bruce_handler.fetch_insight_results(insight_id=insight_id)
            # Example
            >>> count = num
            >>> insight_id = "insightID"
            >>> fetched_results = bruce_handler.fetch_insight_results(insight_id=insight_id, count=count)

        """
        try:
            # If on_prem is not provided, use the default value from the class attribute
            if on_prem is None:
                on_prem = self.on_prem

            # Construct the URL based on the on_prem flag
            protocol = "http" if on_prem else "https"

            # Endpoint URL
            url = c.GET_INSIGHT_RESULT.format(
                protocol=protocol, data_url=self.data_url, count=count
            )

            # Prepare the request payload
            payload = {"insightID": insight_id}

            # Send the request via HTTP PUT with headers
            response = requests.put(url, json=payload, headers=self.header)

            # Check the response status code
            response.raise_for_status()

            response_data = json.loads(response.text)

            if not response_data["success"]:
                raise ValueError(response_data)

            return response_data["data"]

        except requests.exceptions.RequestException as e:
            error_message = (
                ERROR_MESSAGE(response, url)
                if "response" in locals()
                else f"\n[URL] {url}\n[EXCEPTION] {e}"
            )
            self.logger.error(f"[EXCEPTION] {type(e).__name__}: {error_message}")
            return []

        except Exception as e:
            self.logger.error(f"[EXCEPTION] {e}")
            return []

    def vector_upsert(
        self,
        insight_id: str,
        vector: list,
        payload: dict,
        on_prem: Optional[bool] = None,
    ) -> dict:
        try:
            # If on_prem is not provided, use the default value from the class attribute
            if on_prem is None:
                on_prem = self.on_prem

            # Construct the URL based on the on_prem flag
            protocol = "http" if on_prem else "https"

            # Endpoint URL
            url = c.VECTOR_UPSERT.format(protocol=protocol, data_url=self.data_url)

            # Prepare the request payload
            data = {
                "insightID": insight_id,
                "vector": vector,
                "payload": payload,
            }

            # Send the request via HTTP POST with headers
            response = requests.post(url, json=data, headers=self.header)

            # Check the response status code
            response.raise_for_status()

            response_data = response.json()

            if not response_data["success"]:
                raise ValueError(response_data)

            return response_data["data"]

        except requests.exceptions.RequestException as e:
            error_message = (
                ERROR_MESSAGE(response, url)
                if "response" in locals()
                else f"\n[URL] {url}\n[EXCEPTION] {e}"
            )
            self.logger.error(f"[EXCEPTION] {type(e).__name__}: {error_message}")
            return {}

        except Exception as e:
            self.logger.error(f"[EXCEPTION] {e}")
            return {}

    def vector_search(
        self,
        query_vector: list,
        insight_list: list,
        document_list: list,
        limit: int = 100,
        on_prem: Optional[bool] = None,
    ) -> list:
        try:
            # If on_prem is not provided, use the default value from the class attribute
            if on_prem is None:
                on_prem = self.on_prem

            # Construct the URL based on the on_prem flag
            protocol = "http" if on_prem else "https"

            # Endpoint URL
            url = c.VECTOR_SEARCH.format(protocol=protocol, data_url=self.data_url)

            # Prepare the request payload
            payload = {
                "query_vector": query_vector,
                "insightIDList": insight_list,
                "documentIDList": document_list,
                "limit": limit,
            }

            # Send the request via HTTP POST with headers
            response = requests.post(url, json=payload, headers=self.header)

            # Check the response status code
            response.raise_for_status()

            response_data = response.json()

            if not response_data["success"]:
                raise ValueError(response_data)

            return response_data["data"]

        except requests.exceptions.RequestException as e:
            error_message = (
                ERROR_MESSAGE(response, url)
                if "response" in locals()
                else f"\n[URL] {url}\n[EXCEPTION] {e}"
            )
            self.logger.error(f"[EXCEPTION] {type(e).__name__}: {error_message}")
            return []

        except Exception as e:
            self.logger.error(f"[EXCEPTION] {e}")
            return []
