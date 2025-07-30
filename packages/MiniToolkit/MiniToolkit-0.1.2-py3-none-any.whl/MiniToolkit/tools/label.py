import json
from pathlib import Path

import cv2
import numpy as np

from MiniToolkit.tools.mask import polygon_to_box, polygon_to_mask
from MiniToolkit.tools.path import check_dir_or_path


def just_load_label(label_path: str | Path):
    with open(label_path, "r", encoding="utf-8") as file:
        loaded_label = json.load(file)

    return loaded_label


def convert_label_to_instances(label: dict, classes_name_to_id: dict):
    image_height = label["imageHeight"]
    image_width = label["imageWidth"]

    instances = []
    for shape in label["shapes"]:
        class_name = shape["label"]
        if class_name not in classes_name_to_id:
            continue
        class_id = classes_name_to_id[class_name]
        if len(shape["points"]) == 1:
            print("跳过标注点数为1的实例")
            continue
        elif len(shape["points"]) == 2: # box分支
            box = np.array(shape["points"], dtype=np.int32).reshape((-1))
            polygon = np.array([[box[0], box[1]], [box[2], box[1]], [box[2], box[3]], [box[0], box[3]]])
        else: # polygon分支
            polygon = np.array(shape["points"], dtype=np.int32)
            box = polygon_to_box(polygon, image_height, image_width)

        mask = polygon_to_mask(polygon, image_height, image_width)

        instances.append(
            {
                "class_id": class_id,
                "label": class_name,
                "polygon": polygon,
                "box": box,
                "mask": mask,
                "group_id": shape.get("group_id", None),
                "area": np.sum(mask),
            }
        )

    return instances


def convert_instances_to_label(
    instances: list[dict],
    classes_id_to_name: dict,
    image_name: str | Path,
    image_height: int,
    image_width: int,
):
    shapes = []
    for instance in instances:
        class_id = instance["class_id"]
        if class_id not in classes_id_to_name:
            continue
        class_name = classes_id_to_name[class_id]
        polygon = instance["polygon"].tolist()
        if len(polygon) < 3: # box分支
            shape_type = "rectangle"
        else: # 多边形分支
            shape_type = "polygon"
        shapes.append(
            {
                "label": class_name,
                "points": polygon,
                "group_id": None,
                "shape_type": shape_type,
                "flags": {},
            }
        )
    image_name = check_dir_or_path(image_name).name
    label = {
        "version": "4.6.0",
        "flags": {},
        "shapes": shapes,
        "imagePath": image_name,
        "imageData": None,
        "imageHeight": image_height,
        "imageWidth": image_width,
    }
    return label



def check_available(
    label_path: str | Path,
    available_labels: list | dict = ["wanglei", "molei"],
    not_available_labels: list | dict = ["null", "blur"],
) -> bool:
    available = False
    label_path = check_dir_or_path(label_path)
    with open(str(label_path), "r") as f:
        label = json.load(f)
        for shape in label["shapes"]:
            if shape in not_available_labels:
                # return False
                available = False
                break
            if shape["label"] in available_labels:
                available = True

    return available


def get_shapes_from_label(
    label_path: str | Path,
    label_to_id: dict,
    image_height: int,
    image_width: int,
    by_label: bool = False,
) -> np.ndarray:
    label_path = check_dir_or_path(label_path)

    assert label_path.exists(), f"{label_path}文件不存在"
    assert label_path.suffix == ".json", "目前仅支持json文件格式的labelme标注"

    shapes = []
    if by_label:
        shapes = {key: [] for key in label_to_id}

    with open(str(label_path), "r") as f:
        label = json.load(f)
        for shape in label["shapes"]:
            if shape["label"] not in label_to_id:
                continue
            if len(shape["points"]) < 3:
                continue

            points = []
            for point in shape["points"]:
                if 0 <= point[0] <= image_width and 0 <= point[1] <= image_height:
                    points.append(point)
                else:
                    point[0] = max(0, min(point[0], image_width))
                    point[1] = max(0, min(point[1], image_height))
                    points.append(point)

            if all(point[0] == 0 or point[0] == image_width or point[1] == 0 or point[1] == image_height for point in points):
                continue

            if by_label:
                if points in shapes[shape["label"]]:
                    continue
                shapes[shape["label"]].append(points)

            else:
                shape["points"] = points
                if shape in shapes:
                    continue
                shapes.append(shape)

    return shapes


