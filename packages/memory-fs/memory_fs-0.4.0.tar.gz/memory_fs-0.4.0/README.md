# Memory-FS

Memory-FS is a Python library that provides a type-safe, in-memory file system. It is designed with an action-based architecture and supports pluggable path handlers and file types, making it flexible for various use cases. This project originated from `OSBot_Cloud_FS`.

## Key Features

*   **In-Memory Storage:** All file operations occur in memory, ensuring fast read and write access.
*   **Type-Safe:** Utilizes `osbot_utils.type_safe` to enforce data integrity and prevent type-related errors.
*   **Action-Based Architecture:** Core functionalities such as save, load, delete, and list are encapsulated in dedicated action classes, promoting modularity and extensibility.
*   **Pluggable Path Handlers:** Supports different strategies for organizing file paths, including handlers for latest versions, temporal (time-based) versioning, and explicit versioning.
*   **Extensible File Types:** Allows for easy definition and addition of new file types with custom serialization and deserialization logic.
*   **Two-File Pattern:** Stores metadata (as JSON) separately from the actual file content. This enables rich file information and efficient metadata operations.

## Technical Deep Dive

For a more detailed understanding of the project's architecture, please refer to the technical architecture document located in `docs/technical_architecture_debrief.md`.

## Basic Usage Example

Here's a simple example of how to use `Memory-FS` to save and load data:

```python
from osbot_utils.utils.testing.Duration import Duration

from memory_fs.Memory_FS import Memory_FS
from memory_fs.path_handlers.Path__Handler__Latest import Path__Handler__Latest
from memory_fs.schemas.Schema__Memory_FS__File__Config import Schema__Memory_FS__File__Config
from memory_fs.file_types.Memory_FS__File__Type__Json import Memory_FS__File__Type__Json

# 1. Instantiate Memory_FS
memory_fs = Memory_FS()

# 2. Configure Schema__Memory_FS__File__Config
latest_handler = Path__Handler__Latest()
file_config = Schema__Memory_FS__File__Config(
    path_handlers     = [latest_handler],      # Pass a list of instances
    default_handler   = Path__Handler__Latest,          # Pass the type for default
    file_type         = Memory_FS__File__Type__Json()
)

# Data to save
data_to_save = {"message": "Hello, Memory-FS!", "version": 1.0}
file_name    = "example" # File name without extension, as type handles it

# 3. Save a dictionary
# The key in saved_paths will be the handler's name (e.g., 'latest')
# Wrap in Duration to see execution time, similar to original example
with Duration(prefix='Memory_FS__Save', print_result=True):
    saved_paths = memory_fs.save(file_data=data_to_save, file_config=file_config, file_name=file_name)

if saved_paths:
    # Assuming Path__Handler__Latest has name 'latest'
    # And that metadata path is what we want to primarily refer to
    primary_metadata_path = saved_paths.get(latest_handler.name)
    print(f"File metadata saved at path like: {primary_metadata_path}")

    # To get full metadata, one would typically load the metadata file itself
    # For this example, we just show the path.
else:
    print("File not saved.")


# 4. Load the data back
# The load method should use the config to find the file.
# Wrap in Duration to see execution time
with Duration(prefix='Memory_FS__Load', print_result=True):
    loaded_data = memory_fs.load_data(file_name=file_name, file_config=file_config)

print(f"Data loaded from {file_name}.{file_config.file_type.file_extension}: {loaded_data}")

# Example of how to list files (path will vary based on handler)
# print(memory_fs.files(config=file_config))
# Details for a specific file (path will vary based on handler, e.g. 'latest/example.json')
# file_details = memory_fs.file_details(file_path='latest/example.json', config=file_config) # Replace with actual path
# if file_details:
#     print(f"Details for 'latest/example.json': {file_details}")

```

**Note:** The project currently uses `Memory_FS__File__System` for in-memory storage. The path handlers like `Path__Handler__Latest` are defined, but their specific `generate_path` logic might be simulated in some actions (as seen in `Memory_FS__Save`). The example above reflects a functional case based on the current codebase.
