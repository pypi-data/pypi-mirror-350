# Generating by sila2.code_generator; sila2.__version__: 0.7.3

from uuid import UUID

from sila2.server import SilaServer

from labscheduler.scheduler_implementation import Scheduler

from .feature_implementations.labconfigurationcontroller_impl import LabConfigurationControllerImpl
from .feature_implementations.schedulingservice_impl import SchedulingServiceImpl
from .generated.labconfigurationcontroller import LabConfigurationControllerFeature
from .generated.schedulingservice import SchedulingServiceFeature


class Server(SilaServer):
    scheduler_interface: Scheduler

    def __init__(self, server_uuid: UUID | None = None):
        super().__init__(
            server_name="Scheduler",
            server_type="SchedulerServer",
            server_version="0.1",
            server_description="A server providing schedules",
            server_vendor_url="https://gitlab.com/SiLA2/sila_python",
            server_uuid=server_uuid,
        )
        self.scheduler_interface = Scheduler()
        self.labconfigurationcontroller = LabConfigurationControllerImpl(self, self.scheduler_interface)
        self.schedulingservice = SchedulingServiceImpl(self, self.scheduler_interface)

        self.set_feature_implementation(LabConfigurationControllerFeature, self.labconfigurationcontroller)
        self.set_feature_implementation(SchedulingServiceFeature, self.schedulingservice)
