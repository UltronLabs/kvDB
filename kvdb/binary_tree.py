import pickle
from .logical import LogicalBase, ValueRef


class BinaryTree(LogicalBase):
    # ...

    def __init__(self, storage) -> None:
        super().__init__()
        self._storage = storage
        self.node_ref_class = None

    def _get(self, node, key):
        """
        This method performs a binary search on the tree for a given key.

        Args:
            node (Node): The node to start the search from.
            key (str/int): The key to search for in the tree.

        Returns:
            Value associated with the key if found.

        Raises:
            KeyError: If the key is not found in the tree.
        """
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif node.key < key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)

        raise KeyError

    def set(self, key, value):
        """
        This method is used to insert a key-value pair into the binary tree.

        First, it checks if the storage is locked. If it is, it refreshes the tree reference.

        Then it inserts the key-value pair into the tree at the correct position, which is found by following
        the current tree reference. The value is wrapped in a `value_ref_class` before insertion.

        After the insertion, the tree reference is updated to the new root of the tree.
        """
        if self.storage.lock():
            self._refresh_tree_ref()
        self._tree_ref = self.insert(
            self._follow(self._tree_ref), key, self.value_ref_class(value)
        )

    def _insert(self, node, key, value_ref):
        """
        This method is used to insert a new node into a binary tree.

        Parameters:
        node: The current node in the binary tree.
        key: The key of the new node to be inserted.
        value_ref: The reference to the value of the new node.
        """

        # If the current node is None, it means we've reached an empty spot where we can insert our new node.
        if node is None:
            new_node = BinaryNode(
                self.node_ref_class(), key, value_ref, self.node_ref_class(), 1
            )

        # If the key of the new node is less than the key of the current node,
        # we need to insert the new node in the left subtree.
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node,
                # Recursively call the _insert method for the left child of the current node.
                left_ref=self._insert(self._follow(node.left_ref), key, value_ref),
            )

        # If the key of the new node is greater than the key of the current node,
        # we need to insert the new node in the right subtree.
        elif node.key < key:
            new_node = BinaryNode.from_node(
                node,
                # Recursively call the _insert method for the right child of the current node.
                right_ref=self._insert(self._follow(node.right_ref), key, value_ref),
            )

        # If the keys are equal, we update the value of the current node with the new value.
        else:
            new_node = BinaryNode.from_node(node, value_ref=value_ref)

        # Return a reference to the new node.
        return self.node_ref_class(referent=new_node)


class BinaryNodeRef(ValueRef):
    def prepare_to_store(self, storage):
        """
        This method is used to prepare the node for storage.
        """

        # If the node exists (i.e., it's not None)
        if self._referent:
            # Store all references of the node into storage.
            # This ensures that all child nodes are properly saved before the parent node.
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_string(referent):
        return pickle.dumps(
            {
                "left": referent.left_ref.address,
                "key": referent.key,
                "value": referent.value_ref.address,
                "right": referent.right_ref.address,
                "length": referent.length,
            }
        )


class BinaryNode(object):
    def store_refs(self, storage):
        """
        This method stores the value, left and right references of the node into storage.
        """

        self.value_ref.store(storage)

        self.left_ref.store(storage)

        self.right_ref.store(storage)
