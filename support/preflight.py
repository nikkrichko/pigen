import os
import pkg_resources
from typing import Iterable, List, Optional


def _load_requirements(requirements_file: str) -> List[str]:
    reqs: List[str] = []
    with open(requirements_file, 'r', encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith('#'):
                reqs.append(line)
    return reqs


def preflight_check(env_vars: Optional[Iterable[str]] = None,
                    requirements: Optional[Iterable[str]] = None,
                    requirements_file: str = 'requirements.txt') -> bool:
    """Verify environment variables and installed packages.

    Parameters
    ----------
    env_vars : Iterable[str], optional
        Names of required environment variables. Defaults to ['OPENAI_API_KEY'].
    requirements : Iterable[str], optional
        Explicit package requirement strings. If omitted, ``requirements_file``
        is read.
    requirements_file : str
        Path to the requirements file.

    Returns
    -------
    bool
        True if all checks pass.

    Raises
    ------
    EnvironmentError
        If an environment variable is missing.
    ImportError
        If a package is not installed or version conflicts.
    """
    env_vars = list(env_vars) if env_vars is not None else ['OPENAI_API_KEY']
    missing_env = [var for var in env_vars if not os.getenv(var)]
    if missing_env:
        raise EnvironmentError(f"Missing environment variables: {', '.join(missing_env)}")

    if requirements is None:
        requirements = _load_requirements(requirements_file)

    try:
        pkg_resources.require(list(requirements))
    except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict) as exc:
        msg = exc.args[0] if exc.args else str(type(exc))
        raise ImportError(msg) from exc

    return True


if __name__ == '__main__':
    try:
        preflight_check()
        print('[pigen] Preflight check successful.')
    except Exception as exc:  # pragma: no cover - direct script execution
        print(f'[pigen] Preflight check failed: {exc}')
        raise
