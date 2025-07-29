

from enum import Enum
from typing import Optional
from state_of_the_art.tables.base_table import BaseTable

class KnowledgeGraphTable(BaseTable):
    table_name = "knowledge_graph"
    schema = {"node": {"type": str}, "related_node": {"type": str}, 'relationship_type': {'type': str}}

    def add_node(self, node_name: str, node_relation: Optional[str] = None, relationship_type: Optional['RelationshipType'] = None):
        # test if type of node is string
        if not isinstance(node_name, str):
            raise ValueError(f"Node name must be a string, got {type(node_name)}")

        if not node_relation:
            node_relation = ''
            relationship_type = RelationshipType.RELATED.value
        

        self.add(node=node_name, related_node=node_relation, relationship_type=relationship_type)

    def get_related_topics(self, topic: str) -> list[str] | None:
        result = []

        df = self.read()
        relations_of_topic = df.loc[(df['node'] == topic) ]
        result += relations_of_topic["related_node"].unique().tolist()

        # read all related topics nodes
        relations_of_topic = df.loc[(df['related_node'] == topic) ]
        result += relations_of_topic["node"].unique().tolist()

        # remove empty strings
        result = [r for r in result if r]   

        return result

    def add_relationship(self, topic: str, related_topic: str):
        self.add(node=topic, related_node=related_topic, relationship_type=RelationshipType.RELATED.value)
    
    def get_all_topics(self) -> list[str]:
        return self.read()["node"].unique().tolist()


class RelationshipType(str, Enum):
    RELATED = 'related'
    SIMILAR = 'similar'
    CONTRAST = 'contrast'
    CAUSE = 'cause'
    EFFECT = 'effect'
    PARENT = 'parent'
    CHILD = 'child'
