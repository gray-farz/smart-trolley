from sshConnection import SSHConnection
from projectVariables import ProjectVariables
class SSHGroupConnection():

    def putToMultipleDevice(deviceIpList,sourceFilePath,destinationFilePath,fileNameInDestination):
        
        for i in range(len(deviceIpList)):
            try:
                ssh = SSHConnection(deviceIpList[i])
                ssh.put(sourceFilePath, os.path.join(destinationFilePath, fileNameInDestination ))
                ssh.close()
            except:
                pass
				
	def getFromMultipleDevice(deviceIpList,gottenFilePath,destinationFilePath,fileNameInDestination):
        for i in range(len(deviceIpList)):
            try:
                ssh = SSHConnection(deviceIpList[i])
                ssh.put(gottenFilePath, os.path.join(destinationFilePath, fileNameInDestination ))
                ssh.close()
            except:
                pass