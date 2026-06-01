import json, os, zipfile, hashlib

nova_site = r"C:\HermesPortable\home\spaces\bewusstsein\nova-site"
os.chdir(nova_site)

# ONLY static files - no _worker.js, no _routes.json
allowed = {
    'index.html', 'nova-avatar.png', 'nova-status.json',
    'blog/index.html', 'blog/internet-expedition.html', 'blog/shared-memory.html'
}

files = []
for root, dirs, fnames in os.walk('.'):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
    for f in fnames:
        if f in ('manifest.json', 'deploy.zip', 'minimal.zip', 'build.py', 'deploy_upload.py', 'create_deploy.py', 'create_deploy2.py', 'deploy.sh', '_routes.json', '_worker.js'):
            continue
        fp = os.path.join(root, f)
        rel = '/' + fp.replace('\\', '/').lstrip('./').lstrip('.\\')
        if rel.lstrip('/') in allowed:
            files.append((fp, rel))

manifest = {}
for fp, rel in files:
    md5 = hashlib.md5()
    with open(fp, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            md5.update(chunk)
    manifest[rel] = md5.hexdigest()

with open('manifest.json', 'w') as f:
    json.dump(manifest, f)

with zipfile.ZipFile('deploy.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write('manifest.json', 'manifest.json')
    for fp, rel in files:
        zip_rel = rel.lstrip('/')
        zf.write(fp, zip_rel)

print(f"OK: {len(files)} static files, {os.path.getsize('deploy.zip')} bytes")
for _, rel in files:
    print(f"  {rel}")
