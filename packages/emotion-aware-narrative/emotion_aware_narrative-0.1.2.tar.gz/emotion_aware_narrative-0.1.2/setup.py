from setuptools import setup, find_packages

setup(
    name="emotion-aware-narrative",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "numpy>=1.21.0",
    ],
    author="Sanjana Robbi",
    author_email="sanjanarobbi123@gmail.com",
    description="An AI-powered emotion detection system for game narrative enhancement",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sanjthebest/Emotion-Aware-Narrative-Engine",
    license="MIT",
    license_files=(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    keywords="emotion, nlp, game-development, ai, narrative",
    project_urls={
        "Bug Reports": "https://github.com/sanjthebest/Emotion-Aware-Narrative-Engine/issues",
        "Source": "https://github.com/sanjthebest/Emotion-Aware-Narrative-Engine",
    },
    include_package_data=True,
) 