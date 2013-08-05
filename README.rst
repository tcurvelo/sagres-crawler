
Primeiro instale as dependências:

    pip install -r requirements.txt


Rodando:

    PYTHONIOENCODING=UTF-8 python servidores_pb.py >> servidores.csv


O sagres fecha sua conexão depois de alguns requests. O crawler 
reinicia da mesma entidade gestora, mas acaba gerando algumas linhas 
repetidas. Nesse caso, recomendo ao final remover linhas iguais:

    sort -u < servidores.csv > servidores_u.csv


OBS.: O ano e o mês de referência estão fixos no código.
