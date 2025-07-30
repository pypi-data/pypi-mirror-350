# demo/wiki_to_md.py
'''
Tool demo for converting Wikipedia articles to Markdown format using Toolio's tool-calling capabilities.

Loosely based on https://github.com/erictherobot/wikipedia-markdown-generator

Example usage:
```python
python demo/wiki_to_md.py "Artificial Intelligence" --with-images
```
'''
import os
import re
import asyncio
import urllib.parse
from pathlib import Path

import httpx
import wikipedia  # pip install wikipedia
from toolio.tool import tool, param
from toolio.llm_helper import local_model_runner

# Configuration
OUTPUT_DIR = Path('md_output')
OUTPUT_DIR.mkdir(exist_ok=True)

IMAGE_DIR = OUTPUT_DIR / 'images' 
IMAGE_DIR.mkdir(exist_ok=True)

@tool('wiki_to_md',
      desc='Convert a Wikipedia article to Markdown format',
      params=[
          param('topic', str, 'Wikipedia topic/article name', True),
          param('with_images', bool, 'Whether to include and download images', False)
      ])
async def wiki_to_md(topic=None, with_images=False):
    '''
    Convert a Wikipedia article to Markdown format with optional image downloading
    '''
    try:
        # Get Wikipedia page
        page = wikipedia.page(topic)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Disambiguation needed. Options: {', '.join(e.options[:5])}"
    except wikipedia.exceptions.PageError:
        return f"Page not found: {topic}"

    # Start with title
    markdown_text = f"# {topic}\n\n"

    # Convert section headers
    content = re.sub(r"=== ([^=]+) ===", r"### \1", page.content)
    content = re.sub(r"== ([^=]+) ==", r"## \1", content)

    # Split and process sections
    sections = re.split(r"\n(## .*)\n", content)
    for i in range(0, len(sections), 2):
        if i + 1 < len(sections) and any(line.strip() for line in sections[i + 1].split("\n")):
            markdown_text += f"{sections[i]}\n{sections[i+1]}\n\n"

    # Handle images if requested
    if with_images:
        async with httpx.AsyncClient() as client:
            for image_url in page.images:
                image_filename = urllib.parse.unquote(os.path.basename(image_url))
                image_path = IMAGE_DIR / image_filename

                # Download image
                resp = await client.get(image_url)
                if resp.status_code == 200:
                    image_path.write_bytes(resp.content)
                    markdown_text += f"\n![{image_filename}](./images/{image_filename})\n"

    # Write output file
    out_file = OUTPUT_DIR / f"{topic.replace(' ', '_')}.md"
    out_file.write_text(markdown_text)

    return f"Generated Markdown file: {out_file}\nContent preview:\n\n{markdown_text[:500]}..."

# MLX_MODEL_PATH = 'mlx-community/Mistral-Nemo-Instruct-2407-4bit'
MLX_MODEL_PATH = 'mlx-community/Llama-3.2-3B-Instruct-4bit'

toolio_mm = local_model_runner(MLX_MODEL_PATH, tool_reg=[wiki_to_md])

PROMPT = 'Convert Wikipedia\'s article on "Mars" to Markdown format. Put the result in the md_output directory.'

async def async_main(tmm):
    msgs = [{'role': 'user', 'content': PROMPT}]
    rt = await tmm.complete_with_tools(msgs)
    print(rt.first_choice_text)

if __name__ == '__main__':
    asyncio.run(async_main(toolio_mm))
