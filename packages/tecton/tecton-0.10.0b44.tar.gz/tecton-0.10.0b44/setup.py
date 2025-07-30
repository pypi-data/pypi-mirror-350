import codecs
import os.path
import pathlib

import setuptools
import tomlkit


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    path = pathlib.Path(rel_path).resolve()
    if path.exists():
        for line in read(rel_path).splitlines():
            if line.startswith("VERSION"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
        exc = RuntimeError("Unable to find version string.")
        raise exc
    else:
        # NOTE: we use `99.99.99.dev` here instead of raising an exception, since
        # pip-tools executes this file as part of dependency resolution. And our
        # version file isn't available nor necessary for it.
        return "99.99.99.dev"


def add_rift_extension_package(sdk_version):
    # There is no SDK version "99.99.99" in PyPI.
    # For SDK "99.99.99", we use extensions in repo (external_repos/duckdb/bin) for local test,
    # or download the latest from S3 in m13n job
    if sdk_version.startswith("99.99.99"):
        return

    base_dir = pathlib.Path(__file__).resolve().parent
    pyproject_toml = base_dir / "./pyproject.toml"

    with open(pyproject_toml, "r") as f:
        config = tomlkit.load(f)

    rift_extension_package = f"tecton-rift-extensions=={sdk_version}"
    for rift_extra in ["rift", "rift-materialization"]:
        config["project"]["optional-dependencies"][rift_extra].append(rift_extension_package)

    with open(pyproject_toml, "w") as f:
        tomlkit.dump(config, f)


sdk_version = get_version("tecton/_gen_version.py")

add_rift_extension_package(sdk_version)
setuptools.setup(version=sdk_version)
