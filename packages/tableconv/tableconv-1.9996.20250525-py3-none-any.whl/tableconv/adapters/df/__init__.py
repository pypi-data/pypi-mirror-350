from tableconv.adapters.df.base import adapters, read_adapters, write_adapters  # noqa: F401

from .ascii import *  # noqa: F401 F403
from .avro import *  # noqa: F401 F403
from .aws_athena import *  # noqa: F401 F403
from .aws_dynamodb import *  # noqa: F401 F403
from .aws_logs import *  # noqa: F401 F403
from .duckdb import *  # noqa: F401 F403
from .gsheets import *  # noqa: F401 F403
from .iceberg import *  # noqa: F401 F403
from .jc import *  # noqa: F401 F403
from .jira import *  # noqa: F401 F403
from .json import *  # noqa: F401 F403
from .leveldb import *  # noqa: F401 F403
from .nested_list import *  # noqa: F401 F403
from .numbers import *  # noqa: F401 F403
from .osquery import *  # noqa: F401 F403
from .pandas_io import *  # noqa: F401 F403
from .pcap import *  # noqa: F401 F403
from .protobuf import *  # noqa: F401 F403
from .python import *  # noqa: F401 F403
from .rdbms import *  # noqa: F401 F403
from .smart_sheet import *  # noqa: F401 F403
from .sql_literal import *  # noqa: F401 F403
from .sumo_logic import *  # noqa: F401 F403
from .text_array import *  # noqa: F401 F403
from .yaml import *  # noqa: F401 F403

# TODO: Register adapters in a cleaner way (dynamic adapter loading?). Just get rid of the `import *` pattern!
