from typing                                             import Optional, Any
from memory_fs.actions.Memory_FS__Data                  import Memory_FS__Data
from memory_fs.actions.Memory_FS__Deserialize           import Memory_FS__Deserialize
from memory_fs.actions.Memory_FS__Paths                 import Memory_FS__Paths
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from memory_fs.schemas.Schema__Memory_FS__File          import Schema__Memory_FS__File
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from osbot_utils.type_safe.Type_Safe                    import Type_Safe
from memory_fs.core.Memory_FS__File_System              import Memory_FS__File_System


class Memory_FS__Load(Type_Safe):
    file_system: Memory_FS__File_System

    @cache_on_self
    def memory_fs__data(self):
        return Memory_FS__Data(file_system=self.file_system)

    @cache_on_self
    def memory_fs__deserialize(self):
        return Memory_FS__Deserialize(file_system=self.file_system)

    @cache_on_self
    def memory_fs__paths(self):
        return Memory_FS__Paths()


    def load(self, file_config : Schema__Memory_FS__File__Config  # Load file from the appropriate path based on config
              ) -> Optional[Schema__Memory_FS__File]:

        if file_config.default_handler:
            # Load from default handler's path only
            path = self.memory_fs__paths()._get_handler_path(file_config, file_config.default_handler)
            if path:
                return self.memory_fs__data().load(path)
        else:
            # Try each handler in order until we find the file
            for handler in file_config.path_handlers:
                if handler.enabled:
                    path = self.memory_fs__paths()._get_handler_path(file_config, handler)
                    if path and self.memory_fs__data().exists(path):
                        file = self.memory_fs__data().load(path)
                        if file:
                            return file

        return None

    def load_content(self, file_config : Schema__Memory_FS__File__Config  # Load content for a file
                     ) -> Optional[bytes]:
        # First load the metadata to get content path
        file = self.load(file_config)
        if not file:
            return None

        # Get the content path from metadata
        if file.metadata.content_paths:
            # If there's a default handler, try its content path first
            if file_config.default_handler and file_config.default_handler.name in file.metadata.content_paths:
                content_path = file.metadata.content_paths[file_config.default_handler.name]
                content = self.memory_fs__data().load_content(content_path)
                if content:
                    return content

            # Otherwise try any available content path
            for content_path in file.metadata.content_paths.values():
                content = self.memory_fs__data().load_content(content_path)
                if content:
                    return content

        return None

    def load_data(self, file_config : Schema__Memory_FS__File__Config  # Load and deserialize file data
                  ) -> Optional[Any]:
        # Load raw content
        content_bytes = self.load_content(file_config)
        if not content_bytes:
            return None

        # Load metadata to get file type info
        file = self.load(file_config)
        if not file:
            return None

        # Deserialize based on file type
        return self.memory_fs__deserialize()._deserialize_data(content_bytes, file_config.file_type)
