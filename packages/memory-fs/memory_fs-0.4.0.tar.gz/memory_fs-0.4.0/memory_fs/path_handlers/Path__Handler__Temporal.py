from typing                                             import List
from osbot_utils.helpers.Safe_Id                        import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from memory_fs.schemas.Schema__Memory_FS__Path__Handler import Schema__Memory_FS__Path__Handler


class Path__Handler__Temporal(Schema__Memory_FS__Path__Handler): # Handler that stores files in temporal directory structure
    name  : Safe_Id       = Safe_Id("temporal")
    areas : List[Safe_Id] = []

    def generate_path(self, file_name: str, file_ext: str, is_metadata: bool = True) -> Safe_Str__File__Path:
        from datetime import datetime
        now = datetime.now()
        time_path = now.strftime("%Y/%m/%d/%H")
        areas_path = "/".join(str(area) for area in self.areas) if self.areas else ""

        ext = ".json" if is_metadata else f".{file_ext}"

        if areas_path:
            return Safe_Str__File__Path(f"{time_path}/{areas_path}/{file_name}{ext}")
        else:
            return Safe_Str__File__Path(f"{time_path}/{file_name}{ext}")
