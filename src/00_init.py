"""
Etapa 0 del pipeline: SETUP DEL ENTORNO
------------------------------------------------------------
Una sola responsabilidad: dejar el entorno listo para correr el pipeline.

  Hace: - crea el entorno virtual en .venv/ si no existe
        - instala requirements.txt dentro de ese entorno

Se corre con el Python del sistema (aun no hay venv):

Ejecutar:  python src/00_init.py
"""

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR_VENV = RAIZ / ".venv"
REQUIREMENTS = RAIZ / "requirements.txt"


def python_del_venv():
    """Ruta al interprete dentro del venv, segun el sistema operativo."""
    if sys.platform == "win32":
        return DIR_VENV / "Scripts" / "python.exe"
    return DIR_VENV / "bin" / "python"


def main():
    if DIR_VENV.exists():
        print(f"[ok]         el entorno ya existe en {DIR_VENV}")
    else:
        print(f"[creando]    entorno virtual en {DIR_VENV}")
        subprocess.run([sys.executable, "-m", "venv", str(DIR_VENV)], check=True)

    print(f"[instalando] dependencias desde {REQUIREMENTS.name}")
    subprocess.run(
        [str(python_del_venv()), "-m", "pip", "install", "--upgrade", "pip"],
        check=True,
    )
    subprocess.run(
        [str(python_del_venv()), "-m", "pip", "install", "-r", str(REQUIREMENTS)],
        check=True,
    )

    print()
    print("[ok]         entorno listo. Ahora activa el venv y corre el pipeline:")
    if sys.platform == "win32":
        print("             .venv\\Scripts\\activate")
    else:
        print("             source .venv/bin/activate")
    print("             python src/run_pipeline.py")


main()
