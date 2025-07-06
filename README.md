<p align="center">
<img src="https://github.com/user-attachments/assets/24d6a4c4-6313-4b89-99c2-3c15783d7eaa" alt="working demo" />
</p>

<h1 align="center"> LeVibes </h1>
<p align="center">Generate <bold>motivational</bold> social media posts with <bold>AI</bold> and <bold>LeBron James</bold>

<p align="center">
  <img alt="Stars" src="https://img.shields.io/github/stars/makors/levibes" />
  <img alt="Watchers" src="https://img.shields.io/github/watchers/makors/levibes" />
</p>

## Installation

### Prerequisites

- Python 3.12 or higher
- [uv](https://astral.sh/uv)
- OpenAI API key (if using AI features)

## Features

- **AI-powered caption generation** using OpenAI models
- **Multi-language support** for international audiences
- **File-based captions** for custom motivational quotes
- **Batch processing** for multiple images at once
- **Interactive and CLI modes** for different workflows
- **TikTok caption generation** with hashtags
- **Customizable output directories** and organized file structure

### Setup

1. Clone the repository
   ```bash
   git clone https://github.com/makors/levibes.git
   cd levibes
   ```

2. Install dependencies
   ```bash
   uv sync
   ```

3. Set up environment variables (only if using AI features)
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY="your_openai_api_key_here"
   ```

## Usage

### Interactive Mode
```bash
uv run main.py
```

### CLI Options
See all available options:
```bash
uv run main.py --help
```

### Examples

Generate 5 AI captions:
```bash
uv run main.py -s ai -n 5
```

Use captions from a text file:
```bash
uv run main.py -s file -c captions.txt -n 3
```

Generate captions in Spanish:
```bash
uv run main.py -s ai -l spanish -n 3
```

Full automated run:
```bash
uv run main.py -s ai -n 3 -i ./images -o ./output --no-confirm --no-tiktok
```

### Options

- `-s, --caption-source`: Choose 'ai' or 'file' for caption source
- `-n, --num-images`: Number of images to generate
- `-i, --images-dir`: Directory containing source images
- `-o, --output-dir`: Output directory for generated images
- `-c, --caption-file`: Text file with captions (for file mode)
- `-l, --language`: Language for AI captions (default: english)
- `-m, --model`: OpenAI model to use
- `--no-confirm`: Skip confirmation prompts
- `--no-tiktok`: Skip TikTok caption generation

## Contributing

Contributions are welcome! Here's how to contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name` (replace `feature-name`)
3. Make your changes
4. Add tests if applicable
5. Run the application to ensure it works
6. Submit a PR

### Development Setup

```bash
git clone your-fork-url
cd levibes
uv sync
```