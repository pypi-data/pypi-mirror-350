from plexflow.core.plex.library.folders.assets.plex_asset import PlexAsset

class PlexVideoAsset(PlexAsset):
    def __init__(self, path, root, title, year):
        super().__init__(path, root, title, year)
