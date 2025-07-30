#!/usr/bin/env python3
import os
import shutil
import argparse
import re
import json
import zipfile
import time
from pathlib import Path
from datetime import datetime

class ProjectCleaner:
    def __init__(self, directory='.', dry_run=False, verbose=False, ignore_patterns=None, 
                 json_output=False, backup=False):
        self.directory = os.path.abspath(directory)
        self.dry_run = dry_run
        self.verbose = verbose
        self.json_output = json_output
        self.backup = backup
        self.backup_path = os.path.join(self.directory, '.trash_backup.zip')
        self.total_removed = 0
        self.total_size = 0
        self.report_data = {
            'timestamp': datetime.now().isoformat(),
            'directory': self.directory,
            'dry_run': self.dry_run,
            'items': [],
            'stats': {
                'total_items': 0,
                'total_size_bytes': 0,
                'dirs_count': 0,
                'files_count': 0
            }
        }
        
        self.default_patterns = [
            r'venv$', r'env$', r'\.env$', r'\.venv$',
            r'\.pyc$', r'\.pyo$', r'__pycache__$', r'\.pytest_cache$',
            r'\.cache$', r'\.mypy_cache$', r'\.ruff_cache$', r'\.coverage$',
            r'\.log$', r'build$', r'dist$', r'\.egg-info$', r'\.eggs$',
            r'\.DS_Store$', r'Thumbs\.db$',
            r'~$', r'\.tmp$', r'\.temp$', r'\.swp$', r'\.swo$',
            r'node_modules$',
            r'\.o$', r'\.a$', r'\.so$', r'\.dll$',
        ]
        
        self.patterns = self.default_patterns
        if ignore_patterns:
            self.patterns = [p for p in self.patterns if p not in ignore_patterns]
            
        self.cleanignore_paths = []
        self._load_cleanignore()
        
        if self.backup and not self.dry_run:
            self.backup_zip = zipfile.ZipFile(self.backup_path, 'w', zipfile.ZIP_DEFLATED)
        else:
            self.backup_zip = None
    
    def _load_cleanignore(self):
        cleanignore_path = os.path.join(self.directory, '.cleanignore')
        if os.path.exists(cleanignore_path):
            with open(cleanignore_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        path = os.path.join(self.directory, line)
                        self.cleanignore_paths.append(os.path.abspath(path))
    
    def get_size_str(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
    
    def should_remove(self, path):
        abs_path = os.path.abspath(path)
        
        # Проверяем .cleanignore
        for ignore_path in self.cleanignore_paths:
            if abs_path.startswith(ignore_path) or abs_path == ignore_path:
                return False
        
        name = os.path.basename(path)
        for pattern in self.patterns:
            if re.search(pattern, name):
                return True
        return False
    
    def clean(self):
        start = time.time()
        if not self.json_output:
            print(f"🧹 Начинаю очистку проекта в {self.directory}")
            print(f"{'(Тестовый режим)' if self.dry_run else ''}")
        
        for root, dirs, files in os.walk(self.directory, topdown=True):
            for d in list(dirs):
                full_path = os.path.join(root, d)
                if self.should_remove(full_path):
                    self.remove_item(full_path, is_dir=True)
                    dirs.remove(d)
            
            for f in files:
                full_path = os.path.join(root, f)
                if self.should_remove(full_path):
                    self.remove_item(full_path, is_dir=False)
        
        if self.backup_zip:
            self.backup_zip.close()
            
        duration = time.time() - start
        
        self.report_data['stats']['total_items'] = self.total_removed
        self.report_data['stats']['total_size_bytes'] = self.total_size
        self.report_data['duration_seconds'] = duration
        
        if self.json_output:
            print(json.dumps(self.report_data, indent=2))
            return
            
        print(f"\n✨ Очистка завершена за {duration:.2f} сек")
        print(f"🗑️  Удалено: {self.total_removed} объектов ({self.get_size_str(self.total_size)})")
        
        if self.backup and not self.dry_run:
            print(f"📦 Создан бэкап: {self.backup_path}")
            
        if self.dry_run:
            print("\n⚠️  Это был тестовый режим, ничего на самом деле не удалено")
            print("   Запустите без --dry-run для реальной очистки")
    
    def remove_item(self, path, is_dir):
        rel_path = os.path.relpath(path, self.directory)
        
        try:
            size = 0
            if is_dir:
                if os.path.exists(path):
                    size = sum(f.stat().st_size for f in Path(path).glob('**/*') if f.is_file())
                    
                    if self.backup and not self.dry_run:
                        for root, _, files in os.walk(path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                archive_path = os.path.relpath(file_path, self.directory)
                                self.backup_zip.write(file_path, archive_path)
                                
                    if not self.dry_run:
                        shutil.rmtree(path)
                        
                    self.report_data['stats']['dirs_count'] += 1
            else:
                if os.path.exists(path):
                    size = os.path.getsize(path)
                    
                    if self.backup and not self.dry_run:
                        self.backup_zip.write(path, rel_path)
                        
                    if not self.dry_run:
                        os.remove(path)
                        
                    self.report_data['stats']['files_count'] += 1
            
            self.total_removed += 1
            self.total_size += size
            
            item_data = {
                'path': rel_path,
                'size_bytes': size,
                'is_dir': is_dir,
                'removed': not self.dry_run
            }
            self.report_data['items'].append(item_data)
            
            if self.verbose and not self.json_output:
                print(f"{'Нашел' if self.dry_run else 'Удалил'}: {rel_path} ({self.get_size_str(size)})")
            
        except Exception as e:
            error_msg = f"Ошибка при удалении {rel_path}: {str(e)}"
            if not self.json_output:
                print(error_msg)
            self.report_data.setdefault('errors', []).append(error_msg)


def main():
    parser = argparse.ArgumentParser(description='Очистка проекта от временных файлов и папок')
    parser.add_argument('directory', nargs='?', default='.', help='Директория проекта (по умолчанию: текущая)')
    parser.add_argument('--dry-run', action='store_true', help='Тестовый режим (без реального удаления)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Подробный вывод')
    parser.add_argument('--ignore', nargs='+', help='Паттерны, которые следует игнорировать')
    parser.add_argument('--json', action='store_true', help='Вывод отчета в JSON формате')
    parser.add_argument('--backup', action='store_true', help='Создать архив удаляемых файлов')
    
    args = parser.parse_args()
    
    cleaner = ProjectCleaner(
        directory=args.directory,
        dry_run=args.dry_run,
        verbose=args.verbose,
        ignore_patterns=args.ignore,
        json_output=args.json,
        backup=args.backup
    )
    cleaner.clean()


if __name__ == "__main__":
    main() 