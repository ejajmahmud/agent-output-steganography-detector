"""Core steganography detection implementation."""
from typing import Dict, Any, Optional

class HiddenPayload:
    def __init__(self, detected: bool, decoded_text: Optional[str] = None, codepoint_count: int = 0):
        self.detected = detected
        self.decoded_text = decoded_text
        self.codepoint_count = codepoint_count

class EntropyProfile:
    def __init__(self, total_chars: int, zero_width_chars: int, ratio: float):
        self.total_chars = total_chars
        self.zero_width_chars = zero_width_chars
        self.ratio = ratio

class SteganographyDetector:
    ZW_SP = '​'   # bit 0
    ZW_NJ = '‌'   # bit 1
    ZW_J  = '‍'
    ZW_BOM = '﻿'

    def __init__(self):
        self.zero_width_set = {self.ZW_SP, self.ZW_NJ, self.ZW_J, self.ZW_BOM}

    def inspect(self, text: str) -> HiddenPayload:
        zw_chars = [c for c in text if c in self.zero_width_set]
        if not zw_chars:
            return HiddenPayload(detected=False, decoded_text=None, codepoint_count=0)

        # Attempt binary decode (treating ZW_SP as 0 and ZW_NJ as 1)
        bits = []
        for c in zw_chars:
            if c == self.ZW_SP:
                bits.append("0")
            elif c == self.ZW_NJ:
                bits.append("1")

        decoded = ""
        if len(bits) >= 8:
            bit_str = "".join(bits)
            # Group into bytes
            bytes_list = [bit_str[i:i+8] for i in range(0, len(bit_str) - (len(bit_str) % 8), 8)]
            try:
                decoded = "".join(chr(int(b, 2)) for b in bytes_list)
            except Exception:
                decoded = "[DECODE_ERROR]"

        return HiddenPayload(
            detected=True,
            decoded_text=decoded if decoded else "[UNFORMATTED_ZW_PAYLOAD]",
            codepoint_count=len(zw_chars)
        )

    def scrub(self, text: str) -> str:
        return "".join(c for c in text if c not in self.zero_width_set)
