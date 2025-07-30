from setuptools import setup, find_packages

def read_requirements(file):
    with open(file, 'r') as f:
        return f.read().splitlines()
    
setup(
    name='ecq_llmfactory',  # Replace with your package name
    version='0.1.17',           # Initial release version
    description='LLMFactory is a modular framework built on LangChain, offering a factory-based approach for seamless integration and management of Large Language Models (LLMs) from multiple providers, ensuring flexibility, scalability, and maintainability.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Linh Vo',
    author_email='linh.vo@e-cq.net',
    url='https://kappa.e-cq.net/linh.vo/llmfactory',
    packages=find_packages(),
    install_requires=read_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Adjust based on your LICENSE
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
