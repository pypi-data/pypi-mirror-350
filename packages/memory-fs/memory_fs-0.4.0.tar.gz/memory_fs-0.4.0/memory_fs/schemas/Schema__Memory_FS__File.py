from memory_fs.schemas.Schema__Memory_FS__File__Info     import Schema__Memory_FS__File__Info
from osbot_utils.type_safe.Type_Safe                     import Type_Safe
from memory_fs.schemas.Schema__Memory_FS__File__Config   import Schema__Memory_FS__File__Config
from memory_fs.schemas.Schema__Memory_FS__File__Metadata import Schema__Memory_FS__File__Metadata


class Schema__Memory_FS__File(Type_Safe):
    config   : Schema__Memory_FS__File__Config
    info     : Schema__Memory_FS__File__Info
    metadata : Schema__Memory_FS__File__Metadata