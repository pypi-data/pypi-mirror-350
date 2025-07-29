from setuptools import setup, find_packages

setup(
    name='technical-analysis-mcp',
    version='0.2.1',
    packages=find_packages(),
    install_requires=[
        "mcp>=1.0.0",
        "akshare",
        "pandas",
        "fastapi"
    ],
    author='Li Bin',
    author_email='binlish81@qq.com',
    description='Technical analysis tools for investment advisory',
    entry_points={
        'console_scripts': [
            'technical-analysis-mcp=technical_analysis.main:main',
            'technical-analysis-http=technical_analysis.http:app'
        ]
    }
)