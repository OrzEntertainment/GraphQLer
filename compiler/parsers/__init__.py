"""Parsers:
Parsers are classes used to parse a specific object type out from the introspection query result.
They don't perform any enrichments to the existing objects, only filtering
"""
from .object_list_parser import ObjectListParser
from .query_list_parser import QueryListParser
from .mutation_list_parser import MutationListParser
from .input_object_list_parser import InputObjectListParser
from .enum_list_parser import EnumListParser
from .parser import Parser
