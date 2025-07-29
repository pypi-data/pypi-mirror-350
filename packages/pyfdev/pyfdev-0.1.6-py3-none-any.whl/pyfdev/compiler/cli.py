import sys
import os
import subprocess
import platform
import argparse
import tempfile
from pyfdev.compiler.parser import parse
from pyfdev.compiler.transpiler import transpile


def install_tcc():
    system = platform.system()
    try:
        if system == "Linux":
            subprocess.check_call(["sudo", "apt-get", "update"])
            subprocess.check_call(["sudo", "apt-get", "install", "-y", "tcc"])
        elif system == "Darwin":
            subprocess.check_call(["brew", "install", "tcc"])
        elif system == "Windows":
            subprocess.check_call(["choco", "install", "tcc", "-y"])
        else:
            print(f"  Automatic TCC install not supported on {system}", file=sys.stderr)
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"  Failed to install TCC: {e}", file=sys.stderr)
        sys.exit(1)

def compile_and_run(c_code: str, base_name: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        c_file = os.path.join(tmpdir, base_name + ".c")
        exe_file = os.path.join(tmpdir, base_name + (".exe" if platform.system() == "Windows" else ""))

        # Write C code to temporary .c file
        with open(c_file, "w") as f:
            f.write(c_code)

        # Compile using TCC
        try:
            subprocess.run(["tcc", c_file, "-o", exe_file], check=True)
        except FileNotFoundError:
            print("  TCC compiler not found. Run with --install-tcc or install manually.", file=sys.stderr)
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"  Compilation failed: {e}", file=sys.stderr)
            sys.exit(1)

        # Execute the binary
        run_cmd = [exe_file] if platform.system() == "Windows" else [exe_file]
        try:
            result = subprocess.run(run_cmd, capture_output=True, text=True, check=True)
            print(result.stdout, end="")
        except subprocess.CalledProcessError as e:
            print(f" Runtime error: {e}", file=sys.stderr)
            sys.exit(1)


def run_pyfast(file_path: str):
    if not os.path.exists(file_path):
        print(f" File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    with open(file_path, "r") as f:
        code = f.read()

    try:
        tokens = parse(code)
        c_code = transpile(tokens)
    except Exception as e:
        print(f" Error during parsing/transpilation: {e}", file=sys.stderr)
        sys.exit(1)

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    compile_and_run(c_code, base_name)

def main():
    arg_parser = argparse.ArgumentParser(
        prog="pyfdev",
        description="PyFast Dev - Transpile and execute .pf code to native C"
    )
    arg_parser.add_argument(
        "--install-tcc",
        action="store_true",
        help="Detect OS and install Tiny C Compiler automatically"
    )
    arg_parser.add_argument(
        "file",
        nargs="?",
        help="Path to your .pf source file"
    )
    arg_parser.add_argument(
        "-v", "--version",
        action="version",
        version="pyfdev 0.1.2"
    )

    args = arg_parser.parse_args()

    if args.install_tcc:
        install_tcc()
        print("TCC installation complete.")
        return

    if not args.file:
        arg_parser.print_help()
        sys.exit(1)

    run_pyfast(args.file)

if __name__ == "__main__":
    main()
