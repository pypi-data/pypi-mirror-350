import json
import mimetypes
from typing import Optional, TypeVar, Any, Type, Generic
from pydantic import BaseModel
import requests

from .request_utils import RequestUtils
from .types.assistants import AssistantResponse
from .types.chat import ChatCompletionMessage
from ..shared.assistants_types import (
    AssistantFile,
    AssistantFileUploadResponse,
    AssistantUploadImageResponse,
)
from ..shared.conversations_types import SignedUploadUrlResponse
from ..shared.defines import VariableNames
from ..shared.protected_types import SignedUrlResponse
from .project_helpers import scout

DEFAULT_MODEL = "gpt-4o"

# Create generic type variables for request and response
RequestType = TypeVar("RequestType", bound=BaseModel)
ResponseType = TypeVar("ResponseType", bound=BaseModel)
ResponseFormatType = TypeVar("ResponseFormatType", bound=BaseModel)


class Response(Generic[ResponseType]):
    def __init__(self, status_code: int, data: ResponseType):
        self.status_code = status_code
        self.data = data


class AssistantData(BaseModel):
    metadata: dict
    content: str
    embedding: Optional[list] = None


class AssistantDataList(BaseModel):
    list: list[AssistantData]


class ScoutAPI:
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_access_token: Optional[str] = None,
    ) -> None:
        self._base_url = base_url or scout.context.get(VariableNames.SCOUT_API_URL)
        if self._base_url is None or self._base_url == "":
            raise ValueError(
                f"{VariableNames.SCOUT_API_URL} is not set in SCOUT_CONTEXT"
            )

        api_access_token = api_access_token or scout.context.get(
            VariableNames.SCOUT_API_ACCESS_TOKEN
        )
        if api_access_token is None or api_access_token == "":
            raise ValueError(
                f"{VariableNames.SCOUT_API_ACCESS_TOKEN} is not set in SCOUT_CONTEXT"
            )

        self._headers = {
            "Authorization": f"Bearer {api_access_token}",
            "Content-Type": "application/json",
        }

    def _get_validated_data(
        self, response: Any, response_model: Optional[Type[ResponseType]] = None
    ) -> Any:
        if response_model and isinstance(response, dict):
            validated_data = response_model.model_validate(response)
        else:
            validated_data = response

        return validated_data

    # Generic requests
    def get(
        self,
        url: str,
        params: RequestType,
        response_model: Optional[Type[ResponseType]] = None,
    ) -> Response[Any]:
        request_data = params.model_dump() if isinstance(params, BaseModel) else params

        response, status_code = RequestUtils.get(
            url=f"{self._base_url}{url}",
            headers=self._headers,
            params=request_data,
        )

        validated_data = self._get_validated_data(response, response_model)

        return Response(status_code=status_code, data=validated_data)

    def put(
        self,
        url: str,
        data: RequestType,
        response_model: Optional[Type[ResponseType]] = None,
    ) -> Response[Any]:
        request_data = data.model_dump() if isinstance(data, BaseModel) else data

        response, status_code = RequestUtils.put(
            url=f"{self._base_url}{url}", headers=self._headers, payload=request_data
        )

        validated_data = self._get_validated_data(response, response_model)

        return Response(status_code=status_code, data=validated_data)

    def post(
        self,
        url: str,
        data: RequestType | dict,
        response_model: Optional[Type[ResponseType]] = None,
        files: Optional[dict] = None,
    ) -> Response[Any]:
        request_data = data.model_dump() if isinstance(data, BaseModel) else data

        if files:
            local_headers = self._headers.copy()
            local_headers.pop("Content-Type")

            response, status_code = RequestUtils.post(
                url=f"{self._base_url}{url}",
                headers=local_headers,
                data=request_data,
                files=files,
            )
        else:
            response, status_code = RequestUtils.post(
                url=f"{self._base_url}{url}",
                headers=self._headers,
                json_payload=request_data,
            )

        validated_data = self._get_validated_data(response, response_model)

        return Response(status_code=status_code, data=validated_data)

    def delete(
        self, url: str, response_model: Optional[Type[ResponseType]] = None
    ) -> Response[Any]:
        response, status_code = RequestUtils.delete(
            url=f"{self._base_url}{url}",
            headers=self._headers,
        )

        validated_data = self._get_validated_data(response, response_model)

        return Response(status_code=status_code, data=validated_data)

    # Embeddings

    def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        response, status_code = RequestUtils.post(
            url=f"{self._base_url}/api/embeddings/",
            headers=self._headers,
            json_payload={"texts": texts},
        )

        return response

    # TODO create a method that takes an array of message
    def chat_completion(
        self,
        messages: list[ChatCompletionMessage] | str,
        model: Optional[str] = None,
        assistant_id: Optional[str] = None,
        stream: Optional[bool] = None,
        response_format: Optional[Type[ResponseFormatType]] = None,
        debug: Optional[bool] = False,
        allowed_tools: Optional[list[str]] = None,
        llm_args: Optional[dict] = None,
    ) -> Any:
        model = model or DEFAULT_MODEL
        stream = stream or False

        if isinstance(messages, str):
            messages = [ChatCompletionMessage(role="user", content=messages)]

        payload = {
            "messages": [message.model_dump() for message in messages],
            "model": model,
            "stream": stream,
            **({"assistant_id": assistant_id} if assistant_id else {}),
            **({"allowed_tools": allowed_tools} if allowed_tools is not None else {}),
            **({"llm_args": llm_args} if llm_args else {}),
        }

        if response_format:
            payload["response_format"] = response_format.model_json_schema()

        if debug:
            print(f"payload: {payload}")

        response, status_code = RequestUtils.post(
            url=f"{self._base_url}/api/chat/completion/",
            headers=self._headers,
            json_payload=payload,
            stream=stream,
        )

        if response_format:
            # extract the last message from the response to ignore tools calls
            try:
                if stream:
                    content = response.get("content", "")
                else:
                    content = response.get("messages", [])[-1].get("content", "")

                return response_format.model_validate(json.loads(content))
            except Exception as e:
                raise Exception(f"Error processing Response: {response}") from e

        return response

    # Assistants

    def create_assistant(
        self,
        name: str,
        description: str,
        instructions: str,
        use_system_prompt: bool = True,
        prompt_starters: list[str] = [],
        visibility_type: str = "private",
        avatar_url: Optional[str] = None,
        allowed_functions: Optional[list[str]] = None,
        variables: Optional[dict[str, str]] = None,
        secrets: Optional[dict[str, str]] = None,
        allowed_external_services: Optional[list[str]] = None,
        ui_url: Optional[str] = None,
    ) -> Any:
        payload = {
            "name": name,
            "description": description,
            "instructions": instructions,
            "use_system_prompt": use_system_prompt,
            "prompt_starters": prompt_starters,
            "visibility": {"type": visibility_type},
            "avatar_url": avatar_url,
            **({"variables": variables} if variables is not None else {}),
            **({"secrets": secrets} if secrets is not None else {}),
            **(
                {"allowed_functions": allowed_functions}
                if allowed_functions is not None
                else {}
            ),
            **(
                {"allowed_external_services": allowed_external_services}
                if allowed_external_services is not None
                else {}
            ),
            **({"ui_url": ui_url} if ui_url is not None else {}),
        }

        response, status_code = RequestUtils.post(
            url=f"{self._base_url}/api/assistants/",
            headers=self._headers,
            json_payload=payload,
        )

        return response

    def update_assistant(
        self,
        assistant_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        instructions: Optional[str] = None,
        use_system_prompt: Optional[bool] = True,
        prompt_starters: Optional[list[str]] = None,
        visibility_type: Optional[str] = "private",
        avatar_url: Optional[str] = None,
        ui_url: Optional[str] = None,
        links: Optional[list[str]] = None,
        allowed_functions: Optional[list[str]] = None,
        variables: Optional[dict[str, str]] = None,
        secrets: Optional[dict[str, Optional[str]]] = None,
        allowed_external_services: Optional[list[str]] = None,
    ) -> Any:
        payload = {
            **({"name": name} if name is not None else {}),
            **({"description": description} if description is not None else {}),
            **({"instructions": instructions} if instructions is not None else {}),
            **(
                {"use_system_prompt": use_system_prompt}
                if use_system_prompt is not None
                else {}
            ),
            **(
                {"prompt_starters": prompt_starters}
                if prompt_starters is not None
                else {}
            ),
            **(
                {"visibility": {"type": visibility_type}}
                if visibility_type is not None
                else {}
            ),
            **({"avatar_url": avatar_url} if avatar_url is not None else {}),
            **({"ui_url": ui_url} if ui_url is not None else {}),
            **({"links": links} if links is not None else {}),
            **({"variables": variables} if variables is not None else {}),
            **({"secrets": secrets} if secrets is not None else {}),
            **(
                {"allowed_functions": allowed_functions}
                if allowed_functions is not None
                else {}
            ),
            **(
                {"allowed_external_services": allowed_external_services}
                if allowed_external_services is not None
                else {}
            ),
        }

        response, status_code = RequestUtils.patch(
            url=f"{self._base_url}/api/assistants/{assistant_id}",
            headers=self._headers,
            json_payload=payload,
        )

        return response

    def get_assistants(self) -> Any:
        response, status_code = RequestUtils.get(
            url=f"{self._base_url}/api/assistants", headers=self._headers
        )

        return response

    def upload_assistant_avatar(
        self,
        assistant_id: str,
        file_path: str,
    ) -> AssistantUploadImageResponse:
        with open(file_path, "rb") as f:
            content_type = mimetypes.guess_type(file_path)[0]
            files = {"file": (file_path, f, content_type)}
            local_headers = self._headers.copy()
            local_headers.pop("Content-Type")

            response, status_code = RequestUtils.post(
                url=f"{self._base_url}/api/assistants/{assistant_id}/avatar/upload",
                headers=local_headers,
                files=files,
            )
        return AssistantUploadImageResponse(**response)

    def upload_assistant_file(
        self,
        assistant_id: str,
        file_path: str,
    ) -> AssistantFileUploadResponse:
        with open(file_path, "rb") as f:
            files = {"file": f}
            local_headers = self._headers.copy()
            local_headers.pop("Content-Type")

            response, status_code = RequestUtils.post(
                url=f"{self._base_url}/api/assistants/{assistant_id}/files",
                headers=local_headers,
                files=files,
            )
        return AssistantFileUploadResponse(**response)

    def list_assistant_files(
        self,
        assistant_id: str,
    ) -> list[AssistantFile]:
        response, status_code = RequestUtils.get(
            url=f"{self._base_url}/api/assistants/{assistant_id}/files",
            headers=self._headers,
        )
        return [AssistantFile(**file) for file in response]

    def edit_assistant_file(
        self,
        assistant_id: str,
        file_uid: str,
        filename: str = "Default",
        description: Optional[str] = None,
    ) -> Any:
        data = {}
        data.update({"file_name": filename})
        data.update({"file_description": description}) if description else None

        response, status_code = RequestUtils.put(
            url=f"{self._base_url}/api/assistants/{assistant_id}/files/{file_uid}",
            headers=self._headers,
            payload=data,
        )
        return response

    def delete_assistant_file(
        self,
        assistant_id: str,
        file_uid: str,
    ) -> AssistantResponse:
        response, status_code = RequestUtils.delete(
            url=f"{self._base_url}/api/assistants/{assistant_id}/files/{file_uid}",
            headers=self._headers,
        )
        return AssistantResponse(**response)

    # Conversations

    def create_conversation(
        self,
        assistant_id: Optional[str] = None,
        model: Optional[str] = None,
        title: Optional[str] = None,
        payload: Optional[dict[str, Any]] = None,
        time_zone_offset: str = "-0400",
    ) -> Any:
        request_payload: dict[str, Any] = {}
        request_payload.update({"assistant_id": assistant_id}) if assistant_id else None
        request_payload.update({"model": model if model else DEFAULT_MODEL})
        request_payload.update({"title": title}) if title else None
        request_payload.update({"payload": payload}) if payload else None
        request_payload.update({"time_zone_offset": time_zone_offset})

        response, status_code = RequestUtils.post(
            url=f"{self._base_url}/api/conversations/",
            headers=self._headers,
            json_payload=request_payload,
        )
        return response

    def search_assistant_data(
        self,
        assistant_id: str,
        query: str,
        strategy: Optional[dict] = None,
        where: Optional[dict] = None,
    ) -> Any:
        response, status_code = RequestUtils.post(
            url=f"{self._base_url}/api/assistants/{assistant_id}/search",
            headers=self._headers,
            json_payload={"query": query, "strategy": strategy, "where": where},
        )
        return response

    def create_assistant_data(
        self, assistant_id: str, data: AssistantData | AssistantDataList
    ) -> Any:
        data_list = (
            data.model_dump().get("list")
            if isinstance(data, AssistantDataList)
            else [data.model_dump()]
        )

        response, status_code = RequestUtils.post(
            url=f"{self._base_url}/api/assistants/{assistant_id}/data",
            headers=self._headers,
            json_payload={"data": data_list},
        )
        return response

    def update_assistant_data(
        self,
        assistant_id: str,
        data_id: str,
        metadata: dict,
        content: str,
        embedding: Optional[list] = None,
    ) -> Any:
        response, status_code = RequestUtils.put(
            url=f"{self._base_url}/api/assistants/{assistant_id}/data/{data_id}",
            headers=self._headers,
            payload={"metadata": metadata, "content": content, "embedding": embedding},
        )
        return response

    def query_assistant_data(self, assistant_id: str, where: dict) -> Any:
        response, status_code = RequestUtils.get(
            url=f"{self._base_url}/api/assistants/{assistant_id}/data",
            headers=self._headers,
            params=where,
        )
        return response

    def delete_assistant_data(
        self, assistant_id: str, id: Optional[str] = None, where: Optional[dict] = None
    ) -> Any:
        if id is None and where is None:
            raise ValueError("Either 'id' or 'where' must be provided.")

        response, status_code = RequestUtils.delete(
            url=f"{self._base_url}/api/assistants/{assistant_id}/data",
            headers=self._headers,
            json_payload={"where": where, "id": id},
        )
        return response

    def get_conversation_signed_upload_url(
        self,
        conversation_id: str,
        file_path: str,
    ) -> SignedUploadUrlResponse:
        payload = {"file_path": file_path}

        response, status_code = RequestUtils.post(
            url=f"{self._base_url}/api/conversations/{conversation_id}/signed-upload-url",
            headers=self._headers,
            json_payload=payload,
        )
        try:
            return SignedUploadUrlResponse.model_validate(response)
        except Exception as e:
            raise ValueError(f"Invalid response: {response}") from e

    def get_signed_url(
        self,
        path: str,
    ) -> SignedUrlResponse:
        response, status_code = RequestUtils.get(
            url=f"{self._base_url}/api/protected/{path}",
            headers=self._headers,
        )

        return SignedUrlResponse.model_validate(response)

    def get_conversation_signed_url(
        self,
        conversation_id: str,
        file_path: str,
    ) -> SignedUrlResponse:
        response, status_code = RequestUtils.get(
            url=f"{self._base_url}/api/protected/conversations/{conversation_id}/{file_path}",
            headers=self._headers,
        )

        return SignedUrlResponse.model_validate(response)

    def chunk_document(self, file_path: str) -> dict:
        with open(file_path, "rb") as f:
            files = {"file": f}
            local_headers = self._headers.copy()
            local_headers.pop("Content-Type")

            response, status_code = RequestUtils.post(
                url=f"{self._base_url}/api/utils/chunk-document",
                headers=local_headers,
                files=files,
            )
        return response

    def get_document_text(self, file_path: str, args: Optional[dict] = None) -> dict:
        with open(file_path, "rb") as f:
            files = {"file": f}
            local_headers = self._headers.copy()
            local_headers.pop("Content-Type")

            response, status_code = RequestUtils.post(
                url=f"{self._base_url}/api/utils/get-file-text-content",
                headers=local_headers,
                files=files,
                json_payload=args,
            )
        return response

    def llm_filter_documents(
        self,
        query: str,
        context: str,
        documents: dict[str, str],
        batch_size: int = 10,
        model_id: Optional[str] = None,
    ) -> dict:
        response, status_code = RequestUtils.post(
            url=f"{self._base_url}/api/utils/llm-filter-documents",
            headers=self._headers,
            json_payload={
                "query": query,
                "context": context,
                "documents": documents,
                "batch_size": batch_size,
                "model_id": model_id,
            },
        )
        return response

    def text_to_speech(
        self,
        text: str,
        model: Optional[str] = None,
        voice: Optional[str] = None,
        api_args: Optional[dict] = None,
    ) -> bytes:
        json_payload = {
            "text": text,
            **({"model": model} if model is not None else {}),
            **({"voice": voice} if voice is not None else {}),
            **({"api_args": api_args} if api_args is not None else {}),
        }

        response = requests.post(
            url=f"{self._base_url}/api/audio/speech",
            headers=self._headers,
            json=json_payload,
        )
        return response.content

    def execute_assistant_function(
        self,
        assistant_id: str,
        function_name: str,
        payload: dict,
        response_model: Type[ResponseType],
    ) -> Response[ResponseType]:
        assistant_id = assistant_id
        api_url = f"/api/assistants/{assistant_id}/functions/{function_name}"
        result = self.post(url=api_url, data=payload, response_model=response_model)
        return result
