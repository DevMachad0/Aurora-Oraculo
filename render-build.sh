#!/usr/bin/env bash

# Atualiza os pacotes do sistema
apt-get update

# Instala o espeak e suas dependências
apt-get install -y espeak libespeak1 libespeak-dev

# Instala as dependências do Python
pip install -r requirements.txt
