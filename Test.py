import os


def create_user_folder(folder_name):
    """
    Creates a folder with the user-specified name in the current working directory.

    Args:
        folder_name (str): Name of the folder to create

    Returns:
        str: Path of the created folder or None if there was an error
    """
    try:
        # Get current working directory
        current_directory = os.getcwd()

        # Create the full path for the new folder
        folder_path = os.path.join(current_directory, folder_name)

        # Check if folder already exists
        if not os.path.exists(folder_path):
            # Create the folder
            os.makedirs(folder_path)

        return folder_path

    except Exception:
        return None

# Example usage
print(create_user_folder('¨Exportacion'))