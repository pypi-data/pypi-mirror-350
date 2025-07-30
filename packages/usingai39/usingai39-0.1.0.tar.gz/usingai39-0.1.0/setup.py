from setuptools import setup, find_packages

setup(
    name='usingai39',
    version='0.1.0',
    author='Sang hyuck Won',
    author_email='yhnujk@naver.com',
    description='A collection of AI-powered tools for games and apps.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yhnujk/ai_tools_project.git',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='==3.9.*',
    install_requires=[
        'Pillow>=9.0.0,<10.0.0',
        'requests>=2.20.0,<3.0.0',
        'openai>=1.0.0,<1.23.0',
        'google-generativeai>=0.2.0,<0.3.2',
        'python-dotenv>=0.20.0,<1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'usingai = ai_tools.main:main'
        ],
    },
)
