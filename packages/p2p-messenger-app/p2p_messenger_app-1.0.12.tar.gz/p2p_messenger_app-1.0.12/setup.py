from setuptools import setup, find_packages

setup(
    name="p2p_messenger_app",
    version="1.0.12",
    packages=find_packages(),
    py_modules=['node', 'client'],
    install_requires=[
        'cryptography==42.0.2',
        'pycryptodome==3.20.0',
        'psutil',
    ],
    entry_points={
        'console_scripts': [
            'p2p_messenger=node:main',
            'p2p_chat_client=client:main',
        ],
    },
    author="Alfonso Hernández González",
    author_email="alfonsohernandezgonzalez@gmail.com",
    description="Aplicación de mensajería P2P con salas de chat",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/alfonsohernandezgonzalez/p2p_messenger",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
        'p2p_messenger': ['*.py'],
    },
    include_package_data=True,
) 