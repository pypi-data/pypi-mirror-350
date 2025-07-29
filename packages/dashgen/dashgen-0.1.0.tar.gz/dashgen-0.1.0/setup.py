from setuptools import setup, find_packages

setup(
    name="dashgen",
    version="0.1.0",
    author="Vinicius Moreira",
    author_email="vinicius@77indicadores.com.br",
    description="Gere dashboards visuais como imagens usando HTML/CSS e Playwright.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/77-Indicadores/dashgen",  # opcional
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "playwright",
        "jinja2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7",
)
