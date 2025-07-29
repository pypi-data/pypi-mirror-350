# Riffusion API

![Banner](https://storage.googleapis.com/corpusant-public/banner.jpg)

Code for API access to Riffusion's frontier models to make incredible music

This API is in a private beta and subject to change. Contact api@riffusion.com for inquiries and access.

## Usage
Set your API key:

```bash
export RIFFUSION_API_KEY="<your-api-key>"
```

Install the Python client:
```bash
pip install riff-api
```

Make some music:

```python
from riff_api import RiffAPIClient

client = RiffAPIClient()

response = client.prompt(
    "Explain the concept of time in French, piano chill",
    save_to="chill.m4a",
)
```

This will generate a full song with lyrics and music. Run multiple times for variations.

## Endpoints

### `/prompt`

This endpoint creates a song from a single natural language description the desired lyrical content and/or musical style. It's the simplest way to create.

The API will generate lyrics based on your topic, as well as pick specific sound prompts. If you don't describe a musical style or lyrics content, it will choose for you.

Get creative with your topics! Here are a few ideas:

 * "Rap fun facts about Alaskan history"
 * "Explain the concept of time in French"
 * "My nephew Remi is a superhero with laser eyes. Make him a theme song with a rock orchestra"

Currently the API only supports returning base64 encoded bytes of an m4a file.

### `/compose`

This endpoint provides a more powerful capability for music lovers to craft the exact sound they want. You can specify custom lyrics and multiple sound prompts with individually controllable strengths for deeper control.

The returned output contains detailed timestamps for each word in the lyrics.

## Repo

* `riff_api/types.py` - API schema
* `riff_api/examples/prompt` - Examples for creating a song via the client, requests, and curl
* `riff_api/examples/compose` - Examples for custom creation
