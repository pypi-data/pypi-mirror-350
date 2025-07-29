from setuptools import setup, find_packages
import os

# 动态库文件路径
dynamic_libraries = [
    'PieperKine/PieperKine.cpython-39-x86_64-linux-gnu.so',
    'PieperKine/PieperKine.cp39-win_amd64.pyd'
]

# 确保动态库文件存在
for library in dynamic_libraries:
    if not os.path.exists(library):
        raise FileNotFoundError(f"Required dynamic library '{library}' not found. Please ensure it exists in the directory.")

setup(
    name='PieperKine',
    version='1.0.2',
    packages=find_packages(),
    include_package_data=True,  # 启用 MANIFEST.in
    package_data={
        'PieperKine': [
            'PieperKine.cpython-39-x86_64-linux-gnu.so',
            'PieperKine.cp39-win_amd64.pyd'
        ]
    },
    install_requires=[
        'numpy',
        'scipy',
    ],
    python_requires='>=3.9',
    description='Inverse Kinematics Based on the Pieper Method',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Frank',
    url='https://github.com/Frank/PieperKine',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)