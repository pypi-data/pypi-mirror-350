from memory_fs.schemas.Schema__Memory_FS__File__Content    import Schema__Memory_FS__File__Content
from memory_fs.schemas.Enum__Memory_FS__File__Content_Type import Enum__Memory_FS__File__Content_Type
from osbot_utils.helpers.safe_str.Safe_Str__File__Name     import Safe_Str__File__Name
from osbot_utils.helpers.Safe_Id                           import Safe_Id
from osbot_utils.type_safe.Type_Safe                       import Type_Safe


class Schema__Memory_FS__File__Info(Type_Safe):
    file_name    : Safe_Str__File__Name         = None          # e.g., "article.html"
    file_ext     : Safe_Id                      = None          # e.g., "html"
    content_type : Enum__Memory_FS__File__Content_Type = None          # e.g., HTML
    content      : Schema__Memory_FS__File__Content                      # Reference to content metadata