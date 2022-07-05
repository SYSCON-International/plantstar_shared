from plantstar_shared.SysconType import SysconType


# `None` tells the system to use the real status retrieved, where a `bool` value is used to signify that we want to mock the status of some process: `is_running_mock_status`
# Local dev systems do not use this, as the API call is entirely skipped on the APU
# The first group represents Live VM Systems
# The second group represents Live (Real) Systems

class DataCollectionModuleProcessNames(SysconType):
    PROCESS_SPAWNER = ("Process Spawner", None, None)
    RAW_DATA_PROCESSOR_INTERFACE = ("Raw Data Processor Interface", None, None)
    RTL_RIO_3 = ("RTL RIO 3", True, None)
