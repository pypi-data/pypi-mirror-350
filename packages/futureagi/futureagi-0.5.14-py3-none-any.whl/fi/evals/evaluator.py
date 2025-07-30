import inspect
import json
import logging
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

from requests import Response

import fi.evals.templates as templates_module
from fi.api.auth import APIKeyAuth, ResponseHandler
from fi.api.types import HttpMethod, RequestConfig
from fi.evals.templates import EvalTemplate
from fi.evals.types import BatchRunResult, EvalResult, EvalResultMetric
from fi.testcases import ConversationalTestCase, LLMTestCase, MLLMTestCase, TestCase
from fi.utils.errors import InvalidAuthError
from fi.utils.routes import Routes
from fi.utils.utils import get_keys_from_env, get_base_url_from_env


class EvalResponseHandler(ResponseHandler[BatchRunResult, None]):
    """Handles responses for evaluation requests"""

    @classmethod
    def _parse_success(cls, response: Response) -> BatchRunResult:
        return cls.convert_to_batch_results(response.json())

    @classmethod
    def _handle_error(cls, response: Response) -> None:
        if response.status_code == 400:
            response.raise_for_status()
        elif response.status_code == 403:
            raise InvalidAuthError()
        else:
            raise Exception(
                f"Error in evaluation: {response.status_code}, response: {response.text}"
            )

    @classmethod
    def convert_to_batch_results(cls, response: Dict[str, Any]) -> BatchRunResult:
        """
        Convert API response to BatchRunResult

        Args:
            response: Raw API response dictionary

        Returns:
            BatchRunResult containing evaluation results
        """
        eval_results = []

        for result in response.get("result", {}):
            for evaluation in result.get("evaluations", []):
                new_metadata = {}
                if evaluation.get("metadata"):
                    if isinstance(evaluation.get("metadata"), dict):
                        metadata = evaluation.get("metadata")
                    elif isinstance(evaluation.get("metadata"), str):
                        metadata = json.loads(evaluation.get("metadata"))
                    else:
                        metadata = {}
                    new_metadata["usage"] = metadata.get("usage", {})
                    new_metadata["cost"] = metadata.get("cost", {})
                    new_metadata["explanation"] = metadata.get("explanation", {})
                eval_results.append(
                    EvalResult(
                        data=evaluation.get("data"),
                        failure=evaluation.get("failure"),
                        reason=evaluation.get("reason", ""),
                        runtime=evaluation.get("runtime", 0),
                        metadata=new_metadata,
                        metrics=[
                            EvalResultMetric(id=metric["id"], value=metric["value"])
                            for metric in evaluation.get("metrics", [])
                        ],
                    )
                )

        return BatchRunResult(eval_results=eval_results)


class EvalInfoResponseHandler(ResponseHandler[dict, None]):
    """Handles responses for evaluation info requests"""

    @classmethod
    def _parse_success(cls, response: Response) -> dict:
        data = response.json()
        if "result" in data:
            return data["result"]
        else:
            raise Exception(f"Failed to get evaluation info: {data}")

    @classmethod
    def _handle_error(cls, response: Response) -> None:
        if response.status_code == 400:
            response.raise_for_status()
        if response.status_code == 403:
            raise InvalidAuthError()
        raise Exception(f"Failed to get evaluation info: {response.status_code}")


