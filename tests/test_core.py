"""Unit tests for agent-output-steganography-detector."""
import unittest
from agent_output_steganography_detector.core import SteganographyDetector

class TestSteganographyDetector(unittest.TestCase):
    def setUp(self):
        self.detector = SteganographyDetector()

    def test_clean_text(self):
        res = self.detector.inspect("Normal visible sentence with zero covert characters.")
        self.assertFalse(res.detected)
        self.assertEqual(res.codepoint_count, 0)

    def test_encode_and_detect_binary(self):
        # 8 bits: 01000001 = 'A'
        bits = "01000001"
        payload = "".join(self.detector.ZW_NJ if b == "1" else self.detector.ZW_SP for b in bits)
        text = f"Hello{payload}World"
        res = self.detector.inspect(text)
        self.assertTrue(res.detected)
        self.assertEqual(res.codepoint_count, 8)
        self.assertEqual(res.decoded_text, "A")

    def test_scrub_removes_all_zw_chars(self):
        text = f"A​B‌C﻿D"
        cleaned = self.detector.scrub(text)
        self.assertEqual(cleaned, "ABCD")
