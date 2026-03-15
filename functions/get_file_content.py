import os
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file_path = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs

        if not valid_file_path:
            raise PermissionError(f'Cannot read "{file_path}" as it is outside the permitted working directory')
        
        if not os.path.isfile(file_path_abs):
            raise FileNotFoundError(f'File not found or is not a regular file: "{file_path}"')

        MAX_CHARS = 10000

        with open(file_path_abs, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        print(file_content_string)

    except PermissionError as e:
        print(f"Error: {e}")

    except NotADirectoryError as e:
        print(f"Error: {e}")

    except FileNotFoundError as e:
        print(f"Error: {e}")

    except OSError as e:
        return f"OS Error: {e}"

    except Exception as e:
        return f"Unexpected Error: {e}"
    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="See file content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to the file to be read. Should include the file name and extension.",
            ),
        },
    ),
)