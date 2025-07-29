from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='custom-json-serializer', 
    version='0.2.7', 
    packages=find_packages(where="."), 
    package_dir={"": "."}, 
    install_requires=[],  
    author='Ваше Имя',
    author_email='ваш.email@example.com',
    description='Пользовательский JSON сериализатор',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AlHudnitskii/custom_json_serializer',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)  