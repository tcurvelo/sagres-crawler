Crawler para gerar lista de servidores municipais da Paraíba a partir 
do `SAGRES <http://sagres.tce.pb.gov.br/>`_

Primeiro instale as dependências:

    pip install -r requirements.txt


Rodando:

    python servidores_pb.py >> servidores.csv


O sagres fecha sua conexão depois de alguns requests. O crawler
reinicia da mesma entidade gestora, mas acaba gerando algumas linhas
repetidas. Nesse caso, recomendo ao final remover linhas iguais:

    sort -u < servidores.csv > servidores_u.csv


OBS.: O ano e o mês de referência estão fixos no código.
