# Copyright (c) Meta Platforms, Inc. and affiliates.

from __future__ import annotations


class Hash256AndMetadata:
    """Container for MIH queries"""

    def __init__(self, _hash, metadata) -> None:
        self._hash = _hash
        self.metadata = metadata


class HashAndQuality:
    """Container for multiple-value object: the hash is a 64-character hex
    string and the quality is an integer in the range 0..100."""

    def __init__(self, _hash, quality) -> None:
        self._hash = _hash
        self.quality = quality

    def getHash(self):
        return self._hash

    def getQuality(self):
        return self.quality


class HashesAndQuality:
    """Container for multiple-value object."""

    def __init__(
        self,
        _hash,
        hashRotate90,
        hashRotate180,
        hashRotate270,
        hashFlipX,
        hashFlipY,
        hashFlipPlus1,
        hashFlipMinus1,
        quality,
    ) -> None:
        self._hash = _hash
        self.hashRotate90 = hashRotate90
        self.hashRotate180 = hashRotate180
        self.hashRotate270 = hashRotate270
        self.hashFlipX = hashFlipX
        self.hashFlipY = hashFlipY
        self.hashFlipPlus1 = hashFlipPlus1
        self.hashFlipMinus1 = hashFlipMinus1
        self.quality = quality
