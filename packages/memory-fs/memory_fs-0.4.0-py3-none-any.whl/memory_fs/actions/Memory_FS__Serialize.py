from typing                                             import Any
from memory_fs.schemas.Enum__Memory_FS__Serialization   import Enum__Memory_FS__Serialization
from osbot_utils.type_safe.Type_Safe                    import Type_Safe
from memory_fs.core.Memory_FS__File_System              import Memory_FS__File_System

class Memory_FS__Serialize(Type_Safe):
    file_system: Memory_FS__File_System

    def _serialize_data(self, data: Any, file_type) -> bytes:                                   # Serialize data based on file type's serialization method
        serialization = file_type.serialization

        if serialization == Enum__Memory_FS__Serialization.STRING:
            if isinstance(data, str):
                return data.encode(file_type.encoding.value)
            else:
                return str(data).encode(file_type.encoding.value)

        elif serialization == Enum__Memory_FS__Serialization.JSON:
            import json
            json_str = json.dumps(data, indent=2)
            return json_str.encode(file_type.encoding.value)

        elif serialization == Enum__Memory_FS__Serialization.BINARY:
            if isinstance(data, bytes):
                return data
            else:
                raise ValueError(f"Binary serialization expects bytes, got {type(data)}")

        elif serialization == Enum__Memory_FS__Serialization.BASE64:
            import base64
            if isinstance(data, bytes):
                return base64.b64encode(data)
            else:
                return base64.b64encode(str(data).encode('utf-8'))

        elif serialization == Enum__Memory_FS__Serialization.TYPE_SAFE:
            if hasattr(data, 'json'):
                json_str = data.json()
                return json_str.encode(file_type.encoding.value)
            else:
                raise ValueError(f"TYPE_SAFE serialization requires object with json() method, got {type(data)}")

        else:
            raise ValueError(f"Unknown serialization method: {serialization}")