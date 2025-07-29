from __future__ import annotations

import typing as T

from pydantic import BaseModel


class PromptRequest(BaseModel):
    """
    Create a song from a single text description of the sound and lyrics
    """

    prompt: str
    """ Description of the sound and lyrics """

    instrumental: bool = False
    """ Whether to generate an instrumental with no lyrics """

    audio_format: T.Literal["m4a"] = "m4a"
    """ Audio format to return """

    moderate_inputs: bool = True
    """ If True, runs moderation checks on the prompts and lyrics """


class PromptResponse(BaseModel):
    """
    Output of the /prompt endpoint
    """

    id: str
    """ UUID of the generated song """

    lyrics: str | None = None
    """ Lyrics of the song, if not instrumental """

    timestamped_lyrics: list[TimestampedWord] | None = None
    """ Timestamps for each word in the lyrics """

    sound_prompt: str
    """ Sound prompt used to create the song """

    audio_format: T.Literal["m4a"]
    """ Audio format of the returned song """

    audio_b64: str
    """ Base64 encoded bytes of the requested audio format """
    
    title: str
    """ Title of the song. """


class ComposeRequest(BaseModel):
    """
    Create a song using lyrics a list of sound prompts
    """

    sound_prompts: list[SoundPrompt]
    """ List of sound prompts to use """

    lyrics: str | None = None
    """ Lyrics to use for the song, or None for an instrumental """

    lyrics_strength: float = 0.5
    """ Strength of the vocals in the song [0, 1] """

    audio_format: T.Literal["m4a"] = "m4a"
    """ Audio format to return """

    seed: int | None = None
    """ Random seed for reproducible results """

    moderate_inputs: bool = True
    """ If True, runs moderation checks on the prompts and lyrics """

    weirdness: float = 0.5
    """ Weirdness of the generated audio, [0, 1] """


class ComposeResponse(BaseModel):
    """
    Output of the /compose endpoint
    """

    id: str
    """ UUID of the generated song """

    lyrics: str | None = None
    """ Lyrics of the song, if present """

    timestamped_lyrics: list[TimestampedWord] | None = None
    """ Timestamps for each word in the lyrics """

    sound_prompts: list[SoundPrompt]
    """ List of sound prompts used to create the song """

    audio_b64: str
    """ Base64 encoded bytes of the requested audio format """

    audio_format: T.Literal["m4a"]
    """ Format of the returned audio """

    title: str
    """ Title of the song. """


class SoundPrompt(BaseModel):
    """
    Description of a sound prompt with a strength [-1.0, 1.0]
    """

    text: str
    """ Description of the sound prompt """

    strength: float = 0.5
    """ Strength of the sound prompt [0, 1] """


class TimestampedWord(BaseModel):
    """
    A timestamped word in the lyrics
    """

    text: str
    """ Word in the lyrics """

    start: float
    """ Start time of the word in seconds """
