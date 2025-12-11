# FG-Sequencer
FG Sequencer is a Python utility that converts fighting game input strings into clear, visual combo diagrams.
It reads sequences from a JSON file (with metadata like game, character, and comments), maps each input to its corresponding icon via a configurable mapping.json, and generates PNG images that stack inputs row‑by‑row with separators.

# Examples
Turn these:

<img width="528" height="114" alt="image" src="https://github.com/user-attachments/assets/ffb32df2-4c80-4ad1-8275-650d8e2d3c0d" />
<img width="428" height="87" alt="image" src="https://github.com/user-attachments/assets/b950ca05-82f4-4168-a242-d7bbc9df92f2" />

 into these:
 
<img width="448" height="169" alt="MVC2 - Rogue - 5" src="https://github.com/user-attachments/assets/fd7248f1-e0af-4f46-b9ab-261c5bd8397b" />
<img width="295" height="111" alt="2XKO - VI - 1" src="https://github.com/user-attachments/assets/4e8b69de-dcd3-48bb-b3da-fd79fafd284e" />

_(the PNG font is transparent)_

You can then reuse these images for your own purpose (document, video incrustation, quick sharing... etc).

# Key features
- 🔄 Game‑aware mapping: prioritizes game‑specific icons, with fallback to universal Basic/Advanced Notation.
- 🖼️ Automatic layout: rows separated by padded grey lines, with scaling options for output size.
- 📝 Comment blocks: adds readable annotations under each sequence, with dynamic font scaling and line wrapping.
- 📂 Organized output: images saved in timestamped folders, named by game, character, and entry index.

# Pre-requisites
**You need:**
- Python 3.9+ (tested with 3.10 and above)
- Pillow for image creation, resizing, drawing text, and handling icons (installation may be needed as it is not part of the standard Python library: pip install pillow)
- textwrap → part of Python’s standard library (no install needed)
- json, os, sys, re, datetime → all standard library modules (no install needed)

**Notes:**
- If you want nicer fonts for comments, you may need a system font like arial.ttf. On Linux/macOS, you can point to another font file path if Arial isn’t available.
- The script is expected to be cross‑platform but was tested on MS Windows only.

# Deployment
1. Download the package from this page.
2. Ready to use.
3. DO NOT DELETE the mapping.json or the 'img' folder content as they are necessary for the script to work.

# How to use
1. Go the folder where you downloaded the package.
2. Create and fill your input file, based on the example.json file provided. Use classic or numpad notations.
3. Open a command prompt (or Bash or PowerShell) and run this command: python ./fg_sequencer.py name_of_your_file.json
   For example: python ./fg_sequencer.py my_fav_combos.json
   Optional: after your input file, you can also enter an additional argument that will be used to scale the output images (must be an integer ranging between 10 and 100).
4. Your images will be generated in a subfolder named with the date and time.

# Limitations and flexibility
By default, the classic notations and numpad notations are registered in the mapping.json file. If you feel like something is missing (or ran into a notation-related issue while attempting to run the script), feel free to edit the mapping file and/or add new icons to suit your needs. HOWEVER, I DO NOT INTEND TO UPDATE THE DEFAULT MAPPING SO PLEASE DO SO AT YOUR OWN DISCRETION.
Actual limitations to the script custom logic: only the " " (space), "xx" (cancel), "+" (combination) and "," (sequence partitioner or link) are considered as separators when parsing the string. The string for a sequence must be written on a single line in your input json file for the script to parse properly.
That's it.
