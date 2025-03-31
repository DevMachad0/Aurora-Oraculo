#!/usr/bin/env bash

# Atualiza os pacotes do sistema
apt-get update

# Instala o espeak e suas dependências
apt-get install -y espeak libespeak1 libespeak-dev

# Instala a biblioteca libespeak necessária para o pyttsx3
apt-get install -y libespeak1

# Instala as dependências do Python
pip install -r requirements.txt
