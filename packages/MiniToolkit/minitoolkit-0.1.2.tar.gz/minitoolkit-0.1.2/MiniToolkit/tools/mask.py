import cv2
import numpy as np

# def polygon_to_mask(polygon, image_height, image_width):
#     mask = np.zeros((image_height, image_width), dtype=np.uint8)
#     polygon = np.array(polygon, dtype=np.int32)
#     cv2.fillPoly(mask, [polygon], 1)

#     return mask


# def mask_to_polygons(mask, pixel_threshold=8):
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     polygons = []
#     for contour in contours:
#         if len(contour) < 3:
#             continue
#         contour = contour.squeeze().astype(np.float32)
#         x, y, w, h = cv2.boundingRect(contour)
#         if (w < pixel_threshold) or (h < pixel_threshold):
#             continue
#         points = contour.tolist()
#         polygons.append(points)

#     return polygons


def mask_to_polygons(
    mask: np.ndarray,
    area_threshold: int = 4000,
    min_point_threshold: int = 10,
    max_point_threshold: int = 35,
    approx_tolerance: float = 0.001,
) -> list[np.array]:
    mask = mask.astype(bool)
    contours = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    polygons = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < area_threshold:
            continue

        if len(contour) <= min_point_threshold:
            polygons.append(contour.reshape(-1, 2).astype(np.int32))
            continue

        epsilon = approx_tolerance * cv2.arcLength(contour, True)
        for _ in range(10):
            polygon = cv2.approxPolyDP(contour, epsilon, True)
            if len(polygon) >= max_point_threshold:
                epsilon *= 1.3
            elif len(polygon) <= min_point_threshold:
                epsilon *= 0.8
            else:
                break

        polygons.append(polygon.reshape(-1, 2).astype(np.int32))

    return polygons


def mask_to_polygon(
    mask: np.ndarray,
    strategy: str = "largest",
    approx: bool = True,
    approx_tolerance: float = 0.001,
):

    # contours = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contours = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]

    if contours:
        if strategy == "concat":  # concatenate all segments
            contour = np.concatenate([x.reshape(-1, 2) for x in contours])
        elif strategy == "largest":  # select largest segment
            contour = np.array(contours[np.array([len(x) for x in contours]).argmax()]).reshape(-1, 2)

        if approx:
            epsilon = approx_tolerance * cv2.arcLength(contour, True)
            polygon = cv2.approxPolyDP(contour, epsilon, True)
            polygon = polygon.reshape(-1, 2).astype(np.int32)

        else:
            polygon = contour.reshape(-1, 2).astype(np.int32)

    else:
        polygon = np.zeros((0, 2)).astype(np.int32)

    return polygon


def polygon_to_mask(polygon: np.ndarray, height: int, width: int):
    # polygon的形状[x,y]
    # mask的形状[h,w]
    mask = np.zeros((height, width), dtype=np.uint8)
    polygon = np.array(polygon, dtype=int)
    cv2.fillConvexPoly(mask, polygon, 1)
    mask = mask.astype(bool)

    return mask


def polygon_to_box(polygon: np.ndarray, height: int, width: int):
    x, y = polygon.T  # segment xy
    inside = (x >= 0) & (y >= 0) & (x <= width) & (y <= height)
    x, y = x[inside], y[inside]
    box = np.array([x.min(), y.min(), x.max(), y.max()], dtype=polygon.dtype) if any(x) else np.zeros(4, dtype=polygon.dtype)

    return box


# 考虑到mask不一定是完全连续的，也就是可能与多个多边形对应，因此这里不实现mask2box


# def get_contours_from_mask(mask: np.ndarray, refine=True, remove=False):
#     contours, _ = cv2.findContours(mask.astype(np.uint8) * 255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#     if refine:  # Refine contours
#         approx_contours = []
#         for contour in contours:
#             # Approximate contour
#             epsilon = 0.001 * cv2.arcLength(contour, True)
#             approx = cv2.approxPolyDP(contour, epsilon, True)
#             approx_contours.append(approx)

#         if remove:
#             # Remove too big contours ( >90% of image size)
#             if len(approx_contours) > 1:
#                 areas = [cv2.contourArea(contour) for contour in approx_contours]
#                 image_size = mask.shape[0] * mask.shape[1]
#                 filtered_approx_contours = [
#                     contour for contour, area in zip(approx_contours, areas) if area < image_size * 0.9
#                 ]
#                 approx_contours = filtered_approx_contours

