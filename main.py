from pyangus.client.client import AngusClient
import argparse


if __name__ == '__main__':
    parametro = argparse.ArgumentParser(description="Parametros Client PyAngus")

    parametro.add_argument("--token", "-c", required=True, help="Token de Associação do Conjunto", type=str)
    parametro.add_argument("--mode", "-m", required=False, help="query, info, consulta_registros", type=str)
    parametro.add_argument("--filter_search", "-filter", required=False, help="Consulta no Conjunto de dados", type=str)
    parametro.add_argument("--offset", "-offset", required=False, help="Offset da Consulta", type=int)
    parametro.add_argument("--limit", "-limit", required=False, help="Limit da Consulta", type=int)
    parametro.add_argument("--id_conjunto", "-id", required=False, help="Id do Conjunto", type=str)
    parametro.add_argument("--output", "-o", required=False, help="Salvar como csv", type=str)
    par = vars(parametro.parse_args())

    token = par.get("token")
    mode = par.get("mode")
    filter_search = par.get("filter_search")
    offset = par.get("offset")
    limit = par.get("limit")
    id_conjunto = par.get("id_conjunto")
    output = par.get("output")

    client = AngusClient(token_collection=token)
    if mode == 'query':
        if filter_search is None:
            filter_search = ''
        df = client.query(
            filter_search=filter_search,
            offset=offset,
            limit=limit
        )
        print(df)
        if output is not None:
            df.to_csv(output, sep=';')
    elif mode == 'consulta_registros':
        df = client.consulta_registros(
            id_conjunto=id_conjunto
        )
        print(df)
        if output is not None:
            df.to_csv(output, sep=';')
    elif mode == 'info':
        df = client.info()
        print(df)
        if output is not None:
            df.to_csv(output, sep=';')
