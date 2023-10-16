from pathlib import Path

# Списки для різних категорій файлів
JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MP3_AUDIO = []
MY_OTHER = []
ARCHIVES = []

# Реєстр категорій для розподілу файлів
REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'MP3': MP3_AUDIO,
    'ZIP': ARCHIVES,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()

def get_extension(name: str) -> str:
    # Отримуємо розширення файлу
    return Path(name).suffix[1:].upper()

def scan(folder: Path):
    # Рекурсивно скануємо папку та розподіляємо файли
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue

        extension = get_extension(item.name)
        full_name = folder / item.name
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:
                REGISTER_EXTENSION[extension]
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)
                MY_OTHER.append(full_name)