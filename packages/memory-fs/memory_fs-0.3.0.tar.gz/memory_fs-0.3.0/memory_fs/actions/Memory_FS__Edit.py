from memory_fs.schemas.Schema__Memory_FS__File          import Schema__Memory_FS__File
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from memory_fs.core.Memory_FS__File_System              import Memory_FS__File_System
from osbot_utils.type_safe.Type_Safe                    import Type_Safe


class Memory_FS__Edit(Type_Safe):
    file_system : Memory_FS__File_System

    def clear(self) -> None:                                                                    # Clear all files and directories
        self.file_system.files.clear()
        self.file_system.content_data.clear()

    def copy(self, source      : Safe_Str__File__Path ,                                        # Copy a file from source to destination
                   destination : Safe_Str__File__Path
              ) -> bool:
        if source not in self.file_system.files:
            return False

        file = self.file_system.files[source]
        self.save(destination, file)

        # Also copy content if it exists
        if source in self.file_system.content_data:
            self.save_content(destination, self.file_system.content_data[source])

        return True

    def delete(self, path : Safe_Str__File__Path                                               # Delete a file at the given path
                ) -> bool:
        if path in self.file_system.files:
            del self.file_system.files[path]
            return True
        return False

    def delete_content(self, path : Safe_Str__File__Path                                       # Delete content at the given path
                        ) -> bool:
        if path in self.file_system.content_data:
            del self.file_system.content_data[path]
            return True
        return False

    def move(self, source      : Safe_Str__File__Path ,                                        # Move a file from source to destination
                   destination : Safe_Str__File__Path
              ) -> bool:
        if source not in self.file_system.files:
            return False

        file = self.file_system.files[source]
        self.save(destination, file)
        self.delete(source)

        # Also move content if it exists
        if source in self.file_system.content_data:
            self.save_content(destination, self.file_system.content_data[source])
            self.delete_content(source)

        return True

    def save(self, path : Safe_Str__File__Path ,                                               # Save a file metadata at the given path
                   file : Schema__Memory_FS__File
              ) -> bool:
        self.file_system.files[path] = file                                                                # Store the file metadata
        return True

    def save_content(self, path    : Safe_Str__File__Path ,                                    # Save raw content at the given path
                           content : bytes
                      ) -> bool:
        self.file_system.content_data[path] = content                                                       # Store the raw content
        return True
