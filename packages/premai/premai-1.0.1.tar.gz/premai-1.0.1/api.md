# Chat

Types:

```python
from premai.types import (
    ChatCreateCompletionResponse,
    ChatRetrieveInternalModelsResponse,
    ChatRetrieveModelsResponse,
)
```

Methods:

- <code title="post /api/v1/chat/completions">client.chat.<a href="./src/premai/resources/chat.py">create_completion</a>(\*\*<a href="src/premai/types/chat_create_completion_params.py">params</a>) -> <a href="./src/premai/types/chat_create_completion_response.py">ChatCreateCompletionResponse</a></code>
- <code title="get /api/v1/chat/internalModels">client.chat.<a href="./src/premai/resources/chat.py">retrieve_internal_models</a>() -> <a href="./src/premai/types/chat_retrieve_internal_models_response.py">object</a></code>
- <code title="get /api/v1/chat/models">client.chat.<a href="./src/premai/resources/chat.py">retrieve_models</a>() -> <a href="./src/premai/types/chat_retrieve_models_response.py">ChatRetrieveModelsResponse</a></code>

# Internal

## Chat

Types:

```python
from premai.types.internal import (
    ChatCreateCompletionResponse,
    ChatListInternalModelsResponse,
    ChatListModelsResponse,
)
```

Methods:

- <code title="post /api/internal/chat/completions">client.internal.chat.<a href="./src/premai/resources/internal/chat.py">create_completion</a>(\*\*<a href="src/premai/types/internal/chat_create_completion_params.py">params</a>) -> <a href="./src/premai/types/internal/chat_create_completion_response.py">ChatCreateCompletionResponse</a></code>
- <code title="get /api/internal/chat/internalModels">client.internal.chat.<a href="./src/premai/resources/internal/chat.py">list_internal_models</a>() -> <a href="./src/premai/types/internal/chat_list_internal_models_response.py">object</a></code>
- <code title="get /api/internal/chat/models">client.internal.chat.<a href="./src/premai/resources/internal/chat.py">list_models</a>() -> <a href="./src/premai/types/internal/chat_list_models_response.py">ChatListModelsResponse</a></code>
