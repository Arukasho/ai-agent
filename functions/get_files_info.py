import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            raise PermissionError(f'Cannot list "{directory}" as it is outside the permitted working directory')
        
        if not os.path.isdir(target_dir):
            raise NotADirectoryError(f'"{directory}" is not a directory')

        content_list = os.listdir(target_dir)
        content_info = []

        for content in content_list:
            content_directory = os.path.normpath(os.path.join(target_dir, content))
            info_text = f"{content}: file_size= {os.path.getsize(content_directory)} bytes, is_dir={os.path.isdir(content_directory)}"
            content_info.append(info_text)

        content_summary = "\n".join(content_info)

        print(content_summary)
        return content_summary

    except PermissionError as e:
        print(f"Error: {e}")

    except NotADirectoryError as e:
        print(f"Error: {e}")

    except FileNotFoundError as e:
        return f"File Not Found: {e}"

    except OSError as e:
        return f"OS Error: {e}"

    except Exception as e:
        return f"Unexpected Error: {e}"