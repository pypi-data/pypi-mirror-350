from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenericOpenAIParameters(_message.Message):
    __slots__ = ("model_name", "base_url")
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    BASE_URL_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    base_url: str
    def __init__(self, model_name: _Optional[str] = ..., base_url: _Optional[str] = ...) -> None: ...

class AzureOpenAIParameters(_message.Message):
    __slots__ = ("base_url", "resource_name", "deployment_id", "api_version")
    BASE_URL_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    base_url: str
    resource_name: str
    deployment_id: str
    api_version: str
    def __init__(self, base_url: _Optional[str] = ..., resource_name: _Optional[str] = ..., deployment_id: _Optional[str] = ..., api_version: _Optional[str] = ...) -> None: ...

class CompletionModelParameters(_message.Message):
    __slots__ = ("generic_openai_parameters", "azure_openai_parameters")
    GENERIC_OPENAI_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    AZURE_OPENAI_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    generic_openai_parameters: GenericOpenAIParameters
    azure_openai_parameters: AzureOpenAIParameters
    def __init__(self, generic_openai_parameters: _Optional[_Union[GenericOpenAIParameters, _Mapping]] = ..., azure_openai_parameters: _Optional[_Union[AzureOpenAIParameters, _Mapping]] = ...) -> None: ...
