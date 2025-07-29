import os
import platform
import subprocess
import sys
from pathlib import Path
import json
import shutil

def create_config(path):
    path.mkdir(parents=True, exist_ok=True)
    config_file = path / "config.json"
    if not config_file.exists():
        json.dump({
            "host": "127.0.0.1",
            "port": 8765,
            "db_path": str(Path.home() / "PieDataDB")
        }, open(config_file, "w"), indent=4)
        print(f"Создан config.json по пути {config_file}")
    else:
        print(f"Файл конфигурации уже существует: {config_file}")
    return config_file

def install_linux():
    config_dir = Path.home() / ".PieDataServer"
    create_config(config_dir)

    systemd_dir = Path.home() / ".config/systemd/user"
    systemd_dir.mkdir(parents=True, exist_ok=True)
    service_file = systemd_dir / "piedataserver.service"

    service_file.write_text(f"""[Unit]
Description=PieData Server (WebSocket API)
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/env piedataserver
Restart=on-failure
WorkingDirectory=%h
Environment=HOME=%h

[Install]
WantedBy=default.target
""")
    print(f"Сервис установлен в {service_file}")
    subprocess.run(["systemctl", "--user", "daemon-reload"])
    subprocess.run(["systemctl", "--user", "enable", "--now", "piedataserver.service"])
    print("Сервис PieDataServer запущен.")

def install_windows():
    appdata = Path(os.getenv("APPDATA")) / "PieDataServer"
    create_config(appdata)

    python_exe = shutil.which("python") or shutil.which("python3")
    if not python_exe:
        print("❌ Python не найден в PATH.")
        sys.exit(1)

    bin_cmd = f'"{python_exe}" -m piedata.server'
    subprocess.run(
    f'sc create PieDataServer binPath= "{bin_cmd}" start= auto DisplayName= "PieData Server"',
    shell=True
)


    subprocess.run(["sc", "start", "PieDataServer"], shell=True)
    print("Служба PieDataServer зарегистрирована и запущена.")

def main():
    if platform.system() == "Windows":
        install_windows()
    elif platform.system() in {"Linux", "Darwin"}:
        install_linux()
    else:
        print("❌ Неподдерживаемая операционная система.")

if __name__ == "__main__":
    main()
