class Scene:
    def __init__(self, **kwargs):
        self.is_paused = True

    @property
    def name(self) -> str:
        return __name__

    def on_awake(self) -> None:
        """
        Will be called upon startup. Must be overrided
        """
        pass

    def on_delete(self) -> None:
        """
        Will be called upon destruction. Must be overrided
        """
        pass

    def update(self) -> None:
        """
        Will be called upon every frame. Must be overrided
        """
        pass