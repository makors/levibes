from PIL import Image, ImageDraw, ImageFont
from yaspin import yaspin
import os
import random
from .config import (
    DEFAULT_IMAGE_SIZE,
    FONT_NAMES,
    PADDING_SCALING_FACTOR,
    LINE_SPACING_RATIO,
    MAX_TEXT_WIDTH_RATIO,
    FONT_SIZE_RATIO,
    SUPPORTED_IMAGE_FORMATS,
)


@yaspin(text="Generating images...", color="cyan")
def generate_images(captions, path_to_images, output_dir):
    image_paths = [
        os.path.join(path_to_images, file)
        for file in os.listdir(path_to_images)
        if file.endswith(SUPPORTED_IMAGE_FORMATS)
    ]
    random.shuffle(image_paths)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_paths = []

    for i, image_path in enumerate(image_paths):
        if i >= len(captions):
            break

        caption_text = captions[i]

        with Image.open(image_path) as img:
            padding_scaling_factor = PADDING_SCALING_FACTOR
            line_spacing_ratio = LINE_SPACING_RATIO

            width, height = img.size
            if width != height:
                size = min(width, height)
                left = (width - size) / 2
                top = (height - size) / 2
                right = (width + size) / 2
                bottom = (height + size) / 2
                img = img.crop((left, top, right, bottom))

            img = img.resize(DEFAULT_IMAGE_SIZE)

            font_size = int(img.width / FONT_SIZE_RATIO)
            font = None
            wrapped_text = None

            font_names = FONT_NAMES

            while font_size > 0:
                for name in font_names:
                    try:
                        font = ImageFont.truetype(name, font_size)
                        if "VariableFont" in name:
                            font.set_variation_by_name("Regular")
                        break
                    except IOError:
                        continue
                if not font:
                    font = ImageFont.load_default()

                draw = ImageDraw.Draw(img)
                max_text_width = int(img.width * MAX_TEXT_WIDTH_RATIO)

                lines = []
                words = caption_text.split(" ")
                current_line = ""
                word_too_long = False
                for word in words:
                    word_bbox = draw.textbbox((0, 0), word, font=font)
                    if (word_bbox[2] - word_bbox[0]) > max_text_width:
                        word_too_long = True
                        break

                    test_line = f"{current_line} {word}" if current_line else word
                    line_bbox = draw.textbbox((0, 0), test_line, font=font)
                    if line_bbox[2] - line_bbox[0] <= max_text_width:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word

                if word_too_long:
                    font_size -= 2
                    continue

                if current_line:
                    lines.append(current_line)

                wrapped_text = lines
                break

            if not wrapped_text:
                print(
                    f"Warning: Could not fit caption on image {os.path.basename(image_path)}. Caption may be too long."
                )
                # fallback to a tiny font size if it couldn't fit
                for name in font_names:
                    try:
                        font = ImageFont.truetype(name, 10)
                        if "VariableFont" in name:
                            font.set_variation_by_name("Regular")
                        break
                    except IOError:
                        continue
                if not font:
                    font = ImageFont.load_default()
                wrapped_text = [caption_text]

            draw = ImageDraw.Draw(img)
            # bbox of a string with ascenders and descenders to determine line height
            line_bbox = draw.textbbox((0, 0), "gh", font=font)
            line_height = line_bbox[3] - line_bbox[1]
            line_spacing = int(line_height * line_spacing_ratio)

            text_block_height = (len(wrapped_text) * line_height) + (
                max(0, len(wrapped_text) - 1) * line_spacing
            )

            padding = int(line_height * padding_scaling_factor)

            bar_height = text_block_height + (1.65 * padding)

            new_img = Image.new(
                "RGB", (img.width, img.height + int(bar_height)), "white"
            )
            new_img.paste(img, (0, int(bar_height)))

            draw = ImageDraw.Draw(new_img)

            text_x = int(img.width * 0.05)
            current_y = int(((bar_height - text_block_height) / 2))

            for line in wrapped_text:
                draw.text((text_x, current_y), line, font=font, fill="black")
                current_y += line_height + line_spacing

            filename = os.path.basename(image_path)
            output_path = os.path.join(output_dir, f"captioned_{filename}")
            new_img.save(output_path)
            output_paths.append(output_path)

    return output_paths
