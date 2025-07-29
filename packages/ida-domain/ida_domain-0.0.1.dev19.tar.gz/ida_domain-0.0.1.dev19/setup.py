from setuptools import setup, find_packages
example_code = """import argparse
import ida_domain

parser = argparse.ArgumentParser(description=\"IDA Domain usage example, version {ida_domain.VersionInfo.api_version}\")
parser.add_argument(\"-f\", \"--input-file\", help=\"Binary input file to be loaded\", type=str, required=True)
args = parser.parse_args()

print(f\"IDA Domain usage example, version {ida_domain.VersionInfo.api_version}\")

ida_options = (ida_domain.IdaCommandBuilder()
                .auto_analysis(True)
                .new_database(True))

db = ida_domain.Database()

if db.open(args.input_file, ida_options):
    print(f\"Entry point: {hex(db.entry_point)}\")

    print(f\"Metadata:\")
    for key, value in db.metadata.items():
        print(f\" {key}: {value}\")

    for f in db.functions.get_all():
        print(f\"Function - name {f.name}, start ea {hex(f.start_ea)}, end ea {f.end_ea}\")

    for s in db.segments.get_all():
        print(f\"Segment - name {s.label}\")

    for t in db.types.get_all():
        if t.name is not None:
            print(f\"Type - name {t.name}, id {t.get_tid()}\")
        else:
            print(f\"Type - id {t.get_tid()}\")

    for c in db.comments.get_all(False):
        print(f\"Comment - value {c}\")

    for s1 in db.strings.get_all():
        print(f\"String - value {s1}\")

    for n in db.names.get_all():
        print(f\"Name - value {n}\")

    for b in db.basic_blocks.get_between(db.minimum_ea, db.maximum_ea):
        print(f\"Basic block - start ea {hex(b.start_ea)}, end ea {hex(b.end_ea)}\")

    for inst in db.instructions.get_between(db.minimum_ea, db.maximum_ea):
        ret, dec = db.instructions.get_disassembly(inst)
        if ret:
            print(f\"Instruction - ea {hex(inst.ea)}, asm {dec}\")

    db.close(False)"""

setup(
    name="ida-domain",
    version="0.0.1.dev19",
    author="Hex-Rays SA",
    author_email="support@hex-rays.com",
    description="IDA Domain API",
    long_description=f"""
# IDA Domain API
\n**⚠️ This is a dev pre-release version. APIs may change without notice and pre-release versions may be deleted at any time.**


## The IDA Domain API provides a Domain Model on top of IDA SDK

## Prerequisites 

export IDADIR=[IDA Installation dir]

eg: IDADIR="/Applications/Applications/IDA Professional 9.1.app/Contents/MacOS/"

## Usage example:

```python
{example_code}
```
""",
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
      "Development Status :: 2 - Pre-Alpha",
      "License :: OSI Approved :: MIT License",
      "Programming Language :: Python :: 3",
      "Operating System :: OS Independent",
      "Topic :: Software Development :: Disassemblers",
    ],
    packages=["ida_domain", "ida_domain.windows", "ida_domain.macos", "ida_domain.linux"],
    package_dir={
        "ida_domain": "ida_domain",
        "ida_domain.windows": "ida_domain/windows",
        "ida_domain.macos": "ida_domain/macos",
        "ida_domain.linux": "ida_domain/linux",
    },
    include_package_data=True,
    package_data={
        "ida_domain": ["*.py"],
        "ida_domain.windows": ["*.py", "*.pyd", "*.dll", "*.pyi"],
        "ida_domain.macos": ["*.py", "*.so", "*.dylib", "*.pyi"],
        "ida_domain.linux": ["*.py", "*.so", "*.pyi"],
    },
    zip_safe=False,
)
