from __future__ import annotations
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

import base64
import filetype
from binascii import Error as BinasciiError
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import (
    Annotated,
    Any,
    Literal,
    Optional,
    Self,
    Union,
)

from pydantic import (
    AnyUrl,
    BaseModel,
    Field,
    FilePath,
    field_validator,
    model_validator,
)
from ...utils.image_llamaindex import resolve_binary


class MessageRole(str, Enum):
    """Message role."""

    SYSTEM = "system"
    DEVELOPER = "developer"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"
    TOOL = "tool"
    CHATBOT = "chatbot"
    MODEL = "model"


class TextBlock(BaseModel):
    block_type: Literal["text"] = "text"
    text: str


class ImageBlock(BaseModel):
    block_type: Literal["image"] = "image"
    image: bytes | None = None
    path: FilePath | None = None
    url: AnyUrl | str | None = None
    image_mimetype: str | None = None
    detail: str | None = None

    @field_validator("url", mode="after")
    @classmethod
    def urlstr_to_anyurl(cls, url: str | AnyUrl | None) -> AnyUrl | None:
        """Store the url as Anyurl."""
        if isinstance(url, AnyUrl):
            return url
        if url is None:
            return None

        return AnyUrl(url=url)

    def validate_image(self) -> 'ImageBlock':
        """
        Validate and process image data.
        """
        if not self.image:
            if not self.image_mimetype:
                path = self.path or self.url
                if path:
                    suffix = Path(str(path)).suffix.replace(".", "") or None
                    mimetype = filetype.get_type(ext=suffix)
                    if mimetype and str(mimetype.mime).startswith("image/"):
                        self.image_mimetype = str(mimetype.mime)
            return self

        try:
            # Check if image is already base64 encoded
            base64.b64decode(self.image, validate=True)
        except BinasciiError:
            # Not base64 - encode it
            self.image = base64.b64encode(self.image)

        self._guess_mimetype(base64.b64decode(self.image))
        return self

    def _guess_mimetype(self, img_data: bytes) -> None:
        if not self.image_mimetype:
            guess = filetype.guess(img_data)
            self.image_mimetype = guess.mime if guess else None

    def resolve_image(self, as_base64: bool = False) -> BytesIO:
        """
        Resolve an image such that PIL can read it.

        Args:
            as_base64 (bool): whether the resolved image should be returned as base64-encoded bytes

        """
        return resolve_binary(
            raw_bytes=self.image,
            path=self.path,
            url=str(self.url) if self.url else None,
            as_base64=as_base64,
        )


class AudioBlock(BaseModel):
    block_type: Literal["audio"] = "audio"
    audio: bytes | None = None
    path: FilePath | None = None
    url: AnyUrl | str | None = None
    format: str | None = None

    @field_validator("url", mode="after")
    @classmethod
    def urlstr_to_anyurl(cls, url: str | AnyUrl) -> AnyUrl:
        """Store the url as Anyurl."""
        if isinstance(url, AnyUrl):
            return url
        return AnyUrl(url=url)

    def validate_audio(self) -> 'AudioBlock':
        """
        Validate and process audio data.
        """
        if not self.audio:
            return self

        try:
            # Check if audio is already base64 encoded
            base64.b64decode(self.audio, validate=True)
        except Exception:
            # Not base64 - encode it
            self.audio = base64.b64encode(self.audio)

        self._guess_format(base64.b64decode(self.audio))
        return self

    def _guess_format(self, audio_data: bytes) -> None:
        if not self.format:
            guess = filetype.guess(audio_data)
            self.format = guess.extension if guess else None

    def resolve_audio(self, as_base64: bool = False) -> BytesIO:
        """
        Resolve an audio such that PIL can read it.

        Args:
            as_base64 (bool): whether the resolved audio should be returned as base64-encoded bytes

        """
        return resolve_binary(
            raw_bytes=self.audio,
            path=self.path,
            url=str(self.url) if self.url else None,
            as_base64=as_base64,
        )


