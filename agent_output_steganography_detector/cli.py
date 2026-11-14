"""CLI for agent-output-steganography-detector."""
import argparse
import sys
from .core import SteganographyDetector

def main():
    parser = argparse.ArgumentParser(description="Agent Output Steganography Detector CLI")
    parser.add_argument("--demo", action="store_true", help="Run steganography detection and scrub demo")
    args = parser.parse_args()

    if args.demo:
        detector = SteganographyDetector()
        # Encode 'SECRET' in zero-width bits
        secret = "AI"
        bits = "".join(f"{ord(c):08b}" for c in secret)
        zw_payload = "".join(detector.ZW_NJ if b == "1" else detector.ZW_SP for b in bits)
        covert_text = f"Here is the benign response{zw_payload} from the agent."

        res = detector.inspect(covert_text)
        print(f"[+] Covert text inspected: detected={res.detected}, count={res.codepoint_count} zw chars")
        print(f"[+] Decoded secret payload: '{res.decoded_text}'")
        scrubbed = detector.scrub(covert_text)
        print(f"[+] Scrubbed safe text: '{scrubbed}'")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
