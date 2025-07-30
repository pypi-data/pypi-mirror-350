from setuptools import setup
from pathlib import Path

long_description = (Path(__file__).parent / 'README.md').read_text()

setup(
    name='lilliepy-dir-router',
    version='7.0.0',
    packages=['lilliepy_dir_router'],
    install_requires=[
        'reactpy',
        'reactpy-router',
        'asyncio',
        'flask',
        'flask_cors',
        'flask_sock',
        'markdown'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    description='File-based router for ReactPy or LilliePy framework',
    keywords=[
        "lilliepy", "lilliepy-dir-router", "reactpy", "router", 
        "file router", "file based router", "file-router", "file-based-router"
    ],
    url='https://github.com/websitedeb/lilliepy-dir-router',
    author='Sarthak Ghoshal',
    author_email='sarthak22.ghoshal@gmail.com',
    license='MIT',
    python_requires='>=3.6',
)
