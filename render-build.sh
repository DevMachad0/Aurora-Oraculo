#!/usr/bin/env bash

# Atualiza os pacotes do sistema
apt-get update

# Instala o espeak e suas dependências
apt-get install -y espeak libespeak1 libespeak-dev

# Verifica se a biblioteca libespeak.so.1 está instalada
if [ ! -f /usr/lib/x86_64-linux-gnu/libespeak.so.1 ]; then
    echo "Erro: libespeak.so.1 não encontrada. Verifique a instalação do espeak."
    exit 1
fi

# Instala as dependências do Python
pip install -r requirements.txt
