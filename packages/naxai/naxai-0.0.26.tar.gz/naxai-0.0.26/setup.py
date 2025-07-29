from setuptools import setup, find_packages

setup(
    name='naxai',
    packages=find_packages(),
    description='Python sdk for Naxai\'s API',
    version='0.0.26',
    url='https://github.com/kevinRR2018/naxai-sdk-python',
    author='kevin',
    author_email='k.bertin@ringring.be',
    keywords=['voice','naxai','sdk', "sms", "email", "communication"],
    install_requires=['pydantic>=2.0',
                      'httpx'],
    )
