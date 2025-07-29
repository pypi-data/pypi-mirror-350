from setuptools import setup, find_packages

setup(
    name="SAMIRTextEr",  
    version="1.1.1",
    author="Samir",
    author_email="schornograph@gmail.com",
    description="Ein Modul zur korrigierung von Deutschen Rechtschreibfehlern.",    
    packages=find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
