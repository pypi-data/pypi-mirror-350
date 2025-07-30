from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FileType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOCUMENT: _ClassVar[FileType]
    IMAGE: _ClassVar[FileType]
    VIDEO: _ClassVar[FileType]
    AUDIO: _ClassVar[FileType]
    OTHER: _ClassVar[FileType]
DOCUMENT: FileType
IMAGE: FileType
VIDEO: FileType
AUDIO: FileType
OTHER: FileType

class File(_message.Message):
    __slots__ = ("mission_id", "name", "type", "url")
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    name: str
    type: FileType
    url: str
    def __init__(self, mission_id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[_Union[FileType, str]] = ..., url: _Optional[str] = ...) -> None: ...

class UploadFileRequest(_message.Message):
    __slots__ = ("mission_id", "name", "type", "content")
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    name: str
    type: FileType
    content: bytes
    def __init__(self, mission_id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[_Union[FileType, str]] = ..., content: _Optional[bytes] = ...) -> None: ...

class UploadFileResponse(_message.Message):
    __slots__ = ("success", "file")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    file: File
    def __init__(self, success: bool = ..., file: _Optional[_Union[File, _Mapping]] = ...) -> None: ...

class GetFileRequest(_message.Message):
    __slots__ = ("mission_id", "name")
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    name: str
    def __init__(self, mission_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class GetFileResponse(_message.Message):
    __slots__ = ("file", "content")
    FILE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    file: File
    content: bytes
    def __init__(self, file: _Optional[_Union[File, _Mapping]] = ..., content: _Optional[bytes] = ...) -> None: ...

class GetFilesByMissionRequest(_message.Message):
    __slots__ = ("mission_id",)
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    def __init__(self, mission_id: _Optional[str] = ...) -> None: ...

class GetFilesByMissionResponse(_message.Message):
    __slots__ = ("files",)
    FILES_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[File]
    def __init__(self, files: _Optional[_Iterable[_Union[File, _Mapping]]] = ...) -> None: ...

class GetFilesByNameRequest(_message.Message):
    __slots__ = ("mission_id", "name")
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    name: str
    def __init__(self, mission_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class GetFilesByNameResponse(_message.Message):
    __slots__ = ("success", "file")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    file: File
    def __init__(self, success: bool = ..., file: _Optional[_Union[File, _Mapping]] = ...) -> None: ...

class DeleteFileRequest(_message.Message):
    __slots__ = ("mission_id", "name")
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    name: str
    def __init__(self, mission_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class DeleteFileResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
