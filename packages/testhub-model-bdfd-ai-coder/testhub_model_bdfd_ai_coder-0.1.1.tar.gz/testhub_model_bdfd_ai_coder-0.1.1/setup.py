from setuptools import setup, find_packages

setup(
    name="testhub_model_bdfd_ai_coder",
    version="0.1.1",
    author="Tu Nombre",
    author_email="tuemail@example.com",
    description="A Python package for Testhub BDFD AI Coder API",
    packages=find_packages(),
    install_requires=[
        "requests",  # Aquí pones los módulos que tu paquete necesita
    ],
    python_requires=">=3.6",
)
