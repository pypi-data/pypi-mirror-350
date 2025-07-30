from setuptools import setup, find_packages

setup(
    name='alpamyslinalg',  
    version='0.1.1',
    description='Линейная алгебра: матрицы, СЛАУ и т.д.',
    author='Алпамыс',
    author_email='useralser90@gmail.com',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
