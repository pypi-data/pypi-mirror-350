#!/usr/bin/env python3

import os
import hashlib
import argparse
from collections import defaultdict
from datetime import datetime
from send2trash import send2trash
import sys

def calculate_hash(path, hash_type='md5', buffer_size=65536):
    if hash_type == 'md5':
        hasher = hashlib.md5()
    elif hash_type == 'sha256':
        hasher = hashlib.sha256()
    else:
        raise ValueError(f"Хз что за хеш такой: {hash_type}")
    
    try:
        with open(path, 'rb') as f:
            while True:
                chunk = f.read(buffer_size)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except (IOError, OSError) as e:
        print(f"Чтение {path} сломалось: {e}")
        return None

def find_duplicates(directory, hash_type='md5', recursive=False):
    print(f"Шерстим директорию: {directory}")
    
    hashes = defaultdict(list)
    
    cnt = 0
    bad_files = 0
    
    if recursive:
        file_walker = os.walk(directory)
    else:
        all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        file_walker = [(directory, [], all_files)]
    
    for root, _, files in file_walker:
        for name in files:
            cnt += 1
            full_path = os.path.join(root, name)
            
            if os.path.islink(full_path):
                continue
                
            sys.stdout.write(f"\rПросмотрено файлов: {cnt}")
            sys.stdout.flush()
            
            digest = calculate_hash(full_path, hash_type)
            if digest:
                filesize = os.path.getsize(full_path)
                hashes[digest].append((full_path, filesize))
            else:
                bad_files += 1
    
    print(f"\nВсего проверили {cnt} файлов, с {bad_files} были проблемы")
    
    dupes = {}
    for digest, files in hashes.items():
        if len(files) > 1:
            dupes[digest] = files
    return dupes

def human_readable_size(bytes):
    units = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']
    i = 0
    size = float(bytes)
    while size >= 1024.0 and i < len(units) - 1:
        size /= 1024.0
        i += 1
    return f"{size:.1f} {units[i]}"

def handle_duplicates(dupes, interactive=True, trash=False, keep_newest=False):
    if not dupes:
        print("Ничего лишнего не найдено!")
        return
    
    print(f"\nНашли {len(dupes)} групп дубликатов:")
    
    freed_space = 0
    killed = 0
    
    group_num = 1
    for file_hash, file_list in dupes.items():
        file_list.sort(key=lambda x: x[1])
        filesize = file_list[0][1]
        
        print(f"\nГруппа {group_num}/{len(dupes)} (Хеш: {file_hash[:7]}...{file_hash[-7:]})")
        print(f"Весит: {human_readable_size(filesize)}")
        
        for idx, (fpath, _) in enumerate(file_list, 1):
            mtime = os.path.getmtime(fpath)
            print(f"  {idx}. {fpath} (изменен: {datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')})")
        
        killlist = []
        
        if interactive:
            while True:
                answer = input("\nЧто удалить? (номера через запятую, 's' чтобы пропустить, 'a' для удаления всех кроме первого): ")
                
                if answer.lower() == 's':
                    break
                elif answer.lower() == 'a':
                    killlist = list(range(2, len(file_list) + 1))
                    break
                else:
                    try:
                        nums = [int(x.strip()) for x in answer.split(',') if x.strip()]
                        if all(1 <= n <= len(file_list) for n in nums):
                            killlist = nums
                            break
                        else:
                            print(f"Эй, введи числа от 1 до {len(file_list)}")
                    except ValueError:
                        print("Не понял... Введи номера через запятую, 's' или 'a'")
        elif keep_newest:
            newest_idx = -1
            newest_time = -1
            
            for i, (f, _) in enumerate(file_list):
                mtime = os.path.getmtime(f)
                if mtime > newest_time:
                    newest_time = mtime
                    newest_idx = i
            
            killlist = []
            for i in range(len(file_list)):
                if i != newest_idx:
                    killlist.append(i+1)
        else:
            killlist = list(range(2, len(file_list) + 1))
        
        for idx in sorted(killlist, reverse=True):
            path = file_list[idx-1][0]
            try:
                if trash:
                    print(f"В корзину летит: {path}")
                    send2trash(path)
                    freed_space += filesize
                    killed += 1
                else:
                    print(f"Стираем с лица земли: {path}")
                    os.remove(path)
                    freed_space += filesize
                    killed += 1
            except Exception as e:
                print(f"Не вышло удалить {path}: {e}")
        
        group_num += 1
    
    print(f"\nПодчищено: {killed} файлов, освобождено {human_readable_size(freed_space)}")

def cli():
    parser = argparse.ArgumentParser(description="Поиск и удаление дубликатов файлов")
    parser.add_argument("directory", nargs='?', default=".", help="Директория для сканирования (по умолчанию: текущая)")
    parser.add_argument("-r", "--recursive", action="store_true", help="Рекурсивный поиск во всех поддиректориях")
    parser.add_argument("--hash", choices=["md5", "sha256"], default="md5", help="Алгоритм хеширования (по умолчанию: md5)")
    parser.add_argument("-y", "--yes", action="store_true", help="Неинтерактивный режим (автоматически удалять все дубликаты кроме первого)")
    parser.add_argument("--newest", action="store_true", help="Сохранять только самый новый файл из дубликатов (работает только с -y)")
    parser.add_argument("-t", "--trash", action="store_true", help="Перемещать файлы в корзину вместо безвозвратного удаления")
    
    args = parser.parse_args()
    
    folder = os.path.abspath(args.directory)
    
    if not os.path.exists(folder):
        print(f"Упс, директории {folder} не существует")
        return
    
    if not os.path.isdir(folder):
        print(f"Эй, {folder} - это не директория")
        return
    
    duplicates = find_duplicates(folder, args.hash, args.recursive)
    handle_duplicates(duplicates, interactive=not args.yes, trash=args.trash, keep_newest=args.newest)

def main():
    try:
        cli()
    except KeyboardInterrupt:
        print("\nОк-ок, завершаемся!")

if __name__ == "__main__":
    main() 