from pathlib import Path
from shutil import copy, move

def check_dir_or_path(dir_or_path):
    return Path(dir_or_path)


def check_suffix(suffix):
    return (suffix if suffix.startswith(".") else f".{suffix}").lower()


def find_files_in_dir(
    dir: str | Path,
    suffixes: list[str] = [".jpeg", ".jpg", ".png", ".json"],
    recurrence=True,
) -> list[Path]:
    dir = check_dir_or_path(dir)
    suffixes = [check_suffix(suffix) for suffix in suffixes]
    files = dir.rglob("*") if recurrence else dir.glob("*")
    files = [file for file in files if file.is_file() and file.suffix.lower() in suffixes]

    return files


# 递归版本(找图)
def find_images_in_dir(
    image_dir: str | Path,
    image_suffixes: list[str] = [".jpeg", ".jpg", ".png"],
    recurrence=False,
) -> list[Path]:
    return find_files_in_dir(image_dir, image_suffixes, recurrence)


# 递归版本(找标签)
def find_labels_in_dir(
    label_dir: str | Path,
    label_suffixes: list[str] = [".json"],
    recurrence=False,
) -> list[Path]:
    return find_files_in_dir(label_dir, label_suffixes, recurrence)


def find_related_file_by_suffixes(path: str | Path, suffixes: list[str] = [".jpeg", ".jpg", ".png", ".json"]) -> Path:
    path = check_dir_or_path(path)
    suffixes = [check_suffix(suffix) for suffix in suffixes]
    parent = path.parent
    stem = path.stem
    files = parent.glob(f"{stem}.*")
    files = [file for file in files if file.is_file() and file.suffix.lower() in suffixes]
    file = files[0] if files else None

    return file


def find_label_path_from_image(
    image_path: str | Path,
    label_suffixes: list[str] = [".json"],
) -> Path:
    return find_related_file_by_suffixes(image_path, label_suffixes)


def find_image_path_from_label(
    label_path: str | Path,
    image_suffixes: list[str] = [".jpeg", "jpg", "png"],
) -> Path:
    return find_related_file_by_suffixes(label_path, image_suffixes)


def copy_file(
    source_path: str | Path,
    target_path: str | Path,
):
    source_path = check_dir_or_path(source_path)
    target_path = check_dir_or_path(target_path)

    assert source_path.suffix.lower() == target_path.suffix.lower()

    target_path.parent.mkdir(parents=True, exist_ok=True)

    copy(source_path, target_path)


def move_file(
    source_path: str | Path,
    target_path: str | Path,
):
    source_path = check_dir_or_path(source_path)
    target_path = check_dir_or_path(target_path)

    assert source_path.suffix.lower() == target_path.suffix.lower()

    target_path.parent.mkdir(parents=True, exist_ok=True)

    move(source_path, target_path)


def link_file(
    source_path: str | Path,
    target_path: str | Path,
):
    source_path = check_dir_or_path(source_path)
    target_path = check_dir_or_path(target_path)

    assert source_path.suffix.lower() == target_path.suffix.lower()

    target_path.parent.mkdir(parents=True, exist_ok=True)

    target_path.hardlink_to(source_path)


def find_sites_in_dir(dir: str | Path) -> list[Path]:
    dir = check_dir_or_path(dir)
    sites = [
        folder for folder in dir.rglob("*") if folder.is_dir() and not any(subfolder.is_dir() for subfolder in folder.iterdir())
    ]

    return sites


def find_image_name_from_annotation(annotation: dict | str | Path) -> Path:
    if isinstance(annotation, dict):
        image_name = annotation["meta"]["path"]

    if isinstance(annotation, str):
        annotation = Path(annotation)

    if isinstance(annotation, Path):
        if "@" in annotation.name:
            image_name = annotation.name.split("@")[0]
        else:
            image_name = annotation.stem

    return image_name


def find_annotation_path_from_image(
    image_path: Path,
    annotation_suffix: str = ".annotate",
) -> Path:
    annotation_paths = list(image_path.parent.glob(f"{image_path.name}@*{annotation_suffix}"))
    annotation_path = annotation_paths[0] if annotation_paths else None

    return annotation_path


# 返回格式为 [点位名称，具体文件地址]
def find_file_in_dir(source_dir, img_suffix) -> list:
    image_dirs = []
    point_dirs = list(Path(source_dir).iterdir())
    data_dirs = []

    for point_dir in point_dirs:
        image_dir = sorted(Path(point_dir).rglob(f"*{img_suffix}"))
        image_dirs.append(image_dir)

    for x, y in zip(point_dirs, image_dirs):
        data_dirs.append([x, y])

    return data_dirs
