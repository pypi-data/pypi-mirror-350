# Fundamentals of AI - Model

[![Pipeline status](https://github.com/Dar3cz3Q-University/FoAI-Model/actions/workflows/ci.yml/badge.svg)](https://github.com/Dar3cz3Q-University/FoAI-Model/tree/master)
[![Version](https://img.shields.io/endpoint?url=https%3A%2F%2Fdar3cz3q-university.github.io%2FFoAI-Model%2Fversion.json
)](https://github.com/Dar3cz3Q-University/FoAI-Model/tree/master)  
[![PyPI version](https://img.shields.io/pypi/v/foai_model)](https://pypi.org/project/foai_model/)
[![Python version](https://img.shields.io/pypi/pyversions/foai_model)](https://pypi.org/project/foai_model/)

---

## Installation

1. Clone repository
    ``` shell
    git clone git@github.com:Dar3cz3Q-University/FoAI-Model.git
    ```
2. Install dependencies
    ``` shell
    poetry install
    ```
3. Manually install torch
    * With CUDA
        ``` shell
        poetry run pip install torch==2.5.1+cu121 torchvision==0.20.1+cu121 --index-url https://download.pytorch.org/whl/cu121
        ```
    * Only CPU
         ``` shell
        poetry run pip install torch==2.6.0 torchvision==0.21.0
        ```
4. Train model
    ``` shell
    poetry run train
    ```

## Report

[View the report](https://dar3cz3q-university.github.io/FoAI-Model/)

## Related repositories

* [FoAI-Frontend](https://github.com/Dar3cz3Q-University/FoAI-Frontend)  
* [FoAI-Backend](https://github.com/Dar3cz3Q-University/FoAI-Backend)
