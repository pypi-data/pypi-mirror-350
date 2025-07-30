import abc
import asyncio
from typing import List, Dict, Any, Union
from concurrent.futures import ThreadPoolExecutor

import httpx
from pydantic import TypeAdapter

from zenetics.models.evaluator import EvaluatorAssignment
from zenetics.models.generation import Generation
from zenetics.models.test_case import TestCase
from zenetics.models.test_run import EvaluatorResult, TestRun
from zenetics.models.test_suite import TestSuite


class ZeneticsAPIError(Exception):
    """General exception for Zenetics API errors."""

    pass


class ZeneticsAPIConnectionError(ZeneticsAPIError):
    """Raised when Zenetics API cannot be reached."""

    pass


class ZeneticsAPIClientInterface(abc.ABC):
    @abc.abstractmethod
    def get_test_suite(self, suite_id: str) -> TestSuite:
        pass

    @abc.abstractmethod
    def get_test_cases(self, suite_id: str) -> List[TestCase]:
        pass

    @abc.abstractmethod
    def get_evaluators(self, suite_id: str) -> List[EvaluatorAssignment]:
        pass

    @abc.abstractmethod
    def list_test_suites(self) -> List[TestSuite]:
        pass

    @abc.abstractmethod
    def evaluate(
        self,
        test_suite_id: int,
        test_case: TestCase,
        evaluator: EvaluatorAssignment,
        generation: Generation,
    ) -> EvaluatorResult:
        pass

    @abc.abstractmethod
    async def evaluate_async(
        self,
        test_suite_id: int,
        test_case: TestCase,
        evaluator: EvaluatorAssignment,
        generation: Generation,
    ) -> EvaluatorResult:
        pass

    @abc.abstractmethod
    async def evaluate_batch(
        self,
        test_suite_id: int,
        evaluation_items: List[Dict[str, Any]],
        max_concurrent: int = 5,
    ) -> List[EvaluatorResult]:
        pass

    @abc.abstractmethod
    def check_connection(self) -> bool:
        pass


