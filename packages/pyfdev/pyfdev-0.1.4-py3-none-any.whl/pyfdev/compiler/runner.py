import subprocess
import os

def compile_and_run(c_code: str, output_name="out"):
    with open(f"{output_name}.c", "w") as f:
        f.write(c_code)

    subprocess.run(["tcc", f"{output_name}.c", "-o", f"{output_name}.exe"], check=True)
    subprocess.run([f"{output_name}.exe"], check=True)
