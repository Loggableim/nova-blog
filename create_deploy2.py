import zipfile, os, json

from pathlib import Path

nova_site = str(Path(__file__).resolve().parent)
os.chdir(nova_site)

# Find all files to upload
files_to_upload = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for f in files:
        if f.startswith('.'):
            continue
        fp = os.path.join(root, f)
        # Convert to forward-slash relative path
        rel = fp.replace('\\', '/')
        if rel.startswith('./'):
            rel = rel[2:]
        files_to_upload.append((fp, rel))

# Create manifest
manifest = {}
for fp, rel in files_to_upload:
    size = os.path.getsize(fp)
    manifest[rel] = str(size)
    print(f"{rel}: {size} bytes")

with open('manifest.json', 'w') as f:
    json.dump(manifest, f)

# Create zip
with zipfile.ZipFile('deploy.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write('manifest.json', 'manifest.json')
    for fp, rel in files_to_upload:
        zf.write(fp, rel)

size = os.path.getsize('deploy.zip')
print(f"\nZip size: {size} bytes")
print(f"Files in zip: {len(files_to_upload)}")
