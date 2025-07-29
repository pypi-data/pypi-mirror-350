"""
Contact events resource for the Naxai People SDK.

This module provides methods for recording and managing contact events in the Naxai platform,
allowing users to track customer interactions, behaviors, and activities. These events can
be used for contact segmentation, automation triggers, and analytics to better understand
customer engagement and journeys.

Available Functions:
    send(identifier, name=None, type_=None, timestamp=None, idempotency_key=None, data=None)
        Send an event for a specific contact.
        Records events like purchases, logins, page views etc. with optional metadata.

"""

import datetime
from typing import Literal, Optional
from pydantic import Field, validate_call

class EventsResource:
    """ events resource for people.contacts resource"""

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.headers = {"Content-Type": "application/json"}

    @validate_call
    def send(self,
            identifier: str,
            name: Optional[str] = None,
            type_: Optional[Literal["event"]] = Field(default=None),
            timestamp: Optional[int] = datetime.datetime.now(tz=datetime.timezone.utc),
            idempotency_key: Optional[str] = Field(default=None, max_length=200),
            data: Optional[dict[str,str]] = None):

        """
        Send an event for a specific contact in the Naxai People API.
        
        This method allows you to record events associated with a contact, such as
        "purchase_completed", "email_opened", or any custom event type. Events can be
        used for segmentation, automation triggers, and analytics.
        
        Args:
            identifier (str): The unique identifier of the contact. This can be the Naxai ID,
                email address, phone number, or external ID depending on your configuration.
            name (Optional[str]): The name of the event (e.g., "purchase_completed",
                "login", "page_viewed"). Required for meaningful event tracking.
            type_ (Optional[Literal["event"]]): The type of the event. Currently only
                "event" is supported. Defaults to None.
            timestamp (Optional[int]): The timestamp when the event occurred, in milliseconds
                since epoch. Defaults to the current UTC time.
            idempotency_key (Optional[str]): A unique key to prevent duplicate event
                submissions. If you provide the same key for multiple requests, only the
                first one will be processed. Max length is 200 characters.
            data (Optional[dict[str,str]]): Additional properties for the event as key-value
                pairs. These can be used for filtering in segments and providing context.
        
        Returns:
            None
        
        Raises:
            ValueError: If the identifier is empty or invalid.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to send events.
        
        Example:
            ```python
            # Send a purchase event with product details
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                response = client.people.contacts.events.send(
                    identifier="john.doe@example.com",  # Using email as identifier
                    name="purchase_completed",
                    timestamp=int(
                        datetime.datetime.now(tz=datetime.timezone.utc).timestamp() * 1000),
                    idempotency_key="order_12345",
                    data={
                        "product_id": "prod_123",
                        "product_name": "Premium Subscription",
                        "amount": "99.99",
                        "currency": "USD",
                        "payment_method": "credit_card"
                    }
                )
                print(f"Event sent successfully: {response}")
            ```
        
        Note:
            - The timestamp should be in milliseconds since epoch (Unix time * 1000)
            - Using an idempotency_key is recommended to prevent duplicate events
            - The data dictionary can contain any custom properties relevant to the event
            - Events are processed asynchronously and may not be immediately available
              for segmentation
        """
        data = {
            "name": name,
            "type": type_,
            "timestamp": timestamp,
            "idempotencyKey": idempotency_key,
            "data": data
        }
        # pylint: disable=protected-access
        return self._client._request("POST",
                                     self.root_path + "/" + identifier + "/events",
                                     json=data,
                                     headers=self.headers)
