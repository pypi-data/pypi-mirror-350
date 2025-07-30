# coding:utf-8
import json
import time
import asyncio
import httpx
import hashlib
from typing import Dict, Any, Optional, Union
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('AsyncQueryCompany')


class AsyncQueryCompany:
    """Asynchronous API client for Bainiu Data services."""

    def __init__(self, client_id: str = "", client_key: str = "",
                 host: str = "http://openapi.bainiudata.com", max_retries: int = 2,
                 timeout: float = 60.0):
        """
        Initialize the AsyncQueryCompany client.

        Args:
            client_id: Client ID for authentication
            client_key: Client key for authentication
            host: API host URL
            max_retries: Maximum number of retries for failed requests
            timeout: Request timeout in seconds
        """
        self.HOST = host
        self.client_id = client_id
        self.client_key = client_key
        self.max_retries = max_retries
        self.timeout = timeout
        logger.info("AsyncQueryCompany initialized with client_id: %s", client_id)

    def _get_headers(self) -> Dict[str, str]:
        """
        Generate authentication headers with current timestamp.

        Returns:
            Dictionary containing authentication headers
        """
        timespan = int(time.time())
        md5str = f'{self.client_id}-{timespan}-{self.client_key}'
        token = hashlib.md5(md5str.encode("utf-8")).hexdigest().upper()
        headers = {
            "CLIENTID": self.client_id,
            "AUTHORIZATION": token,
            "TIMESPAN": str(timespan),
            "Content-Type": "application/json"
        }
        return headers


    async def post_api(self, url: str, query_data: Union[Dict, str], refresh_auth: bool = False) -> Dict[str, Any]:
        """
        Make an asynchronous POST request to the API.

        Args:
            url: API endpoint URL (full URL)
            query_data: Request data as dictionary or JSON string
            refresh_auth: Force refresh of authentication headers

        Returns:
            API response parsed as dictionary

        Raises:
            httpx.HTTPError: If the request fails after maximum retries
            ValueError: If the response cannot be parsed as JSON
        """
        self.headers = self._get_headers()

        # Ensure query_data is a JSON string
        if isinstance(query_data, dict):
            data = json.dumps(query_data)
        else:
            data = query_data

        retries = 0
        last_error = None

        while retries <= self.max_retries:
            try:
                if retries > 0:
                    logger.info(f"Retry attempt {retries}/{self.max_retries}")
                    # Update headers with fresh token on retry
                    self.headers = self._get_headers()

                async with httpx.AsyncClient() as client:
                    logger.debug(f"Making POST request to {url}")
                    response = await client.post(
                        url=url,
                        content=data,
                        headers=self.headers,
                        timeout=self.timeout
                    )
                    # Check HTTP status code
                    response.raise_for_status()
                    # Try to decode the response as JSON
                    try:
                        resp_text = response.text.encode("utf-8").decode("unicode-escape")
                        result = json.loads(resp_text)
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse JSON response: {resp_text}")
                        raise ValueError(f"Invalid JSON response: {e}")

                    # Check for authorization errors in the response
                    if isinstance(result, dict) and result.get('code')=='200':
                        logger.info("Request successful")
                        return result
                    else:
                        logger.warning(f"Authorization Faild code:{result.get('code')} {json.dumps(result,ensure_ascii=False)}")
                        return result

            except (httpx.HTTPError, httpx.TimeoutException) as e:
                last_error = e
                logger.warning(f"Request failed: {e}")
                retries += 1
                if retries <= self.max_retries:
                    # Add exponential backoff
                    await asyncio.sleep(1 * (2 ** (retries - 1)))
                continue

        # If we've exhausted all retries
        logger.error(f"Maximum retries reached. Last error: {last_error}")
        raise last_error or httpx.RequestError("Failed after maximum retries")


async def get_company_detail(company_name: str = "重庆白牛科技有限公司",
                             key_type: str = "1",
                             version: str = "A1") -> Dict[str, Any]:
    """
    Asynchronously retrieve company details by name or identifier.

    Args:
        company_name: Company name or identifier
        key_type: Search type (1: name, 2: unified social credit code, 3: business registration number, 4: org code)
        version: API version

    Returns:
        Company details as dictionary
    """
    query = AsyncQueryCompany(client_id = "",
    client_key = "")
    url = f"{query.HOST}/openapi/common/company_detail/"

    data = {
        "key": company_name,
        "key_type": key_type,
        "version": version
    }

    try:
        result = await query.post_api(url, data)
        return result
    except Exception as e:
        logger.error(f"Error fetching company detail: {e}")
        raise


async def main():
    """Main entry point for the application."""
    try:
        result = await get_company_detail()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        logger.error(f"Application error: {e}")
        return 1
    return 0


if __name__ == "__main__":

    asyncio.run(main())