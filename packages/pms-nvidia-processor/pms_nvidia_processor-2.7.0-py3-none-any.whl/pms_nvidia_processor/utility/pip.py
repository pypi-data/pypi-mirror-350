import subprocess
import tomllib  # Python 3.11+
import re
from pathlib import Path
from packaging.version import Version


def get_pip_list_from_poetry_lock(direcotry: str) -> list[str]:
    req_txt = subprocess.check_output(
        [
            "poetry",
            "export",
            "--direcotry",
            direcotry,
            "--without-hashes",
            "-f",
            "requirements.txt",
        ],
        text=True,
    )
    pip_packages = [
        line.strip()
        for line in req_txt.splitlines()
        if line.strip() and not line.startswith("#")
    ]
    return pip_packages


def _convert_caret_version(ver: str) -> str:
    try:
        v = Version(ver.strip("^"))
        if v.major > 0:
            return f">={v},<{v.major + 1}.0.0"
        else:
            return f">={v},<{v.major}.{v.minor + 1}.0"
    except Exception:
        return ver  # fallback


def _convert_tilde_version(ver: str) -> str:
    try:
        v = Version(ver.strip("~"))
        return f">={v},<{v.major}.{v.minor + 1}.0"
    except Exception:
        return ver


def _format_dependancy(pkg, ver):
    if isinstance(ver, str):
        ver = ver.strip()
        if ver in {"*", ""} or "*" in ver:
            return pkg
        elif ver.startswith("^"):
            return f"{pkg}{_convert_caret_version(ver)}"
        elif ver.startswith("~"):
            return f"{pkg}{_convert_tilde_version(ver)}"
        else:
            return f"{pkg}{ver}"
    else:
        return pkg  # 복잡한 경우 이름만


def get_pip_list_from_pyproject_toml(pyproject_path: str) -> list[str]:
    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    poetry_tool = pyproject.get("tool", {}).get("poetry", {})
    dependencies = poetry_tool.get("dependencies", {})

    # python 자체는 제외
    deps = [
        _format_dependancy(pkg, ver)
        for pkg, ver in dependencies.items()
        if pkg.lower() != "python"
    ]
    return deps
