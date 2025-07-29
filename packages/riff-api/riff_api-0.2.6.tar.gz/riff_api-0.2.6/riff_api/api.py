import base64
import os
import typing as T
import requests

from . import types


class RiffAPIClient:
    """
    Python client for the Riffusion API
    """

    def __init__(
        self,
        api_url: str | None = None,
        api_key: str | None = None,
    ):
        if api_url is None:
            api_url = os.environ.get(
                "RIFFUSION_API_URL",
                "https://wb.riffusion.com/api/v1",
            )

        if api_key is None:
            api_key = os.environ.get("RIFFUSION_API_KEY")
            if not api_key:
                raise ValueError(
                    "Pass an API key or set the RIFFUSION_API_KEY environment variable"
                )

        self.api_key: T.Final[str] = api_key
        self.api_url: T.Final[str] = api_url.rstrip("/")

    def prompt(
        self,
        prompt: str,
        instrumental: bool = False,
        audio_format: T.Literal["m4a"] = "m4a",
        save_to: str | None = None,
        moderate_inputs: bool = True,
    ) -> types.PromptResponse:
        """
        Create a song from a single text description of the sound and lyrics
        """

        request = types.PromptRequest(
            prompt=prompt,
            instrumental=instrumental,
            audio_format=audio_format,
            moderate_inputs=moderate_inputs,
        )

        response = requests.post(
            url=f"{self.api_url}/prompt",
            json=request.model_dump(),
            headers={"Api-Key": self.api_key},
        )

        response.raise_for_status()

        response_type = types.PromptResponse(**response.json())

        if save_to is not None:
            assert (
                request.audio_format == save_to.split(".")[-1]
            ), "The save extension must match the audio format"
            self.save_audio(response_type.audio_b64, save_to)

        return response_type

    def compose(
        self,
        sound_prompts: list[types.SoundPrompt],
        lyrics: str | None = None,
        lyrics_strength: float = 0.5,
        seed: int | None = None,
        audio_format: T.Literal["m4a"] = "m4a",
        moderate_inputs: bool = True,
        weirdness: float = 0.5,
        save_to: str | None = None,
    ) -> types.ComposeResponse:
        """
        Create a song using lyrics a list of sound prompts
        """
        request = types.ComposeRequest(
            sound_prompts=sound_prompts,
            lyrics=lyrics,
            lyrics_strength=lyrics_strength,
            audio_format=audio_format,
            seed=seed,
            moderate_inputs=moderate_inputs,
            weirdness=weirdness,
        )

        response = requests.post(
            url=f"{self.api_url}/compose",
            json=request.model_dump(),
            headers={"Api-Key": self.api_key},
        )

        response.raise_for_status()

        response_type = types.ComposeResponse(**response.json())

        if save_to is not None:
            assert (
                request.audio_format == save_to.split(".")[-1]
            ), "The save extension must match the audio format"
            self.save_audio(response_type.audio_b64, save_to)

        return response_type

    @staticmethod
    def save_audio(
        audio_b64: str,
        filename: str,
    ) -> None:
        """
        Save the audio from a Riffusion response to a file
        """
        audio_bytes = base64.b64decode(audio_b64)
        with open(filename, "wb") as f:
            f.write(audio_bytes)
