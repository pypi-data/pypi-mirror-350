# Prompt

Types:

```python
from system_prompt_storage.types import (
    PromptCreateResponse,
    PromptRetrieveResponse,
    PromptUpdateResponse,
    PromptListResponse,
    PromptRetrieveContentResponse,
    PromptUpdateMetadataResponse,
)
```

Methods:

- <code title="post /prompt">client.prompt.<a href="./src/system_prompt_storage/resources/prompt.py">create</a>(\*\*<a href="src/system_prompt_storage/types/prompt_create_params.py">params</a>) -> <a href="./src/system_prompt_storage/types/prompt_create_response.py">PromptCreateResponse</a></code>
- <code title="get /prompt/{id}">client.prompt.<a href="./src/system_prompt_storage/resources/prompt.py">retrieve</a>(id) -> str</code>
- <code title="put /prompt/{id}">client.prompt.<a href="./src/system_prompt_storage/resources/prompt.py">update</a>(path_id, \*\*<a href="src/system_prompt_storage/types/prompt_update_params.py">params</a>) -> str</code>
- <code title="get /prompts">client.prompt.<a href="./src/system_prompt_storage/resources/prompt.py">list</a>(\*\*<a href="src/system_prompt_storage/types/prompt_list_params.py">params</a>) -> <a href="./src/system_prompt_storage/types/prompt_list_response.py">PromptListResponse</a></code>
- <code title="delete /prompt/{id}">client.prompt.<a href="./src/system_prompt_storage/resources/prompt.py">delete</a>(id) -> None</code>
- <code title="get /prompt/{id}/content">client.prompt.<a href="./src/system_prompt_storage/resources/prompt.py">retrieve_content</a>(id, \*\*<a href="src/system_prompt_storage/types/prompt_retrieve_content_params.py">params</a>) -> str</code>
- <code title="put /prompt/{id}/metadata">client.prompt.<a href="./src/system_prompt_storage/resources/prompt.py">update_metadata</a>(path_id, \*\*<a href="src/system_prompt_storage/types/prompt_update_metadata_params.py">params</a>) -> str</code>
