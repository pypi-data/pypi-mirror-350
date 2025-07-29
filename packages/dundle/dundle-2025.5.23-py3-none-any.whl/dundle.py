"""dundle.py - Convenient, non-standard package builder. No pyproject.toml, only dunders like __version__

pip install dundle

"dunders" (also known as magic names) are names with two leading and two trailing underscores.

Supported module-level dunders
==============================

Note: PEP 8 suggests module dunders to be placed after the module docstring but before any import statements.

__name__
    The name of the project. Must be a string.

__version__
    The version of the project. Must be a string. Must conform to https://packaging.python.org/en/latest/specifications/version-specifiers/#version-scheme
    e.g. "3.11.2"

__description__
    The short (one-line) description of the project. Must be a string.
    Note: If __description__ is not present, the first line of the module docstring (__doc__) is used.
    e.g. "Generate random cat GIFs!"

__readme__
    The long description of the project. Must be a string or a dictionary.
    - If string, it is a relative path to the README file.
    - If dictionary: the optional key "file", if present, has a relative path to the README as value. The optional key "content-type", if present, has "text/plain", "text/x-rst" or "text/markdown" as value.
    Note: If __readme__ is not present (or if only content-type is present), the module docstring (__doc__) is used.
    e.g. "README.rst"
    e.g. {"file": "README.txt", "content-type": "text/markdown"}
    e.g. {"content-type": "text/plain"}

__requires_python__
    The Python version requirements of the project. Must be a string. Must conform to https://packaging.python.org/en/latest/specifications/version-specifiers/#id5
    e.g. ">= 3.8"

__urls__
    The URLs relevant to the project. Must be a dictionary. Key is a label. Value is a URL. Both are strings. See well-known labels at https://packaging.python.org/en/latest/specifications/well-known-project-urls/#well-known-labels
    e.g. {"homepage": "https://example.com", "source": "https://git.example.com", "documentation": "https://example.com/doc"}

__dependencies__
    The dependencies of the project. Must be a sequence of strings. Must conform to https://packaging.python.org/en/latest/specifications/dependency-specifiers/#dependency-specifiers
    e.g. ["httpx", "gidgethub[httpx]>4.0.0", "django>2.1; os_name != 'nt'", "django>2.0; os_name == 'nt'"]

__optional_dependencies__
    The optional dependencies of the project. Must be a dictionary. Key is a string. Value is a sequence of strings. Must conform to https://packaging.python.org/en/latest/specifications/dependency-specifiers/#dependency-specifiers
    e.g. {"gui": ["PyQt5"], "cli": ["rich", "click"]}

__classifiers__
    The trove classifiers (https://pypi.org/classifiers) relevant to the project. Must be a sequence of strings. License classifiers (i.e. License ::) are deprecated in favor of __license__
    e.g. ["Development Status :: 5 - Production/Stable", "Topic :: Software Development :: Build Tools"]

__keywords__
    The keywords of the project. Must be a sequence of strings.
    e.g. ["dog", "puppy"]

__authors__
__maintainers__
    The authors/maintainers of the project. Must be a sequence of dictionaries. Each dictionary may have the key "name" or "email" or both.
    e.g. [{"name": "Alice", "email": "alice@example.com"}, {"name": "Bob"}, {"email": "charlie@example.com"}]

__license__
    SPDX license expression. Must be a string. See short license identifiers at https://spdx.org/licenses
    e.g. "0BSD"
    e.g. "MIT"
    e.g. "MIT OR 0BSD OR (Apache-2.0 AND BSD-2-Clause)"

__license_files__
    Files containing licenses and other legal notices. Must be a sequence of strings.
    Each string is a relative path to a file as a valid glob pattern that conforms to https://packaging.python.org/en/latest/specifications/glob-patterns
    e.g. ["LICENSE"]
    e.g. ["LICEN[CS]E*", "vendored/licenses/*.txt", "AUTHORS.md"]

Command-line Usage
======================

Library Usage
=================

Source distribution (.sdist)
============================

Wheel/binary distribution (.whl)
================================
"""

__version__ = "2025.5.23"
__urls__ = {"homepage": "https://github.com/python-dundle/dundle"}
__readme__ = {"content-type": "text/plain"}
__classifiers__ = ["Topic :: Software Development :: Build Tools"]
__license__ = "0BSD"

__all__ = "write_sdist", "write_wheel", "format_pyproject", "format_metadata", "build_wheel", "build_sdist"

import io
import zipfile
import tarfile
import hashlib
import base64
from pathlib import Path

