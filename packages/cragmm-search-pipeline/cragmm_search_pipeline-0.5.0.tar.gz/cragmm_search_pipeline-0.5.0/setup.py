from setuptools import find_packages, setup

setup(
    name="cragmm_search_pipeline",
    version="0.5.0",
    description="CragMM unified search pipeline for text and image",
    author="Haidar Khan",
    author_email="haidark@gmail.com",
    url="https://github.com/xiaoyangfb/crag-mm",
    packages=find_packages(),
    install_requires=[
        "transformers>=4.20.0",
        "pillow",
        "requests",
        "chroma-hnswlib>=0.7.6",
        "chromadb>=1.0.3",
        "bs4",
        "torch",
        "numpy",
        "tqdm",
        "huggingface_hub",
        "pillow",
        "pydantic",
        "requests",
        "lmdb>=1.6.2"
    ],
)
