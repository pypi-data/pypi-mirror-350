from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='segmentation_assessment', # name of packe which will be package dir below project
    version='0.9.7',
    #url='https://github.com/yourname/yourproject',
    author='Gregoire Menard',
    author_email='gregoire.menard.72@hotmail.fr',
    description='Assessment of the segmentation quality',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={"console_scripts":["assessment_with_ground_truth=segmentation_assessment:assessment_with_ground_truth","assessment_without_ground_truth=segmentation_assessment:assessment_without_ground_truth"]},
    packages=find_packages(), #auto_discover packages
    install_requires=[],
)
