"""
Naxai Python SDK for interacting with the Naxai API.

This package provides client libraries for accessing Naxai's communication and customer
data management platform, offering both synchronous and asynchronous interfaces. The SDK
enables developers to integrate Naxai's voice, SMS, email, and customer data capabilities
into their Python applications with a clean, intuitive API.

Main components:
- NaxaiClient: Synchronous client for applications using traditional request-response patterns
- NaxaiAsyncClient: Asynchronous client for high-performance applications using asyncio
"""

from .async_client import NaxaiAsyncClient
from .client import NaxaiClient


__all__ = ["NaxaiAsyncClient", "NaxaiClient"]
