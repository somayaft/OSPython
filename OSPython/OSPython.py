class ProcessCB:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = int(arrival_time)
        self.burst_time = int(burst_time)
        self.remaining_time = int(burst_time)
        self.start_time = 0
        self.finish_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
    

def read_processes_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            pid, at, bt = [], [], []
            contextSwitch =  int(lines[0].strip())
            tq =  int(lines[1].strip())
 
            for line in lines[2:]:
                parts = line.strip().split()
                pid.append(parts[0])
                at.append(int(parts[1]))
                bt.append(int(parts[2]))
            return contextSwitch , tq , pid, at, bt 
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return [], [], []


def fcfs(pid,at,bt):
    print("Gantt Chart :")
    dpid=[]
    dat=[]
    dbt=[]
 #  s = 0
    for i in range(len(pid)):
        dpid.append(pid[i])
        dat.append(at[i])
        dbt.append(bt[i])
    l=len(pid)
    gantt=[]
    s=0
    for i in range(l):
         #  C = pid[at.index(min(at))]
        ind=at.index(min(at))
        if min(at)>s:
            for m in range(s,min(at)):
#         if min(at) > s:
#             for m in range(s, min(at)):
                gantt.append("IDLE")
        for j in range(s,s+bt[ind]):
            gantt.append(pid[ind])
#              if C !=pid[ind]:
#             s+= contextSwitch
#         s += bt[ind]
        s+=bt[ind]
        pid.pop(ind)
        at.pop(ind)
        bt.pop(ind)
    print(gantt)
    tat=[]
    wt=[]
    print("Process\t AT\tBT\tTAT\tWT")
    for i in range(len(dpid)):
        l=len(gantt)
        for k in range(l-1,-1,-1):
            if gantt[k]==dpid[i]:
                tat.append(k+1-dat[i])
                wt.append(tat[i]-dbt[i])
                break
    for i in range(len(dpid)):
        print(dpid[i],"\t",dat[i],"\t",dbt[i],"\t",tat[i],"\t",wt[i])
    print("Average TAT = ",sum(tat)/len(tat))
    print("Average WT = ",sum(wt)/len(wt))

# fcfs(['p1','p2','p3','p4','p5'],[4,6,0,6,5],[5,4,3,2,4])

def srtf(pid,at,bt):
    print("\nResults for SRTF:")
    print("Gantt Chart :")
    process={}
    gantt=[]
    for i in range(len(pid)):
        process[pid[i]]=[at[i],bt[i]]
    start=0
    while process!={}:
        short_pro=''
        short_job=1000
        for i in process:
            if process[i][0]<=start and process[i][1]<short_job:
                short_job=process[i][1]
                short_pro=i
        if short_pro=='':
            gantt.append('IDLE')
            start+=1
        else:
            gantt.append(short_pro)
            process[short_pro]=[process[short_pro][0],process[short_pro][1]-1]
            start+=1
            if process[short_pro][1]==0:
                del process[short_pro]
    print(gantt)
    tat=[]
    wt=[]
    print("Process\t AT\tBT\tTAT\t WT")
    for i in range(len(pid)):
        l=len(gantt)
        for k in range(l-1,-1,-1):
            if gantt[k]==pid[i]:
                tat.append(k+1-at[i])
                wt.append(tat[i]-bt[i])
                break
    for i in range(len(pid)):
        print(pid[i],"\t",at[i], "\t", bt[i], "\t", tat[i],"\t",wt[i])
    print("Average TAT = ",sum(tat)/len(tat))
    print("Average WT = ",sum(wt)/len(wt))
    
srtf(['p1','p2','p3','p4'],[0,2,3,8],[12,4,6,5])





def rr(pid,at,bt,tq):
    print("\nResults for RR:")
    print("Gantt Chart :")
    process={}
    gantt=[]
    for i in range(len(pid)):
        process[pid[i]]=[at[i],bt[i],0]
    start=0
    check=0
    while process!={}:
        curr_job=''
        for i in process:
            if process[i][0]<=start and process[i][2]==0:
                curr_job=i
                break
        if curr_job=='':
            if check==1:
                gantt.append('IDLE')
                start+=1
            elif check==0:
                for i in process:
                    process[i]=[process[i][0],process[i][1],0]
                check=1
        else:
            if(process[curr_job][1]<=tq):
                for i in range(process[curr_job][1]):
                    gantt.append(curr_job)
                    start+=1
                del process[curr_job]
            else:
                for i in range(tq):
                    gantt.append(curr_job)
                    start+=1
                process[curr_job]=[process[curr_job][0],process[curr_job][1]-tq,1]
            check=0
    print(gantt)
    tat=[]
    wt=[]
    print("Process\t AT\tBT\tTAT\t WT")
    for i in range(len(pid)):
        l=len(gantt)
        for k in range(l-1,-1,-1):
            if gantt[k]==pid[i]:
                tat.append(k+1-at[i])
                wt.append(tat[i]-bt[i])
                break
    for i in range(len(pid)):
        print(pid[i],"\t",at[i], "\t", bt[i], "\t", tat[i],"\t",wt[i])
    print("Time Quantum =",tq)
    print("Average TAT = ",sum(tat)/len(tat))
    print("Average WT = ",sum(wt)/len(wt))
    
rr(['p1','p2','p3','p4','p5'],[0,11,12,3,14],[5,3,1,2,3],2)


def main(file_path):
    contextSwitch,tq, pid, at, bt = read_processes_from_file(file_path)
    if pid:
        print("\nResults for FCFS:")
        fcfs(pid, at, bt)

        print("\nResults for SRTF:")
        # srtf(pid, at, bt)

        print("\nResults for RR:")
        # rr(pid, at, bt, tq)
    else:
        print("Error: No processes found or invalid input file.")


if __name__ == "__main__":
    file_path = r"C:\Users\Sumaya\OneDrive\Desktop\OS\OS.txt" 
    main(file_path)




