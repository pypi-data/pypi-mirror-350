from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="whispa_app",
    version="2.2.0",
    description="GUI for Whisper transcription & MarianMT translation",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Damilare Eniolabi",
    author_email="damilareeniolabi@gmail.com",
    url="https://github.com/damoojeje/whispa_app",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "whispa_app": [
            "assets/*.ico",
            "assets/*.png"
        ]
    },
    python_requires=">=3.10",
    install_requires=[
        "customtkinter>=5.1.1",
        "psutil>=5.9.0",
        "faster-whisper>=0.7.0",
        "transformers>=4.31.0",
        "huggingface-hub>=0.14.1",
        "sentencepiece>=0.1.97",
        "requests>=2.28.0",
        "sacremoses>=0.0.53",
        "torch>=2.0.1; sys_platform != 'win32'",
        "torch==2.0.1+cpu; sys_platform == 'win32'",
    ],
    entry_points={
        "console_scripts": [
            "whispa=whispa_app.run:main"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    keywords=[
        "whisper",
        "transcription",
        "translation",
        "GUI",
        "speech-to-text"
    ]
)