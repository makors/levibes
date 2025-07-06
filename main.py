"""
LeVibes - Motivational Image Caption Generator

Entry point for the application.
"""

import os
import sys
from dotenv import load_dotenv
import gratient
from src.levibes.cli import (
    display_welcome,
    get_user_inputs,
    ask_caption_source,
    get_caption_file_path,
    confirm_captions,
    ask_retry,
    display_success,
    ask_tiktok_caption,
)
from src.levibes.caption_generation import (
    generate_captions,
    generate_tiktok_captions,
    read_captions_from_file,
)
from src.levibes.generate_images import generate_images
from src.levibes.utils.file_helpers import (
    create_unique_output_dir,
    ensure_directory_exists,
)
from src.levibes.config import load_cli_args


def validate_cli_args(args):
    """
    Validate CLI arguments and show errors if invalid.
    
    Args:
        args: Parsed CLI arguments
        
    Returns:
        True if valid, False otherwise
    """
    # If caption source is file, caption file must be provided
    if args.caption_source == "file" and not args.caption_file:
        print("Error: --caption-file is required when using --caption-source file")
        return False
        
    # Validate caption file exists and has enough captions
    if args.caption_file:
        import os
        if not os.path.exists(args.caption_file):
            print(f"Error: Caption file '{args.caption_file}' does not exist")
            return False
        
        if not os.path.isfile(args.caption_file):
            print(f"Error: '{args.caption_file}' is not a file")
            return False
            
        # Check if file has enough captions
        if args.num_images:
            try:
                with open(args.caption_file, "r", encoding="utf-8") as f:
                    captions = [line.strip() for line in f if line.strip()]
                    if len(captions) < args.num_images:
                        print(f"Error: Caption file only contains {len(captions)} captions, but {args.num_images} images requested")
                        return False
            except Exception as e:
                print(f"Error reading caption file: {e}")
                return False
    
    # Validate images directory
    if args.images_dir:
        import os
        if not os.path.exists(args.images_dir):
            print(f"Error: Images directory '{args.images_dir}' does not exist")
            return False
        
        if not os.path.isdir(args.images_dir):
            print(f"Error: '{args.images_dir}' is not a directory")
            return False
            
        # Check if directory has enough images
        if args.num_images:
            image_files = [f for f in os.listdir(args.images_dir) if f.endswith((".jpg", ".jpeg", ".png"))]
            if len(image_files) < args.num_images:
                print(f"Error: Images directory only contains {len(image_files)} images, but {args.num_images} images requested")
                return False
    
    # Validate num_images is positive
    if args.num_images is not None and args.num_images <= 0:
        print("Error: Number of images must be positive")
        return False
        
    return True


def main():
    """Main application entry point."""
    load_dotenv()
    
    # Load CLI arguments
    args = load_cli_args()
    
    # Validate CLI arguments
    if not validate_cli_args(args):
        sys.exit(1)

    display_welcome()

    # Ask user to choose caption source (or use CLI arg)
    caption_source = ask_caption_source(args.caption_source)

    # Only check for OpenAI API key if user chooses AI
    if caption_source == "ai" and not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set in your .env file")

    # Get user inputs (or use CLI args)
    num_images, path_to_images, output_dir = get_user_inputs(
        args.num_images, args.images_dir, args.output_dir
    )

    captions = []

    if caption_source == "ai":
        # AI-generated captions with confirmation loop
        while True:
            ai_captions = generate_captions(num_images, args.model, args.language)

            if confirm_captions(ai_captions, args.no_confirm):
                captions.extend(ai_captions)
                break
            else:
                if not ask_retry(args.no_confirm):
                    print("No captions approved. Exiting.")
                    return
    else:
        while True:
            caption_file_path = get_caption_file_path(num_images, args.caption_file)
            try:
                captions = read_captions_from_file(caption_file_path, num_images)
                if confirm_captions(captions, args.no_confirm):
                    break
                else:
                    if not ask_retry(args.no_confirm):
                        print("No captions approved. Exiting.")
                        return
            except (FileNotFoundError, ValueError) as e:
                print(f"Error reading caption file: {e}")
                if not ask_retry(args.no_confirm):
                    print("Exiting due to file error.")
                    return

    if not captions:
        print("No captions were generated. Please try again.")
        return

    ensure_directory_exists(output_dir)
    unique_output_dir = create_unique_output_dir(output_dir)

    generate_images(captions, path_to_images, unique_output_dir)

    display_success(unique_output_dir)

    # TikTok caption generation (only available with AI)
    if caption_source == "ai" and ask_tiktok_caption(args.no_tiktok):
        tiktok_caption = ""

        while True:
            tiktok_caption = generate_tiktok_captions(1, args.model, args.language)
            if confirm_captions(tiktok_caption, args.no_confirm):
                break
            else:
                if not ask_retry(args.no_confirm):
                    print("No TikTok caption approved. Exiting.")
                    return

        print("\n")

    print(gratient.green("Thank you for using LeVibes!"))


if __name__ == "__main__":
    main()
