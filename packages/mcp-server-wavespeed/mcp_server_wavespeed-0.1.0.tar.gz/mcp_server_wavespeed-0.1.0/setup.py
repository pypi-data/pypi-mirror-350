from setuptools import setup, find_packages

setup(
    name='mcp-server-wavespeed',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pydantic',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'mcp-wavespeed=wavespeed.__main__:main'
        ]
    }
)