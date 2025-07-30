from setuptools import setup, find_packages

setup(
    name="kaoutar-wissal_pyaral",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # Core dependencies
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        
        # Preprocessing
        "scikit-learn>=1.0.0",
        "imbalanced-learn>=0.9.0",
        "fancyimpute>=0.7.0",
        "category_encoders>=2.4.0",
        
        # Visualisation (optionnel)
        "matplotlib>=3.5.0",
        "seaborn>=0.11.2",
        
        # Utilitaires
        "tqdm>=4.64.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        'dev': [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "flake8>=4.0.0",
            "black>=22.0.0",
        ],
        'docs': [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ]
    },
    python_requires='>=3.8',
    author="Votre Nom",
    author_email="votre@email.com",
    description="Une bibliothèque complète de prétraitement de données",
    long_description="Bibliothèque Python pour le prétraitement automatisé de données (nettoyage, transformation, feature engineering, etc.)",  # Description textuelle simple
    long_description_content_type="text/plain",  # Type de contenu explicite
    url="https://github.com/votrecompte/preprocessor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)