from unicodedata import name
from xmlrpc.client import ServerProxy
import json
import os
from psutil import cpu_times, net_io_counters
from ttypes import  InterfaceInstantStats, InstantStatistics, NamedPidList, ProcessStats


server = ServerProxy('http://localhost:10019/RPC2')


#Get Supervior State 
def sup_State() :
    return server.supervisor.getState()

#Get Supervisor PID
def sup_PID():
    return server.supervisor.getPID()

#Get Supervisor Log ()
def sup_readAllLog():
    print(server.supervisor.readLog(0,0))

#Get Supervisor API Version
def sup_APIVer():
    return server.supervisor.getAPIVersion()

#Get Superivsor Version
def sup_Version():
    return server.supervisor.getSupervisorVersion()

#Get Supervisor Indentification
def sup_Indentification():
    return server.supervisor.getIdentification()

#Get Information of process by name
def process_Info(process_name):
    return server.supervisor.getProcessInfo(process_name)
#Get Information of all process
def process_AllInfo():
    return server.supervisor.getAllProcessInfo()

#Get logfile ouput of process
def process_readLogFile_out(name,offset, length):
    return server.supervisor.readProcessStdoutLog(name,offset,length)
#Get logfile error of process
def process_readLogFile_err(name, offset, length):
    return server.supervisor.readProcessStderrLog(name, offset,length)

#Get process PID
def process_PID(name):
    process_Information=process_Info(name)
    jsonRaw = json.dumps(process_Information)
    jsonParse = json.loads(jsonRaw)
    return jsonParse["pid"]

#Get swap used by process
def process_swap(pid_process):
    stream = os.popen("grep --color VmSwap /proc/"+ str(pid_process)+"/status")
    output = stream.read()
    return output

#Get mem, cpu, core of process running on
def process_memory_usage(pid_porcess):
    stream = os.popen("ps -o pid,psr,%cpu,%mem,comm -p "+ str(pid_porcess))
    output = stream.read()
    return output
    
#Get Host Name
def get_hostname():
    stream = os.popen("hostname")
    output = stream.readlines(2)
    return output
        

# def get_process_logstdout(name):
#     process_Information=process_Info(name)
#     jsonRaw = json.dumps(process_Information)
#     jsonParse = json.loads(jsonRaw)
#     path_logfile= jsonParse["stdout_logfile"]

def test():
    stream = os.popen("top -b -n1")
    output = stream.readlines(7)
    return output
# a function that get the status of each core of the CPU and return it as a list by using the psutil library
# def get_cpu_status():
#     cpu_status = []
#     for i in range(psutil.cpu_count()):
#         cpu_status.append(psutil.cpu_percent(interval=1, percpu=True)[i])
#     return cpu_status

# print(get_cpu_status())
def instant_io_statistics() -> InterfaceInstantStats:
    """ Return the instant values of receive / sent bytes per network interface. """
    result: InterfaceInstantStats = {}
    # IO details
    io_stats = net_io_counters(pernic=True)
    for intf, io_stat in io_stats.items():
        result[intf] = io_stat.bytes_recv, io_stat.bytes_sent
    return result
print(instant_io_statistics())

#print("grep --color VmSwap /proc/"+ str(3) +"/status")
#print(process_swap(process_PID("Demo_1")))


# get status of each core of CPU by using ps command


