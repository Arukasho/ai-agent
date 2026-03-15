import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file_path = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs

        if not valid_file_path:
            raise PermissionError(f'Cannot execute "{file_path}" as it is outside the permitted working directory')
        
        if not os.path.isfile(file_path_abs):
            raise FileNotFoundError(f'"{file_path}" does not exist or is not a regular file: "{file_path}"')

        if not file_path.endswith(".py"):
            raise ValueError(f'"{file_path}" is not a Python file')

        command = ["python", file_path_abs]

        if args is not None:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

        output = ""

        if completed_process.returncode != 0:
            output += f"Process exited with code {completed_process.returncode}\n"

        if not completed_process.stdout and not completed_process.stderr:
            output += "No output produced", "\n"
        else:
            if completed_process.stdout:
                output += f'STDOUT: {completed_process.stdout}\n'
            if completed_process.stderr:
                output += f'STDERR: {completed_process.stderr}\n'

        print(output)
        return output


    except PermissionError as e:
        print(f"Error: {e}")

    except NotADirectoryError as e:
        print(f"Error: {e}")

    except FileNotFoundError as e:
        print(f"Error: {e}")

    except ValueError as e:
        print(f"Error: {e}")

    except OSError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Error: {e}")

    except subprocess.TimeoutExpired:
        print("Command took longer than 30 seconds and was stopped.")

    except subprocess.CalledProcessError as e:
        print(f"Error: executing Python file: {e}")    


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "args"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to the python file to be run.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Array of python files to be run.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Python file to be run.",
                    ),
                ),
            },
        ),
    )