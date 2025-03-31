#!/usr/bin/env bash

# Atualiza os pacotes e instala o espeak
apt-get update && apt-get install -y espeak

# Instala as dependências do Python
pip install -r requirements.txt
