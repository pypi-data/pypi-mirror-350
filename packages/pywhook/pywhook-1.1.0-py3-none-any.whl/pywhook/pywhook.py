from .types import WebhookRequest, EndpointConfig
from .types.errors import WebhookError
from typing import List, Dict, Any, Callable
import requests
import threading
import time


class Webhook:
    """
    A Python client for interacting with https://webhook.site.

    This class allows you to:
    - Create and delete webhook tokens.
    - Retrieve received requests.
    - Wait for new incoming requests.
    - Download file content uploaded with requests.
    - Set default responses for incoming requests.
    - Attach callback functions to be notified on new requests.
    - Access various token-specific URLs.

    Usage example:
        webhook = Webhook("your-token-uuid")
        print(webhook.url)
        webhook.set_response("Received", status=200)
        req = webhook.wait_for_request(timeout=30)
        files = webhook.download_request_content(req)
        for key, file_data in files.items():
            with open(f"{key}.{file_data['filename'].split('.')[-1]}", "wb") as f:
                f.write(file_data["bytes"])
    
    Attributes:
        token_id (str): The unique token ID from webhook.site.

    Methods:
        create_token: Class method to create a new token.
        get_requests: Retrieve past requests for the token.
        get_latest_request: Retrieve the most recent request.
        wait_for_request: Block until a new request arrives or timeout.
        set_response: Configure the default response for requests.
        download_request_content: Download files uploaded with a request.
        on_request: Attach a callback to be notified of new requests.
        delete_token: Delete the token.
        detach_callback: Remove a running callback.
        detach_all_callbacks: Stop all running callbacks.
    """

    BASE_URL = 'https://webhook.site'

    def __init__(self, uuid: str):
        """
        Initialize the Webhook with a token ID.

        Args:
            uuid (str): Unique token ID provided by webhook.site.
        """
        self.token_id = uuid
        self._on_request_threads: List[Dict[str, Any]] = []

    @staticmethod
    def create_token(**kwargs) -> EndpointConfig:
        """
        Creates a new token on webhook.site.

        Args:
            **kwargs: Additional parameters passed to requests.post.

        Raises:
            WebhookError: If the token creation fails.

        Returns:
            EndpointConfig: JSON response containing token details.
        """
        res = requests.post(f"{Webhook.BASE_URL}/token", **kwargs)
        res.raise_for_status()
        if res.status_code != 201:
            raise WebhookError(f"Token creation failed with status {res.status_code}: {res.text}")
        return res.json()

    @property
    def url(self) -> str:
        return f"https://webhook.site/{self.token_id}"

    @property
    def urls(self) -> List[str]:
        template_urls = [
            "https://webhook.site/{uuid}",
            "https://{uuid}.webhook.site",
            "{uuid}@emailhook.site",
            "{uuid}.dnshook.site"
        ]
        return [url.format(uuid=self.token_id) for url in template_urls]

    def get_requests(self, sorting="newest", per_page=50, page=1, date_from=None, date_to=None, query=None) -> List[WebhookRequest]:
        """
        Retrieves past requests received by the token.

        Args:
            sorting (str): Sort order.
            per_page (int): Number of requests per page.
            page (int): Page number.
            date_from (str): Filter from this date.
            date_to (str): Filter to this date.
            query (str): Query filter.

        Raises:
            WebhookError: If the request fetch fails.

        Returns:
            List[WebhookRequest]: List of received requests.
        """
        parameters = {k: v for k, v in locals().items() if k in ['sorting', 'per_page', 'page', 'date_from', 'date_to', 'query'] and v is not None}
        response = requests.get(f'{Webhook.BASE_URL}/token/{self.token_id}/requests', params=parameters)
        response.raise_for_status()
        return response.json()

    def get_latest_request(self) -> WebhookRequest:
        """
        Retrieves the most recent request received by the token.

        Raises:
            WebhookError: If the fetch fails.

        Returns:
            WebhookRequest: The latest request object.
        """
        response = requests.get(f'{Webhook.BASE_URL}/token/{self.token_id}/request/latest')
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def delete_token(self) -> None:
        """
        Deletes the webhook token.

        Raises:
            WebhookError: If the deletion fails.
        """
        response = requests.delete(f'{Webhook.BASE_URL}/token/{self.token_id}')
        response.raise_for_status()
        if response.status_code != 204:
            raise WebhookError(f"Failed to delete token: {response.status_code} - {response.text}")

    def wait_for_request(self, timeout: int = 15, interval: float = 0.1) -> WebhookRequest:
        """
        Waits for a new request to arrive.

        Args:
            timeout (int): How many seconds to wait.
            interval (float): Polling interval in seconds.

        Raises:
            TimeoutError: If no new request arrives in time.

        Returns:
            WebhookRequest: The new incoming request.
        """
        latest_req = self.get_latest_request()
        start_time = time.time()
        while time.time() - start_time < timeout:
            req = self.get_latest_request()
            if req and req != latest_req:
                return req
            time.sleep(interval)
        raise TimeoutError(f"Didn't receive a request in time. Timed out after {timeout} seconds.")

    def on_request(self, callback: Callable[[WebhookRequest], None], interval: float = 0.1) -> None:
        """
        Attaches a callback function that is triggered when a new request is received.

        Args:
            callback (Callable): Function to call with new request.
            interval (float): Polling interval in seconds.
        """
        def listen_to_requests(latest_req):
            while not kill_event.is_set():
                req = self.get_latest_request()
                if req and req != latest_req:
                    callback(req)
                    latest_req = req
                time.sleep(interval)

        kill_event = threading.Event()
        latest_req = self.get_latest_request()
        thread = threading.Thread(target=listen_to_requests, args=(latest_req,))
        self._on_request_threads.append({"thread": thread, "kill_event": kill_event})
        thread.start()

    def get_token_details(self) -> Dict[str, Any]:
        """
        Retrieves details about the token.

        Returns:
            dict: Token details from webhook.site.
        """
        response = requests.get(f"{self.BASE_URL}/token/{self.token_id}")
        response.raise_for_status()
        return response.json()

    def set_response(self, content, status=200, content_type="text/plain") -> Dict[str, Any]:
        """
        Sets the default response for incoming requests.

        Args:
            content (str): Response body.
            status (int): HTTP status code.
            content_type (str): MIME type.

        Raises:
            WebhookError: If setting response fails.

        Returns:
            dict: Response confirmation.
        """
        url = f"{self.BASE_URL}/token/{self.token_id}"
        payload = {
            "default_content": content,
            "default_status": status,
            "default_content_type": content_type,
        }
        res = requests.put(url, json=payload)
        res.raise_for_status()
        return res.json()

    def download_request_content(self, request: WebhookRequest) -> List[bytes]:
        """
        Downloads file content attached to a webhook request.

        Args:
            request (WebhookRequest): A webhook request object or dict containing request data.

        Raises:
            WebhookError: If the request object lacks an 'id' or 'uuid', or if downloading a file fails.

        Returns:
            dict: A dictionary where keys are file keys from the request, and values are dicts with:
                - 'id': File ID on webhook.site
                - 'filename': Original filename
                - 'name': Field name used in the form
                - 'bytes': Raw bytes of the file content
                - 'size': Size in bytes
                - 'content_type': MIME type of the file
        """
        
        if isinstance(request, dict):
            request_id = request.get('uuid')
        else:
            request_id = getattr(request, 'id', None)
        
        if not request_id:
            raise WebhookError("The provided request object does not have an 'id' or 'uuid' attribute/key.")
        
        out = {}
        print(request['files'].values())
        for key, file in request['files'].items():
            url = f"{self.BASE_URL}/token/{self.token_id}/request/{request_id}/download/{file['id']}"
            response = requests.get(url)
            if response.status_code != 200:
                raise WebhookError(f"Failed to download request content: {response.status_code} - {response.text}")
            out[key] = {"id": file['id'], "filename": file['filename'], "name": file['name'], "bytes": response.content, "size": file['size'], 'content_type': file['content_type']}
        
        return out



    @property
    def callbacks_on_request(self) -> List[Dict[str, Any]]:
        return self._on_request_threads

    def detach_callback(self, index: int) -> List[Dict[str, Any]]:
        """
        Detaches and stops a callback by index.

        Args:
            index (int): Index of callback to remove.

        Raises:
            IndexError: If index is out of range.

        Returns:
            List: Remaining callbacks.
        """
        if index >= len(self._on_request_threads):
            raise IndexError("Callback index out of range.")
        self._on_request_threads[index]["kill_event"].set()
        self._on_request_threads[index]["thread"].join()
        self._on_request_threads.pop(index)
        return self.callbacks_on_request

    def detach_all_callbacks(self) -> None:
        """
        Stops and removes all request listeners.
        """
        for entry in self._on_request_threads:
            entry["kill_event"].set()
            entry["thread"].join()
        self._on_request_threads.clear()

    def __enter__(self):
        """
        Enables context manager usage.
        Returns:
            Webhook: Self.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Cleans up on exit from context.
        """
        self.detach_all_callbacks()
        self.delete_token()