#!/usr/bin/env python3
"""
Simple image downloader that converts images to PNG or keeps JPG format.
"""

import os
import requests
from PIL import Image
from urllib.parse import urlparse
import tempfile
import sys


def download_image(url, output_dir="./images"):
    """Download an image and convert it to PNG or keep as JPG."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Download the image
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Create a temporary file to store the downloaded image
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)
            temp_path = temp_file.name
        
        # Open the image with PIL
        with Image.open(temp_path) as img:
            # Convert RGBA to RGB if necessary (for PNG with transparency)
            if img.mode in ('RGBA', 'LA'):
                # Create a white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Determine output format and filename
            parsed_url = urlparse(url)
            original_filename = os.path.basename(parsed_url.path)
            
            # Check if original is JPG/JPEG
            original_ext = os.path.splitext(original_filename)[1].lower()
            is_jpg = original_ext in ['.jpg', '.jpeg']
            
            # Generate filename
            if original_filename and '.' in original_filename:
                name_without_ext = os.path.splitext(original_filename)[0]
            else:
                name_without_ext = "image"
            
            if is_jpg:
                output_filename = f"{name_without_ext}.jpg"
                output_path = os.path.join(output_dir, output_filename)
                img.save(output_path, "JPEG", quality=95)
                print(f"Saved as JPG: {output_path}")
            else:
                output_filename = f"{name_without_ext}.png"
                output_path = os.path.join(output_dir, output_filename)
                img.save(output_path, "PNG")
                print(f"Saved as PNG: {output_path}")
        
        # Clean up temporary file
        os.unlink(temp_path)
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
    except Exception as e:
        print(f"Error processing image: {e}")


def main():
    """Main loop for downloading images."""
    print("Image Downloader")
    print("Enter image URLs (or 'exit' to quit)")
    print()
    
    while True:
        try:
            url = input("Enter image URL: ").strip()
            
            if url.lower() == 'exit':
                print("Goodbye!")
                break
            
            if not url:
                continue
            
            if not url.startswith(('http://', 'https://')):
                print("Please enter a valid URL starting with http:// or https://")
                continue
            
            download_image(url)
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