class ZeneticsAPIClient(ZeneticsAPIClientInterface):
    def __init__(
        self, api_key: str, api_url: str, portal_url: str, max_workers: int = 2
    ):
        self.api_key = api_key
        self.api_url = api_url
        self.portal_url = portal_url
        self.max_workers = max_workers

        # Synchronous client
        self._client = httpx.Client(
            base_url=self.api_url,
            headers={
                "X-ZENETICS-API-KEY": self.api_key,
                "Accept": "application/json",
            },
            timeout=60.0,
        )

        # Thread pool for concurrent operations
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

        # Async client (lazy initialization)
        self._async_client = None

    def _get_async_client(self) -> httpx.AsyncClient:
        """
        Lazy initialization of the async client.

        Returns:
            httpx.AsyncClient: The async HTTP client
        """
        if self._async_client is None or self._async_client.is_closed:
            self._async_client = httpx.AsyncClient(
                base_url=self.api_url,
                headers={
                    "X-ZENETICS-API-KEY": self.api_key,
                    "Accept": "application/json",
                },
                timeout=60.0,
            )
        return self._async_client

    async def _close_async_client(self):
        """Close the async client if it exists and is open."""
        if self._async_client and not self._async_client.is_closed:
            await self._async_client.aclose()
            self._async_client = None

    def __del__(self):
        """Cleanup resources on object destruction."""
        if hasattr(self, "_client") and self._client:
            self._client.close()

        if hasattr(self, "_executor") and self._executor:
            self._executor.shutdown(wait=False)

        # For async client, we can't use await in __del__, so we'll rely
        # on garbage collection or explicit close calls

    def get_test_suite(self, suite_id: str) -> TestSuite:
        """
        Fetch a test suite by ID from the Zenetics API.

        Args:
            suite_id: ID of the test suite to fetch

        Returns:
            TestSuite: The requested test suite

        Raises:
            ZeneticsAPIError: If the API request fails
        """
        try:
            response = self._client.get(f"/v1/runner/testsuites/{suite_id}")
            response.raise_for_status()

            # Parse response data
            data = response.json()

            # Create TestSuite instance from response data
            return TestSuite.model_validate(data)

        except httpx.TimeoutException:
            raise ZeneticsAPIError(
                f"Request timed out while fetching test suite {suite_id}"
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ZeneticsAPIError(f"Test suite {suite_id} not found")
            elif e.response.status_code == 401:
                raise ZeneticsAPIError("Invalid API key")
            elif e.response.status_code == 403:
                raise ZeneticsAPIError("Insufficient permissions to access test suite")
            else:
                raise ZeneticsAPIError(f"HTTP error occurred: {str(e)}")
        except httpx.RequestError as e:
            raise ZeneticsAPIError(f"Request failed: {str(e)}")
        except ValueError as e:
            raise ZeneticsAPIError(f"Failed to parse API response: {str(e)}")
        except Exception as e:
            raise ZeneticsAPIError(f"Unexpected error: {str(e)}")

    def get_test_cases(self, suite_id: str) -> List[TestCase]:
        """
        Fetch test cases for a specific test suite from the Zenetics API.

        Args:
            suite_id: ID of the test suite

        Returns:
            List[TestCase]: List of test cases for the suite

        Raises:
            ZeneticsAPIError: If the API request fails
        """
        try:
            response = self._client.get(f"/v1/runner/testsuites/{suite_id}/testcases")
            response.raise_for_status()

            data = response.json()

            # Parse the response into TestCase objects
            return [TestCase.model_validate(test_case) for test_case in data]

        except httpx.TimeoutException:
            raise ZeneticsAPIError("Request timed out while fetching test cases")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ZeneticsAPIError("Invalid API key")
            elif e.response.status_code == 403:
                raise ZeneticsAPIError("Insufficient permissions to access test cases")
            elif e.response.status_code == 404:
                raise ZeneticsAPIError(f"Test suite {suite_id} not found")
            else:
                raise ZeneticsAPIError(f"HTTP error occurred: {str(e)}")
        except httpx.RequestError as e:
            raise ZeneticsAPIError(f"Request failed: {str(e)}")
        except ValueError as e:
            raise ZeneticsAPIError(f"Failed to parse API response: {str(e)}")
        except Exception as e:
            raise ZeneticsAPIError(f"Unexpected error: {str(e)}")

    def get_evaluators(self, suite_id: str) -> List[EvaluatorAssignment]:
        """
        Fetch evaluators assigned to a test suite.

        Args:
            suite_id: ID of the test suite

        Returns:
            List of EvaluatorAssignment objects

        Raises:
            ZeneticsAPIError: If the API request fails
        """
        try:
            # Make API request
            response = self._client.get(f"/v1/runner/testsuites/{suite_id}/evaluators")
            response.raise_for_status()

            # Parse response data
            data = response.json()

            # Use TypeAdapter for parsing list of EvaluatorAssignment
            adapter = TypeAdapter(List[EvaluatorAssignment])
            return adapter.validate_python(data)

        except httpx.TimeoutException:
            raise ZeneticsAPIError(
                f"Request timed out while fetching evaluators for test suite {suite_id}"
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ZeneticsAPIError(f"Test suite {suite_id} not found")
            elif e.response.status_code == 401:
                raise ZeneticsAPIError("Invalid API key")
            elif e.response.status_code == 403:
                raise ZeneticsAPIError("Insufficient permissions to access evaluators")
            else:
                raise ZeneticsAPIError(
                    f"HTTP error {e.response.status_code} while fetching evaluators"
                )
        except httpx.RequestError as e:
            raise ZeneticsAPIError(f"Network error while fetching evaluators: {str(e)}")
        except ValueError as e:
            raise ZeneticsAPIError(f"Failed to parse evaluators response: {str(e)}")
        except Exception as e:
            raise ZeneticsAPIError(
                f"Unexpected error while fetching evaluators: {str(e)}"
            )

    def list_test_suites(self) -> List[TestSuite]:
        """
        Fetch all test suites from the Zenetics API.

        Returns:
            List[TestSuite]: List of test suites

        Raises:
            ZeneticsAPIError: If the API request fails
            ValueError: If the response cannot be parsed
        """
        try:
            response = self._client.get("/v1/runner/testsuites")
            response.raise_for_status()

            data = response.json()

            # Parse the response into TestSuite objects
            return [TestSuite.model_validate(suite) for suite in data]

        except httpx.TimeoutException:
            raise ZeneticsAPIError("Request timed out while fetching test suites")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ZeneticsAPIError("Invalid API key")
            elif e.response.status_code == 403:
                raise ZeneticsAPIError("Insufficient permissions to list test suites")
            elif e.response.status_code == 404:
                raise ZeneticsAPIError("Test suites endpoint not found")
            else:
                raise ZeneticsAPIError(f"HTTP error occurred: {str(e)}")
        except httpx.RequestError as e:
            raise ZeneticsAPIError(f"Request failed: {str(e)}")
        except ValueError as e:
            raise ZeneticsAPIError(f"Failed to parse API response: {str(e)}")
        except Exception as e:
            raise ZeneticsAPIError(f"Unexpected error: {str(e)}")

    def create_test_run(self, test_run: TestRun) -> str:
        """
        Create a new test run on the Zenetics API.

        Returns:
            Test Run URl: URl of the test run in Zenetics.

        Raises:
            ZeneticsAPIError: If the API request fails
        """
        try:
            # Make API request
            response = self._client.post(
                "/v1/runner/testruns", json=test_run.model_dump()
            )
            response.raise_for_status()

            # Parse response data
            data = response.json()

            # generate the url with the test run id
            test_run_id = data["id"]
            application_id = data["applicationId"]
            test_run_url = f"{self.portal_url}/test-management/apps/"
            test_run_url += f"{application_id}/test-runs/{test_run_id}"

            return test_run_url

        except httpx.TimeoutException:
            raise ZeneticsAPIError("Request timed out while creating test run")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ZeneticsAPIError("Invalid API key")
            elif e.response.status_code == 403:
                raise ZeneticsAPIError("Insufficient permissions to create test runs")
            elif e.response.status_code == 400:
                # Try to get detailed error message from response
                try:
                    error_data = e.response.json()
                    error_message = error_data.get("message", str(e))
                    raise ZeneticsAPIError(f"Invalid test run data: {error_message}")
                except Exception as e:
                    raise ZeneticsAPIError(f"Invalid test run data: {str(e)}")
            else:
                raise ZeneticsAPIError(
                    f"HTTP error {e.response.status_code} while creating test run"
                )
        except httpx.RequestError as e:
            raise ZeneticsAPIError(f"Network error while creating test run: {str(e)}")
        except Exception as e:
            raise ZeneticsAPIError(
                f"Unexpected error while creating test run: {str(e)}"
            )

    def _prepare_evaluation_data(
        self,
        test_suite_id: int,
        test_case: TestCase,
        evaluator: EvaluatorAssignment,
        generation: Generation,
    ) -> Dict[str, Any]:
        """
        Prepare the data structure for an evaluation request.

        Args:
            test_suite_id: ID of the test suite
            test_case: TestCase object
            evaluator: EvaluatorAssignment object
            generation: Generation object

        Returns:
            Dict[str, Any]: Formatted request data
        """
        return {
            "testSuiteId": test_suite_id,
            "testCaseId": test_case.id,
            "evaluatorAssignmentId": evaluator.id,
            "generation": {
                "output": generation.output,
                "retrievalContext": generation.retrieval_context,
                "metadata": generation.metadata.model_dump(),
            },
        }

    def evaluate(
        self,
        test_suite_id: int,
        test_case: TestCase,
        evaluator: EvaluatorAssignment,
        generation: Generation,
    ) -> EvaluatorResult:
        """
        Run evaluation for test case and evaluator on the Zenetics API.

        Args:
            test_suite_id: ID of the test suite
            test_case: TestCase object
            evaluator: EvaluatorAssignment object
            generation: Generation object

        Returns:
            EvaluatorResult: The result of the evaluation

        Raises:
            ZeneticsAPIError: If the API request fails
        """
        evaluation_request_data = self._prepare_evaluation_data(
            test_suite_id, test_case, evaluator, generation
        )

        try:
            # Make API request
            response = self._client.post(
                "/v1/runner/evaluations", json=evaluation_request_data
            )
            response.raise_for_status()

            # Parse response data
            evaluator_result = EvaluatorResult.model_validate(response.json())
            return evaluator_result

        except httpx.TimeoutException:
            raise ZeneticsAPIError("Request timed out while evaluating test case")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ZeneticsAPIError("Invalid API key")
            elif e.response.status_code == 403:
                raise ZeneticsAPIError(
                    "Insufficient permissions to evaluate test cases"
                )
            elif e.response.status_code == 400:
                # Try to get detailed error message from response
                try:
                    error_data = e.response.json()
                    error_message = error_data.get("message", str(e))
                    raise ZeneticsAPIError(f"Invalid evaluation data: {error_message}")
                except Exception as e:
                    raise ZeneticsAPIError(f"Invalid evaluation data: {str(e)}")
            else:
                raise ZeneticsAPIError(
                    f"HTTP error {e.response.status_code} while evaluating test case"
                )
        except httpx.RequestError as e:
            raise ZeneticsAPIError(
                f"Network error while evaluating test case: {str(e)}"
            )
        except Exception as e:
            raise ZeneticsAPIError(
                f"Unexpected error while evaluating test case: {str(e)}"
            )

    async def evaluate_async(
        self,
        test_suite_id: int,
        test_case: TestCase,
        evaluator: EvaluatorAssignment,
        generation: Generation,
    ) -> EvaluatorResult:
        """
        Run evaluation asynchronously for test case and evaluator on the Zenetics API.

        Args:
            test_suite_id: ID of the test suite
            test_case: TestCase object
            evaluator: EvaluatorAssignment object
            generation: Generation object

        Returns:
            EvaluatorResult: The result of the evaluation

        Raises:
            ZeneticsAPIError: If the API request fails
        """
        evaluation_request_data = self._prepare_evaluation_data(
            test_suite_id, test_case, evaluator, generation
        )

        client = self._get_async_client()

        try:
            # Make API request
            response = await client.post(
                "/v1/runner/evaluations", json=evaluation_request_data
            )
            response.raise_for_status()

            # Parse response data
            evaluator_result = EvaluatorResult.model_validate(response.json())
            return evaluator_result

        except httpx.TimeoutException:
            raise ZeneticsAPIError("Request timed out while evaluating test case")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ZeneticsAPIError("Invalid API key")
            elif e.response.status_code == 403:
                raise ZeneticsAPIError(
                    "Insufficient permissions to evaluate test cases"
                )
            elif e.response.status_code == 400:
                # Try to get detailed error message from response
                try:
                    error_data = e.response.json()
                    error_message = error_data.get("message", str(e))
                    raise ZeneticsAPIError(f"Invalid evaluation data: {error_message}")
                except Exception as e:
                    raise ZeneticsAPIError(f"Invalid evaluation data: {str(e)}")
            else:
                raise ZeneticsAPIError(
                    f"HTTP error {e.response.status_code} while evaluating test case"
                )
        except httpx.RequestError as e:
            raise ZeneticsAPIError(
                f"Network error while evaluating test case: {str(e)}"
            )
        except Exception as e:
            raise ZeneticsAPIError(
                f"Unexpected error while evaluating test case: {str(e)}"
            )

    async def evaluate_batch(
        self,
        test_suite_id: int,
        evaluation_items: List[Dict[str, Any]],
        max_concurrent: int = None,
    ) -> List[Union[EvaluatorResult, Exception]]:
        """
        Run multiple evaluations in parallel asynchronously.

        Args:
            test_suite_id: ID of the test suite
            evaluation_items: List of dictionaries containing test_case, evaluator,
                              and generation. Each dict should have keys:
                              "test_case", "evaluator", "generation"
            max_concurrent: Maximum number of concurrent evaluations
                            (defaults to self.max_workers)

        Returns:
            List of EvaluatorResult objects or Exceptions for failed evaluations

        Note:
            This method doesn't raise exceptions for individual evaluation
            failures. Instead, it returns a mix of EvaluatorResult objects
            and Exceptions.
        """
        if max_concurrent is None:
            max_concurrent = self.max_workers

        # Create a semaphore to limit concurrency
        semaphore = asyncio.Semaphore(max_concurrent)

        async def _evaluate_with_semaphore(item):
            async with semaphore:
                try:
                    return await self.evaluate_async(
                        test_suite_id=test_suite_id,
                        test_case=item["test_case"],
                        evaluator=item["evaluator"],
                        generation=item["generation"],
                    )
                except Exception as e:
                    # Return exception instead of raising it to avoid stopping all tasks
                    return e

        # Schedule all evaluations
        tasks = [_evaluate_with_semaphore(item) for item in evaluation_items]

        # Wait for all evaluations to complete
        results = await asyncio.gather(*tasks)

        return results

    def evaluate_parallel(
        self,
        test_suite_id: int,
        evaluation_items: List[Dict[str, Any]],
        max_concurrent: int = None,
    ) -> List[Union[EvaluatorResult, Exception]]:
        """
        Run multiple evaluations in parallel using ThreadPoolExecutor.
        This is a synchronous wrapper around evaluate_batch for non-async code.

        Args:
            test_suite_id: ID of the test suite
            evaluation_items: List of dictionaries containing test_case,
                              evaluator, and generation. Each dict should
                              have keys: "test_case", "evaluator", "generation"
            max_concurrent: Maximum number of concurrent evaluations
                            (defaults to self.max_workers)

        Returns:
            List of EvaluatorResult objects or Exceptions for
            failed evaluations.
        """

        async def _run_batch():
            try:
                return await self.evaluate_batch(
                    test_suite_id=test_suite_id,
                    evaluation_items=evaluation_items,
                    max_concurrent=max_concurrent,
                )
            finally:
                # Ensure async client is closed
                await self._close_async_client()

        # Run the async function in an event loop
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(_run_batch())
        finally:
            loop.close()

    def check_connection(self) -> bool:
        """
        Check if the Zenetics API can be reached.

        Returns:
            bool: True if connection is successful

        Raises:
            ZeneticsAPIError: If the connection check fails
        """
        try:
            self.list_test_suites()
            return True
        except Exception as e:
            raise ZeneticsAPIError(f"Connection check failed: {str(e)}")

    async def check_connection_async(self) -> bool:
        """
        Check if the Zenetics API can be reached asynchronously.

        Returns:
            bool: True if connection is successful

        Raises:
            ZeneticsAPIError: If the connection check fails
        """
        client = self._get_async_client()

        try:
            response = await client.get("/v1/runner/testsuites")
            response.raise_for_status()
            return True
        except Exception as e:
            raise ZeneticsAPIError(f"Async connection check failed: {str(e)}")
