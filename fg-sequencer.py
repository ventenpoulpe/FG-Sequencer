import os
import sys
import re
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap

# Constants
IMG_FOLDER = "img"
MAPPING_FILE = "mapping.json"
ICON_SIZE = (128, 128)

# Separators
CONVERTIBLE_SEPARATORS = ['xx', '+']
ROW_BREAK_SEPARATOR = ','
NEUTRAL_SEPARATORS = [' ', '.']
ALL_SEPARATORS = CONVERTIBLE_SEPARATORS + [ROW_BREAK_SEPARATOR] + NEUTRAL_SEPARATORS

def load_mapping():
    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    mapping = {}
    for entry in data:
        token = entry["input"]
        mapping.setdefault(token, []).append(entry)
    return mapping

def parse_sequence(sequence):
    pattern = f"({'|'.join(map(re.escape, ALL_SEPARATORS))})"
    tokens = re.split(pattern, sequence)
    return [token.strip() for token in tokens if token.strip()]

def resolve_icon_path(token, mapping, game):
    if token not in mapping:
        return None
    entries = mapping[token]
    # 1. Prefer game-specific entry
    for entry in entries:
        if entry["category"].lower() == game.lower():
            return os.path.join(IMG_FOLDER, game, entry["filename"])
    # 2. Fallback to Basic/Advanced Notation
    for entry in entries:
        if entry["category"] in ["Basic Notation", "Advanced Notation"]:
            return os.path.join(IMG_FOLDER, entry["category"], entry["filename"])
    # 3. Last resort
    entry = entries[0]
    return os.path.join(IMG_FOLDER, entry["category"], entry["filename"])

    # Draw comment block
def draw_comment(draw, comment, total_width, y_offset):
    # Add 16px spacing before comment
    y_offset += 16

    # Dynamically scale font size
    font_size = max(12, total_width // 30)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Wrap comment text to fit image width
    max_chars_per_line = max(10, total_width // (font_size // 1.5))
    lines = wrap(comment, width=int(max_chars_per_line))

    line_height = font.getbbox("Ay")[3]  # height of one line
    comment_height = line_height * len(lines) + 16  # 8px padding top/bottom

    # Draw black rectangle
    draw.rectangle([0, y_offset, total_width, y_offset + comment_height], fill=(0, 0, 0, 255))

    # Draw each line centered
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        draw.text(((total_width - text_w) // 2, y_offset + 8 + i * line_height),
                  line, font=font, fill=(255, 255, 255, 255))
    return comment_height + 16  # total vertical space used

def build_image(tokens, mapping, game, comment):
    rows = [[]]
    for token in tokens:
        if token in NEUTRAL_SEPARATORS:
            continue
        elif token == ROW_BREAK_SEPARATOR:
            rows.append([])
        elif token in mapping:
            icon_path = resolve_icon_path(token, mapping, game)
            if icon_path and os.path.exists(icon_path):
                icon = Image.open(icon_path).convert("RGBA").resize(ICON_SIZE)
                rows[-1].append(icon)
            else:
                print(f"⚠️ Image not found for token '{token}' at {icon_path}")
        else:
            print(f"⚠️ Token '{token}' not found in mapping.")

    row_widths = [ICON_SIZE[0] * len(row) for row in rows if row]
    total_width = max(row_widths) if row_widths else ICON_SIZE[0]
    num_rows = len([row for row in rows if row])
    total_height = ICON_SIZE[1] * num_rows + (num_rows - 1) * 17

    # Create base image first
    result = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))

    y_offset = 0
    for row_index, row in enumerate(rows):
        x_offset = 0
        for icon in row:
            result.paste(icon, (x_offset, y_offset), icon)
            x_offset += ICON_SIZE[0]
        y_offset += ICON_SIZE[1]
        if row_index < num_rows - 1 and row:
            y_offset += 8
            line = Image.new("RGBA", (total_width, 1), (128, 128, 128, 255))
            result.paste(line, (0, y_offset))
            y_offset += 9  # 8px below + 1px line

    # Now add comment block
    draw = ImageDraw.Draw(result)
    extra_height = draw_comment(draw, comment, total_width, y_offset)

    # Expand canvas to fit comment
    final = Image.new("RGBA", (total_width, total_height + extra_height), (0, 0, 0, 0))
    final.paste(result, (0, 0))
    draw = ImageDraw.Draw(final)
    draw_comment(draw, comment, total_width, y_offset)

    return final


def main():
    if len(sys.argv) != 3:
        print("Usage: python string_sequencer.py <json_file> <scale_percentage>")
        sys.exit(1)

    json_file = sys.argv[1]
    try:
        scale_percentage = int(sys.argv[2])
        if not (10 <= scale_percentage <= 100):
            raise ValueError
    except ValueError:
        print("Error: scale_percentage must be an integer between 10 and 100.")
        sys.exit(1)

    with open(json_file, "r", encoding="utf-8") as f:
        sequences = json.load(f)

    mapping = load_mapping()

    # Create output folder with timestamp
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")  # use - instead of :
    output_folder = os.path.join(os.getcwd(), timestamp)
    os.makedirs(output_folder, exist_ok=True)


    for i, entry in enumerate(sequences, start=1):
        # Sequence key may be "sequence" or "string"
        seq_text = entry.get("sequence") or entry.get("string")
        tokens = parse_sequence(seq_text)
        game_type = entry["type"]
        comment = entry.get("comment", "")
        image = build_image(tokens, mapping, game_type, comment)
        if image:
            new_width = int(image.width * scale_percentage / 100)
            new_height = int(image.height * scale_percentage / 100)
            image = image.resize((new_width, new_height), Image.LANCZOS)
            filename = f"{entry['game']} - {entry['character']} - {i}.png"
            image.save(os.path.join(output_folder, filename))
            print(f"✅ Generated: {filename}")
        else:
            print(f"⏭️ Skipped entry {i}: No valid tokens found.")

if __name__ == "__main__":
    main()
