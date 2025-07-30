from pathlib import Path
import shutil
import cv2
import numpy as np
from .Std_Json import Std_Json


def set_image_root_dir_for_Std_Json(
    std_json: Std_Json, image_root_dir: str | Path, image_key="image", is_remove=False
):
    image_root_dir = (
        Path(image_root_dir) if isinstance(image_root_dir, str) else image_root_dir
    )
    for item in std_json:
        if is_remove:
            item[image_key] = str(Path(item[image_key]).relative_to(image_root_dir))
        else:
            item[image_key] = str(image_root_dir / item[image_key])
    return std_json


def Std_Json_image_to_dir(std_json: Std_Json, save_dir, image_key="image"):
    for item in std_json:
        image = Path(item[image_key])
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        if not image.exists():
            print(image, "not exists!")
            continue
        shutil.copy2(image, save_dir)


# plot functions for Std_Json
def plot_polygon(
    image: np.ndarray,
    polygon: list | np.ndarray,
    color: tuple = (0, 255, 0),
    thickness: int = 2,
    render_index_points=True,
):
    polygon = np.array(polygon)
    assert polygon.ndim == 2, "polygon must be 2D array"
    assert polygon.shape[0] > 2, "polygon must have at least 3 points"
    assert polygon.shape[1] == 2, "polygon must have 2 columns"

    polygon = polygon.reshape((-1, 1, 2)).astype(np.int32)
    cv2.polylines(image, [polygon], True, color, thickness)
    if render_index_points:
        for i in range(len(polygon)):
            u, v = polygon[i][0][0], polygon[i][0][1]
            cv2.putText(
                image,
                f"{i}",
                (u, v),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (225, 0, 0),
                2,
            )
    return image


def plot_bbox(
    image: np.ndarray,
    bbox: list | np.ndarray,
    color: tuple = (0, 255, 0),
    thickness: int = 2,
    render_index_points=True,
):
    bbox = np.array(bbox)
    assert bbox.ndim == 1, "bbox must be 1D array"
    assert bbox.shape[0] == 4, "bbox must have 4 elements (x1,y1,x2,y2)"
    x1, y1, x2, y2 = bbox
    cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
    if render_index_points:
        cv2.putText(
            image,
            "0",
            (x1, y1),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (225, 0, 0),
            2,
        )
        cv2.putText(
            image,
            "1",
            (x2, y2),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (225, 0, 0),
            2,
        )
    return image


def plot_point(
    image: np.ndarray,
    point: tuple | list | np.ndarray,
    color: tuple = (0, 0, 255),
    thickness: int = 2,
):
    point = np.array(point)
    assert point.ndim == 1, "point must be 1D array"
    assert len(point) == 2, "point must have 2 elements (x,y)"
    x, y = point
    cv2.circle(image, (x, y), 5, color, thickness)
    return image


def plot_text(
    image: np.ndarray,
    text: str,
    point: tuple | list | np.ndarray,
    color: tuple = (255, 0, 0),
    thickness: int = 2,
):
    point = np.array(point)
    assert point.ndim == 1, "point must be 1D array"
    assert len(point) == 2, "point must have 2 elements (x,y)"
    x, y = point
    cv2.putText(
        image,
        text,
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        thickness,
    )
    return image


def plot_item(
    info_item: dict,
    image: str | Path,
    out_image: str | Path,
    plot_geo_names: list,
    coor_is_norm=False,
    **kwargs,
):
    if not Path(image).exists():
        print(image, "not exists!")
        return
    image = cv2.imread(image)
    h, w = image.shape[:2]
    for info_name in plot_geo_names:
        if info_name == "polygon":
            polygon = np.array(info_item[info_name])
            if coor_is_norm:
                polygon *= [w, h]
            image = plot_polygon(image, polygon, **kwargs)
        elif info_name == "bbox":
            bbox = np.array(info_item[info_name])
            if coor_is_norm:
                bbox *= [w, h, w, h]
            image = plot_bbox(image, bbox, **kwargs)
        elif info_name == "point":
            point = np.array(info_item[info_name])
            if coor_is_norm:
                point *= [w, h]
            image = plot_point(image, point, **kwargs)
        elif info_name == "text":
            image = plot_text(image, info_item[info_name], **kwargs)
        else:
            raise ValueError(f"info_name {info_name} not supported!")

    out_image = Path(out_image)
    out_image.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_image), image)


def plot_geo_for_Std_Json(
    std_json: Std_Json,
    out_dir: str | Path,
    plot_item_func=plot_item,
    image_key="image",
    plot_geo_name=["polygon", "bbox", "point", "text"],
    coor_is_norm=False,
    **kwargs
):
    """
    参数:
        std_json (Std_Json): 包含注释和图像路径的 Std_Json 对象。
        out_dir (str | Path): 保存输出图像的目录。
        plot_item_func (function, optional): 用于在图像上绘制几何的函数。默认为 plot_item。
        image_key (str, optional): Std_Json 项目中包含图像路径的键。默认为 "image"。
        plot_info_name (list, optional): 要绘制的几何类型列表。默认为 ["polygon", "bbox", "point", "text"]。
        coor_is_norm (bool, optional): 几何中的坐标是否归一化。默认为 False。
        **kwargs: 传递给 plot_item_func 的其他关键字参数。
    """
    for item in std_json:
        image_path = item[image_key]
        out_image = Path(out_dir) / Path(image_path).name
        plot_item_func(item, image_path, out_image, plot_geo_name,coor_is_norm,**kwargs)
