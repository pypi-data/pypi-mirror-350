# Prompts

Types:

```python
from system_prompt_storage.types import (
    Prompt,
    PromptRetrieveResponse,
    PromptListResponse,
    PromptRetrieveContentResponse,
)
```

Methods:

- <code title="post /prompt">client.prompts.<a href="./src/system_prompt_storage/resources/prompts.py">create</a>(\*\*<a href="src/system_prompt_storage/types/prompt_create_params.py">params</a>) -> <a href="./src/system_prompt_storage/types/prompt.py">Prompt</a></code>
- <code title="get /prompt/{id}">client.prompts.<a href="./src/system_prompt_storage/resources/prompts.py">retrieve</a>(id, \*\*<a href="src/system_prompt_storage/types/prompt_retrieve_params.py">params</a>) -> str</code>
- <code title="get /prompts">client.prompts.<a href="./src/system_prompt_storage/resources/prompts.py">list</a>(\*\*<a href="src/system_prompt_storage/types/prompt_list_params.py">params</a>) -> <a href="./src/system_prompt_storage/types/prompt_list_response.py">PromptListResponse</a></code>
- <code title="delete /prompt/{id}">client.prompts.<a href="./src/system_prompt_storage/resources/prompts.py">delete</a>(id) -> None</code>
- <code title="get /prompt/{id}/content">client.prompts.<a href="./src/system_prompt_storage/resources/prompts.py">retrieve_content</a>(id, \*\*<a href="src/system_prompt_storage/types/prompt_retrieve_content_params.py">params</a>) -> str</code>
