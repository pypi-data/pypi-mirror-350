
from radiens.api import api_allego
from radiens.api.api_utils.util import BaseClient
from radiens.utils.constants import ALLEGO_CORE_ADDR


class WorkspaceClient(BaseClient):
    """
    Workspace client object for AllegoClient
    """

    def __init__(self):
        """ """
        super().__init__()

    @property
    def hubs(self) -> dict:
        """
        dict of active radiens hubs, with hub ID as key.
        """
        return self._hubs()

    @property
    def id(self) -> str:
        """
        UID of this client session.
        """
        return self._id()

    def workspace_save(self, workspace_id=None, tags="", notes=""):
        """
        Saves current workspace

        Parameters:
            workspace_id (str): optional workspace ID
            tags (str): optional tags
            notes (str): optional notes

        Returns:
            None

        Example:
            >>> client.workspace_save(workspace_id='my_wspace', tags='my_tags', notes='my_notes)
            None
        """
        if workspace_id is None:
            return api_allego.workspace_save(ALLEGO_CORE_ADDR, True, tags, notes)
        else:
            return api_allego.workspace_save_as(ALLEGO_CORE_ADDR, workspace_id, True, tags, notes)

    def workspace_switch(self, workspace_id: str):
        """
        Switches to requested workspace

        Parameters:
            workspace_id (str): workspace ID

        Returns:
            None

        Example:
            >>> client.workspace_switch('my_wspace')
            None
        """
        return api_allego.workspace_switch(ALLEGO_CORE_ADDR, workspace_id)

    def workspace_delete(self, workspace_id: str):
        """
        Deletes requested workspace

        Parameters:
            workspace_id (str): workspace ID

        Returns:
            None

        Example:
            >>> client.workspace_delete('my_wspace')
            None
        """
        return api_allego.workspace_delete(ALLEGO_CORE_ADDR, workspace_id)

    def workspace_current(self):
        """
        Returns current workspace ID

        Returns:
            workspaces (pandas.DataFrame)

        Example:
            >>> client.workspace_current()
            df
        """
        return api_allego.workspace_current(ALLEGO_CORE_ADDR)

    def workspace_list(self):
        """
        Returns table of all available workspaces

        Returns:
            workspaces (pandas.DataFrame)

        Example:
            >>> client.workspace_list()
            df
        """
        return api_allego.workspace_list(ALLEGO_CORE_ADDR)
