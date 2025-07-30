from setuptools import setup, find_packages

setup(
    name='django-tailwind-template',
    version='0.1.0',
    author='Kiran Sindagi',
    author_email='kiransindagi1@gmail.com',
    description='A custom Django project template with Tailwind CSS',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/django-tailwind-template',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        'django',
    ],
)