class DocumentBlock(BaseModel):
    block_type: Literal["document"] = "document"
    data: Optional[bytes] = None
    path: Optional[Union[FilePath | str]] = None
    url: Optional[str] = None
    title: Optional[str] = None
    document_mimetype: Optional[str] = None

    @model_validator(mode="after")
    def document_validation(self) -> Self:
        self.document_mimetype = self.document_mimetype or self._guess_mimetype()

        if not self.title:
            self.title = "input_document"

        # skip data validation if it's not provided
        if not self.data:
            return self

        try:
            decoded_document = base64.b64decode(self.data, validate=True)
        except BinasciiError:
            decoded_document = self.data
            self.data = base64.b64encode(self.data)

        return self

    def resolve_document(self) -> BytesIO:
        """
        Resolve a document such that it is represented by a BufferIO object.
        """
        return resolve_binary(
            raw_bytes=self.data,
            path=self.path,
            url=str(self.url) if self.url else None,
            as_base64=False,
        )

    def guess_format(self) -> str | None:
        path = self.path or self.url
        if not path:
            return None

        return Path(str(path)).suffix.replace(".", "")

    def _guess_mimetype(self) -> str | None:
        if self.data:
            guess = filetype.guess(self.data)
            return str(guess.mime) if guess else None

        suffix = self.guess_format()
        if not suffix:
            return None

        guess = filetype.get_type(ext=suffix)
        return str(guess.mime) if guess else None


class FunctionCall(BaseModel):
    name: str
    arguments: str


class WebSearchInfo(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None
    snippet: Optional[str] = None
    hostname: Optional[str] = None
    hostlogo: Optional[str] = None
    date: Optional[str] = None


class Extra(BaseModel):
    web_search_info: List[WebSearchInfo]


class Delta(BaseModel):
    role: str
    content: str
    name: Optional[str] = ""
    function_call: Optional[FunctionCall] = None
    extra: Optional[Extra] = None


class ChoiceStream(BaseModel):
    delta: Delta


class Message(BaseModel):
    role: str
    content: str


class Choice(BaseModel):
    message: Message
    extra: Optional[Extra] = None


class ChatResponse(BaseModel):
    """Chat response."""
    choices: list[Choice]


class ChatResponseStream(BaseModel):
    """Chat response stream."""

    choices: list[ChoiceStream]
    usage: dict
    # message: ChatMessage


ContentBlock = Annotated[
    Union[TextBlock, ImageBlock, AudioBlock, DocumentBlock], Field(
        discriminator="block_type")
]


class ChatMessage(BaseModel):
    role: MessageRole = MessageRole.USER
    additional_kwargs: Dict[str, Any] = Field(default_factory=dict)
    web_search: bool = False
    thinking: bool = False
    blocks: List[ContentBlock] = Field(default_factory=list)

    def __init__(self, content: any | None = None, **data: Any) -> None:
        # Handle LlamaIndex compatibility
        if "role" in data and isinstance(data["role"], Enum):
            data["role"] = data["role"].value

        # Handle blocks field for both Qwen and LlamaIndex
        if "blocks" in data:
            if not isinstance(data["blocks"], list):
                data["blocks"] = [data["blocks"]]
            else:
                # Validate each block
                valid_blocks = []
                for block in data["blocks"]:
                    # Handle different block types
                    if isinstance(block, (str, TextBlock)):
                        if isinstance(block, str):
                            block = TextBlock(text=block)
                        valid_blocks.append(block)

                    elif isinstance(block, dict):
                        block_type = block.get("block_type")
                        if block_type == "text":
                            valid_blocks.append(TextBlock(**block))
                        elif block_type == "image":
                            valid_blocks.append(ImageBlock(**block))
                        elif block_type == "audio":
                            valid_blocks.append(AudioBlock(**block))
                        elif block_type == "document":
                            valid_blocks.append(DocumentBlock(**block))
                    else:
                        valid_blocks.append(block)

                data["blocks"] = valid_blocks

        # Convert additional_kwargs to dict if it's not already
        if "additional_kwargs" in data and not isinstance(data["additional_kwargs"], dict):
            try:
                data["additional_kwargs"] = dict(data["additional_kwargs"])
            except Exception:
                data["additional_kwargs"] = {}

        # Handle content initialization
        if content is not None:
            if isinstance(content, str):
                data["blocks"] = [TextBlock(text=content)]
            elif isinstance(content, list):
                data["blocks"] = content
            else:
                # Handle other content types
                data["blocks"] = [TextBlock(text=str(content))]

        # Call parent constructor
        super().__init__(**data)

    @property
    def content(self) -> str | None:
        """
        Keeps backward compatibility with the old `content` field.

        Returns:
            The cumulative content of the TextBlock blocks, None if there are none.

        """
        content = ""
        for block in self.blocks:
            if isinstance(block, TextBlock):
                content += block.text

        return content or None

    def __str__(self) -> str:
        return f"{self.role.value}: {self.content}"
