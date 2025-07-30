from setuptools import setup, find_packages
setup(
  name = 'MetaRagTool',
  packages = find_packages(),
  version = '0.3.12',
  license='MIT',
  description = 'TYPE YOUR DESCRIPTION HERE',
  author = 'Ali Mobarekati',
  author_email = 'ali7919mb@yhaoo.com',
  url = 'https://github.com/user/ali7919',
  download_url = 'https://github.com/ali7919/MetaRAG/archive/refs/tags/v0.3.12.tar.gz',
  keywords = ['Ai', 'RAG', 'LLM'],
  install_requires=[
    'faiss-cpu',
    'hazm',
    'PyPDF2',
    'datasets>=3',
    'huggingface_hub',
    'gradio',
    'weave',

    # you can remove these and it will still work on google Colab
    'transformers',
    'sentence-transformers',
    'langchain-text-splitters',
    'matplotlib',
    'wandb==0.19.2',
    'google-genai',
    'openai',
    'tqdm',
    'nltk',
    'pandas',
    # 'numpy'

      ],
  classifiers=[
    'Development Status :: 3 - Alpha',

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)