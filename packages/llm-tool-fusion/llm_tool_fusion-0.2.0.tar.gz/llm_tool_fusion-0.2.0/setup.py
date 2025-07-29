from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as arq:
    readme = arq.read()

setup(
    name='llm-tool-fusion',
    version='0.2.0',
    license='MIT',
    author='Caua ramos',
    author_email='cauamedinax@gmail.com',
    description=u'Biblioteca Python que simplifica e unifica a definição e chamada de ferramentas para grandes modelos de linguagem (LLMs). Compatível com Ollama, LangChain, OpenAI e outros frameworks.',
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords='llm tool fusion',
    packages=['llm_tool_fusion'],
    install_requires=[],
    url='https://github.com/caua1503/llm-tool-fusion',
)