class Evaluator(APIKeyAuth):
    """Client for evaluating LLM test cases"""

    def __init__(
        self,
        fi_api_key: Optional[str] = None,
        fi_secret_key: Optional[str] = None,
        fi_base_url: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        Initialize the Eval Client

        Args:
            fi_api_key: API key
            fi_secret_key: Secret key
            fi_base_url: Base URL

        Keyword Args:
            timeout: Optional timeout value in seconds (default: 200)
            max_queue_bound: Optional maximum queue size (default: 5000)
            max_workers: Optional maximum number of workers (default: 8)
        """
        super().__init__(fi_api_key, fi_secret_key, fi_base_url, **kwargs)
        self._max_workers = kwargs.get("max_workers", 8)  # Default to 8 if not provided

    def evaluate(
        self,
        eval_templates: Union[EvalTemplate, List[EvalTemplate]],
        inputs: Union[
            TestCase,
            List[TestCase],
            LLMTestCase,
            List[LLMTestCase],
            MLLMTestCase,
            List[MLLMTestCase],
            ConversationalTestCase,
            List[ConversationalTestCase],
        ],
        timeout: Optional[int] = None,
        protect_flash: bool = False,
    ) -> BatchRunResult:
        """
        Run a single or batch of evaluations independently

        Args:
            eval_templates: Single evaluation template or list of evaluation templates
            inputs: Single LLM test case or list of LLM test cases
            timeout: Optional timeout value for the evaluation
            protect_flash: Whether to use the ProtectFlash system for content moderation

        Returns:
            BatchRunResult containing evaluation results

        Raises:
            ValidationError: If the inputs do not match the evaluation templates
            Exception: If the API request fails
        """
        # Convert single items to lists for consistent handling
        if not isinstance(eval_templates, list):
            eval_templates = [eval_templates]
        if not isinstance(inputs, list):
            inputs = [inputs]

        # Get evaluation template configs
        eval_templates = self._get_eval_configs(eval_templates)

        # Validate inputs
        self._validate_inputs(inputs, eval_templates)

        # Prepare payload
        payload = {
            "inputs": [test_case.model_dump() for test_case in inputs],
            "config": {
                template.eval_id: template.config for template in eval_templates
            },
        }
        
        # Add protect_flash parameter if it's enabled
        if protect_flash:
            payload["protect_flash"] = True
        all_results = []
        failed_inputs = []

        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            future_to_input = {}
            for test_case_input in inputs:
                payload = {
                    "inputs": [test_case_input.model_dump()],
                    "config": {
                        template.eval_id: template.config for template in eval_templates
                    },
                }
                future = executor.submit(
                    self.request,
                    config=RequestConfig(
                        method=HttpMethod.POST,
                        url=f"{self._base_url}/{Routes.evaluate.value}",
                        json=payload,
                        timeout=timeout or self._default_timeout,
                    ),
                    response_handler=EvalResponseHandler,
                )
                future_to_input[future] = test_case_input

            for future in as_completed(future_to_input):
                try:
                    response: BatchRunResult = future.result(timeout=timeout or self._default_timeout)
                    all_results.extend(response.eval_results)
                except TimeoutError:
                    input_case = future_to_input[future]
                    logging.error(f"Evaluation timed out for input: {input_case}")
                    failed_inputs.append(input_case)
                except Exception as exc:
                    input_case = future_to_input[future]
                    logging.error(f"Evaluation failed for input {input_case}: {str(exc)}")
                    failed_inputs.append(input_case)

        if failed_inputs:
            logging.warning(f"Failed to evaluate {len(failed_inputs)} inputs out of {len(inputs)} total inputs")

        return BatchRunResult(eval_results=all_results)

    def _validate_inputs(
        self,
        inputs: List[TestCase],
        eval_objects: List[EvalTemplate],
    ):
        """
        Validate the inputs against the evaluation templates

        Args:
            inputs: List of test cases to validate
            eval_objects: List of evaluation templates to validate against

        Returns:
            bool: True if validation passes

        Raises:
            Exception: If validation fails or templates don't share common tags
        """

        # First validate that all eval objects share at least one common tag
        if len(eval_objects) > 1:
            # Get sets of tags for each eval object
            tag_sets = [set(obj.eval_tags) for obj in eval_objects]

            # Find intersection of all tag sets
            common_tags = set.intersection(*tag_sets)

            if not common_tags:
                template_names = [obj.name for obj in eval_objects]
                raise Exception(
                    f"Evaluation templates {template_names} must share at least one common tag. "
                    f"Current tags for each template: {[list(tags) for tags in tag_sets]}"
                )

        # Then validate each eval object's required inputs
        for eval_object in eval_objects:
            eval_object.validate_config(eval_object.config)
            eval_object.validate_input(inputs)

        return True

    def _get_eval_configs(
        self, eval_templates: List[EvalTemplate]
    ) -> List[EvalTemplate]:

        for template in eval_templates:
            eval_id = template.eval_id
            eval_info = self._get_eval_info(eval_id)
            template.name = eval_info["name"]
            template.description = eval_info["description"]
            template.eval_tags = eval_info["eval_tags"]
            template.required_keys = eval_info["config"]["required_keys"]
            template.output = eval_info["config"]["output"]
            template.eval_type_id = eval_info["config"]["eval_type_id"]
            template.config_schema = (
                eval_info["config"]["config"] if "config" in eval_info["config"] else {}
            )
            template.criteria = eval_info["criteria"]
            template.choices = eval_info["choices"]
            template.multi_choice = eval_info["multi_choice"]
        return eval_templates

    @lru_cache(maxsize=100)
    def _get_eval_info(self, eval_id: str) -> Dict[str, Any]:
        url = (
            self._base_url
            + "/"
            + Routes.evaluate_template.value.format(eval_id=eval_id)
        )
        response = self.request(
            config=RequestConfig(method=HttpMethod.GET, url=url),
            response_handler=EvalInfoResponseHandler,
        )
        return response

    def list_evaluations(self):
        """
        Fetch information about all available evaluation templates by getting eval_info
        for each template class defined in templates.py.

        Returns:
            List[Dict[str, Any]]: List of evaluation template information dictionaries
        """
        eval_infos = []
        # Dynamically find and instantiate EvalTemplate subclasses
        for name, cls in inspect.getmembers(templates_module, inspect.isclass):
            # Ensure it's a subclass of EvalTemplate and not EvalTemplate itself
            if issubclass(cls, EvalTemplate) and cls is not EvalTemplate:
                try:
                    template_instance = cls()
                    eval_info = self._get_eval_info(template_instance.eval_id)
                    eval_infos.append(eval_info)
                except Exception as e:
                    # Handle cases where instantiation or fetching info might fail
                    raise Exception(f"Could not process template {name}: {e}")
        return eval_infos

evaluate = lambda eval_templates, inputs, timeout=None: Evaluator().evaluate(eval_templates, inputs, timeout)

list_evaluations = lambda: Evaluator().list_evaluations()