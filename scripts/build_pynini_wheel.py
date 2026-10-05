"""Assemble a platform wheel from Bazel's Python runfiles archive."""

import argparse
import pathlib
import re
import sys
import sysconfig
import zipfile

from wheel.wheelfile import WheelFile


ROOT = pathlib.Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "opengrm" / "pynini"


def package_files(archive):
  files = {}
  for entry in archive.namelist():
    parts = pathlib.PurePosixPath(entry).parts
    if "opengrm" in parts:
      index = parts.index("opengrm")
      relative = pathlib.PurePosixPath(*parts[index:])
      if (len(relative.parts) == 3 and relative.parts[1] == "pynini"
          and relative.name.startswith("pynini")
          and relative.suffix == ".so"):
        files[str(relative)] = archive.read(entry)
    if "openfst" in parts:
      index = parts.index("openfst")
      relative = pathlib.PurePosixPath(*parts[index:])
      if relative.as_posix() in (
          "openfst/__init__.py",
          "openfst/pywrapfst.py",
          "openfst/extensions/__init__.py",
          "openfst/extensions/python/__init__.py",
      ) or (relative.parent.as_posix() == "openfst/extensions/python"
            and relative.name.startswith("pywrapfst")
            and relative.suffix == ".so"):
        files[str(relative)] = archive.read(entry)
  for subdir in ("lib", "export"):
    for path in (PACKAGE / subdir).glob("*.py"):
      if not path.name.endswith("_test.py") and "example" not in path.name:
        files[str(path.relative_to(ROOT))] = path.read_bytes()
  files["opengrm/pynini/pynini.pyi"] = (PACKAGE / "pynini.pyi").read_bytes()
  return files


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("archive", type=pathlib.Path)
  parser.add_argument("output", type=pathlib.Path)
  parser.add_argument("--sha", required=True)
  args = parser.parse_args()
  if not re.fullmatch(r"[0-9a-f]{40}", args.sha):
    parser.error("--sha must be a full Git commit hash")
  version = f"1.4.1.dev0+g{args.sha[:12]}"
  with zipfile.ZipFile(args.archive) as archive:
    files = package_files(archive)
  if "openfst/pywrapfst.py" not in files:
    raise RuntimeError("Bazel runfiles archive is missing openfst/pywrapfst.py")
  for directory, module in (
      ("openfst/extensions/python", "pywrapfst"),
      ("opengrm/pynini", "pynini"),
  ):
    if not any(path.startswith(f"{directory}/{module}") and path.endswith(".so")
               for path in files):
      raise RuntimeError(f"Bazel runfiles archive is missing {directory}/{module}*.so")
  python_tag = f"cp{sys.version_info.major}{sys.version_info.minor}"
  platform = sysconfig.get_platform().replace("-", "_").replace(".", "_")
  stem = f"opengrm_pynini-{version}-{python_tag}-{python_tag}-{platform}"
  dist_info = f"opengrm_pynini-{version}.dist-info"
  files[f"{dist_info}/METADATA"] = (
      "Metadata-Version: 2.3\n"
      "Name: opengrm-pynini\n"
      f"Version: {version}\n"
      "Summary: Bazel-built Pynini and OpenFst Python bindings\n"
      "Requires-Dist: absl-py\n"
  ).encode()
  files[f"{dist_info}/WHEEL"] = (
      "Wheel-Version: 1.0\n"
      "Generator: build_pynini_wheel.py\n"
      "Root-Is-Purelib: false\n"
      f"Tag: {python_tag}-{python_tag}-{platform}\n"
  ).encode()
  args.output.mkdir(parents=True, exist_ok=True)
  with WheelFile(args.output / f"{stem}.whl", "w") as wheel:
    for name, data in sorted(files.items()):
      wheel.writestr(name, data)


if __name__ == "__main__":
  main()
