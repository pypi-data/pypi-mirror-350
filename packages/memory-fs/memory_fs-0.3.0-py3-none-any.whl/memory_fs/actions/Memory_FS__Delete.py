from typing                                             import Dict
from memory_fs.actions.Memory_FS__Edit                  import Memory_FS__Edit
from memory_fs.actions.Memory_FS__Load                  import Memory_FS__Load
from osbot_utils.helpers.Safe_Id                        import Safe_Id
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from memory_fs.core.Memory_FS__File_System              import Memory_FS__File_System
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class Memory_FS__Delete(Type_Safe):
    file_system: Memory_FS__File_System

    @cache_on_self
    def memory_fs__edit(self):
        return Memory_FS__Edit(file_system=self.file_system)

    @cache_on_self
    def memory_fs__load(self):
        return Memory_FS__Load(file_system=self.file_system)

    @cache_on_self
    def memory__fs_storage(self):
        return Memory_FS__Storage(file_system=self.file_system)

    def delete(self, file_config : Schema__Memory_FS__File__Config  # Delete file from all configured paths
                ) -> Dict[Safe_Id, bool]:
        results = {}

        # First, try to load the file to get all its paths
        file = self.memory_fs__load().load(file_config)

        if file and file.metadata.paths:
            # Delete using actual paths from metadata
            for handler_name, path in file.metadata.paths.items():
                results[handler_name] = self.memory_fs__edit().delete(path)

            # Also delete content files
            if file.metadata.content_paths:
                for path in file.metadata.content_paths.values():
                    self.memory_fs__edit().delete_content(path)
        else:
            # Fallback: try to delete from all configured handlers
            for handler in file_config.path_handlers:
                if handler.enabled:
                    # Generate expected paths and try to delete
                    # This is a simplified version - in reality, we'd need more info
                    results[handler.name] = False

        return results