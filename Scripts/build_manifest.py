from pathlib import Path
import json
import re

SERMON_FOLDER = Path("Sermon")
OUTPUT_FILE = SERMON_FOLDER / "slides.json"

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


def natural_sort_key(path: Path):
    """
    Sort filenames naturally.

    Example:
    1.jpg
    2.jpg
    10.jpg

    instead of:
    1.jpg
    10.jpg
    2.jpg
    """
    parts = re.split(r"(\d+)", path.name)

    return [
        int(part) if part.isdigit() else part.lower()
        for part in parts
    ]


def main():
    # Make sure the Sermon folder exists.
    SERMON_FOLDER.mkdir(parents=True, exist_ok=True)

    # Find all supported slide images.
    slides = [
        file
        for file in SERMON_FOLDER.iterdir()
        if file.is_file()
        and file.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    # Put them in numerical/natural filename order.
    slides.sort(key=natural_sort_key)

    # Generate the manifest.
    manifest = {
        "slideCount": len(slides),
        "slides": [
            slide.name
            for slide in slides
        ]
    }

    # Save slides.json.
    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            manifest,
            file,
            indent=2,
            ensure_ascii=False
        )

        # Add a final newline.
        file.write("\n")

    print(f"Found {len(slides)} sermon slides.")

    if slides:
        print("Slides:")
        for index, slide in enumerate(slides, start=1):
            print(f"  {index}: {slide.name}")
    else:
        print("No slide images were found.")

    print(f"Generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
