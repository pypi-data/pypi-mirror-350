from setuptools import setup, find_packages
import byzh_rc
setup(
    name='byzh_rc',
    version=byzh_rc.__version__,
    author="byzh_rc",
    description="更方便的深度学习",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'wcwidth',
        'thop',
        'matplotlib',
        'seaborn',
    ],
)
