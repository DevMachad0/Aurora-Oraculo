#!/usr/bin/env bash

# Atualiza os pacotes do sistema
apt-get update

# Instala o espeak e suas dependências
apt-get install -y espeak libespeak1 libespeak-dev

# Garante que a biblioteca libespeak esteja instalada
apt-get install -y libespeak1

# Instala as dependências do Python
pip install -r requirements.txt

# Verifica se a biblioteca libespeak está acessível
ldconfig
