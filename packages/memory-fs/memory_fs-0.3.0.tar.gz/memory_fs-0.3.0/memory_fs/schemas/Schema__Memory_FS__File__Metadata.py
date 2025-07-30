from typing                                             import Dict, Optional
from osbot_utils.helpers.Random_Guid                    import Random_Guid
from osbot_utils.helpers.Safe_Id                        import Safe_Id
from osbot_utils.helpers.Timestamp_Now                  import Timestamp_Now
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.helpers.safe_str.Safe_Str__Hash        import Safe_Str__Hash
from osbot_utils.type_safe.Type_Safe                    import Type_Safe
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config


class Schema__Memory_FS__File__Metadata(Type_Safe):
    paths                : Dict[Safe_Id, Safe_Str__File__Path]    # Paths to metadata files
    content_paths        : Dict[Safe_Id, Safe_Str__File__Path]    # Paths to content files
    content_hash         : Safe_Str__Hash                        = None
    chain_hash           : Optional[Safe_Str__Hash]              = None
    previous_version_path: Optional[Safe_Str__File__Path]        = None
    timestamp            : Timestamp_Now
    file_id              : Random_Guid
    config               : Schema__Memory_FS__File__Config