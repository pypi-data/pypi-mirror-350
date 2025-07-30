from memory_fs.actions.Memory_FS__Data                  import Memory_FS__Data
from memory_fs.actions.Memory_FS__Paths                 import Memory_FS__Paths
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from memory_fs.core.Memory_FS__File_System              import Memory_FS__File_System
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class Memory_FS__Exists(Type_Safe):
    file_system: Memory_FS__File_System

    @cache_on_self
    def memory_fs__data(self):
        return Memory_FS__Data(file_system=self.file_system)

    def memory_fs__paths(self):
        return Memory_FS__Paths()

    def exists(self, file_config : Schema__Memory_FS__File__Config  # Check if file exists based on config strategy
               ) -> bool:

        if file_config.default_handler:
            # Check only the default handler's path
            path = self.memory_fs__paths()._get_handler_path(file_config, file_config.default_handler)
            return path is not None and self.memory_fs__data().exists(path)
        else:
            # Check ALL paths - file exists only if present in all configured paths
            for handler in file_config.path_handlers:
                if handler.enabled:
                    path = self.memory_fs__paths()._get_handler_path(file_config, handler)
                    if not path or not self.memory_fs__data().exists(path):
                        return False
            return len(file_config.path_handlers) > 0  # At least one handler must be configured


