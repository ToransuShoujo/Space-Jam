from panda3d.core import PandaNode, Loader, NodePath, CollisionNode, CollisionSphere, CollisionInvSphere, \
    CollisionCapsule, Vec3


class PlacedObject(PandaNode):
    # Just a generic object in the scene at this point. No relation to collisions.
    def __init__(self, loader: Loader, model_path: str, parent_node: NodePath, node_name: str):
        self.model_node: NodePath = loader.loadModel(model_path)

        # We want to make sure we are having the right type passed to this parameter, or else throw an error.
        if not isinstance(self.model_node, NodePath):
            raise AssertionError("PlacedObject loader.loadModel(" + model_path + ") did not return a proper PandaNode!")

        self.model_node.reparentTo(parent_node)
        self.model_node.setName(node_name)


class CollidableObject(PlacedObject):
    # Now, we related our PlacedObject to collisions by using it as a helper class for this function to create collisions.
    def __init__(self, loader: Loader, model_path: str, parent_node: NodePath, node_name: str):
        super(CollidableObject, self).__init__(loader, model_path, parent_node, node_name)
        # Every single type of collider will get the "_cNode" tag behind it to signify that it's a collidable object.
        self.collision_node = self.model_node.attachNewNode(CollisionNode(node_name + "_cNode"))
        self.collision_node.show()


class InverseSphereCollidableObject(CollidableObject):
    def __init__(self, loader: Loader, model_path: str, parent_node: NodePath, node_name: str, col_position_vec: Vec3,
                 col_radius: float):
        super(InverseSphereCollidableObject, self).__init__(loader, model_path, parent_node, node_name)
        self.collision_node.node().addSolid(CollisionInvSphere(col_position_vec, col_radius))
        self.collision_node.show()


class CapsuleCollidableObject(CollidableObject):
    # a and b are respectively the furthest point on a capsule collider on either side.
    def __init__(self, loader: Loader, model_path: str, parent_node: NodePath, node_name: str, ax: float, ay: float,
                 az: float, bx: float, by: float, bz: float, r: float):
        super(CapsuleCollidableObject, self).__init__(loader, model_path, parent_node, node_name)
        self.collision_node.node().addSolid(CollisionCapsule(ax, ay, az, bx, by, bz, r))
        self.collision_node.show()


class SphereCollidableObject(CollidableObject):
    def __init__(self, loader: Loader, model_path: str, parent_node: NodePath, node_name: str, col_position_vec: Vec3,
                 col_radius: float):
        super(SphereCollidableObject, self).__init__(loader, model_path, parent_node, node_name)
        self.collision_node.node().addSolid(CollisionSphere(col_position_vec, col_radius))
        self.collision_node.show()
