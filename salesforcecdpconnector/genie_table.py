#
#  Copyright (c) 2022, salesforce.com, inc.
#  All rights reserved.
#  SPDX-License-Identifier: BSD-3-Clause
#  For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#

class PrimaryKeys:
    name = ''
    display_name = ''
    index_order = ''

    def __init__(self, name, display_name, index_order):
        self.name = name
        self.display_name = display_name
        self.index_order = index_order

    def __eq__(self, other):
        return self.name == other.name and self.display_name == other.display_name \
               and self.index_order == other.index_order


class Relationship:
    from_table = ''
    to_table = ''
    from_entity_attribute = ''
    to_entity_attribute = ''
    cardinality = ''

    def __init__(self, from_table, to_table, from_entity_attribute='', to_entity_attribute='', cardinality=''):
        self.from_table = from_table
        self.to_table = to_table
        self.from_entity_attribute = from_entity_attribute
        self.to_entity_attribute = to_entity_attribute
        self.cardinality = cardinality

    def __eq__(self, other):
        return self.from_table == other.from_table and self.to_table == other.to_table \
               and self.from_entity_attribute == other.from_entity_attribute \
               and self.to_entity_attribute == other.to_entity_attribute and self.cardinality == other.cardinality


class Field:
    name = ''
    display_name = ''
    type = ''
    is_measure = False
    is_dimension = False

    def __init__(self, name, display_name, type, is_measure=False, is_dimension=False):
        self.name = name
        self.display_name = display_name
        self.type = type
        self.is_measure = is_measure
        self.is_dimension = is_dimension

    def __eq__(self, other):
        return self.name == other.name and self.display_name == other.display_name \
               and self.type == other.type and self.is_measure == other.is_measure \
               and self.is_dimension == other.is_dimension


class GenieTable:
    name = ''
    display_name = ''
    category = ''
    primary_keys = []
    partition_by = ''
    fields = []
    relationships = []
    indexes = []

    def __init__(self, name='', display_name='', category='', primary_keys=[], partition_by='', fields=[],
                 relationships=[], indexes=[]):
        self.name = name
        self.display_name = display_name
        self.category = category
        self.primary_keys = primary_keys
        self.partition_by = partition_by
        self.fields = fields
        self.relationships = relationships
        self.indexes = indexes

    def __eq__(self, other):
        return self.name == other.name and self.display_name == other.display_name \
               and self.category == other.category and all(self.primary_keys[i] == other.primary_keys[i] for i in range(len(self.primary_keys))) \
               and self.partition_by == other.partition_by and all(self.fields[i] == other.fields[i] for i in range(len(self.fields))) \
               and all(self.relationships[i] == other.relationships[i] for i in range(len(self.relationships))) \
               and all(self.indexes[i] == other.indexes[i] for i in range(len(self.indexes)))