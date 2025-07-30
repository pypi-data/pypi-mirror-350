import os
from nbforge.logger import setup_logger

logger = setup_logger(__name__)


def write_to_file(output_dir, file_name, file_content):
    """
    Writes content to a file in the specified output directory, creating the directory if it doesn't exist.

    Args:
        output_dir (str): Directory to write to.
        file_name (str): Name of the file to write.
        file_content (str): Content to write to the file.

    Returns:
        None
    """
    os.makedirs(output_dir, exist_ok=True)
    os.path.join(output_dir, file_name)
    file_path = f"{output_dir}/{file_name}"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(file_content)
