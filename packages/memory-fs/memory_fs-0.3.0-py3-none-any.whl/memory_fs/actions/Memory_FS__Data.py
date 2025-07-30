from typing                                                 import List, Optional, Dict, Any
from memory_fs.schemas.Schema__Memory_FS__File              import Schema__Memory_FS__File
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path
from memory_fs.core.Memory_FS__File_System                  import Memory_FS__File_System
from osbot_utils.type_safe.Type_Safe                        import Type_Safe


class Memory_FS__Data(Type_Safe):
    file_system : Memory_FS__File_System

    def exists(self, path : Safe_Str__File__Path                                               # Check if a file exists at the given path
                ) -> bool:
        return path in self.file_system.files

    def exists_content(self, path : Safe_Str__File__Path                                       # Check if content exists at the given path
                        ) -> bool:
        return path in self.file_system.content_data

    # todo: this method should return a strongly typed class (ideally one from the file)
    def get_file_info(self, path : Safe_Str__File__Path                                        # Get file information (size, hash, etc.)
                       ) -> Optional[Dict[Safe_Id, Any]]:
        file = self.file_system.files.get(path)
        if not file:
            return None

        content_size = 0
        if file.info and file.info.content:
            content_size = int(file.info.content.size)                                         # Get size from metadata

        return {Safe_Id("exists")       : True                                               ,
                Safe_Id("size")         : content_size                                       ,
                Safe_Id("content_hash") : file.metadata.content_hash                         ,
                Safe_Id("timestamp")    : file.metadata.timestamp                            ,
                Safe_Id("content_type") : str(file.info.content_type.value) if file.info else None,
                Safe_Id("paths")        : file.metadata.paths                                }

    def list_files(self, prefix : Safe_Str__File__Path = None                                  # List all files, optionally filtered by prefix
                    ) -> List[Safe_Str__File__Path]:
        if prefix is None:
            return list(self.file_system.files.keys())

        prefix_str = str(prefix)
        if not prefix_str.endswith('/'):
            prefix_str += '/'

        return [path for path in self.file_system.files.keys()
                if str(path).startswith(prefix_str)]

    def load(self, path : Safe_Str__File__Path                                                 # Load a file metadata from the given path
              ) -> Optional[Schema__Memory_FS__File]:
        return self.file_system.files.get(path)

    def load_content(self, path : Safe_Str__File__Path                                         # Load raw content from the given path
                      ) -> Optional[bytes]:
        return self.file_system.content_data.get(path)

    # todo: this should return a python object (and most likely moved into a Memory_FS__Stats class)
    def stats(self) -> Dict[Safe_Id, Any]:                                                     # Get file system statistics
        total_size = 0
        for path, content in self.file_system.content_data.items():
            total_size += len(content)

        return {Safe_Id("type")            : Safe_Id("memory")       ,
                Safe_Id("file_count")      : len(self.file_system.files)        ,
                Safe_Id("content_count")   : len(self.file_system.content_data) ,
                Safe_Id("total_size")      : total_size             }
