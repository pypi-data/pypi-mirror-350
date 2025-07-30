from setuptools import setup, find_packages

setup(
    name="converter_letra_numero",
    version="0.1.0",
    description="Converte letras (A–Z) em índices numéricos (0–25)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Seu Nome",
    author_email="seu.email@exemplo.com",
    url="https://github.com/davidsilcard/converter_letra_numero",  # sem .git
    license="MIT",
    packages=find_packages(exclude=["tests*", "docs*"]),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    project_urls={                  # <-- aqui
        "Documentation": "https://github.com/davidsilcard/converter_letra_numero#readme",
        "Source":        "https://github.com/davidsilcard/converter_letra_numero",
        "Tracker":       "https://github.com/davidsilcard/converter_letra_numero/issues",
    },
)
