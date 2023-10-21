""" Retrier
This moule will retry any immediate errors that arise during the query. This is not responsible for running the same query / mutation again,
rather, it's responsible for modifying the query / mutation to make it work. Scenarios:
- We have a NON-NULL column that is selected for in the output, but the server is responding with NULL, you will get the following error:
  {'message': 'Cannot return null for non-nullable field Transaction.payer.'}.
  In this scenario, we will need to remove the payer key from the mutation / query output fields
"""

from fuzzer.fengine.retrier.utils import find_block_end, remove_lines_within_range
from utils.request_utils import send_graphql_request

import logging


class Retrier:
    def __init__(self, logger: logging.Logger):
        self.logger = logger.getChild(__name__)
        self.max_retries = 3

    def retry(self, url: str, payload: str, response: dict, retry_count) -> tuple[dict, bool]:
        """Retries the payload based on the error

        Args:
            url (str): The url of the endpoint
            payload (str): The payload (either a query or mutation)
            response (dict): The response containing the error
            retry_count (int): The number of times we've retried

        Returns:
            tuple[dict, bool]: The response, and whether the retry succeeded or not
        """
        error = response["errors"][0]
        if "Cannot return null for non-nullable field" in error["message"]:
            locations = error["locations"]
            for location in locations:
                payload = self.get_new_payload_for_retry_non_null(payload, location)
            self.logger.info(f"Retrying with new payload:\n {payload}")
            response = send_graphql_request(url, payload)
            if "errors" in response:
                if retry_count < self.max_retries:
                    return self.retry(url, payload, response, retry_count + 1)
                else:
                    return (response, False)
            else:
                return (response, True)
        else:
            return (response, False)

    def get_new_payload_for_retry_non_null(self, payload: str, location: dict) -> str:
        """Gets a new payload from the original payload, and the location of the error

        Args:
            payload (str): The payload
            error (dict): The error

        Returns:
            str: A string of the new payload
        """
        line_number = location["line"]
        block_end = find_block_end(payload, line_number - 1)
        new_payload = remove_lines_within_range(payload, line_number - 1, block_end)
        return new_payload