def get_mask_from_label(
    label_path: Path,
    label_to_id: dict,
    image_height: int,
    image_width: int,
    one_hot: bool = True,
) -> np.ndarray:
    # assert label_path.exists(), f"{label_path}文件不存在"
    assert label_path.suffix == ".json", "目前仅支持json文件格式的labelme标注"

    with open(str(label_path), "r") as f:
        label = json.load(f)

        if one_hot:
            mask = np.zeros((len(label_to_id), image_height, image_width), dtype=np.uint8)  # [cls, h, w]
        else:
            mask = np.zeros(
                (len(label_to_id), len(label["shapes"]), image_height, image_width),
                dtype=np.uint8,
            )  # [cls, n, h, w]

        for shape_index, shape in enumerate(label["shapes"]):
            if shape["label"] not in label_to_id:
                continue
            points = np.array(shape["points"], dtype=np.int32)
            if one_hot:
                cv2.fillPoly(mask[label_to_id[shape["label"]]], [points], 1)
            else:
                cv2.fillPoly(mask[label_to_id[shape["label"]]][shape_index], [points], 1)

        return mask


def get_polygons_from_label(
    label_path: Path,
    label_to_id: dict,
    image_height: int = None,
    image_width: int = None,
    cls_exclusion_list: list = [],
    attr_exclusion_list: list = [],
    encoding: str = "utf-8",
    id_map=None,
):
    polygons = []
    with open(label_path, "r", encoding=encoding) as file:
        label = json.load(file)
        height = label["imageHeight"] if image_height is None else image_height
        width = label["imageWidth"] if image_width is None else image_width
        shapes = label["shapes"]
        for shape in shapes:
            if id_map:
                shape["label"] = id_map[shape["label"]]
            if shape["label"] not in label_to_id:
                continue

            if label_to_id[shape["label"]] in cls_exclusion_list:
                continue

            group_id = convert_attributes_to_int(shape["group_id"])
            if group_id & set(attr_exclusion_list):
                continue

            label_id = label_to_id[shape["label"]]
            group_id = shape["group_id"]

            points = shape["points"]
            if points[-1] == points[0]:
                points = points[:-1]
            if len(points) < 3:
                continue

            normalized_points = [[point[0] / width, point[1] / height] for point in points]
            flattened_croods = [crood for point in normalized_points for crood in point]
            truncated_croods = [max(0.0, min(1.0, crood)) for crood in flattened_croods]
            polygon = [label_id] + [group_id] + truncated_croods
            if polygon not in polygons:
                polygons.append(polygon)

    return polygons


def save_label_to_json(
    label: dict,
    save_path: str | Path,
    encoding: str = "utf-8",
    ensure_ascii: bool = False,
    indent: int = 2,
    lines=False,
):
    save_path = check_dir_or_path(save_path)

    save_path.parent.mkdir(parents=True, exist_ok=True)

    if lines:
        with open(save_path.with_suffix(".jsonl"), "w", encoding=encoding) as file:
            for line in label:
                data = json.dumps(line, ensure_ascii=ensure_ascii)
                file.write(f"{data}\n")
    else:
        with open(save_path.with_suffix(".json"), "w", encoding=encoding) as file:
            json.dump(label, file, ensure_ascii=ensure_ascii, indent=indent)


def save_label_to_txt(
    label: list,
    save_path: str | Path,
    encoding: str = "utf-8",
):  # yolo format polygons
    save_path = check_dir_or_path(save_path)

    assert save_path.suffix.lower() == ".txt"

    save_path.parent.mkdir(parents=True, exist_ok=True)

    with open(save_path, "w", encoding=encoding) as file:
        for polygon in label:
            # 保留attr
            # string = " ".join([f"{val:.6f}" if idx > 1 else (str(0) if val is None else str(val)) for idx, val in enumerate(polygon)])

            # 去除attr
            string = " ".join([f"{val:.6f}" if idx > 1 else str(val) for idx, val in enumerate(polygon) if idx != 1])

            file.write(string + "\n")


def convert_attributes_to_int(nums: int) -> set[int]:
    # num2set
    if nums == 0 or nums is None:
        groups = {0}
    else:
        groups = set()
        while nums > 0:
            groups.add(int(nums % 10))
            nums //= 10
    return groups
