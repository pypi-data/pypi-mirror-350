"""
VectorDBCloud Python Client
Main client class for interacting with VectorDBCloud API
"""

import requests
from typing import Dict, List, Optional, Any, Union
from .exceptions import VectorDBCloudError, AuthenticationError, APIError

class VectorDBCloud:
    """
    VectorDBCloud API Client

    Official Python client for VectorDBCloud API with updated base URL.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.vectordbcloud.com/prod",
        timeout: int = 30
    ):
        """
        Initialize VectorDBCloud client.

        Args:
            api_key: Your VectorDBCloud API key
            base_url: API base URL (defaults to production)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'VectorDBCloud-Python-SDK/1.1.0'
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to API.

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            API response data

        Raises:
            AuthenticationError: Invalid API key
            APIError: API error response
            VectorDBCloudError: General SDK error
        """
        url = self.base_url + endpoint

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )

            if response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            elif response.status_code == 403:
                raise AuthenticationError("Access forbidden")
            elif not response.ok:
                raise APIError("API error: " + str(response.status_code) + " - " + response.text)

            return response.json() if response.content else {}

        except requests.exceptions.RequestException as e:
            raise VectorDBCloudError("Request failed: " + str(e))

    # Core API methods
    def health(self) -> Dict[str, Any]:
        """Check API health status."""
        return self._request('GET', '/core/health')

    def version(self) -> Dict[str, Any]:
        """Get API version information."""
        return self._request('GET', '/core/version')

    # Authentication methods
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        User login.

        Args:
            email: User email
            password: User password

        Returns:
            Login response with token
        """
        return self._request('POST', '/auth/login', {
            'email': email,
            'password': password
        })

    def logout(self) -> Dict[str, Any]:
        """User logout."""
        return self._request('POST', '/auth/logout')

    # Vector search methods
    def search_vector(
        self,
        vector: List[float],
        limit: int = 10,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Perform vector similarity search.

        Args:
            vector: Query vector
            limit: Maximum results to return
            filters: Optional search filters

        Returns:
            Search results
        """
        data = {
            'vector': vector,
            'limit': limit
        }
        if filters:
            data['filters'] = filters

        return self._request('POST', '/search/vector', data)

    def search_semantic(
        self,
        text: str,
        limit: int = 10,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Perform semantic text search.

        Args:
            text: Query text
            limit: Maximum results to return
            filters: Optional search filters

        Returns:
            Search results
        """
        data = {
            'text': text,
            'limit': limit
        }
        if filters:
            data['filters'] = filters

        return self._request('POST', '/search/semantic', data)

    # AI methods
    def generate_embedding(self, text: str) -> Dict[str, Any]:
        """
        Generate text embedding.

        Args:
            text: Input text

        Returns:
            Embedding vector
        """
        return self._request('POST', '/ai/embedding', {'text': text})

    def generate_text(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Generate text using AI.

        Args:
            prompt: Input prompt
            **kwargs: Additional generation parameters

        Returns:
            Generated text
        """
        data = {'prompt': prompt}
        data.update(kwargs)
        return self._request('POST', '/ai/genai', data)

    # Billing methods
    def get_usage(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return self._request('GET', '/billing/usage')

    def get_invoices(self) -> Dict[str, Any]:
        """Get billing invoices."""
        return self._request('GET', '/billing/invoices')

    # Vector database connections
    def connect_weaviate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Connect to Weaviate database."""
        return self._request('POST', '/vectordb/weaviate', config)

    def connect_pinecone(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Connect to Pinecone database."""
        return self._request('POST', '/vectordb/pinecone', config)

    def connect_chroma(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Connect to ChromaDB database."""
        return self._request('POST', '/vectordb/chromadb', config)

    def connect_qdrant(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Connect to Qdrant database."""
        return self._request('POST', '/vectordb/qdrant', config)

    def connect_milvus(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Connect to Milvus database."""
        return self._request('POST', '/vectordb/milvus', config)

    # Generic request method
    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make generic API request.

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            API response
        """
        return self._request(method, endpoint, data, params)
