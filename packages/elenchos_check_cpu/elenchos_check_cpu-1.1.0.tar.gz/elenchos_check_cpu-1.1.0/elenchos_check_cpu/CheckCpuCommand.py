from cleo.helpers import option
from elenchos.command.CheckCommand import CheckCommand

from elenchos_check_cpu.CheckCpuPlugin import CheckCpuPlugin


class CheckCpuCommand(CheckCommand):
    """
    A Élenchos command for checking CPU usage.
    """
    name = 'check:cpu'
    description = 'Test CPU usage'
    options = [option('interval',
                      'i',
                      description='The interval between the two CPU statistics gatherings in seconds.',
                      flag=False,
                      value_required=True,
                      default=2.0),
               option('warning',
                      'w',
                      description='The warning level for CPU user in %.',
                      flag=False,
                      value_required=False),
               option('critical',
                      'c',
                      description='The critical level for CPU user in %.',
                      flag=False,
                      value_required=False)]

    # ------------------------------------------------------------------------------------------------------------------
    def _handle(self) -> int:
        """
        Executes this command.
        """
        warning = round(float(self.option('warning')), 6) if self.option('warning') else None
        critical = round(float(self.option('critical')), 6) if self.option('critical') else None
        interval = int(self.option('interval'))
        plugin = CheckCpuPlugin(interval, warning, critical)

        return plugin.check().value

# ----------------------------------------------------------------------------------------------------------------------
