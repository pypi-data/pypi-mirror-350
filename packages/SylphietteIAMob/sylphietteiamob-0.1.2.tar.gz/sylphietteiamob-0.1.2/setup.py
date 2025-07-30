from setuptools import setup, find_packages

setup(
    name="SylphietteIAMob",  # Nome único no PyPI!
    version="0.1.2",
    author="__token__",
    author_email="seu@email.com",
    description="Assistente IA estilo Sylphiette com fala, VTube Studio e Gemini.",
    url="https://github.com/seuusuario/SylphietteIAMob",  # opcional
    packages=find_packages(),
    install_requires=[
        "pyttsx3",
        "google-generativeai",
        "websockets",
        "python-osc"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
