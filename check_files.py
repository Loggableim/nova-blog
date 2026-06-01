import json, os, zipfile, hashlib

nova_site = r"C:\HermesPortable\home\spaces\bewusstsein\nova-site"
os.chdir(nova_site)

allowed = {
    'index.html', 'nova-avatar.png', 'nova-status.json',
    'blog/index.html', 'blog/internet-expedition.html', 'blog/shared-memory.html'
}

files = []
for root, dirs, fnames in os.walk('.'):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
    for f in fnames:
        if f in ('manifest.json', 'deploy.zip', 'minimal.zip', 'build.py', 'deploy_upload.py', 'create_deploy.py', 'create_deploy2.py', 'deploy.sh'):
            continue
        fp = os.path.join(root, f)
        rel = '/' + fp.replace('\\', '/').lstrip('./').lstrip('.\\')
        if rel.lstrip('/') in allowed:
            files.append((fp, rel))

print(f"OK: {len(files)} files")
for _, rel in files:
    print(f"  {rel}")
