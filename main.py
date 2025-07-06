"""
LeVibes - Motivational Image Caption Generator

Entry point for the application.
"""

import os
from dotenv import load_dotenv
import gratient
from src.levibes.cli import (
    display_welcome,
    get_user_inputs,
    confirm_captions,
    ask_retry,
    display_success,
    ask_tiktok_caption,
)
from src.levibes.caption_generation import generate_captions, generate_tiktok_captions
from src.levibes.generate_images import generate_images
from src.levibes.utils.file_helpers import (
    create_unique_output_dir,
    ensure_directory_exists,
)


def main():
    """Main application entry point."""
    load_dotenv(".env")

    display_welcome()

    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set in your .env file")

    num_images, path_to_images, output_dir = get_user_inputs()

    captions = []
    while True:
        ai_captions = generate_captions(num_images)

        if confirm_captions(ai_captions):
            captions.extend(ai_captions)
            break
        else:
            if not ask_retry():
                print("No captions approved. Exiting.")
                return

    if not captions:
        print("No captions were generated. Please try again.")
        return

    ensure_directory_exists(output_dir)
    unique_output_dir = create_unique_output_dir(output_dir)

    generate_images(captions, path_to_images, unique_output_dir)

    display_success(unique_output_dir)

    # now we allow the user to generate a tiktok caption

    if not ask_tiktok_caption():
        return

    tiktok_caption = ""

    while True:
        tiktok_caption = generate_tiktok_captions(num_images)
        if confirm_captions(tiktok_caption):
            break
        else:
            if not ask_retry():
                print("No TikTok caption approved. Exiting.")
                return

    print("\n")

    print(gratient.green("Thank you for using LeVibes!"))


if __name__ == "__main__":
    main()
