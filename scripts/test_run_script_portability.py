#!/usr/bin/env python3
"""Regression checks for the portable app launcher."""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUN_SH = REPO_ROOT / "run.sh"
INSTALL_SH = REPO_ROOT / "install.sh"


def write_executable(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def make_launcher_fixture(with_venv: bool = True) -> tempfile.TemporaryDirectory[str]:
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    shutil.copy2(RUN_SH, root / "run.sh")

    (root / "ui").mkdir()
    (root / "ui" / "app.py").write_text("# fixture app\n", encoding="utf-8")
    (root / "fake-bin").mkdir()

    for command in ("lsof", "open", "ps"):
        write_executable(root / "fake-bin" / command, "#!/usr/bin/env sh\nexit 0\n")
    write_executable(root / "fake-bin" / "curl", "#!/usr/bin/env sh\nexit 0\n")
    write_executable(root / "fake-bin" / "pgrep", "#!/usr/bin/env sh\nexit 1\n")

    if not with_venv:
        return tmp

    (root / ".venv" / "bin").mkdir(parents=True)
    write_executable(
        root / ".venv" / "bin" / "activate",
        """#!/usr/bin/env sh
VIRTUAL_ENV="$PWD/.venv"
export VIRTUAL_ENV
PATH="$VIRTUAL_ENV/bin:$PATH"
export PATH
""",
    )
    write_executable(
        root / ".venv" / "bin" / "streamlit",
        """#!/usr/bin/env sh
echo "stale absolute streamlit wrapper invoked" >&2
exit 126
""",
    )
    write_executable(
        root / ".venv" / "bin" / "python",
        """#!/usr/bin/env sh
mkdir -p "$PWD/tmp"
printf '%s\n' "$@" > "$PWD/tmp/python-argv.txt"
if [ "$1" = "-m" ] && [ "$2" = "streamlit" ] && [ "$3" = "run" ] && [ "$4" = "ui/app.py" ]; then
  exit 0
fi
echo "unexpected python invocation: $*" >&2
exit 44
""",
    )

    return tmp


def run_launcher(root: Path, input_text: str = "") -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PATH"] = f"{root / 'fake-bin'}:{env['PATH']}"
    env["IDLE_HERO_TD_PORT"] = "18501"
    return subprocess.run(
        ["bash", "./run.sh"],
        cwd=root,
        env=env,
        input=input_text,
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )


def make_installer_fixture() -> tempfile.TemporaryDirectory[str]:
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    shutil.copy2(INSTALL_SH, root / "install.sh")
    (root / "requirements.txt").write_text("streamlit>=1.36\n", encoding="utf-8")
    (root / "requirements-ocr-optional.txt").write_text("easyocr\n", encoding="utf-8")
    (root / "fake-bin").mkdir()

    write_executable(
        root / "fake-bin" / "python3",
        """#!/usr/bin/env sh
mkdir -p tmp
printf '%s\n' "$@" >> tmp/python3-argv.txt
if [ "$1" = "-m" ] && [ "$2" = "venv" ] && [ "$3" = ".venv" ]; then
  mkdir -p .venv/bin
  cat > .venv/bin/activate <<'ACTIVATE'
#!/usr/bin/env sh
echo "stale installer activate was sourced" >&2
exit 99
ACTIVATE
  cat > .venv/bin/python <<'PYTHON'
#!/usr/bin/env sh
mkdir -p tmp
printf '%s\n' "$@" >> tmp/venv-python-argv.txt
if [ "$1" = "-m" ] && [ "$2" = "pip" ]; then
  exit 0
fi
echo "unexpected venv python invocation: $*" >&2
exit 44
PYTHON
  chmod +x .venv/bin/activate .venv/bin/python
  exit 0
fi
echo "unexpected python3 invocation: $*" >&2
exit 43
""",
    )
    return tmp


def run_installer(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PATH"] = f"{root / 'fake-bin'}:{env['PATH']}"
    return subprocess.run(
        ["bash", "./install.sh", *args],
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )


def start_detached_sleep() -> int:
    output = subprocess.check_output(["sh", "-c", "sleep 60 >/dev/null 2>&1 & echo $!"], text=True)
    return int(output.strip())


def process_exists(pid: int) -> bool:
    return (
        subprocess.run(
            ["kill", "-0", str(pid)],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode
        == 0
    )


def stop_process(pid: int) -> None:
    subprocess.run(["kill", "-TERM", str(pid)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def write_lsof_for_live_pid(root: Path, pid: int) -> None:
    write_executable(
        root / "fake-bin" / "lsof",
        f"""#!/usr/bin/env sh
if kill -0 {pid} 2>/dev/null; then
  echo {pid}
fi
""",
    )


def test_launcher_uses_relative_venv_python_module() -> None:
    fixture = make_launcher_fixture()
    try:
        root = Path(fixture.name)
        result = run_launcher(root)
        output = result.stdout + result.stderr
        assert result.returncode == 0, output

        argv = (root / "tmp" / "python-argv.txt").read_text(encoding="utf-8").splitlines()
        expected_prefix = ["-m", "streamlit", "run", "ui/app.py"]
        assert argv[:4] == expected_prefix, argv
        assert "--server.address" in argv, argv
        assert "--server.port" in argv, argv
        assert "--server.headless" in argv, argv
        assert "stale absolute streamlit wrapper invoked" not in output, output
    finally:
        fixture.cleanup()


def test_launcher_does_not_source_stale_activate() -> None:
    fixture = make_launcher_fixture()
    try:
        root = Path(fixture.name)
        write_executable(
            root / ".venv" / "bin" / "activate",
            """#!/usr/bin/env sh
echo "stale activate script was sourced" >&2
exit 99
""",
        )

        result = run_launcher(root)
        output = result.stdout + result.stderr
        assert result.returncode == 0, output
        assert "stale activate script was sourced" not in output, output
        assert (root / "tmp" / "python-argv.txt").exists()
    finally:
        fixture.cleanup()


def test_launcher_reports_missing_venv() -> None:
    fixture = make_launcher_fixture(with_venv=False)
    try:
        root = Path(fixture.name)
        result = run_launcher(root)
        output = result.stdout + result.stderr
        assert result.returncode == 1, output
        assert "Missing .venv. Run ./install.sh first." in output, output
    finally:
        fixture.cleanup()


def test_launcher_reports_missing_relative_python() -> None:
    fixture = make_launcher_fixture()
    try:
        root = Path(fixture.name)
        (root / ".venv" / "bin" / "python").unlink()

        result = run_launcher(root)
        output = result.stdout + result.stderr
        assert result.returncode == 1, output
        assert "Missing .venv/bin/python. Run ./install.sh first." in output, output
    finally:
        fixture.cleanup()


def test_launcher_declines_busy_port_kill_before_starting_python() -> None:
    fixture = make_launcher_fixture()
    pid = start_detached_sleep()
    try:
        root = Path(fixture.name)
        write_lsof_for_live_pid(root, pid)

        result = run_launcher(root, "n\n")
        output = result.stdout + result.stderr
        assert result.returncode == 1, output
        assert f"Porta 18501 ja esta em uso pelo(s) processo(s): {pid}" in output, output
        assert "Fechar esse(s) processo(s) e continuar? [s/N]" in output, output
        assert "Mantendo processo(s)." in output, output
        assert not (root / "tmp" / "python-argv.txt").exists()
        assert process_exists(pid)
    finally:
        stop_process(pid)
        fixture.cleanup()


def test_launcher_can_kill_confirmed_busy_port_process_and_continue() -> None:
    fixture = make_launcher_fixture()
    pid = start_detached_sleep()
    try:
        root = Path(fixture.name)
        write_lsof_for_live_pid(root, pid)

        result = run_launcher(root, "s\n")
        output = result.stdout + result.stderr
        assert result.returncode == 0, output
        assert f"Porta 18501 ja esta em uso pelo(s) processo(s): {pid}" in output, output
        assert "Fechar esse(s) processo(s) e continuar? [s/N]" in output, output
        assert (root / "tmp" / "python-argv.txt").exists()
        assert not process_exists(pid)
    finally:
        stop_process(pid)
        fixture.cleanup()


def test_installer_uses_relative_venv_python_without_activate() -> None:
    fixture = make_installer_fixture()
    try:
        root = Path(fixture.name)
        result = run_installer(root, "--with-easyocr")
        output = result.stdout + result.stderr
        assert result.returncode == 0, output
        assert "stale installer activate was sourced" not in output, output

        pip_calls = (root / "tmp" / "venv-python-argv.txt").read_text(encoding="utf-8")
        assert "-m\npip\ninstall\n--upgrade\npip\n" in pip_calls, pip_calls
        assert "-m\npip\ninstall\n-r\nrequirements.txt\n" in pip_calls, pip_calls
        assert "-m\npip\ninstall\n-r\nrequirements-ocr-optional.txt\n" in pip_calls, pip_calls
    finally:
        fixture.cleanup()


def main() -> int:
    test_launcher_uses_relative_venv_python_module()
    test_launcher_does_not_source_stale_activate()
    test_launcher_reports_missing_venv()
    test_launcher_reports_missing_relative_python()
    test_launcher_declines_busy_port_kill_before_starting_python()
    test_launcher_can_kill_confirmed_busy_port_process_and_continue()
    test_installer_uses_relative_venv_python_without_activate()
    print("shell script portability regression checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
