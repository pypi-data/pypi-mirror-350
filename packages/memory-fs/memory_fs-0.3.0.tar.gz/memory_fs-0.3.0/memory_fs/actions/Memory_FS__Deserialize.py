from typing import Any

from memory_fs.core.Memory_FS__File_System import Memory_FS__File_System
from memory_fs.schemas.Enum__Memory_FS__Serialization import Enum__Memory_FS__Serialization
from osbot_utils.type_safe.Type_Safe import Type_Safe


class Memory_FS__Deserialize(Type_Safe):
    file_system: Memory_FS__File_System

    def _deserialize_data(self, content_bytes: bytes, file_type) -> Any:                        # Deserialize data based on file type's serialization method
        serialization = file_type.serialization

        if serialization == Enum__Memory_FS__Serialization.STRING:
            return content_bytes.decode(file_type.encoding.value)

        elif serialization == Enum__Memory_FS__Serialization.JSON:
            import json
            json_str = content_bytes.decode(file_type.encoding.value)
            return json.loads(json_str)

        elif serialization == Enum__Memory_FS__Serialization.BINARY:
            return content_bytes

        elif serialization == Enum__Memory_FS__Serialization.BASE64:
            import base64
            return base64.b64decode(content_bytes)

        elif serialization == Enum__Memory_FS__Serialization.TYPE_SAFE:
            # This would need the actual Type_Safe class to deserialize
            # For now, return the JSON string
            return content_bytes.decode(file_type.encoding.value)

        else:
            raise ValueError(f"Unknown serialization method: {serialization}")
