from pathlib import Path
import shutil
import sys
from file_parser import scan, JPEG_IMAGES, JPG_IMAGES, PNG_IMAGES, SVG_IMAGES, MP3_AUDIO, MY_OTHER, ARCHIVES
from normalize import normalize

def handle_media(file_name: Path, target_folder: Path):
    # Обробляємо медіа-файли: створюємо папку та перейменовуємо файл
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))

def handle_archive(file_name: Path, target_folder: Path):
    # Обробляємо архіви: розпаковуємо та організовуємо файли
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()

def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')
    for file in MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3_AUDIO')
    for file in MY_OTHER:
        handle_media(file, folder / 'MY_OTHER')

    for file in ARCHIVES:
        handle_archive(file, folder / 'ARCHIVES')

    for folder in FOLDERS[::-1]:
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')