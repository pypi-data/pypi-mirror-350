from osbot_utils.helpers.Safe_Id                        import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from memory_fs.schemas.Schema__Memory_FS__Path__Handler import Schema__Memory_FS__Path__Handler


class Path__Handler__Latest(Schema__Memory_FS__Path__Handler):       # Handler that stores files in a 'latest' directory
    name : Safe_Id = Safe_Id("latest")

    def generate_path(self, file_name: str, file_ext: str, is_metadata: bool = True) -> Safe_Str__File__Path:
        ext = ".json" if is_metadata else f".{file_ext}"
        return Safe_Str__File__Path(f"latest/{file_name}{ext}")