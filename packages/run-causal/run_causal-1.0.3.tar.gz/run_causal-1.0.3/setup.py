from setuptools import setup, find_packages

setup(
    name="run_causal",
    version="1.0.3",
    packages=find_packages(),
    install_requires=["catboost==1.2.8","streamlit==1.45.1","numpy==2.2.6","pandas==2.2.3","matplotlib==3.10.3","scikit-learn==1.6.1","shap==0.47.2","scipy==1.15.3","statsmodels==0.14.4","xgboost==3.0.1"],
    entry_points={
        'console_scripts': [
            'run_causal=run_causal.app_launcher:main',
        ],
    },
    author="Aviral Srivastava",
    author_email="aviralsrivastava284@gmail.com",
    description="Get the causal forecast analysis",
    long_description_content_type='text/markdown',
    url="https://github.com/A284viral/run_causal",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)