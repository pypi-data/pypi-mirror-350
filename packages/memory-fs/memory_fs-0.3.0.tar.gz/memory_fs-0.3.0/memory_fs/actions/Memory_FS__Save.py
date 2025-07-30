from typing                                                 import Any, Dict
from memory_fs.actions.Memory_FS__Edit                      import Memory_FS__Edit
from memory_fs.actions.Memory_FS__Paths                     import Memory_FS__Paths
from memory_fs.actions.Memory_FS__Serialize                 import Memory_FS__Serialize
from memory_fs.schemas.Schema__Memory_FS__File              import Schema__Memory_FS__File
from memory_fs.schemas.Schema__Memory_FS__File__Metadata    import Schema__Memory_FS__File__Metadata
from osbot_utils.helpers.safe_str.Safe_Str__File__Name      import Safe_Str__File__Name
from memory_fs.schemas.Schema__Memory_FS__File__Content     import Schema__Memory_FS__File__Content
from memory_fs.schemas.Schema__Memory_FS__File__Info        import Schema__Memory_FS__File__Info
from osbot_utils.helpers.safe_int.Safe_UInt__FileSize       import Safe_UInt__FileSize
from osbot_utils.helpers.safe_str.Safe_Str__Hash            import safe_str_hash
from memory_fs.schemas.Enum__Memory_FS__File__Encoding      import Enum__Memory_FS__File__Encoding
from osbot_utils.decorators.methods.cache_on_self           import cache_on_self
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path
from memory_fs.core.Memory_FS__File_System                  import Memory_FS__File_System
from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config
from osbot_utils.type_safe.Type_Safe                        import Type_Safe


class Memory_FS__Save(Type_Safe):
    file_system: Memory_FS__File_System

    @cache_on_self
    def memory_fs__edit(self):
        return Memory_FS__Edit(file_system=self.file_system)

    @cache_on_self
    def memory__fs_paths(self):
        return Memory_FS__Paths()

    @cache_on_self
    def memory_fs__serialize(self):
        return Memory_FS__Serialize(file_system=self.file_system)

    def save(self, file_data   : Any,  # Save file data using all configured path handlers
                   file_config : Schema__Memory_FS__File__Config,
                   file_name   : str = "file"
              ) -> Dict[Safe_Id, Safe_Str__File__Path]:

        # Get file type from config
        file_type = file_config.file_type
        if not file_type:
            raise ValueError("file_config.file_type is required")

        # Convert data to bytes based on file type's serialization method
        content_bytes = self.memory_fs__serialize()._serialize_data(file_data, file_type)

        # Calculate content hash and size
        if file_type.encoding == Enum__Memory_FS__File__Encoding.BINARY:
            content_hash = safe_str_hash(str(content_bytes))
        else:
            content_hash = safe_str_hash(content_bytes.decode(file_type.encoding.value))

        content_size = Safe_UInt__FileSize(len(content_bytes))

        # Generate all paths for metadata and content using handlers from config
        metadata_paths = {}
        content_paths  = {}

        for handler in file_config.path_handlers:
            if handler.enabled:
                handler_name = handler.name
                # For now, simulate path generation - in real implementation,
                # handlers would have their own generate_path method
                metadata_path = self.memory__fs_paths()._simulate_handler_path(handler, file_name, file_type.file_extension, True)
                content_path  = self.memory__fs_paths()._simulate_handler_path(handler, file_name, file_type.file_extension, False)

                if metadata_path:
                    metadata_paths[handler_name] = metadata_path
                if content_path:
                    content_paths[handler_name] = content_path

        # Use first content path for the content reference
        first_content_path = list(content_paths.values())[0] if content_paths else Safe_Str__File__Path("")

        # Create file content reference
        file_content = Schema__Memory_FS__File__Content(
            size         = content_size,
            encoding     = file_type.encoding,
            content_path = first_content_path
        )

        # Create file info
        file_info = Schema__Memory_FS__File__Info(
            file_name    = Safe_Str__File__Name(f"{file_name}.{file_type.file_extension}"),
            file_ext     = file_type.file_extension,
            content_type = file_type.content_type,
            content      = file_content
        )

        # Create metadata
        metadata = Schema__Memory_FS__File__Metadata(
            paths         = metadata_paths,
            content_paths = content_paths,
            content_hash  = content_hash,
            config        = file_config
        )

        # Create the complete file
        file = Schema__Memory_FS__File(
            config   = file_config,
            info     = file_info,
            metadata = metadata
        )

        saved_paths = {}

        # Save metadata files
        for handler_name, path in metadata_paths.items():
            if self.memory_fs__edit().save(path, file):
                saved_paths[handler_name] = path

        # Save content files
        for handler_name, path in content_paths.items():
            self.memory_fs__edit().save_content(path, content_bytes)

        return saved_paths