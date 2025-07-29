import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crmark",
    version="0.1.1",
    author="chenoly",
    author_email="chenoly@outlook.com",
    description="A robust reversible watermarking method that can robustly extract the watermark in lossy channels and perfectly recover both the cover image and the watermark in lossless channels.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chenoly/crmark",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "torch>=1.10.0",
        "Pillow>=8.0.0",
        "lpips>=0.1.4",
        "bchlib>=2.1.3",
        "kornia>=0.6.0",
        "tqdm>=4.62.0",
        "requests>=2.32.3",
        "torchvision>=0.11.0",
        "scipy>=1.7.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "robust reversible watermarking",
    ],
    project_urls={
        "Bug Reports": "https://github.com/chenoly/crmark/issues",
        "Source": "https://github.com/chenoly/crmark",
        "Documentation": "https://crmark.readthedocs.io",
    },
)