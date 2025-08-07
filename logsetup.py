import logging
from datetime import datetime
logfile_name = "createModel" + str(datetime.now().second) + ".txt"


logging.basicConfig(
        filename=logfile_name,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )





