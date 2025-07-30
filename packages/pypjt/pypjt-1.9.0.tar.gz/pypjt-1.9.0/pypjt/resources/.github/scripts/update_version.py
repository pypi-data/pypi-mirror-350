import os
import re
import sys

version = os.environ.get("NEW_VERSION")
if not version:
    print("Error: NEW_VERSION environment variable not set.", file=sys.stderr)
    sys.exit(1)

files_to_update = [
    {
        "file": "uv.lock",
        "pattern": re.compile(
            r'(?P<block>\[\[package\]\][^\[]*?name\s*=\s*["\']pypjt["\'][^\[]*?version\s*=\s*["\'])(?P<version>\d+\.\d+\.\d+)(["\'])',
            re.DOTALL,
        ),
        "replacement": lambda m: f"{m.group('block')}{version}{m.group(3)}",
    },
    {
        "file": "pyproject.toml",
        "pattern": re.compile(
            r'(?P<block>\[project\]\s+name\s*=\s*["\'].*?["\']\s+version\s*=\s*["\'])(?P<version>\d+\.\d+\.\d+)(["\'])',
            re.DOTALL,
        ),
        "replacement": lambda m: f"{m.group('block')}{version}{m.group(3)}",
    },
]

print(f"Updating version to: {version}")

for entry in files_to_update:
    filename = entry["file"]
    pattern = entry["pattern"]
    replacement_func = entry["replacement"]

    print(f"Processing: {filename}")

    if not os.path.exists(filename):
        print("File not found, skipping.")
        continue

    try:
        with open(filename, encoding="utf-8") as f:
            content = f.read()

        def replacement_with_log(m, replacement_func=replacement_func):
            old_line = f"{m.group('block')}{m.group('version')}{m.group(3)}"
            new_line = replacement_func(m)
            print(f"Matched:\n{old_line}\nReplaced with:\n{new_line}\n")
            return new_line

        new_content, num_replacements = pattern.subn(replacement_with_log, content)

        if num_replacements > 0:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Successfully updated version in {filename}")
        else:
            print("No matching version found or already up-to-date.")
    except Exception as e:
        print(f"Error updating {filename}: {e}", file=sys.stderr)
