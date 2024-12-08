# AI4GOOD-AI-model

Este repositório contém o modelo de Inteligência Artificial desenvolvido para o programa AI4GOOD na Brazil Conference, com foco na predição de incêndios florestais. O objetivo é auxiliar na preservação ambiental e na mitigação de danos causados por incêndios, fornecendo uma ferramenta de análise preditiva. Projeto-84 BT-tracker.

## Como executar o projeto

Para rodar o projeto, siga os passos abaixo, mas antes, faça o unzip da pasta "dados":

1. **Criar um ambiente virtual** (opcional, mas recomendado)

   Crie um ambiente virtual para isolar as dependências do projeto. Isso pode ser feito com o seguinte comando:

   ```bash
   python -m venv venv
   ```

   Depois de criar o ambiente virtual, ative-o:

   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
   - No Linux/macOS:
     ```bash
     source venv/bin/activate
     ```

2. **Instalar as dependências**

   As bibliotecas necessárias estão listadas no arquivo `requirements.txt`. Para instalá-las, rode o comando:

   ```bash
   pip install -r requirements.txt
   ```

3. **Scripts para gerar a base de dados**

   Na pasta `main`, estão disponíveis alguns scripts que foram utilizados para gerar a base de dados. Os dados brutos foram retirados da base de dados do INPE sobre incêndios. Além disso, adicionamos dados do governo federal relativos a `numero_dias_sem_chuva` e `precipitacao`.

   Na pasta `helpers`, há um arquivo chamado `amazonia_legal.py`, que contém as referências dos paths dos arquivos de dados de cada estado.

   Também na pasta `helpers`, há um arquivo chamado `unzip_files.py`, que foi utilizado para descompactar todos os dados brutos provenientes da base de dados do INPE, que vieram zipados.

   Outro arquivo na pasta `helpers` é o `clear_folders.py`, que serviu para tirar os arquivos das pastas que foram criadas quando foi feito o unzip e mover para a pasta raiz do estado.

   Há também um arquivo chamado `clear_dirs.py` na pasta `helpers`, que serviu para entrar em cada pasta de cada estado e apagar o .zip remanescente e a pasta vazia de cada .csv que sobrou quando movemos os arquivos csv para o root.

4. **Treinamento dos modelos**

   Na pasta `main`, há um arquivo chamado `train.py`, onde foi realizado o treinamento dos modelos Logistic Regression, XGBoost e Random Forest.

5. **Resultados do treinamento**

   Na pasta `results`, foram salvos os resultados do treinamento, incluindo:

   - Planilhas com os resultados obtidos.
   - Imagens da matriz de confusão para cada modelo.
   - Os modelos treinados nos formatos `.onnx` e `.pkl`.

   Aguarde mais instruções sobre a descrição e execução de cada script.

## Sobre os dados

Os dados utilizados neste projeto incluem informações sobre incêndios florestais fornecidas pelo INPE, bem como dados meteorológicos, como número de dias sem chuva e precipitação. Essas informações são fundamentais para criar um modelo preditivo que ajude a identificar regiões de risco de incêndios.

## Objetivo

O objetivo deste projeto é desenvolver um modelo preditivo capaz de prever a ocorrência de incêndios florestais, contribuindo para a preservação ambiental. A ferramenta desenvolvida pode ser usada por órgãos de controle e prevenção de incêndios para tomar medidas preventivas e minimizar os impactos ambientais.

## Contribuindo

Se você deseja contribuir com o projeto, fique à vontade para abrir issues e enviar pull requests. Toda ajuda é bem-vinda!

## Licença

Livre


# Executando a API 

## Criar o banco de dados
Caso não tenha o arquivo local.db na pasta da api, procure o script init_db.py e execute-o

## Executar a API 
utilize o seguinte comando para executar a api em modo de desenvolvimento: 

```bash 
uvicorn main:app --reload

```
