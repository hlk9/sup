from unicodedata import name
from xmlrpc.client import ServerProxy
import json
import os
import configparser

from typing import List
from utils import mean
from psutil import cpu_times, net_io_counters,Process, NoSuchProcess
from ttypes import JiffiesList,InterfaceInstantStats, InstantStatistics, NamedPidList, ProcessStats

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
    output = stream.read()
    return output
        
#Get current CPU Usage
def get_current_cpu_usage():
    stream = os.popen("""top -bn 1  | grep '^%Cpu' | tail -n 1 | awk '{print $2"%"}'""")
    output = stream.read()
    return  output

#Get current each core CPU Usage
def get_each_cpu_usage():
    stream = os.popen("""top 1 -bn1  | grep '^%Cpu' |awk '{print $1,$2,$3"\\n"$18,$19,$20,$21}'""")
    output = stream.read()
    return  output
    # a = get_each_cpu_usage()
    # b = a.replace("st ","")               Output cpu stats
    # c=b.replace(" us,","")
    # print(c)

#Get Memory status
def get_memory_status():
    stream = os.popen("free | grep Mem | awk '{print ($3/$2) * 100.0}'")
    output = stream.read()
    return  output

#Get path of supervisord config file
def sup_config_path():
    
# Get instant values of receive / sent bytes per network interface Supvisor
def instant_io_statistics() -> InterfaceInstantStats:
    """ Return the instant values of receive / sent bytes per network interface. """
    result: InterfaceInstantStats = {}
    # IO details
    io_stats = net_io_counters(pernic=True)
    for intf, io_stat in io_stats.items():
        result[intf] = io_stat.bytes_recv, io_stat.bytes_sent
    return result

def instant_cpu_statistics() -> JiffiesList:
    """ Return the instant work+idle jiffies for all the processors.
    The average on all processors is inserted in front of the list. """
    work: List[float] = []
    idle: List[float] = []
    # CPU details
    cpu_stats = cpu_times(percpu=True)
    for cpu_stat in cpu_stats:
        work.append(cpu_stat.user + cpu_stat.nice + cpu_stat.system
                    + cpu_stat.irq + cpu_stat.softirq
                    + cpu_stat.steal + cpu_stat.guest)
        idle.append(cpu_stat.idle + cpu_stat.iowait)
    # return adding CPU average in front of lists
    work.insert(0, mean(work))
    idle.insert(0, mean(idle))
    return list(zip(work, idle))

# Process statistics Supvisor
def instant_process_statistics(pid, children=True) -> ProcessStats:
    """ Return the instant jiffies and memory values for the process identified by pid. """
    work = memory = 0
    try:
        # get main process
        proc = Process(pid)
        # Note: using Process.oneshot has no value (2 accesses and memory_percent not included in cache for Linux)
        # include children CPU times but exclude iowait
        work = sum(proc.cpu_times()[:4])
        memory = proc.memory_percent()
        # consider children
        if children:
            for p in proc.children(recursive=True):
                # children CPU times are already considered in parent
                memory += p.memory_percent()
    except (NoSuchProcess, ValueError):
        # process may have disappeared in the interval
        pass
    # take into account the number of processes for the process work
    return work, memory

#print(instant_process_statistics(16644))
print(process_memory_usage(process_PID("Demo_1")))
print(process_Info("Demo_1"))
#print("grep --color VmSwap /proc/"+ str(3) +"/status")
#print(process_swap(process_PID("Demo_1")))

