class Observer:
    def update(self, event_name, **kwargs):
        raise NotImplementedError("La méthode update() doit être surchargée.")
