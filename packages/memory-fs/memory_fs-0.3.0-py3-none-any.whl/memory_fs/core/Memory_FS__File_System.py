from typing                                              import Dict, List, Optional, Any
from osbot_utils.helpers.safe_str.Safe_Str__File__Path   import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                     import Type_Safe
from memory_fs.schemas.Schema__Memory_FS__File           import Schema__Memory_FS__File


class Memory_FS__File_System(Type_Safe):                                                # In-memory file system that maintains directory structure and file storage
    files          : Dict[Safe_Str__File__Path, Schema__Memory_FS__File]                                  # Path -> File metadata mapping
    content_data   : Dict[Safe_Str__File__Path, bytes]                                           # Path -> Raw content mapping







