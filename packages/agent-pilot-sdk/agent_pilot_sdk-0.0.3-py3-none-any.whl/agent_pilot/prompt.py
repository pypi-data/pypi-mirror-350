import time
import requests
from typing import Dict, Any, List, Optional, TypedDict
import copy
from agent_pilot.models import PromptVersion
import logging
import chevron  # type: ignore
import traceback
from agent_pilot.eval.models import Metric
from agent_pilot.http_client import get_http_client

logger = logging.getLogger(__name__)


class CacheEntry(TypedDict):
    timestamp: float
    prompt_version: PromptVersion


templateCache: Dict[str, CacheEntry] = {}

DEFAULT_EXCLUDE_KEYS = ['model']


def get_prompt(
    task_id: str, version: str, api_key: Optional[str] = None, api_url: Optional[str] = None
) -> PromptVersion:
    """
    Fetches the latest version of a template based on a given slug.
    If a cached version is available and recent (less than 60 seconds old),
    it will return the cached data. Otherwise, it makes an HTTP GET request
    to fetch the template from the specified or default API.

    Parameters:
        slug (str): Unique identifier for the template.
        app_id (str, optional): Application ID for authentication. Defaults to config's app ID.
        api_url (str, optional): API base URL. Defaults to config's API URL.

    Returns:
        dict: JSON response containing template data.

    Raises:
        TemplateError: If fetching the template fails.
    """
    try:
        global templateCache
        now = time.time() * 1000
        cache_entry = templateCache.get(task_id)

        if cache_entry and now - cache_entry['timestamp'] < 60000:
            return cache_entry['prompt_version']

        action = 'GetPromptTemplate'

        body = {
            'TaskId': task_id,
            'PromptVersion': version,
        }
        response_data, response_status_code = get_http_client().post(
            action=action, data=body, api_key=api_key, api_url=api_url
        )

        if response_status_code == 401:
            raise RuntimeError('Invalid or unauthorized API credentials')

        if response_status_code != 200:
            raise RuntimeError(f'Error fetching template: {response_status_code} - {response_data}')

        prompt_version_dict = response_data.get('Result', {}).get('prompt_version', None)
        if prompt_version_dict is None:
            raise RuntimeError('Template not found, are the task ID and version correct?')
        print(f'prompt_version_dict = {prompt_version_dict}')
        prompt_version = PromptVersion(**prompt_version_dict)
        templateCache[task_id] = {'timestamp': now, 'prompt_version': prompt_version}
        return prompt_version

    except requests.exceptions.RequestException as e:
        traceback.print_exc()
        raise RuntimeError(f'Network error while fetching template: {str(e)}') from e
    except Exception as e:
        traceback.print_exc()
        raise RuntimeError(f'Error fetching template: {str(e)}') from e


def render(
    task_id: str,
    version: str,
    variables: Dict[str, Any],
    api_key: Optional[str] = None,
    api_url: Optional[str] = None,
    exclude_keys: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Renders a template by populating it with the provided data.
    Retrieves the raw template, then uses `chevron.render` to substitute variables.

    Parameters:
        slug (str): Template identifier.
        variables (dict): Data for template rendering.
        app_id (str, optional): Application ID for authentication.
        api_url (str, optional): API base URL.

    Returns:
        dict: Rendered template with headers and extra metadata.

    Raises:
        TemplateError: If rendering fails.
    """
    if exclude_keys is None:
        exclude_keys = DEFAULT_EXCLUDE_KEYS

    try:
        prompt_version: PromptVersion = get_prompt(task_id, version, api_key, api_url)

        if prompt_version.messages == 'Template not found, is the project ID correct?':
            raise RuntimeError('Template not found, are the task ID and version correct?')

        content = copy.deepcopy(prompt_version.messages)
        model_name = copy.deepcopy(prompt_version.model_name)
        temperature = copy.deepcopy(prompt_version.temperature)
        top_p = copy.deepcopy(prompt_version.top_p)
        variables = copy.deepcopy(variables)
        extra_headers = {'Task-Id': str(task_id), 'Version': str(version)}

        messages = []

        if content is not None:  # 处理content可能为None的情况
            for message in content:
                if 'Role' in message:
                    message['role'] = message['Role'].lower()
                    del message['Role']
                if 'Content' in message:
                    message['content'] = message['Content']
                    del message['Content']
                # TODO: make this logic pydantic model validation
                if isinstance(message['content'], list):
                    for item in message['content']:
                        if 'Type' in item:
                            item['type'] = item['Type'].lower()
                            del item['Type']
                        if 'Text' in item:
                            item['text'] = item['Text']
                            del item['Text']
                        if 'ImageUrl' in item:
                            item['image_url'] = item['ImageUrl']
                            del item['ImageUrl']
                        if 'text' in item:
                            item['text'] = chevron.render(item['text'], variables)
                        if 'image_url' in item:
                            item['image_url'] = chevron.render(item['image_url'], variables)
                elif isinstance(message['content'], str):
                    message['content'] = chevron.render(message['content'], variables)

                messages.append(message)

        input_dict = {
            'messages': messages,
            'task_id': task_id,
            'version': version,
            'model': model_name,
            'temperature': temperature,
            'top_p': top_p,
            'extra_headers': extra_headers,
            'variables': variables,
            'prompt_template': prompt_version.messages,
        }

        if exclude_keys:
            for key in exclude_keys:
                input_dict.pop(key, None)

        return input_dict

    except Exception as e:
        traceback.print_exc()
        raise RuntimeError(f'Error rendering template: {str(e)}') from e


def get_metric(task_id: str, version: str, api_key: str | None = None, api_url: str | None = None) -> Metric:
    """
    Fetches the latest version of a metric based on a given slug.
    """
    # Not yet implemented, return empty string as placeholder
    prompt_version: PromptVersion = get_prompt(task_id, version, api_key, api_url)

    if not prompt_version.criteria:
        raise RuntimeError('No eval dimension found, are the task ID and version correct?')

    metric: Metric = Metric(criteria=prompt_version.criteria)
    return metric


def list_prompts(
    task_id: str,
    api_key: str | None = None,
    api_url: str | None = None,
) -> List[PromptVersion]:
    """
    Lists all templates for a given task ID.

    Parameters:
        task_id (str): The ID of the task to list templates for.
        api_key (str | None): The API key to use for authentication.
        api_url (str | None): The API URL to use for the request.

    Returns:
        List[PromptVersion]: A list of PromptVersion objects.
    """
    try:
        action = 'ListPromptTemplates'

        body = {
            'TaskId': task_id,
        }
        response_data, response_status_code = get_http_client().post(
            action=action, data=body, api_key=api_key, api_url=api_url
        )

        if response_status_code == 401:
            raise RuntimeError('Invalid or unauthorized API credentials')

        if response_status_code != 200:
            raise RuntimeError(f'Error fetching template: {response_status_code} - {response_data}')

        prompt_version_dicts = response_data.get('Result', {}).get('prompt_versions', None)
        if prompt_version_dicts is None:
            raise RuntimeError('Template not found, are the task ID and version correct?')
        prompt_versions = [PromptVersion(**prompt_version_dict) for prompt_version_dict in prompt_version_dicts]
        return prompt_versions

    except requests.exceptions.RequestException as e:
        traceback.print_exc()
        raise RuntimeError(f'Network error while fetching template: {str(e)}') from e
    except Exception as e:
        traceback.print_exc()
        raise RuntimeError(f'Error fetching template: {str(e)}') from e
