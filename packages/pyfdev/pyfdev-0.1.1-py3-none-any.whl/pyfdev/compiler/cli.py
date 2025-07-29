import sys
import os
import subprocess
import platform
import argparse
from parser import parse
from transpiler import transpile

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
            print(f"Automatic TCC install not supported on {system}", file=sys.stderr)
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Failed to install TCC: {e}", file=sys.stderr)
        sys.exit(1)

def compile_and_run(c_code: str, base_name: str):
    c_file = base_name + ".c"
    exe_file = base_name + (".exe" if platform.system() == "Windows" else "")
    with open(c_file, "w") as f:
        f.write(c_code)

    subprocess.run(["tcc", c_file, "-o", exe_file], check=True)
    run_cmd = [exe_file] if platform.system() == "Windows" else [f"./{exe_file}"]
    result = subprocess.run(run_cmd, capture_output=True, text=True, check=True)
    print(result.stdout, end="")

def run_pyfast(file_path: str):
    with open(file_path, "r") as f:
        code = f.read()
    tokens = parse(code)
    c_code = transpile(tokens)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    compile_and_run(c_code, base_name)

def main():
    parser = argparse.ArgumentParser(prog="pyfdev")
    parser.add_argument(
        "--install-tcc",
        action="store_true",
        help="Detect OS and install Tiny C Compiler automatically"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to your .pf source file"
    )
    args = parser.parse_args()

    if args.install_tcc:
        install_tcc()
        print("TCC installation complete.")
        return

    if not args.file:
        parser.print_help()
        sys.exit(1)

    run_pyfast(args.file)

if __name__ == "__main__":
    main()
