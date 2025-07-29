import os
import shutil
import subprocess
import toml
import hashlib

# Remove dist directory if it exists
if os.path.exists('dist'):
    shutil.rmtree('dist')
    
version = '1.0.0'
with open('pyproject.toml', 'r') as f:
    data = toml.load(f)
    # Parse current version and increment build number
    version_parts = data['project']['version'].split('.')
    version_base = '.'.join(version_parts[:-1]) + '.'
    build_num = int(version_parts[-1]) + 1
    new_version = f"{version_base}{build_num}"
    version = new_version
    data['project']['version'] = new_version
    
    with open('pyproject.toml', 'w') as f:
        toml.dump(data, f)


with open('src/gthelp/__init__.py', 'w') as f:
    f.write(f"__version__ = '{version}'\n")
    with open('src/gthelp/assets/arm64-v8a/libhelper', 'rb') as f2:
        md5 = hashlib.md5(f2.read()).hexdigest()
        f.write(f"__md5__ = '{md5}'\n")

# Build package
subprocess.run(['python', '-m', 'build'], check=True)

# Upload to PyPI
subprocess.run(['python', '-m', 'twine', 'upload', 'dist/*', '--verbose'], check=True)