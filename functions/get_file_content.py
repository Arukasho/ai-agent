import os
from .. import config

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.abspath(file_path)
        valid_file_path = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs

        if not valid_file_path:
            raise PermissionError(f'Cannot read "{file_path}" as it is outside the permitted working directory')
        
        if not os.path.isfile(file_path_abs):
            raise FileNotFoundError(f'File not found or is not a regular file: "{file_path}"')

        

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