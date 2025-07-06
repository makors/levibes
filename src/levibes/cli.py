"""
Command-line interface for LeVibes
"""

from art import text2art
import gratient
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator
from prompt_toolkit.shortcuts import confirm
from .config import DEFAULT_NUM_IMAGES, DEFAULT_IMAGES_DIR, DEFAULT_OUTPUT_DIR


def display_welcome():
    """Display welcome message with ASCII art."""
    ascii_art = text2art("LeVibes", font="bolger")
    gradient_art = gratient.blue(ascii_art)
    print(gradient_art)
    print(gratient.blue("\t   " + "Time to spread some positivity! 💫"))


def get_user_inputs():
    """
    Get user inputs for image generation.

    Returns:
        Tuple of (num_images, path_to_images, output_dir)
    """
    num_images = int(
        prompt(
            "How many images would you like to generate? ",
            default=str(DEFAULT_NUM_IMAGES),
        )
    )

    # Create validator for image directory
    def is_valid_directory(path):
        import os

        return (
            os.path.exists(path)
            and os.path.isdir(path)
            and any(
                file.endswith((".jpg", ".jpeg", ".png")) for file in os.listdir(path)
            )
            and len(
                [f for f in os.listdir(path) if f.endswith((".jpg", ".jpeg", ".png"))]
            )
            >= num_images
        )

    path_validator = Validator.from_callable(
        is_valid_directory,
        error_message="Not a valid image directory (either doesn't exist or doesn't contain enough images).",
        move_cursor_to_end=True,
    )

    path_to_images = prompt(
        "What images do you want to caption? ",
        default=DEFAULT_IMAGES_DIR,
        validator=path_validator,
        validate_while_typing=False,
    )

    output_dir = prompt(
        "Where do you want to save the images? ",
        default=DEFAULT_OUTPUT_DIR,
    )

    return num_images, path_to_images, output_dir


def confirm_captions(captions):
    """
    Display captions to user and get confirmation.

    Args:
        captions: List of generated captions

    Returns:
        True if user confirms, False otherwise
    """
    print("\nBelow are your AI-generated caption(s):")

    if type(captions) == str:
        print(f"- {captions}")
    else:
        for caption in captions:
            print(f"- {caption}")
    print()

    return confirm("Do these caption(s) work for you?")


def ask_retry():
    """Ask user if they want to retry caption generation."""
    return confirm("Would you like to try again with new captions?")


def ask_tiktok_caption():
    """Ask user if they want to generate a tiktok caption."""
    return confirm("Would you like to generate a tiktok caption?")


def display_success(output_dir):
    """Display success message with output directory."""
    print("\n" + gratient.green(f"Images saved to {output_dir}"))