#             # Remove small contours (area < 10% of average area)
#             if len(approx_contours) > 1:
#                 areas = [cv2.contourArea(contour) for contour in approx_contours]
#                 avg_area = np.mean(areas)

#                 filtered_approx_contours = [
#                     contour for contour, area in zip(approx_contours, areas) if area > avg_area * 0.1
#                 ]
#                 approx_contours = filtered_approx_contours

#         contours = approx_contours

#     return contours


def calculate_iou(refer, query):
    intersection = np.logical_and(refer, query)
    union = np.logical_or(refer, query)

    iou = np.sum(intersection) / np.sum(union) if np.sum(union) else 0

    return iou


def calculate_iou_by_mask(mask1: np.ndarray, mask2: np.ndarray, eps: float = 1e-7) -> float:
    """标准的iou比较"""
    # Mask shape:[height, width]
    intersection = np.sum(np.logical_and(mask1, mask2))
    union = np.sum(np.logical_or(mask1, mask2))
    iou = intersection / (union + eps)
    return iou


def calculate_ios_by_mask(mask1: np.ndarray[bool], mask2: np.ndarray[bool], eps: float = 1e-7) -> float:
    """交集/自身面积
    计算自身被召回的比例"""
    # Mask shape:[height, width]
    intersection = np.sum(np.logical_and(mask1, mask2))
    union = np.sum(mask2)
    ios = intersection / (union + eps)
    return ios


def calculate_iou_by_masks(masks1: np.ndarray, masks2: np.ndarray, eps: float = 1e-7) -> np.ndarray:
    # Mask shape:[NorM, height, width]
    if (masks1.size and masks2.size) == 0:
        return 0

    masks1 = masks1[:, None, :, :]
    masks2 = masks2[None, :, :, :]

    intersection = np.sum(np.logical_and(masks1, masks2), axis=(2, 3))
    union = np.sum(np.logical_or(masks1, masks2), axis=(2, 3))
    iou = intersection / (union + eps)

    return iou


def calculate_iou_by_box(box1: np.ndarray, box2: np.ndarray, eps: float = 1e-7) -> float:
    # Box format:[xmin,ymin,xmax,ymax]
    box1_xmin, box1_ymin, box1_xmax, box1_ymax = box1
    box2_xmin, box2_ymin, box2_xmax, box2_ymax = box2

    # fmt: off
    intersection = (
        max(0, min(box1_xmax, box2_xmax) - max(box1_xmin, box2_xmin))
        * max(0, min(box1_ymax, box2_ymax) - max(box1_ymin, box2_ymin))
    )
    # fmt: on

    union = union = (box1_xmax - box1_xmin) * (box1_ymax - box1_ymin) + (box2_xmax - box2_xmin) * (box2_ymax - box2_ymin) - intersection

    iou = intersection / (union + eps)

    return iou


def calculate_iou_by_boxes(
    boxes1: np.ndarray,  # [n, 4]
    boxes2: np.ndarray,  # [m, 4]
    eps: float = 1e-7,
) -> np.ndarray:  # [n, m]
    # boxes1 = boxes1[:, None, :]  # [n, 1, 4]
    # boxes2 = boxes2[None, :, :]  # [1, m, 4]
    if (boxes1.size and boxes2.size) == 0:
        return 0

    # Box format: [xmin, ymin, xmax, ymax]
    boxes1_xmin, boxes1_ymin, boxes1_xmax, boxes1_ymax = np.split(boxes1, 4, -1)
    boxes2_xmin, boxes2_ymin, boxes2_xmax, boxes2_ymax = [array.T for array in np.split(boxes2, 4, -1)]

    # fmt: off
    intersection = (
        (np.minimum(boxes1_xmax, boxes2_xmax) - np.maximum(boxes1_xmin, boxes2_xmin)).clip(0)
        * (np.minimum(boxes1_ymax, boxes2_ymax) - np.maximum(boxes1_ymin, boxes2_ymin)).clip(0)
    )
    # fmt: on

    union = (boxes1_xmax - boxes1_xmin) * (boxes1_ymax - boxes1_ymin) + (boxes2_xmax - boxes2_xmin) * (boxes2_ymax - boxes2_ymin) - intersection

    iou = intersection / (union + eps)

    return iou
