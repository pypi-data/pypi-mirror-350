from compliance_vision.main import get_response
import sys

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: uv run compliance-vision <image_path>")
        sys.exit(1)
    for i in range(1, len(sys.argv)):
        # print(sys.argv[i])
        get_response(sys.argv[i])