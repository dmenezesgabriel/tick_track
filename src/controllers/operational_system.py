import src.utils.platform as platform_utils
from src.models.base_operational_system import BaseOperationalSystem


class DefaultOperationalSystem(BaseOperationalSystem):
    def import_os_utils(self):
        """Import utils for designated operational system"""
        os_name = self.name
        platform_utils.import_os(os_name)

    def get_active_window(self):
        """Get active window for designated operational system"""
        os_name = self.name
        return platform_utils.os_get_active_window(os_name)
