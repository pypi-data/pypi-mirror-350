class IEntityInterface:
    def _getEntityConnection(self):
        if hasattr(self, "connection"):
            return getattr(self, "connection")
        return None
