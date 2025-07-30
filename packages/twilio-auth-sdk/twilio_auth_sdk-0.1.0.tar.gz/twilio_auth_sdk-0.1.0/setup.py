from setuptools import setup, find_packages

setup(
    name='twilio-auth-sdk',
    version='0.1.0',
    author='Titilayo Odufowoke',
    description='Send WhatsApp authentication messages using Twilio',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/teeteelaryo/twilio-auth-sdk',
    packages=find_packages(),
    install_requires=[
        'twilio',
        'python-dotenv'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.6',
)

