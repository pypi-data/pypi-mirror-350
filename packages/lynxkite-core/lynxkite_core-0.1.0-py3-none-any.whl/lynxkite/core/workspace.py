"""For working with LynxKite workspaces."""

import json
from typing import Optional
import dataclasses
import enum
import os
import pycrdt
import pydantic
import tempfile
from . import ops


class BaseConfig(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        extra="allow",
    )


class Position(BaseConfig):
    x: float
    y: float


class NodeStatus(str, enum.Enum):
    planned = "planned"
    active = "active"
    done = "done"


class WorkspaceNodeData(BaseConfig):
    title: str
    params: dict
    display: Optional[object] = None
    input_metadata: Optional[object] = None
    error: Optional[str] = None
    status: NodeStatus = NodeStatus.done
    # Also contains a "meta" field when going out.
    # This is ignored when coming back from the frontend.


class WorkspaceNode(BaseConfig):
    # The naming of these attributes matches the ones for the NodeBase type in React flow
    # modyfing them will break the frontend.
    id: str
    type: str
    data: WorkspaceNodeData
    position: Position
    _crdt: pycrdt.Map

    def publish_started(self):
        """Notifies the frontend that work has started on this node."""
        self.data.error = None
        self.data.status = NodeStatus.active
        if hasattr(self, "_crdt") and "data" in self._crdt:
            with self._crdt.doc.transaction():
                self._crdt["data"]["error"] = None
                self._crdt["data"]["status"] = NodeStatus.active

    def publish_result(self, result: ops.Result):
        """Sends the result to the frontend. Call this in an executor when the result is available."""
        self.data.display = result.display
        self.data.input_metadata = result.input_metadata
        self.data.error = result.error
        self.data.status = NodeStatus.done
        if hasattr(self, "_crdt") and "data" in self._crdt:
            with self._crdt.doc.transaction():
                try:
                    self._crdt["data"]["status"] = NodeStatus.done
                    self._crdt["data"]["display"] = self.data.display
                    self._crdt["data"]["input_metadata"] = self.data.input_metadata
                    self._crdt["data"]["error"] = self.data.error
                except Exception as e:
                    self._crdt["data"]["error"] = str(e)
                    raise e

    def publish_error(self, error: Exception | str | None):
        """Can be called with None to clear the error state."""
        result = ops.Result(error=str(error) if error else None)
        self.publish_result(result)


class WorkspaceEdge(BaseConfig):
    id: str
    source: str
    target: str
    sourceHandle: str
    targetHandle: str


class Workspace(BaseConfig):
    """A workspace is a representation of a computational graph that consists of nodes and edges.

    Each node represents an operation or task, and the edges represent the flow of data between
    the nodes. Each workspace is associated with an environment, which determines the operations
    that can be performed in the workspace and the execution method for the operations.
    """

    env: str = ""
    nodes: list[WorkspaceNode] = dataclasses.field(default_factory=list)
    edges: list[WorkspaceEdge] = dataclasses.field(default_factory=list)
    _crdt: pycrdt.Map

    def normalize(self):
        if self.env not in ops.CATALOGS:
            return self
        catalog = ops.CATALOGS[self.env]
        _ops = {n.id: catalog[n.data.title] for n in self.nodes if n.data.title in catalog}
        valid_targets = set()
        valid_sources = set()
        for n in self.nodes:
            if n.id in _ops:
                for h in _ops[n.id].inputs:
                    valid_targets.add((n.id, h.name))
                for h in _ops[n.id].outputs:
                    valid_sources.add((n.id, h.name))
        self.edges = [
            edge
            for edge in self.edges
            if (edge.source, edge.sourceHandle) in valid_sources
            and (edge.target, edge.targetHandle) in valid_targets
        ]

    def has_executor(self):
        return self.env in ops.EXECUTORS

    async def execute(self):
        return await ops.EXECUTORS[self.env](self)

    def save(self, path: str):
        """Persist the workspace to a local file in JSON format."""
        j = self.model_dump()
        j = json.dumps(j, indent=2, sort_keys=True) + "\n"
        dirname, basename = os.path.split(path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        # Create temp file in the same directory to make sure it's on the same filesystem.
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", prefix=f".{basename}.", dir=dirname, delete=False
        ) as f:
            temp_name = f.name
            f.write(j)
        os.replace(temp_name, path)

    @staticmethod
    def load(path: str) -> "Workspace":
        """Load a workspace from a file.

        After loading the workspace, the metadata of the workspace is updated.

        Args:
            path (str): The path to the file to load the workspace from.

        Returns:
            Workspace: The loaded workspace object, with updated metadata.
        """
        with open(path, encoding="utf-8") as f:
            j = f.read()
        ws = Workspace.model_validate_json(j)
        # Metadata is added after loading. This way code changes take effect on old boxes too.
        ws.update_metadata()
        return ws

    def update_metadata(self):
        """Update the metadata of this workspace.

        The metadata is the information about the operations that the nodes in the workspace represent,
        like the parameters and their possible values.
        This information comes from the catalog of operations for the environment of the workspace.
        """
        if self.env not in ops.CATALOGS:
            return self
        catalog = ops.CATALOGS[self.env]
        for node in self.nodes:
            data = node.data
            op = catalog.get(data.title)
            if op:
                if getattr(data, "meta", None) != op:
                    data.meta = op
                    # If the node is connected to a CRDT, update that too.
                    if hasattr(node, "_crdt"):
                        node._crdt["data"]["meta"] = op.model_dump()
                if node.type != op.type:
                    node.type = op.type
                    if hasattr(node, "_crdt"):
                        node._crdt["type"] = op.type
                if data.error == "Unknown operation.":
                    data.error = None
                    if hasattr(node, "_crdt"):
                        node._crdt["data"]["error"] = None
            else:
                data.error = "Unknown operation."
                if hasattr(node, "_crdt"):
                    node._crdt["data"]["meta"] = {}
                    node._crdt["data"]["error"] = "Unknown operation."

    def connect_crdt(self, ws_crdt: pycrdt.Map):
        self._crdt = ws_crdt
        with ws_crdt.doc.transaction():
            for nc, np in zip(ws_crdt["nodes"], self.nodes):
                if "data" not in nc:
                    nc["data"] = pycrdt.Map()
                np._crdt = nc

    def add_node(self, func):
        """For convenience in e.g. tests."""
        random_string = os.urandom(4).hex()
        node = WorkspaceNode(
            id=f"{func.__op__.name} {random_string}",
            type=func.__op__.type,
            data=WorkspaceNodeData(
                title=func.__op__.name,
                params={},
                display=None,
                input_metadata=None,
                error=None,
                status=NodeStatus.planned,
            ),
            position=Position(x=0, y=0),
        )
        self.nodes.append(node)
        return node

    def add_edge(
        self, source: WorkspaceNode, sourceHandle: str, target: WorkspaceNode, targetHandle: str
    ):
        """For convenience in e.g. tests."""
        edge = WorkspaceEdge(
            id=f"{source.id} {sourceHandle} to {target.id} {targetHandle}",
            source=source.id,
            target=target.id,
            sourceHandle=sourceHandle,
            targetHandle=targetHandle,
        )
        self.edges.append(edge)
        return edge
