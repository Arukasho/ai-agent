import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file_path = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs

        if not valid_file_path:
            raise PermissionError(f'Cannot write to "{file_path}" as it is outside the permitted working directory')
        
        if os.path.isdir(file_path_abs):
            raise IsADirectoryError(f'Cannot write to "{file_path}" as it is a directory')

        os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)

        with open(file_path_abs, "w") as f:
            f.write(content)
            print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')

    except PermissionError as e:
        print(f"Error: {e}")

    except IsADirectoryError as e:
        print(f"Error: {e}")

    except FileNotFoundError as e:
        print(f"Error: {e}")

    except Exception as e:
        return f"Unexpected Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content into a file at the specified path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to write",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write into the file",
            ),
        },
    ),
)