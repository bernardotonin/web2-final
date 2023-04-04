# Pyweb
Funcionalidades implementadas:
- CRUD Cliente
- CRUD Produto

## Opção 1: 

Baixar e instalar projeto do início:

```bash
# escolha uma pasta onde abrir o terminal
# por exemplo na pasta /home/ifpr/dev
cd ~/dev

git clone https://github.com/fscheidt/web2-22.git

cd web2-22/codigos/pyweb

python3 -m venv env --without-pip --system-site-packages

source env/bin/activate

pip install Flask

code .

```

## Opção 2 💥

Caso você já possua o projeto configurado na máquina.

❗❗❗

🔥 Atenção: Esse comando vai <u>**apagar** qualquer mudança no seu código</u> e substituirá pelo código que está no github. Faça uma cópia do seu projeto antes. 

❗❗❗

```bash
# abrir o terminal na pasta raiz do git
# cd <local onde salvou>/web2-22

git fetch
git reset --hard origin/master

cd codigos/pyweb

source env/bin/activate

code .

```