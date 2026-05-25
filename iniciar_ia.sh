#!/bin/bash
echo "Preparando o ambiente..."
cd ~/koboldcpp
# Removemos modelos pesados para economizar RAM
rm -f Meta-Llama-3-8B-Instruct-Q4_K_M.gguf
# Baixa o modelo TinyLlama (mais estável para celulares)
if [ ! -f tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf ]; then
    wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
fi
echo "Iniciando a Inteligência Artificial..."
python3 koboldcpp.py --model tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf --lowvram --threads 2 --skiplauncher
