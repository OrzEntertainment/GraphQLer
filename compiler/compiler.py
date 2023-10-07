"""Compiler class - responsible for:
    - Getting the introspection query results into various files we can use later on
    - Resolving dependencies among objects
    - Tieing queries / mutations to objects
    - Serializing
"""

from pathlib import Path
from compiler.utils import send_graphql_request, write_json_to_file, write_dict_to_yaml, initialize_file
from compiler.introspection_query import introspection_query
from compiler.parsers import QueryListParser, ObjectListParser, MutationListParser, InputObjectListParser, EnumListParser, Parser
from compiler.resolvers import ObjectDependencyResolver, ObjectMethodResolver

import constants
import yaml
import pprint


class Compiler:
    def __init__(self, save_path: str, url: str):
        """Initializes the compiler,
            creates all necessary file paths to save the outputs for run if doesn't already exist

        Args:
            save_path (str): Save directory path
            url (str): URL for graphql introspection query to hit
        """
        self.save_path = save_path
        self.introspection_result_save_path = Path(save_path) / Path(constants.INTROSPECTION_RESULT_FILE_NAME)
        self.object_list_save_path = Path(save_path) / constants.OBJECT_LIST_FILE_NAME
        self.input_object_list_save_path = Path(save_path) / constants.INPUT_OBJECT_LIST_FILE_NAME
        self.mutation_parameter_save_path = Path(save_path) / constants.MUTATION_PARAMETER_FILE_NAME
        self.query_parameter_save_path = Path(save_path) / constants.QUERY_PARAMETER_FILE_NAME
        self.enum_list_save_path = Path(save_path) / constants.ENUM_LIST_FILE_NAME
        self.compiled_object_list_save_path = Path(save_path) / constants.COMPILED_OBJECT_LIST_FILE_NAME
        self.url = url

        # Initialize the parsers we will use
        self.object_list_parser = ObjectListParser()
        self.query_list_parser = QueryListParser()
        self.mutation_list_parser = MutationListParser()
        self.input_object_list_parser = InputObjectListParser()
        self.enum_list_parser = EnumListParser()

        # Create empty files for these files
        Path(self.save_path).mkdir(parents=True, exist_ok=True)
        initialize_file(self.introspection_result_save_path)
        initialize_file(self.object_list_save_path)
        initialize_file(self.input_object_list_save_path)
        initialize_file(self.mutation_parameter_save_path)
        initialize_file(self.query_parameter_save_path)
        initialize_file(self.enum_list_save_path)
        initialize_file(self.compiled_object_list_save_path)

    def run(self):
        """The only function required to be run from the caller, will perform:
        1. Introspection query running
        2. Run the parsers, storing files into objects / query / mutations
        3. Creating dependencies between objects and attaching methods (query/mutations) to objects
        """
        introspection_result = self.get_introspection_query_results()

        self.run_parsers_and_save(introspection_result)
        self.run_resolvers_and_enrich_objects_and_save(introspection_result)

    def get_introspection_query_results(self) -> dict:
        """Run the introspection query, grab results and output to file

        Returns:
            dict: Dictionary of the resulting JSON from the introspection query
        """
        result = send_graphql_request(self.url, introspection_query)
        write_json_to_file(result, self.introspection_result_save_path)
        return result

    def run_parsers_and_save(self, introspection_result: dict):
        """Runs all the parsers and saves them to a YAML file

        Args:
            introspection_result (dict): Introspection results as a dict
        """
        self.run_parser_and_save_list(self.object_list_parser, self.object_list_save_path, introspection_result)
        self.run_parser_and_save_list(self.query_list_parser, self.query_parameter_save_path, introspection_result)
        self.run_parser_and_save_list(self.mutation_list_parser, self.mutation_parameter_save_path, introspection_result)
        self.run_parser_and_save_list(self.input_object_list_parser, self.input_object_list_save_path, introspection_result)
        self.run_parser_and_save_list(self.enum_list_parser, self.enum_list_save_path, introspection_result)

    def run_parser_and_save_list(self, parser_instance: Parser, save_path: str, introspection_result: dict):
        """Runs the given parser instance on the introspection result and saves to the save_path

        Args:
            parser_instance (Parser): Parser instance
            save_path (str): Path to save parsed results (in YAML format)
            introspection_result (dict): Introspection result as a dict
        """
        parsed_result = parser_instance.parse(introspection_result)
        write_dict_to_yaml(parsed_result, save_path)

    def run_resolvers_and_enrich_objects_and_save(self, introspection_result: dict):
        """Runs the enrichments to objeccts like so:
            1. Enriches object-object dependency
            2. Enriches object-method dependency
           and then writes it to a yaml file

        Args:
            introspection_result (dict): Introspection query result
        """
        objects = self.object_list_parser.parse(introspection_result)
        queries = self.query_list_parser.parse(introspection_result)
        mutations = self.mutation_list_parser.parse(introspection_result)

        objects = ObjectDependencyResolver().resolve(objects)
        objects = ObjectMethodResolver().resolve(objects, queries, mutations)

        write_dict_to_yaml(objects, self.compiled_object_list_save_path)
