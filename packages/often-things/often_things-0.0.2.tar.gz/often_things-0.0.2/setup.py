from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='often_things',
  version='0.0.2',
  author='Sebby_child_developer',
  author_email='sebbyrogers20@gmail.com',
  description="This is the module helping you to avoid writing same code many times.",
  packages=find_packages(),
  install_requires=['arcade==2.6.17'],
  python_requires='>=3.6'
)
