import json

def load_commands():
    """Tải các lệnh từ file JSON."""
    try:
        with open('commands.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"commands": {}}
    return data["commands"]

def save_commands(commands):
    """Lưu các lệnh đã cập nhật vào file JSON."""
    with open('commands.json', 'w', encoding='utf-8') as file:
        json.dump({"commands": commands}, file, ensure_ascii=False, indent=4)
