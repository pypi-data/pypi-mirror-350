from pathlib import Path
import shutil

def copy_py_files(src_dir, dst_dir):
    list_files = list(src_dir.glob('**/*.py')) + list(src_dir.glob('**/*.pyi'))
    for file in list_files:
        dst_file = dst_dir / file.relative_to(src_dir)
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        # print(f"Copying {file} to {dst_file}")
        shutil.copy(file, dst_file)

# Usage
src_dir = Path('.\iode')
dst_dir = Path('C:\soft\Miniconda3\Lib\site-packages\iode')
copy_py_files(src_dir, dst_dir)


# Remove each __pycache__ directory
def delete_pycache_directories():
    for pycache_directory in Path('.').glob('**/__pycache__'):
        print(f"deleting {pycache_directory}")
        shutil.rmtree(pycache_directory)
