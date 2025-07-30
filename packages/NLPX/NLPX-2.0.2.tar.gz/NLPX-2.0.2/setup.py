import os
from setuptools import setup


# INSTALL_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()
def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path), 'r', encoding='UTF-8') as fp:
        return fp.read()


long_description = read("README.rst")


setup(
    name='NLPX',
    packages=['nlpx', 'nlpx.model', 'nlpx.dataset', 'nlpx.tokenize'],
    description="A tool set for NLP. Text classification. Trainer. Tokenizer",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='2.0.2',
    install_requires=[
        "xtokenizer>=0.0.4",
        "model-wrapper>=1.0.7",
        "torch-model-hub>=0.1.9",
    ],
    url='https://gitee.com/summry/nlpx',
    author='summy',
    author_email='fkfkfk2024@2925.com',
    keywords=['NLP', 'nlp', 'AI', 'llm', 'GPT', 'Machine learning', 'Deep learning', 'tokenize', 'torch'],
    package_data={
        # include json and txt files
        '': ['*.rst', '*.dtd', '*.tpl'],
    },
    include_package_data=True,
    python_requires='>=3.6',
    zip_safe=False
)
