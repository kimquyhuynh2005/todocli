from setuptools import setup, find_packages

setup(
    name="todo_cli_hkq",
    version="1.0.0",
    packages=find_packages(), # Tự động tìm thư mục src
    install_requires=[
        "rich",               # Tự động cài rich nếu máy chưa có
    ],
    entry_points={
        'console_scripts': [
            # Cú pháp: tên_lệnh_ngắn = đường_dẫn_đến_hàm
            'todo = src.main:main', 
        ],
    },
)