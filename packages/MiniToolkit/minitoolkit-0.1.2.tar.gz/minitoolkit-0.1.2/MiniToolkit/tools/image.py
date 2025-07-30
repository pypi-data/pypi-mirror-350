import math
import random
from io import BytesIO
from pathlib import Path
from typing import Optional, Union

import cv2
import numpy as np
from PIL import Image, ImageFile, ImageOps

ImageFile.LOAD_TRUNCATED_IMAGES = True
# from skimage.metrics import normalized_root_mse as nrmse
# from skimage.metrics import structural_similarity as ssim

from MiniToolkit.tools.path import check_dir_or_path


# PIL -> cv2
def just_load_image(image_path: str | Path, grey=False):
    with Image.open(image_path) as loading_image:
        if loading_image.format not in {"JPEG", "PNG", "BMP"}:
            with BytesIO() as loading_buffer:
                loading_image.save(loading_buffer, format="PNG")
                loading_image = Image.open(loading_buffer)
        loading_image = loading_image.convert("RGB")
        loading_image = ImageOps.exif_transpose(loading_image)
    loaded_image = cv2.cvtColor(np.array(loading_image), cv2.COLOR_RGB2BGR)
    if grey:
        loaded_image = cv2.cvtColor(loaded_image, cv2.COLOR_BGR2GRAY)

    return loaded_image


# cv2 -> PIL
def just_save_image(image: np.array, save_path: str | Path, save_format: str = "JPEG", save_quality: int = 100):
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    image.save(save_path, format=save_format, quality=save_quality)


def load_image(
    image_path: str | Path,
    force_rgb: bool = False,
    force_float: bool = False,
    force_tensor: bool = False,
):
    if force_tensor:
        force_float = True

    with Image.open(image_path) as loading_image:
        # 检查图像格式
        if loading_image.format not in {"JPEG", "PNG", "BMP"}:
            with BytesIO() as loading_buffer:
                loading_image.save(loading_buffer, format="PNG")
                loading_image = Image.open(loading_buffer)

        # 检查颜色空间
        if loading_image.mode != "RGB":
            loading_image = loading_image.convert("RGB")

        # 转为cv2图像格式，即BGR顺序的numpy.ndarray，除非强制指定RGB顺序。
        loaded_image = np.array(loading_image)
        if not force_rgb:
            loaded_image = cv2.cvtColor(loaded_image, cv2.COLOR_RGB2BGR)

        # [0, 255]的uint8转为[0, 1]的float32
        if force_float:
            loaded_image = loaded_image.astype(np.float32) / 255.0

        return loaded_image


# cv2实现的保存图片
def save_image(image: np.ndarray, save_path: str | Path, save_format: str = "JPEG", save_quality: int = 99):
    save_path = check_dir_or_path(save_path)

    assert save_path.suffix.lower() == f".{save_format.lower()}", f"保存格式{save_format}必须与保存路径后缀名{save_path.suffix}匹配。"

    save_path.parent.mkdir(parents=True, exist_ok=True)

    if save_format.lower() == "jpeg":
        cv2.imwrite(str(save_path), image, [int(cv2.IMWRITE_JPEG_QUALITY), save_quality])
    elif save_format.lower() == "png":
        cv2.imwrite(str(save_path), image)
    else:
        raise ValueError(f"不支持保存格式{save_format}。")


def pil_save_image(image: np.array, save_path: str | Path, save_quality: int = 99):
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    image.save(save_path, quality=save_quality)


def load_images_by_window(
    image: str | Path | np.ndarray,
    by_window: bool = True,
    window_size: int = 1024,
):
    if isinstance(image, (str, Path)):
        # image = cv2.imread(str(image))
        image = load_image(image)
    assert isinstance(image, np.ndarray)

    image_height, image_width, _ = image.shape
    # if window_size > max(image_width, image_height):
    #     by_window = False

    if by_window:
        # window_size = min(window_size, image_height, image_width)
        crop_windows = get_sliding_windows(image_width, image_height, window_size)
        cropped_images = crop_image_by_windows(image, crop_windows)
    else:
        # window_size = max(window_size, image_height, image_width)
        # crop_windows = get_windows(image_width, image_height, window_size)
        crop_windows = [[0, 0, image_width, image_height]]
        assert len(crop_windows) == 1
        cropped_images = crop_image_by_windows(image, crop_windows)

    return cropped_images, crop_windows


