from setuptools import setup, find_packages

setup(
    name='blackspammerbd-weblab',
    version='0.0.0',
    description='Most Powerful & Professional Web Security Tool - 2025 by BLACK SPAMMER BD',
    author='BLACK SPAMMER BD',
    author_email='shawponsp6@gmail.com',
    url='https://github.com/BlackSpammerBd/blackspammerbd-weblab',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=2.25',
        'beautifulsoup4>=4.9',
        'termcolor>=1.1',
        'urllib3>=1.26',
        'colorama>=0.4',
        'tqdm>=4.60',
        'lxml>=4.6'
    ],
    entry_points={
        'console_scripts': [
            'black-e=blackspammerbd_weblab.link_extractor:main',
            'black-c=blackspammerbd_weblab.check_sql:main',
            'black-a=blackspammerbd_weblab.admin_finder:main',
            'black-brute=blackspammerbd_weblab.brute_force:main',
            'black-bypass=blackspammerbd_weblab.admin_bypass:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
