from osbot_utils.helpers.safe_int.Safe_UInt__FileSize  import Safe_UInt__FileSize
from osbot_utils.helpers.safe_str.Safe_Str__File__Path import Safe_Str__File__Path
from memory_fs.schemas.Enum__Memory_FS__File__Encoding import Enum__Memory_FS__File__Encoding
from osbot_utils.type_safe.Type_Safe                   import Type_Safe

class Schema__Memory_FS__File__Content(Type_Safe):
    size         : Safe_UInt__FileSize             = None
    encoding     : Enum__Memory_FS__File__Encoding = None
    content_path : Safe_Str__File__Path            = None