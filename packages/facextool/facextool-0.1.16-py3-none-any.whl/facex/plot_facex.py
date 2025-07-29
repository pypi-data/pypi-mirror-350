import json
import base64
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io
import matplotlib.cm as cm


def plot(face_prototype_dir, hat_glasses_prototype_dir, region_weights):
    # Load the JSON annotation from the file
    with open(face_prototype_dir, "r") as json_file:
        annotation = json.load(json_file)

    with open(hat_glasses_prototype_dir, "r") as json_file:
        annotation_hat = json.load(json_file)

    # Decode and load the image
    image_data = base64.b64decode(annotation["imageData"])
    image = Image.open(io.BytesIO(image_data))
    image_array = np.array(image)

    # Prepare the figure and axes
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    ax.imshow(np.zeros(image_array.shape))  # just black background
    ax.axis("off")

    region_pos = {
        "r_ear": 0, "l_ear": 1, "l_eye": 2, "r_eye": 3, "nose": 4,
        "hair": 5, "r_brow": 6, "l_brow": 7, "l_lip": 8, "u_lip": 9,
        "mouth": 10, "neck": 11, "cloth": 12, "neck_l": 13, "skin": 14,
        "background": 15, "l_ear_r": 16, "r_ear_r": 17, "hat": 1, "eye_g": 0,
    }

    region_mapping = {
        "skin": "skin", "nose": "nose", "l_eye": "l_eye", "r_eye": "r_eye",
        "l_brow": "l_brow", "r_brow": "r_brow", "l_ear": "l_ear", "r_ear": "r_ear",
        "mouth": "mouth", "u_lip": "u_lip", "l_lip": "l_lip", "hair": "hair",
        "ear_r": ["l_ear_r", "r_ear_r"], "neck": "neck", "neck_l": "neck_l",
        "cloth": "cloth", "background": "background",
        "eye_g": "eye_g"  # "hat" intentionally removed
    }

    # Ensure consistent order
    value = region_weights.pop("neck_l", None)
    if value is not None:
        region_weights["neck_l"] = value

    # Normalize region weights
    max_value = max(region_weights.values())
    min_value = min(region_weights.values())

    if max_value != min_value:
        region_weights = {
            key: (value - min_value) / (max_value - min_value)
            for key, value in region_weights.items()
        }

    cmap = cm.get_cmap("coolwarm")
    alpha = 1

    for region, weight in region_weights.items():
        polygon_names = region_mapping.get(region)

        if polygon_names == "hat":  # skip drawing hat
            continue

        color = cmap(weight)

        if isinstance(polygon_names, list):
            for polygon_name in polygon_names:
                polygon_points = annotation["shapes"][region_pos[polygon_name]]["points"]
                polygon_patch = patches.Polygon(
                    polygon_points, closed=True, fill=True,
                    facecolor=color, alpha=alpha, edgecolor="black", linewidth=0
                )
                ax.add_patch(polygon_patch)
        elif polygon_names == "eye_g":
            polygon_points = annotation_hat["shapes"][region_pos[polygon_names]]["points"]
            polygon_patch = patches.Polygon(
                polygon_points, closed=True, fill=True,
                facecolor=color, alpha=alpha, edgecolor="black", linewidth=0
            )
            ax.add_patch(polygon_patch)
        else:
            polygon_points = annotation["shapes"][region_pos[polygon_names]]["points"]
            polygon_patch = patches.Polygon(
                polygon_points, closed=True, fill=True,
                facecolor=color, alpha=alpha, edgecolor="black", linewidth=0
            )
            ax.add_patch(polygon_patch)

    # Add colorbar
    norm = plt.Normalize(vmin=0, vmax=1)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    cbar = plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Activation Level")
    cbar.ax.set_yticklabels(["Low", "", "", "", "High"])

    plt.tight_layout()
    plt.show()
    return fig
