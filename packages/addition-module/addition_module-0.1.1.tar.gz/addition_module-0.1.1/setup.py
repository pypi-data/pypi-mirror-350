from setuptools import setup

# Read the contents of README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='addition_module',
    version='0.1.1',
    packages=['addition_module'],
    package_data={
        'addition_module': [
            'obfuscated/*.py',
            'obfuscated/pyarmor_runtime_000000/*',
        ],
    },
    include_package_data=True,
    install_requires=[],
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple addition module with obfuscated code',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/addition_module',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',
)
