from setuptools import setup

setup(
    name="cp32",
    version="1.0.0",    
    py_modules=["cp32"], 
    author="wew1234GD",
    author_email="candyfoxowo28@gmail.com",
    description="simple cipher",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/wew1234GD/32BitCipher",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
