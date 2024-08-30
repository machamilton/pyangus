import pandas
import requests
import pandas as pd
from pyangus.exceptions.client_exception import AngusClientException
from pyangus.exceptions.ingest_exception import AngusIngestException


def _request_angus(method, *args, **kwargs):
    response = requests.request(
        method=method,
        *args,
        **kwargs
    )
    try:
        response_body = response.json()
        if type(response_body) == dict and \
                not(response.status_code == 200 or response.status_code == 201) and \
                len(list(response_body.keys())) == 1 and list(response_body.keys())[0] == 'Mensagem':
            raise AngusClientException(response_body['Mensagem'])
        elif not(response.status_code == 200 or response.status_code == 201):
            raise AngusClientException(response_body)
        return response_body
    except:
        if not(response.status_code == 200 or response.status_code == 201):
            raise AngusClientException(f"Erro {response.status_code}")
        else:
            raise AngusClientException("Erro 500")


def _get_data_angus(*args, **kwargs):
    return _request_angus('GET', *args, **kwargs)


def _send_data_angus(*args, **kwargs):
    return _request_angus('POST', *args, **kwargs)


def _query_select_convert(filter_search):
    array_filter = filter_search.strip().split(" ")
    array_filter_conv = list()
    for index_filter in range(len(array_filter)):
        if array_filter[index_filter] in ["and", "or"]:
            if array_filter[index_filter] == "and":
                array_filter_conv.append("and")
            elif array_filter[index_filter] == "or":
                array_filter_conv.append("or")
        elif array_filter[index_filter] in [">", "<", ">=", "<=", "==", "!="]:
            if array_filter[index_filter] == ">":
                array_filter_conv.append((array_filter[index_filter-1] + "[gt]", array_filter[index_filter + 1]))
            elif array_filter[index_filter] == "<":
                array_filter_conv.append((array_filter[index_filter-1] + "[lt]", array_filter[index_filter + 1]))
            elif array_filter[index_filter] == ">=":
                array_filter_conv.append((array_filter[index_filter-1] + "[gte]", array_filter[index_filter + 1]))
            elif array_filter[index_filter] == "<=":
                array_filter_conv.append((array_filter[index_filter-1] + "[lte]", array_filter[index_filter + 1]))
            elif array_filter[index_filter] == "==":
                array_filter_conv.append((array_filter[index_filter-1] + "[eq]", array_filter[index_filter + 1]))
            elif array_filter[index_filter] == "!=":
                array_filter_conv.append((array_filter[index_filter-1] + "[neq]", array_filter[index_filter + 1]))

    return array_filter_conv


class AngusClient:
    """
    Client para Conexão no Angus Data Lake
    """
    def __init__(self, token_collection, **kwargs):
        """
        Parameters
        ----------
        token_collection: str
            Token de Associação do Conjunto de Dados
        """
        host = kwargs.get("host")
        if host is not None:
            self._host = host
        else:
            self._host = 'https://dados.noctua.sds.pe.gov.br/api/'
        self._token = token_collection

    def query(self, filter_search="", offset=None, limit=None) -> pandas.DataFrame:
        """
        Parameters
        ----------
        filter_search: str
            Filtro da consulta no Portal
        offset: int
            Offset da consulta no Portal
        limit:
            Limit da consulta no Portal

        Returns
        -------
        pandas.DataFrame
            Pandas DataFrame da consulta do conjunto de dados no Portal

        Raises
        ------
        AngusClientException
            Caso de acontecer algum erro de conexão com o Portal
        """
        headers = {"Authorization": self._token}
        params = dict()
        response_body = list()

        if offset is not None:
            headers["offset"] = offset
        if limit is not None:
            headers["limit"] = limit

        if len(str(filter_search)) > 0:
            array_filter = _query_select_convert(filter_search)
            for search in array_filter:
                if type(search) == tuple:
                    params[search[0]] = search[1]
                elif type(search) == str:
                    if search == 'and':
                        continue
                    elif search == 'or':
                        response_body += _get_data_angus(
                            url=self._host + "buscar",
                            params=params,
                            headers=headers
                        )
                        params.clear()

            if len(params) > 0:
                response_body += _get_data_angus(
                    url=self._host + "buscar",
                    params=params,
                    headers=headers
                )
        else:
            response_body += _get_data_angus(
                url=self._host + "buscar",
                headers=headers
            )

        return pd.DataFrame(response_body)

    def info(self) -> pandas.DataFrame:
        """
        Returns
        -------
        pandas.DataFrame
            Pandas DataFrame das info do conjunto de dados

        Raises
        ------
        AngusClientException
            Caso de acontecer algum erro de conexão com o Portal
        """
        response_body = _get_data_angus(
            url=self._host + "info",
            headers={"Authorization": self._token}
        )
        return pd.DataFrame.from_dict(response_body, orient='index')

    def consulta_registros(self, id_conjunto) -> pandas.DataFrame:
        """
        Parameters
        ----------
        id_conjunto: str
            Id do conjunto de dados

        Returns
        -------
        pandas.DataFrame
            Pandas DataFrame da consulta de registros do conjunto de dados

        Raises
        ------
        AngusClientException
            Caso de acontecer algum erro de conexão com o Portal
        """
        response_body = _get_data_angus(
            url=self._host + "consulta_registros",
            params={"id": id_conjunto}
        )
        return pd.DataFrame.from_dict(response_body, orient='index')

    def ingest(self, dataframe) -> bool:
        """

        Parameters
        ----------
        dataframe: pandas.DataFrame

        Returns
        ---------
        bool
            Retorna True caso tenha conseguido ingerir com sucesso ou levantara erro caso contrario

        Raises
        ----------
        AngusIngestException
            Caso de acontecer algum erro de ingestão

        """
        df_tmp = dataframe.copy()
        df_tmp.columns = [i.lower() for i in df_tmp.columns]
        data_send = df_tmp.to_json(orient='records')

        try:
            _send_data_angus(
                url=self._host + "ingerir",
                headers={"Authorization": self._token, "Content-type": "application/json"},
                data=data_send
            )
        except AngusClientException as e:
            raise AngusIngestException(str(e))

        return True
