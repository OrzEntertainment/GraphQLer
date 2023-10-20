"""Regular mutation materializer:
Materializes a mutation that is ready to be sent off
"""

from .regular_materializer import RegularMaterializer
from .utils import prettify_graphql_payload
import logging


class RegularQueryMaterializer(RegularMaterializer):
    def __init__(self, objects: dict, queries: dict, input_objects: dict, enums: dict, logger: logging.Logger):
        super().__init__(objects, queries, input_objects, enums, logger)
        self.objects = objects
        self.queries = queries
        self.input_objects = input_objects
        self.enums = enums
        self.logger = self.logger  # use the base class' logger instead

    def get_payload(self, query_name: str, objects_bucket: dict) -> tuple[str, dict]:
        """Materializes the query with parameters filled in
           1. Make sure all dependencies are satisfied (hardDependsOn)
           2. Fill in the inputs ()

        Args:
            query_name (str): The query name
            objects_bucket (dict): The bucket of objects that have already been created

        Returns:
            tuple[str, dict]: The string of the query, and the used objects list
        """
        self.used_objects = {}  # Reset the used_objects list per run (from parent class)
        query_info = self.queries[query_name]
        query_inputs = self.materialize_inputs(query_info, query_info["inputs"], objects_bucket)
        query_outputs = self.materialize_output(query_info["output"], [], False)

        if query_inputs != "":
            query_inputs = f"({query_inputs})"

        payload = f"""
        query {{
            {query_name} {query_inputs}
            {query_outputs}
        }}
        """
        return prettify_graphql_payload(payload), self.used_objects