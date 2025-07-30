from setuptools import setup, find_packages

setup(
    name="cinder-ml",
    version="1.0.5",
    description="ML model debugging and analysis dashboard",
    author="Rahul Thennarasu",
    author_email="rahulthennarasu07@gmail.com",
    url="https://github.com/RahulThennarasu/cinder",
    packages=find_packages(include=['cinder', 'backend', 'backend.*']),  # Include backend and subpackages
    include_package_data=True,
    package_data={
        'backend.app': ['static/*', 'static/**/*'],
        'backend': ['.env'],
    },
    install_requires=[
        "fastapi>=0.95.0",
        "uvicorn>=0.21.0",
        "numpy>=1.23.0",
        "scikit-learn>=1.0.0",
        "matplotlib>=3.5.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "pytorch": ["torch>=1.12.0"],
        "tensorflow": ["tensorflow>=2.8.0"],
        "all": [
            "torch>=1.12.0",
            "tensorflow>=2.8.0",
            "google-generativeai>=0.3.0",
        ],
    },
    entry_points={
        'console_scripts': [
            'cinder=cinder.cli:main',
        ],
    },
    python_requires=">=3.8",
)