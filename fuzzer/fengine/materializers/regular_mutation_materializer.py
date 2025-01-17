"""Regular mutation materializer:
Materializes a mutation that is ready to be sent off
"""

from .regular_materializer import RegularMaterializer
from .utils import prettify_graphql_payload
from constants import MAX_OUTPUT_SELECTOR_DEPTH, MAX_INPUT_DEPTH
import logging


class RegularMutationMaterializer(RegularMaterializer):
    def __init__(self, objects: dict, mutations: dict, input_objects: dict, enums: dict):
        super().__init__(objects, mutations, input_objects, enums)
        self.objects = objects
        self.mutations = mutations
        self.input_objects = input_objects
        self.enums = enums

    def get_payload(self, mutation_name: str, objects_bucket: dict) -> tuple[str, dict]:
        """Materializes the mutation with parameters filled in
           1. Make sure all dependencies are satisfied (hardDependsOn)
           2. Fill in the inputs ()

        Args:
            mutation_name (str): The mutation name
            objects_bucket (dict): The bucket of objects that have already been created

        Returns:
            tuple[str, dict]: The string of the mutation, and the used objects list
        """
        self.used_objects = {}  # Reset the used_objects list per run (from parent class)
        mutation_info = self.mutations[mutation_name]
        mutation_inputs = self.materialize_inputs(mutation_info, mutation_info["inputs"], objects_bucket, max_depth=MAX_INPUT_DEPTH)
        mutation_output = self.materialize_output(mutation_info["output"], [], False, max_depth=MAX_OUTPUT_SELECTOR_DEPTH)
        mutation_payload = f"""
        mutation {{
            {mutation_name} (
                {mutation_inputs}
            )
            {mutation_output}
        }}
        """
        pretty_payload = prettify_graphql_payload(mutation_payload)
        return pretty_payload, self.used_objects
