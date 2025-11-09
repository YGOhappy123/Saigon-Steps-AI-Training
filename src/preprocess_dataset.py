from pathlib import Path
from dotenv import dotenv_values

config = dotenv_values(".env")

dataset_path = config.get('DATASET_PATH')
if not dataset_path:
    raise ValueError("[DATASET_PATH] missing in environment file.")


def modify_dataset_labels(dataset_path: str, dir_name: str, exclude_classes: list):
    """
    Modifies the label files in the specified labels_directory by replacing the first character
    of each line with '0' to reduce the dataset to single-class.
    Args:
        dataset_path (str): The base path to the dataset.
        dir_name (str): The name of the subdirectory containing label files.
        exclude_classes (list): List of class indices to exclude.
    Raises:
        FileNotFoundError: If the specified directory does not contain labels folder.
    """

    directory = Path(dataset_path, dir_name)
    labels_directory = Path(dataset_path, dir_name, "labels")
    if directory.exists() and not labels_directory.exists():
        raise FileNotFoundError(
            f"The directory [{labels_directory}] is not containing labels folder."
        )

    for file in labels_directory.iterdir():
        if file.is_file():
            with file.open(encoding='utf-8') as f:
                lines = f.readlines()

            modified_lines = []
            for line in lines:
                first_char = line[0]
                if first_char not in exclude_classes:
                    modified_line = f"0 {line[2:]}"
                    modified_lines.append(modified_line)

            with file.open('w', encoding='utf-8') as f:
                for modified_line in modified_lines:
                    f.write(modified_line)


if __name__ == "__main__":
    splitted_dirs = ['train', 'test', 'valid']
    exclude_classes = []
    for dir_name in splitted_dirs:
        modify_dataset_labels(dataset_path, dir_name, exclude_classes)
