"""
setup_project.py
Run this once to create the entire folder structure including output folders.
"""

import os

folders = [
    "data/raw",
    "data/processed",
    "notebooks",
    "src",
    "outputs/figures",
    "outputs/models",
    "dashboard",
    "reports"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"✅ Created: {folder}")

# Create __init__.py for src package
open("src/__init__.py", "a").close()
print("✅ Created: src/__init__.py")

# Create .gitkeep files in empty output folders so they track in git
for folder in ["outputs/figures", "outputs/models", "dashboard", "reports"]:
    gitkeep_path = os.path.join(folder, ".gitkeep")
    open(gitkeep_path, "a").close()
    print(f"✅ Created: {gitkeep_path}")

print("\n🎉 All folders ready! Place your dataset in data/raw/")
