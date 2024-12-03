import setuptools

with open("README.md", "r", encoding="utf-8") as rm:
    long_description = rm.read()

setuptools.setup(
    name='llm-optimizer',
    version='1',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/avni-sixsense/image-handler-sdk',
    packages=['optimizer'],
    install_requires=['requests==2.32.0', 'environ==1.0'],
)