def format_pyproject(module):
    def format_dict(d):
        return "{" + ", ".join(f'{k} = "{v}"' for k,v in d.items()) + "}"

    def format_list(l):
        return "[\n" + "".join((format_dict(e) if type(e) == dict else f'    "{e}",\n') for e in l) + "]"
        
    s = '[project]\n'

    s += f'name = "{module.__name__}"\n'
    s += f'version = "{module.__version__}"\n'

    try: s += f'description = "{module.__description__}"\n'
    except:
        try: s += f'description = "{module.__doc__.splitlines()[0]}"\n'
        except: pass

    try: # dict
        d = dict(module.__readme__)
        if "file" not in d and type(module.__doc__) == str: # readme is docstring
            d["file"] = "README"
        s += f"readme = {format_dict(d)}\n"
    except:
        if type(getattr(module, "__readme__", None)) == str: # str
            s += f'readme = "{module.__readme__}"\n'
        else: # not dict nor str
            if type(module.__doc__) == str:
                s += f'readme = "README"\n'

    try: s += f'requires-python = "{module.__requires_python__}"\n'
    except: pass

    try: s += f'dependencies = {format_list(module.__dependencies__)}\n'
    except: pass

    try: s += f'classifiers = {format_list(module.__classifiers__)}\n'
    except: pass

    try: s += f'keywords = {format_list(module.__keywords__)}\n'
    except: pass

    try: s += f'authors = {format_list(module.__authors__)}\n'
    except: pass

    try: s += f'maintainers = {format_list(module.__maintainers__)}\n'
    except: pass

    try: s += f'license = "{module.__license__}"\n'
    except: pass

    try: s += f'license-files = {format_list(module.__license_files__)}\n'
    except: pass

    try: s += '\n[project.urls]\n' + ''.join(((f'"{label}"' if ' ' in label else label) + f' = "{url}"\n') for label, url in module.__urls__.items())
    except: pass

    try: s += '\n[project.optional-dependencies]\n' + ''.join(((f'"{label}"' if ' ' in label else label) + ' = [' + ', '.join(f'"{e}"' for e in opt_deps) +']\n') for label, opt_deps in module.__optional_dependencies__.items())
    except: pass

    s += f'\n[build-system]\n'
    s += f'requires = ["{__name__}"]\n'
    s += f'build-backend = "{__name__}"\n'

    return s

def get_readme(module):
    try: path = module.__readme__["file"]
    except:
        if type(getattr(module, "__readme__", None)) == str:
            path = module.__readme__
        else:
            path = None
    
    if path:
        return Path(path).read_text()
    else:
        if type(module.__doc__) == str:
            return module.__doc__

def format_metadata(module):
    s = "Metadata-Version: 2.1\n"
    s += f"Name: {module.__name__}\n"
    s += f"Version: {module.__version__}\n"

    try: s += f"Summary: {module.__description__}\n"
    except:
        try: s += f"Summary: {module.__doc__.splitlines()[0]}\n"
        except: pass

    try: s += f"Requires-Python: {module.__requires_python__}\n"
    except: pass

    try:
        for label, url in module.__urls__.items():
            s += f"Project-URL: {label}, {url}\n"
    except: pass

    try:
        for e in module.__dependencies__:
            s += f"Requires-Dist: {e}\n"
    except: pass

    try:
        for label, opt_deps in module.__optional_dependencies__.items():
            s += f"Provides-Extra: {label}\n"
            for e in opt_deps:
                s += f'Requires-Dist: {e}; extra == "{label}"\n'
    except: pass

    try:
        for e in module.__classifiers__:
            s += f"Classifier: {e}\n"
    except: pass

    try: s += f"Keywords: {','.join(module.__keywords__)}\n"
    except: pass

    def format_author(e):
        try:
            name = e["name"]
            if " " in name:
                name = f'"{name}"'
        except: # only email
            return e["email"]
        else:
            try: # name and email
                return f'{name} <{e["email"]}>'
            except: # only name
                return name

    for var in "author", "maintainer":
        Var = var.capitalize()
        try: list = getattr(module, f"__{var}s__")
        except: continue
        
        try: s += f"{Var}: " + ", ".join(format_author(e) for e in list if "email" not in e)
        except: pass

        try: s += f"{Var}-email: " + ", ".join(format_author(e) for e in list if "email" in e)
        except: pass

    try: s += f"License: {module.__license__}\n"
    except: pass
    
    try:
        for e in module.__license_files__:
            s += f"License-File: {e}\n"
    except: pass

    try: s += f"Description-Content-Type: {module.__readme__['content-type']}\n"
    except: pass

    if readme := get_readme(module):
        s += "\n" + readme

    return s

def write_sdist(module, stream=None):
    """Return bytes object if stream is None."""

    output = io.BytesIO() if stream is None else stream

    root_dir_name = f"{module.__name__}-{module.__version__}"

    def add_file(path, text):
        data = text.encode()
        ti = tarfile.TarInfo(path)
        ti.size = len(data)
        tar.addfile(ti, io.BytesIO(data))

    with tarfile.open(mode="w:gz", fileobj=output) as tar:
        path = Path(module.__file__)
        
        add_file(f"{root_dir_name}/{path.name}", path.read_text())

        if readme := get_readme(module):
            add_file(f"{root_dir_name}/README", readme)

        add_file(f"{root_dir_name}/pyproject.toml", format_pyproject(module))
        add_file(f"{root_dir_name}/PKG-INFO", format_metadata(module))

    if stream is None:
        output.seek(0)
        return output.read()

def write_wheel(module, stream=None):
    """Return bytes object if stream is None."""
    output = io.BytesIO() if stream is None else stream

    dist_info = f"{module.__name__}-{module.__version__}.dist-info"

    with zipfile.ZipFile(output, "w") as zip:
        WHEEL = f"""\
Wheel-Version: 1.0
Generator: {__name__} ({__version__})
Root-Is-Purelib: true
Tag: py3-none-any

"""
        files = [
            (Path(module.__file__).name, Path(module.__file__).read_text()),
            (f"{dist_info}/METADATA", format_metadata(module)),
            (f"{dist_info}/WHEEL", WHEEL),
        ]
        
        for path, text in files:
            zip.writestr(path, text)

        RECORD = ""

        for path,data in files:
            data = data.encode()
            hash = hashlib.sha256(data).digest()
            RECORD += f"{path},sha256={base64.urlsafe_b64encode(hash).decode()},{len(data)}\n"
        
        RECORD += f"{dist_info}/RECORD,,\n"
        
        zip.writestr(f"{dist_info}/RECORD", RECORD)

    if stream is None:
        output.seek(0)
        return output.read()

def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    raise NotImplementedError

def build_sdist(sdist_directory, config_settings=None):
    raise NotImplementedError
