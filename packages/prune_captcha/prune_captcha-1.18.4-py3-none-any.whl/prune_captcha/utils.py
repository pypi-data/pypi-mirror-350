import os
import random

from django.conf import settings
from django.http import HttpRequest


def create_and_get_captcha(
    request, *, width=350, height=200, piece_width=80, piece_height=50, precision=2
) -> dict:
    pos_x_solution = random.randint(0, width - piece_width)
    pos_y_solution = random.randint(0, height - piece_height)
    piece_pos_x = random.randint(0, width - piece_width)
    piece_pos_y = random.randint(0, height - piece_height)
    _, _, puzzle_images_path = settings.PUZZLE_IMAGE_STATIC_PATH.rpartition("static/")
    puzzle_images = [
        f
        for f in os.listdir(settings.PUZZLE_IMAGE_STATIC_PATH)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))
    ]
    selected_image = random.choice(puzzle_images)
    request.session["puzzle"] = {
        "pos_x_solution": pos_x_solution,
        "pos_y_solution": pos_y_solution,
        "precision": precision,
    }
    return {
        "width": width,
        "height": height,
        "piece_width": piece_width,
        "piece_height": piece_height,
        "pos_x_solution": pos_x_solution,
        "pos_y_solution": pos_y_solution,
        "piece_pos_x": piece_pos_x,
        "piece_pos_y": piece_pos_y,
        "image": f"{puzzle_images_path}{selected_image}",
    }


def verify_captcha(request: HttpRequest) -> bool:
    pos_x_answer = int(request.POST.get("pos_x_answer"))
    pos_y_answer = int(request.POST.get("pos_y_answer"))
    if pos_x_answer is None or pos_y_answer is None:
        return False
    puzzle = request.session.get("puzzle")
    if (
        abs(puzzle["pos_x_solution"] - pos_x_answer) <= puzzle["precision"]
        and abs(puzzle["pos_y_solution"] - pos_y_answer) <= puzzle["precision"]
    ):
        return True
    else:
        return False
