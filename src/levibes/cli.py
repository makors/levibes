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


def ask_caption_source(caption_source=None):
    """
    Ask user to choose between AI-generated captions and text file captions.

    Args:
        caption_source (str, optional): Pre-specified caption source ('ai' or 'file')

    Returns:
        str: 'ai' for AI-generated captions, 'file' for text file captions
    """
    if caption_source:
        print(f"Using caption source: {caption_source}")
        return caption_source
    
    print("\nHow would you like to generate your captions?")
    print("1. AI-generated captions (requires OpenAI API key)")
    print("2. Read captions from a text file")

    choice = prompt(
        "Enter your choice (1 or 2): ",
        validator=Validator.from_callable(
            lambda x: x in ["1", "2"],
            error_message="Please enter 1 or 2",
            move_cursor_to_end=True,
        ),
    )

    return "ai" if choice == "1" else "file"


def get_caption_file_path(num_images, caption_file=None):
    """
    Get the path to the caption file from the user.

    Args:
        num_images (int): Number of images to generate (for validation)
        caption_file (str, optional): Pre-specified caption file path

    Returns:
        str: Path to the caption file
    """
    if caption_file:
        print(f"Using caption file: {caption_file}")
        return caption_file

    def is_valid_caption_file(file_path):
        import os

        if not os.path.exists(file_path):
            return False
        if not os.path.isfile(file_path):
            return False
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                captions = [line.strip() for line in f if line.strip()]
                return len(captions) >= num_images
        except:
            return False

    file_validator = Validator.from_callable(
        is_valid_caption_file,
        error_message=f"File doesn't exist or doesn't contain at least {num_images} captions (one per line)",
        move_cursor_to_end=True,
    )

    file_path = prompt(
        "Enter the path to your caption file: ",
        validator=file_validator,
        validate_while_typing=False,
    )

    return file_path


def get_user_inputs(num_images=None, path_to_images=None, output_dir=None):
    """
    Get user inputs for image generation.

    Args:
        num_images (int, optional): Pre-specified number of images
        path_to_images (str, optional): Pre-specified path to images
        output_dir (str, optional): Pre-specified output directory

    Returns:
        Tuple of (num_images, path_to_images, output_dir)
    """
    # Get number of images
    if num_images is None:
        num_images = int(
            prompt(
                "How many images would you like to generate? ",
                default=str(DEFAULT_NUM_IMAGES),
            )
        )
    else:
        print(f"Number of images: {num_images}")

    # Get path to images
    if path_to_images is None:
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
    else:
        print(f"Images directory: {path_to_images}")

    # Get output directory
    if output_dir is None:
        output_dir = prompt(
            "Where do you want to save the images? ",
            default=DEFAULT_OUTPUT_DIR,
        )
    else:
        print(f"Output directory: {output_dir}")

    return num_images, path_to_images, output_dir


def confirm_captions(captions, no_confirm=False):
    """
    Display captions to user and get confirmation.

    Args:
        captions: List of generated captions
        no_confirm (bool): Skip confirmation if True

    Returns:
        True if user confirms or no_confirm is True, False otherwise
    """
    print("\nBelow are your caption(s):")

    if type(captions) == str:
        print(f"- {captions}")
    else:
        for caption in captions:
            print(f"- {caption}")
    print()

    if no_confirm:
        print("Auto-confirming captions (--no-confirm flag used)")
        return True

    return confirm("Do these caption(s) work for you?")


def ask_retry(no_confirm=False):
    """
    Ask user if they want to retry caption generation.
    
    Args:
        no_confirm (bool): Skip confirmation if True
    """
    if no_confirm:
        return False
    return confirm("Would you like to try again with new captions?")


def ask_tiktok_caption(no_tiktok=False):
    """
    Ask user if they want to generate a tiktok caption.
    
    Args:
        no_tiktok (bool): Skip TikTok caption generation if True
    """
    if no_tiktok:
        return False
    return confirm("Would you like to generate a tiktok caption?")


def display_success(output_dir):
    """Display success message with output directory."""
    print("\n" + gratient.green(f"Images saved to {output_dir}"))
