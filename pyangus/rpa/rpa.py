from pyangus.exceptions.ingest_exception import AngusIngestException
from pyangus.exceptions.rpa_exception import AngusRpaException
from pyangus.client.client import AngusClient
from functools import wraps


class AngusRPA:
    """
    Decorator para RPA
    ex: @AngusRPA(collection_name="teste")
        collection_name: str
            Nome do Conjunto de Dados cadastrado no Portal
    """
    def __init__(self, token, **kwargs):
        self.angus_client = AngusClient(token_collection=token, **kwargs)

    def __send_dataset_angus(self, pandas_dataset):
        self.angus_client.ingest(pandas_dataset)

    def __call__(self, func):
        @wraps(func)
        def run(*args, **kwargs):
            pandas_dataset = func(*args, **kwargs)
            try:
                self.angus_client.ingest(pandas_dataset)
            except AngusIngestException as e:
                raise AngusRpaException(str(e))
            return pandas_dataset
        return run
