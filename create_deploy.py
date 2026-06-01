import zipfile, os, json
import sys

nova_site = sys.argv[1] if len(sys.argv) > 1 else "."

os.chdir(nova_site)

# Find all files to upload
files_to_upload = []
for root, dirs, files in os.walk('.'):
    # Skip hidden directories
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for f in files:
        if f.startswith('.'):
            continue
        filepath = os.path.join(root, f)
        files_to_upload.append(filepath)

# Create manifest
manifest = {}
for fp in files_to_upload:
    relpath = os.path.normpath(fp).replace('\\', '/')
    if relpath.startswith('./') or relpath.startswith('.\\'):
        relpath = relpath[2:]
    with open(fp, 'rb') as fh:
        content = fh.read()
    manifest[relpath] = str(len(content))

with open(os.path.join(nova_site, 'manifest.json'), 'w') as f:
    json.dump(manifest, f)

# Create zip
zip_path = os.path.join(nova_site, 'deploy.zip')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(os.path.join(nova_site, 'manifest.json'), 'manifest.json')
    for fp in files_to_upload:
        relpath = os.path.normpath(fp).replace('\\', '/')
        if relpath.startswith('./') or relpath.startswith('.\\'):
            relpath = relpath[2:]
        zf.write(fp, relpath)

print(f"Zip size: {os.path.getsize(zip_path)} bytes")
print(f"Files in zip: {len(files_to_upload)}")
for f in files_to_upload:
    print(f"  {os.path.normpath(f).replace(os.sep, '/')[2:]}")
