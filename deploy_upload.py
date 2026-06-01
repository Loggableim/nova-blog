import zipfile, os, json

nova_site = r"C:\HermesPortable\home\spaces\bewusstsein\nova-site"
os.chdir(nova_site)

# Specific files to include
allowed_files = {
    'index.html',
    'nova-avatar.png',
    'nova-status.json',
    'blog/index.html',
    'blog/internet-expedition.html',
}

files_to_upload = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
    for f in files:
        if f.startswith('.') or f in ('manifest.json', 'deploy.zip', 'create_deploy.py', 'create_deploy2.py'):
            continue
        fp = os.path.join(root, f)
        rel = fp.replace('\\', '/')
        if rel.startswith('./'):
            rel = rel[2:]
        if rel in allowed_files:
            files_to_upload.append((fp, rel))

# Create manifest
manifest = {}
for fp, rel in files_to_upload:
    size = os.path.getsize(fp)
    manifest[rel] = str(size)

with open('manifest.json', 'w') as f:
    json.dump(manifest, f)

# Create zip
with zipfile.ZipFile('deploy.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write('manifest.json', 'manifest.json')
    for fp, rel in files_to_upload:
        zf.write(fp, rel)

size = os.path.getsize('deploy.zip')
print(f"Zip size: {size} bytes")
print(f"Files in zip: {len(files_to_upload)}")
for fp, rel in files_to_upload:
    print(f"  {rel}")
