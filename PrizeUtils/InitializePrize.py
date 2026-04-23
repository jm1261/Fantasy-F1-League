###############################################################################
###############################################################################
#                           File: InitializePrizes                            #
#                             Author: Joshua Male                             #
#                    Description: Initialize Sub Directory                    #
#                         Project: Fantasy F1 League                          #
#                              Date: 27/03/2026                               #
#                           Copyright © Joshua Male                           #
###############################################################################
###############################################################################
import sys
import logging
import logging.config

from pathlib import Path
from datetime import datetime

# Date
date = datetime.now().date()

# Adjust path for functions
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Initialize logging software
log_path = Path(project_root, 'Logging').as_posix()
logging.config.fileConfig(
    fname=Path(log_path, 'logging.conf'),
    defaults={'logdir': log_path, 'log_date': date}
)
logger = logging.getLogger(name=Path(__file__).stem)

# Check logger working
logger.info('Prize Utils logging initialized successfully')
