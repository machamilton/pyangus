# PyAngus

## Name
PyAngus Portal Driver

## Description
Lib PyAngus para o Portal do Angus

## Installation
```
pip install -r requirements.txt
```
ou
```
pipenv install --dev
```

## Documentação
Para ver a doc completa do código rodar:
```
pdoc --docformat numpy pyangus
```
ou acessar :
```
./docs/
```

## Usage
```
pip install git+https://gitlab.com/fabricadenegocio/angusgdl/pyangus.git
```
```
from pyangus import AngusClient, AngusRPA
```
AngusClient:
```
token = ''
ang = AngusClient(token_collection=token, host="optional")
ang.info()
ang.query(filter_search="", offset=0, limit=10)
ang.ingest(dataframe)
```
**obs: o parametro filter_search em ang.query pode usar os operadores == != >= > < <= and or**

Para o modulo de RPA usar o decorator em cima da função de RPA com o nome da coleção no parâmetro collection_name ex:
```
@AngusRPA(token="asdtoken", host="optional")
def rpa():
    pass
```


## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## License
MIT License