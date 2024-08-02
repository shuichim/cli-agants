from setuptools import setup, find_packages

setup(
    name='cli-agents',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'openai',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'cli-agents=cli_agents.cli:cli',
        ],
    },
)