def get_sliding_windows(
    image_width: int,
    image_height: int,
    window_size: int,
    all_window: bool = False,  # 是否加入全图窗口
) -> list:
    sliding_windows = []
    window_size = min(window_size, image_height, image_width)

    window_num_on_x = math.ceil(image_width / window_size)
    window_num_on_y = math.ceil(image_height / window_size)

    step_size_on_x = math.ceil((image_width - window_size) / (window_num_on_x - 1)) if window_num_on_x > 1 else image_width
    step_size_on_y = math.ceil((image_height - window_size) / (window_num_on_y - 1)) if window_num_on_y > 1 else image_height

    for x_index in range(window_num_on_x):
        xmin = x_index * step_size_on_x  # 计算初始min
        xmax = min(xmin + window_size, image_width)  # 截断max
        xmin = max(xmax - window_size, 0)  # 反向截断min

        for y_index in range(window_num_on_y):
            ymin = y_index * step_size_on_y
            ymax = min(ymin + window_size, image_height)
            ymin = max(ymax - window_size, 0)
            sliding_windows.append([xmin, ymin, xmax, ymax])

    if all_window:
        sliding_windows.append([0, 0, image_width, image_height])

    return sliding_windows


def get_dynamic_sliding_windows(image_width: int, image_height: int, window_size: int, extra_window_size: int) -> list:
    sliding_windows = []

    window_num_on_x, real_window_size_x, step_size_on_x = caculate_edge_num_size_step(image_width, window_size, extra_window_size)
    window_num_on_y, real_window_size_y, step_size_on_y = caculate_edge_num_size_step(image_height, window_size, extra_window_size)

    for x_index in range(window_num_on_x):
        xmin = x_index * step_size_on_x  # 计算初始min
        xmax = min(xmin + real_window_size_x, image_width)  # 截断max
        xmin = max(xmax - real_window_size_x, 0)  # 反向截断min

        for y_index in range(window_num_on_y):
            ymin = y_index * step_size_on_y
            ymax = min(ymin + real_window_size_y, image_height)
            ymin = max(ymax - real_window_size_y, 0)
            sliding_windows.append([xmin, ymin, xmax, ymax])

    return sliding_windows


def caculate_edge_num_size_step(origin_size, window_size, extra_window_size):
    """
    输入值:原始窗口尺寸
    返回值:滑窗数量,滑窗尺寸,滑动距离
    """
    window_num = origin_size // window_size
    b = origin_size % window_size
    real_num = math.ceil(origin_size / window_size)

    if window_num == 0:
        return 1, origin_size, 0
    elif b == 0:
        return window_num, window_size, window_size

    per_window_extra_are = math.ceil(b / window_num)
    if per_window_extra_are > extra_window_size:
        return real_num, window_size, math.ceil((origin_size - window_size) / (real_num - 1))
    else:
        real_size = window_size + per_window_extra_are
        return window_num, real_size, math.ceil((origin_size - real_size) / (real_num - 1))


def crop_image_by_windows(
    image: np.ndarray,
    windows: list,
) -> list[np.ndarray]:
    cropped_images = []
    for window_xmin, window_ymin, window_xmax, window_ymax in windows:
        cropped_image = image[window_ymin:window_ymax, window_xmin:window_xmax]
        cropped_images.append(cropped_image)

    return cropped_images


def compute_similarity(
    refer_image: np.ndarray,
    query_image: np.ndarray,
    similarity_type: str = "nrmse",
):
    assert similarity_type in {"nrmse", "ssim"}, f"不支持{similarity_type}相似度。"

    refer_height, refer_width, refer_channel = refer_image.shape
    query_height, query_width, query_channel = query_image.shape
    assert refer_channel == query_channel == 3

    if (refer_height, refer_width) != (query_height, query_width):
        refer_image = cv2.resize(refer_image, (query_width, query_height))

    if similarity_type == "nrmse":
        return 1 - nrmse(refer_image, query_image)
    else:
        return ssim(refer_image, query_image, channel_axis=3)


def match_refer_image_for_query(
    query_image: Union[str, Path, np.ndarray],
    refer_images: list[Union[str, Path, np.ndarray]],
    match_type: str = "random",
    similarity_type: str = "ssim",
):
    assert len(refer_images)
    if len(refer_images) == 1:
        return refer_images[0]

    if match_type == "random":
        matched_image = random.choice(refer_images)
        return matched_image

    elif match_type == "latest":  # todo 这个需要写一个从文件名解析时间字符串的函数，或者让传进来的时候把点位时间都传进来。
        assert isinstance(query_image, (str, Path))

        pass

    elif match_type == "max-similarity":
        matched_similarity = 0.0
        if isinstance(query_image, (str, Path)):
            query_image = just_load_image(query_image)
        for refer_image in refer_images:
            if isinstance(refer_image, (str, Path)):
                refer_image = just_load_image(refer_image)
            similarity = compute_similarity(refer_image, query_image, similarity_type=similarity_type)
            if similarity > matched_similarity:
                matched_similarity = similarity
                matched_image = refer_image
        return matched_image

    else:
        raise ValueError(f"{match_type}匹配模式不在实现计划中")


