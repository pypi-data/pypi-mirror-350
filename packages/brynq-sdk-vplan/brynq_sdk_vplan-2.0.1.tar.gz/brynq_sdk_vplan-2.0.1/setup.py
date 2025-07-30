from setuptools import setup, find_namespace_packages

setup(
    name='brynq_sdk_vplan',
    version='2.0.1',
    description='vPlan wrapper from BrynQ',
    long_description='vPlan wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=find_namespace_packages(include=['brynq_sdk*']),
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=4,<5',
        'pandas>=2,<3'
    ],
    zip_safe=False,
)
