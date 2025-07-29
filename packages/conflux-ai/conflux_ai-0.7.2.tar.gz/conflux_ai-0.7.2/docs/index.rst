.. Conflux documentation master file, created by
   sphinx-quickstart on Mon Oct  2 00:53:19 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Conflux's documentation!
====================================

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    getting-started
    base
    handlers
    retrieval
    examples_toc

Conflux
--------

A simple python library to conflux and build applications with Large Language Models.

Installation
------------

.. code-block:: bash

   pip install -U "interact @ git+https://github.com/pritam-dey3/Conflux.git"

or, if you use faiss for similarity search

.. code-block:: bash

    pip install -U "interact[faiss] @ git+https://github.com/pritam-dey3/Conflux.git"


Start learning about Conflux by reading the :doc:`getting-started` guide.

Why Conflux?
-------------

Applications with Large Language Models can get complex very quickly. You need more customizability and control over the prompts and their execution to satisfactorily build an application.

``Conflux`` was created with simplicity and scalability in mind. The core concepts of ``Message`` s, ``Handler`` s, and ``HandlerChain`` s are simple to understand and give *You* the power to build complex applications with ease.

More popular alternatives like ``langchain`` get frustrating to use when you want to customize either the process or the prompts according to your needs. ``Conflux`` gives you control while maintaining a very simple and intuitive API.

