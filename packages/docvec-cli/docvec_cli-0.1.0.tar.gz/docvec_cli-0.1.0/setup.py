import os
from setuptools import setup, find_packages

current_directory = os.path.dirname(__file__)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def read_requirements():
    requirements_path = os.path.join(current_directory, "requirements.txt")
    with open(requirements_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="docvec-cli",
    version="0.1.0",
    author="Onur Baran",
    author_email="baranonur@gmail.com",
    description="DocVec CLI is a powerful command-line tool designed to transform your unstructured local documents (PDF, DOCX, TXT) into query-ready vector embeddings, making them instantly usable for Large Language Models (LLMs) and bolstering Retrieval Augmented Generation (RAG) workflows.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/onurbaran/docvec-cli",
    package_dir={'docvec_cli': 'src'},
    packages=['docvec_cli'],
    #packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    python_requires='>=3.8',
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'docvec=docvec_cli.main:main',
        ],
    },
)