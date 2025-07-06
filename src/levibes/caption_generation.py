from yaspin import yaspin
from openai import OpenAI
import os
from pydantic import BaseModel
from .config import OPENAI_MODEL, OPENAI_TEMPERATURE


class Captions(BaseModel):
    captions: list[str]


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@yaspin(text=f"Generating captions with {OPENAI_MODEL}...", color="cyan")
def generate_captions(num_images):
    openai_response = client.responses.parse(
        model=OPENAI_MODEL,
        temperature=OPENAI_TEMPERATURE,
        input=[{"role": "user", "content": generate_prompt(num_images)}],
        text_format=Captions,
    )

    if openai_response.output_parsed is None:
        raise ValueError("No captions generated")

    return openai_response.output_parsed.captions


@yaspin(text=f"Generating TikTok captions with {OPENAI_MODEL}...", color="cyan")
def generate_tiktok_captions(num_captions=1):
    openai_response = client.responses.parse(
        model=OPENAI_MODEL,
        temperature=OPENAI_TEMPERATURE,
        input=[{"role": "user", "content": generate_tiktok_prompt(num_captions)}],
    )

    if openai_response.output_text is None or openai_response.output_text == "":
        raise ValueError("No TikTok captions generated")

    return openai_response.output_text


def generate_prompt(num_images):
    return f"""Generate {num_images} motivational phrases in all lowercase, under 13 words each. Match this style exactly:

if you went back in time to erase all of your mistakes you would erase yourself
the strongest steel is forged in the hottest fire
all our dreams can come true if we have the courage to pursue them
shoot for the moon. even if you miss, you'll land among the stars

Requirements: deep, philosophical, resonate with young people, minimal use of "you/your", no em dashes or ellipses."""


def generate_tiktok_prompt(num_captions):
    return f"""Generate {num_captions} TikTok caption(s) with an inspirational quote and hashtags. Format the response as a inspirational quote in all lowercase (similar to examples below) directly followed by up to 5 hashtags relating to inspiration and LeBron James. DO NOT RELATE THE QUOTES TO LEBRON JAMES.

Example inspirational quotes (all lowercase):
- if you went back in time to erase all of your mistakes you would erase yourself
- the strongest steel is forged in the hottest fire
- all our dreams can come true if we have the courage to pursue them
- shoot for the moon. even if you miss, you'll land among the stars

Keep the quote 12 words or less and make it resonate with a young audience interested in motivation and personal growth."""
