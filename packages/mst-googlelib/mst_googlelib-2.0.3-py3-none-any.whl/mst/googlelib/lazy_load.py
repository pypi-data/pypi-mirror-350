import logging

logger = logging.getLogger(__name__)


class LazyLoad:
    """Parent class for implementing lazy loading. Child class MUST have a _load_data(force: bool) method.
    Will first check to see if the request attribute already exists and return if so. Otherwise,
    it will call the _load_data method on the child class which should handle loading data from another source.
    After the load it will proceed with attempting to access the attribute.
    """

    loaded: bool

    def load_data(self, force=True):
        """Checks to see if the instance is already loaded, and if not, triggers the load.

        Args:
            force (bool, optional): If True it will perform the load even if the instance is already loaded.
                This may be useful to force the instance to refresh its loaded data. Defaults to True.
        """
        if not self.__dict__.get("loaded", None) or force == True:
            logger.debug(f"Loading {self}")
            self._load_data()
            self.loaded = True

    def __getattr__(self, name):
        if name not in self.__dict__ and name not in ["__iter__", "strip"]:
            if name == "loaded":
                self.loaded = False
            else:
                logger.debug(f"Tried to access missing attribute: {name}")
                self.load_data(force=False)

        return self.__getattribute__(name)
