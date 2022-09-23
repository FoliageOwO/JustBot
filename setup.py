from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

packages = find_packages(include=['jbot', 'jbot.*'])

setup(
    name='jbot',
    version='2.1.3a1',
    description='一个轻量的异步 QQ 机器人框架',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/WindLeaf233/JustBot',
    author='WindLeaf233',
    author_email='me@windleaf.ml',
    packages=find_packages(),
    install_requires=['rich>=12.5.1', 'websockets>=10.3', 'nest-asyncio>=1.5.5', 'aiohttp>=3.8.3',
                      'overrides>=6.2.0', 'jieba>=0.42.1'],
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Robot Framework',
        'Framework :: Robot Framework :: Library',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.8'
    ],
    keywords=['qqbot', 'cqhttp', 'mirai', 'bot']
)
