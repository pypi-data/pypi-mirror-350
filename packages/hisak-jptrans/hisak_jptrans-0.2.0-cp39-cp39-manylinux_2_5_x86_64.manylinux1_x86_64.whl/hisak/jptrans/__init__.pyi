from typing import Union, List

__version__: str


def build_info() -> str: ...


def supported_codecs() -> List[str]: ...


def set_replacement(codec: str, char: bytes): ...


def encode(codec: str, data: Union[str, bytes, bytearray, memoryview], replacement: bool = False) -> bytes: ...


def decode(codec: str, data: Union[bytes, bytearray, memoryview]) -> str: ...
