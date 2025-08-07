import paramiko
def ssh_connect(ip,user,password,command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,username=user,password=password)
    session = client.get_transport().open_session()
    if session.active:
        session.exec_command(command)
        ses_output = session.recv(1024).decode()
        print(ses_output)
        if ses_output.__contains__("Active"):
            print("the service is active and test case is passed")
        else:
            print("Service is not running and the test case is failed.")
        with open("testresults.txt","w",encoding="utf-8") as out_file:
            out_file.write(ses_output)




ssh_connect('96.36.63.189','skumarm','Accruals@2512','systemctl status dtftpkdata-sync')