def get_random_rgb_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def visualize_instance_on_image(
    image: np.ndarray,
    instance: dict,
    class_mapper: dict[int, str] = None,
    state_mapper: Optional[dict[int, str]] = None,
    show_filter: list[Union[str]] = ["class", "state", "box", "polygon"],
    color: Optional[tuple[int]] = None,
    thickness: Optional[int] = None,
):
    if color is None:
        color = get_random_rgb_color()

    if thickness is None:
        thickness = max(round(sum(image.shape) / 2 * 0.001), 2)

    assert "box" in show_filter or "polygon" in show_filter or "mask" in show_filter

    box, polygon, mask = None, None, None
    if "box" in show_filter:
        box = instance.get("box", None)
        if box is not None:
            cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), color, thickness, cv2.LINE_AA)

    if "polygon" in show_filter:
        polygon = instance.get("polygon", None)
        if polygon is not None:
            cv2.polylines(image, [polygon], True, color, thickness, cv2.LINE_AA)

    if "mask" in show_filter:
        pass

    name_localization = None
    if box is not None:
        name_localization = (box[0], box[1])

    if name_localization is None and polygon is not None:
        name_localization = tuple(polygon[0].tolist())

    if name_localization is None and mask is not None:
        pass

    if name_localization is not None:
        show_names = []
        if "class" in show_filter:
            class_id = instance.get("class_id", -1)
            class_name = (class_mapper[class_id] if class_mapper else str(class_id)) if class_id >= 0 else "unknown"
            show_names.append(class_name)
        if "state" in show_filter:
            state_id = instance.get("state_id", -1)
            state_name = (state_mapper[state_id] if state_mapper else str(state_id)) if state_id >= 0 else "unknown"
            show_names.append(state_name)

        if show_names:
            show_name = "-".join(show_names)
            font_scale = thickness / 3
            font_thickness = max(thickness - 1, 1)
            name_width, name_height = cv2.getTextSize(show_name, 0, fontScale=font_scale, thickness=font_thickness)[0]
            outside = name_localization[1] - name_height >= 10
            cv2.rectangle(
                image,
                name_localization,
                (
                    name_localization[0] + name_width,
                    (name_localization[1] - name_height - 10 if outside else name_localization[1] + name_height + 10),
                ),
                color,
                -1,
                cv2.LINE_AA,
            )
            cv2.putText(
                image,
                show_name,
                (
                    name_localization[0],
                    name_localization[1] - 10 if outside else name_localization[1] + name_height + 10,
                ),
                0,
                font_scale,
                (255, 255, 255),
                font_thickness,
                cv2.LINE_AA,
            )


def visualize_title_on_image(
    image: np.ndarray,
    title: str,
    color: Optional[tuple[int]] = None,
    thickness: Optional[int] = None,
):
    title = title.capitalize()

    if color is None:
        color = (0, 0, 0)

    if thickness is None:
        thickness = max(round(sum(image.shape) / 2 * 0.003), 2)

    title_width, title_height = cv2.getTextSize(title, 0, fontScale=thickness / 3, thickness=thickness)[0]
    cv2.putText(
        image,
        title,
        (image.shape[1] - 10 - title_width, 20 + title_height),
        0,
        thickness / 3,
        color,
        thickness,
        cv2.LINE_AA,
    )


def visualize_instances_on_image(
    image: Union[str, Path, np.ndarray],
    instances: list[dict],
    class_mapper: dict[int, str],
    state_mapper: Optional[dict[int, str]] = None,
    class_filter: Optional[Union[list[int], dict[int, str]]] = None,
    state_filter: Optional[Union[list[int], dict[int, str]]] = None,
    show_filter: Optional[list[Union[str]]] = ["class", "state", "box", "polygon"],
    title: Optional[str] = None,
) -> np.ndarray:

    visualizing_image = just_load_image(image) if isinstance(image, (str, Path)) else np.copy(image)

    for instance in instances:
        if class_filter is not None and instance["class_id"] not in class_filter:
            continue
        if state_filter is not None and "state_id" in instance and instance["state_id"] not in state_filter:
            continue

        visualize_instance_on_image(
            visualizing_image,
            instance,
            class_mapper=class_mapper,
            state_mapper=state_mapper,
            show_filter=show_filter,
        )

    if "title" in show_filter and title is not None:
        visualize_title_on_image(visualizing_image, title)

    return visualizing_image
