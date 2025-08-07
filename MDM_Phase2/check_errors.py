import os
from operator import indexOf

from dotenv import load_dotenv

load_dotenv()
test_log = os.environ.get("P1_TEST_LOG_PATH")
certify_log = os.environ.get("P1_CERTIFY_LOG_PATH")
deploy_log = os.environ.get("P1_DEPLOY_LOG_PATH")
phase2_log = os.environ.get("PHASE2_LOG_PATH")

def logs_errors(log_dir):

    error_logs = []
    for filename in os.listdir(log_dir):
        if filename.endswith(".txt"):
            file_path=os.path.join(log_dir, filename)
            with open(file_path, "r") as f:
                content = f.read()
                if 'ERROR' in content:
                    error_logs.append(filename)
    return error_logs

#log_dir = [test_log,certify_log,deploy_log,phase2_log]

error_logs = logs_errors(deploy_log)

if error_logs:
    print("The following log files contains 'ERROR':")
    for log in error_logs:
        print(log)
else:
    print("No log files contains 'ERROR'.")