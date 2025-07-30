import os
from setuptools import setup
from setuptools import find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(name='p1-queue',
      version='0.4.3',
      description='Messaging abstraction for AMQP',
      long_description=README,
      long_description_content_type='text/x-rst',
      author='Turfa Auliarachman',
      author_email='turfa_auliarachman@rocketmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'pika==1.3.2',
          'google-cloud-pubsub==2.19.0',
          'tornado==6.4',
      ],
      zip_safe=False,
      include_package_data=True,
      classifiers=[
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3'
      ])
