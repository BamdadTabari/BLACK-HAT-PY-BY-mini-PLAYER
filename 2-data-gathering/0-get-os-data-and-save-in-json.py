import platform
import psutil
import json

def get_system_info():
    info = {
        'platform': platform.system(),
        'platform-release': platform.release(),
        'platform-version': platform.version(),
        'architecture': platform.machine(),
        'hostname': platform.node(),
        'processor': platform.processor(),
        'ram': f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
        'cpu_cores': psutil.cpu_count(logical=False),
        'disk_usage': f"{psutil.disk_usage('/').percent} %"
    }
    return info

def save_to_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    system_info = get_system_info()
    save_to_file("system_info.json", system_info)
    print(f"System information saved to system_info.json")