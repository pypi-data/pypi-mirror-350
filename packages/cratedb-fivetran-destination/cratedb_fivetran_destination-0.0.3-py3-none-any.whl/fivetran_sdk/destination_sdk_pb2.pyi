from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Encryption(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NONE: _ClassVar[Encryption]
    AES: _ClassVar[Encryption]

class BatchFileFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CSV: _ClassVar[BatchFileFormat]
    PARQUET: _ClassVar[BatchFileFormat]

class Compression(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OFF: _ClassVar[Compression]
    ZSTD: _ClassVar[Compression]
    GZIP: _ClassVar[Compression]
NONE: Encryption
AES: Encryption
CSV: BatchFileFormat
PARQUET: BatchFileFormat
OFF: Compression
ZSTD: Compression
GZIP: Compression

class CapabilitiesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CapabilitiesResponse(_message.Message):
    __slots__ = ("batch_file_format",)
    BATCH_FILE_FORMAT_FIELD_NUMBER: _ClassVar[int]
    batch_file_format: BatchFileFormat
    def __init__(self, batch_file_format: _Optional[_Union[BatchFileFormat, str]] = ...) -> None: ...

class DescribeTableRequest(_message.Message):
    __slots__ = ("configuration", "schema_name", "table_name")
    class ConfigurationEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    configuration: _containers.ScalarMap[str, str]
    schema_name: str
    table_name: str
    def __init__(self, configuration: _Optional[_Mapping[str, str]] = ..., schema_name: _Optional[str] = ..., table_name: _Optional[str] = ...) -> None: ...

class DescribeTableResponse(_message.Message):
    __slots__ = ("not_found", "table", "warning", "task")
    NOT_FOUND_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    WARNING_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    not_found: bool
    table: _common_pb2.Table
    warning: _common_pb2.Warning
    task: _common_pb2.Task
    def __init__(self, not_found: bool = ..., table: _Optional[_Union[_common_pb2.Table, _Mapping]] = ..., warning: _Optional[_Union[_common_pb2.Warning, _Mapping]] = ..., task: _Optional[_Union[_common_pb2.Task, _Mapping]] = ...) -> None: ...

class CreateTableRequest(_message.Message):
    __slots__ = ("configuration", "schema_name", "table")
    class ConfigurationEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    configuration: _containers.ScalarMap[str, str]
    schema_name: str
    table: _common_pb2.Table
    def __init__(self, configuration: _Optional[_Mapping[str, str]] = ..., schema_name: _Optional[str] = ..., table: _Optional[_Union[_common_pb2.Table, _Mapping]] = ...) -> None: ...

class CreateTableResponse(_message.Message):
    __slots__ = ("success", "warning", "task")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    WARNING_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    success: bool
    warning: _common_pb2.Warning
    task: _common_pb2.Task
    def __init__(self, success: bool = ..., warning: _Optional[_Union[_common_pb2.Warning, _Mapping]] = ..., task: _Optional[_Union[_common_pb2.Task, _Mapping]] = ...) -> None: ...

class AlterTableRequest(_message.Message):
    __slots__ = ("configuration", "schema_name", "table")
    class ConfigurationEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    configuration: _containers.ScalarMap[str, str]
    schema_name: str
    table: _common_pb2.Table
    def __init__(self, configuration: _Optional[_Mapping[str, str]] = ..., schema_name: _Optional[str] = ..., table: _Optional[_Union[_common_pb2.Table, _Mapping]] = ...) -> None: ...

class AlterTableResponse(_message.Message):
    __slots__ = ("success", "warning", "task")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    WARNING_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    success: bool
    warning: _common_pb2.Warning
    task: _common_pb2.Task
    def __init__(self, success: bool = ..., warning: _Optional[_Union[_common_pb2.Warning, _Mapping]] = ..., task: _Optional[_Union[_common_pb2.Task, _Mapping]] = ...) -> None: ...

class TruncateRequest(_message.Message):
    __slots__ = ("configuration", "schema_name", "table_name", "synced_column", "utc_delete_before", "soft")
    class ConfigurationEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    SYNCED_COLUMN_FIELD_NUMBER: _ClassVar[int]
    UTC_DELETE_BEFORE_FIELD_NUMBER: _ClassVar[int]
    SOFT_FIELD_NUMBER: _ClassVar[int]
    configuration: _containers.ScalarMap[str, str]
    schema_name: str
    table_name: str
    synced_column: str
    utc_delete_before: _timestamp_pb2.Timestamp
    soft: SoftTruncate
    def __init__(self, configuration: _Optional[_Mapping[str, str]] = ..., schema_name: _Optional[str] = ..., table_name: _Optional[str] = ..., synced_column: _Optional[str] = ..., utc_delete_before: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., soft: _Optional[_Union[SoftTruncate, _Mapping]] = ...) -> None: ...

class SoftTruncate(_message.Message):
    __slots__ = ("deleted_column",)
    DELETED_COLUMN_FIELD_NUMBER: _ClassVar[int]
    deleted_column: str
    def __init__(self, deleted_column: _Optional[str] = ...) -> None: ...

class TruncateResponse(_message.Message):
    __slots__ = ("success", "warning", "task")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    WARNING_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    success: bool
    warning: _common_pb2.Warning
    task: _common_pb2.Task
    def __init__(self, success: bool = ..., warning: _Optional[_Union[_common_pb2.Warning, _Mapping]] = ..., task: _Optional[_Union[_common_pb2.Task, _Mapping]] = ...) -> None: ...

class WriteBatchRequest(_message.Message):
    __slots__ = ("configuration", "schema_name", "table", "keys", "replace_files", "update_files", "delete_files", "file_params")
    class ConfigurationEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class KeysEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bytes
        def __init__(self, key: _Optional[str] = ..., value: _Optional[bytes] = ...) -> None: ...
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    REPLACE_FILES_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FILES_FIELD_NUMBER: _ClassVar[int]
    DELETE_FILES_FIELD_NUMBER: _ClassVar[int]
    FILE_PARAMS_FIELD_NUMBER: _ClassVar[int]
    configuration: _containers.ScalarMap[str, str]
    schema_name: str
    table: _common_pb2.Table
    keys: _containers.ScalarMap[str, bytes]
    replace_files: _containers.RepeatedScalarFieldContainer[str]
    update_files: _containers.RepeatedScalarFieldContainer[str]
    delete_files: _containers.RepeatedScalarFieldContainer[str]
    file_params: FileParams
    def __init__(self, configuration: _Optional[_Mapping[str, str]] = ..., schema_name: _Optional[str] = ..., table: _Optional[_Union[_common_pb2.Table, _Mapping]] = ..., keys: _Optional[_Mapping[str, bytes]] = ..., replace_files: _Optional[_Iterable[str]] = ..., update_files: _Optional[_Iterable[str]] = ..., delete_files: _Optional[_Iterable[str]] = ..., file_params: _Optional[_Union[FileParams, _Mapping]] = ...) -> None: ...

class WriteHistoryBatchRequest(_message.Message):
    __slots__ = ("configuration", "schema_name", "table", "keys", "earliest_start_files", "replace_files", "update_files", "delete_files", "file_params")
    class ConfigurationEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class KeysEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bytes
        def __init__(self, key: _Optional[str] = ..., value: _Optional[bytes] = ...) -> None: ...
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    EARLIEST_START_FILES_FIELD_NUMBER: _ClassVar[int]
    REPLACE_FILES_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FILES_FIELD_NUMBER: _ClassVar[int]
    DELETE_FILES_FIELD_NUMBER: _ClassVar[int]
    FILE_PARAMS_FIELD_NUMBER: _ClassVar[int]
    configuration: _containers.ScalarMap[str, str]
    schema_name: str
    table: _common_pb2.Table
    keys: _containers.ScalarMap[str, bytes]
    earliest_start_files: _containers.RepeatedScalarFieldContainer[str]
    replace_files: _containers.RepeatedScalarFieldContainer[str]
    update_files: _containers.RepeatedScalarFieldContainer[str]
    delete_files: _containers.RepeatedScalarFieldContainer[str]
    file_params: FileParams
    def __init__(self, configuration: _Optional[_Mapping[str, str]] = ..., schema_name: _Optional[str] = ..., table: _Optional[_Union[_common_pb2.Table, _Mapping]] = ..., keys: _Optional[_Mapping[str, bytes]] = ..., earliest_start_files: _Optional[_Iterable[str]] = ..., replace_files: _Optional[_Iterable[str]] = ..., update_files: _Optional[_Iterable[str]] = ..., delete_files: _Optional[_Iterable[str]] = ..., file_params: _Optional[_Union[FileParams, _Mapping]] = ...) -> None: ...

class FileParams(_message.Message):
    __slots__ = ("compression", "encryption", "null_string", "unmodified_string")
    COMPRESSION_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTION_FIELD_NUMBER: _ClassVar[int]
    NULL_STRING_FIELD_NUMBER: _ClassVar[int]
    UNMODIFIED_STRING_FIELD_NUMBER: _ClassVar[int]
    compression: Compression
    encryption: Encryption
    null_string: str
    unmodified_string: str
    def __init__(self, compression: _Optional[_Union[Compression, str]] = ..., encryption: _Optional[_Union[Encryption, str]] = ..., null_string: _Optional[str] = ..., unmodified_string: _Optional[str] = ...) -> None: ...

class WriteBatchResponse(_message.Message):
    __slots__ = ("success", "warning", "task")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    WARNING_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    success: bool
    warning: _common_pb2.Warning
    task: _common_pb2.Task
    def __init__(self, success: bool = ..., warning: _Optional[_Union[_common_pb2.Warning, _Mapping]] = ..., task: _Optional[_Union[_common_pb2.Task, _Mapping]] = ...) -> None: ...
