from setuptools import setup, find_packages

setup(
    name='binance-mcp-server',
    version='1.0.0',
    author='AnalyticAce (DOSSEH Shalom)',
    author_email='dossehdosseh14@gmail.com',
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AnalyticAce/binance-mcp-server',
    packages=find_packages(),
    keywords=['binance', 'mcp', 'server', 'fastmcp', 'crypto', 'trading', 'finance'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.6',
    install_requires=[
        'fastmcp>=2.5.1',
        'click>=8.2.1',
        'python-binance>=1.0.29',
    ],
    entry_points={
        'console_scripts': [
            'binance-mcp-server=binance_mcp_server.cli:app',
        ],
    }
)
