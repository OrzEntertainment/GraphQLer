"""This module will be used to create a object dependency resolver
   The representation of this will be essentially a text-based graph

   The dependencies will be generated from object - object
   while methods such as queries / mutations will be related to objects
   based on either output type or semantic understanding
"""

from constants import BUILT_IN_TYPES, BUILT_IN_TYPE_KINDS


class ObjectDepdenencyResolver:
    def __init__(self, objects: dict):
        self.objects = objects

    def resolve(self) -> dict:
        """Resolve dependencies by adding the 'hardDependsOn' key and 'softDependsOn' key
           hardDependsOn: the object must be created for this object to be instantiated
           softDependsOn: the object can be null on instantiation of this object

        Returns:
            dict: The new enriched objects with an extra 'dependsOn' key
        """
        for gql_object_key, gql_object in self.objects.items():
            self.parse_gql_object(gql_object)
        return self.objects

    def parse_gql_object(self, gql_object: dict) -> dict:
        """Parse a single object, noting down all of the other object this object depends on
           Simply adds an extra key in the object 'dependsOn' which is a list of the objects this
           object depneds on

        Args:
            gql_object (dict): The graphql object

        Returns:
            dict: The enriched object with an extra 'dependsOn' key
        """
        soft_dependent_objects = []
        hard_dependent_objects = []
        for field in gql_object["fields"]:
            # There are 3 cases:
            # - if the kind is SCALAR/OBJECT/INTERFACE/UNION/ENUM/INPUT_OBJECT,
            # - if kind is NON_NULL
            # - if kind is LIST
            if field["kind"] in BUILT_IN_TYPE_KINDS and field["kind"] != "NON_NULL" and field["kind"] != "LIST":
                if field["type"] not in BUILT_IN_TYPES:
                    soft_dependent_objects.append(field["type"])
            if field["kind"] == "NON_NULL":
                if field["ofType"] not in BUILT_IN_TYPES:
                    hard_dependent_objects.append(field["ofType"])
            elif field["kind"] == "LIST":
                if field["ofType"] not in BUILT_IN_TYPES:
                    soft_dependent_objects.append(field["ofType"])
        gql_object["softDependsOn"] = soft_dependent_objects
        gql_object["hardDependsOn"] = hard_dependent_objects
        return gql_object