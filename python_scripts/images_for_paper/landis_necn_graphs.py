#Script to help analyze LANDIS-II NECN outputs
#Created by Steve Flanagan, 2018
#Plots of variables will be saved to a new folder "necn_graphs"
#stored in whatever is specified by the user as the wdir
#If outputs are not renamed they will be overwritten 
#Might get warnings if you have "necn_graphs open - just run again

#import arcpy
import matplotlib.pyplot as plt
import pandas as pd
import os, shutil
import numpy as np


#################################################################
#                  START USER INPUT                             #
#################################################################
#Set the output path
wdir = "C:\\Users\\sflanagan\\desktop\\landis_runs\\100m_final\\Output\\"

#List the scenarios you want to examine
#scen_list = ["pf_300yrs","wf_20_300yrs","wf_50_300yrs","wf_100_300yrs","nf_300yrs"]#,"wfs_1000yrs"]
#scen_list = ["pf_300yrs","wf_20_allsame_300yrs","wf_50_allsame_300yrs","wf_100_allsame_300yrs","nf_300yrs"]
#scen_list = ["pf_leaveall_300yrs","wf_20_leaveall_300yrs","wf_50_leaveall_300yrs","wf_100_leaveall_300yrs","nf_300yrs"]
#scen_list = ["pf_removeall_300yrs","wf_20_removeall_300yrs","wf_50_removeall_300yrs","wf_100_removeall_300yrs","nf_300yrs"]
#scen_list = ["pf33_8_300yrs","wf_20_remove33_8_300yrs","wf_50_remove33_8_300yrs","wf_100_remove33_8_300yrs","nf_300yrs"]
#scen_list = ["pf_leaveevery_300yrs","wf_20_leaveevery_300yrs","wf_50_leaveevery_300yrs","wf_100_leaveevery_300yrs","nf_300yrs"]
scen_list = ["pf_ottmer_300yrs","wf_20_ottmer_300yrs","wf_50_ottmer_300yrs","wf_100_ottmer_300yrs","nf_300yrs"]
#and the numbers for the runs
num_list =["1","2","3","4","5"]

#abbrvs
#abbrvs_list=["2yr","20yr","50yr","100yr","Exclusion"]
abbrvs_list=["2yr RxFire","20yr WF","50yr WF","100yr WF","Fire Exclusion"]
marker_list=["o","v","s","D","+"]
#style_list=[":","-.","--","-","-"]
style_list=["-","-","-","-","-"]
#color_list=['k','k','k','k','0.5']
color_list=['#377eb8', '#ff7f00', '#4daf4a','#f781bf','#000000']

#start, end, step of time
start_time = 0
end_time = 301 #add 1
time_step = 10
max_agb = 32000  #g/m2

#Variable
variables =["AGB"]#["C_DeadWood"]#NEEC, SOMTC

#Much of this can probably be automated but let's start here

#################################################################
#                 END USER INPUT                                #
#################################################################

#Create main directory to save images created
odir = wdir+"necn_graphs"
if os.path.exists(odir):
    shutil.rmtree(odir)
os.makedirs(odir)

  
#Open the spp-log file and loop through desired scenarios
for i in range(0,len(scen_list)):
    print "Generating plots for " + scen_list[i]
    lst = np.zeros((len(variables),end_time))
    
    #Open the file set
    for s in range (0,len(num_list)): 
        pd.set_option('display.max_colwidth', -1)
        p_name = wdir + scen_list[i]+num_list[s]+"\\NECN-succession-log-short.csv"
        df = pd.read_csv(p_name)
     
        for j in range(0,len(variables)):
            v_name = variables[j]
            #aggregate
            lst[j,:] += df[v_name]

    #This will graph the average of each scenario
    lst[:,:] /= len(num_list)
    t = df["Time"]
    fig, ax = plt.subplots()
    plt.xlim(start_time,end_time)
    plt.ylim(0,max_agb)
    plt.ylabel("AGB (g/m2)")
    plt.xlabel("Time (yr)")
    for l in range(0,len(variables)):
        ax.plot(t,lst[l,:], label=variables[j])

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(odir+ "\\"+v_name+"_avg_"+scen_list[i]+".png")  
    
#And lets put all the graphs on the same image
plt.clf()
plt.close()
print "Generating combined plot"
fig, ax = plt.subplots()
plt.xlim(start_time,end_time)
#plt.ylim(0,max_agb)
for l in range(0,len(variables)):
    #plt.title("Total " + variables[l] +" by scenario")
    plt.ylabel("Aboveground biomass (Mg/ha)")
    plt.xlabel("Simulation year")
    for i in range(0,len(scen_list)):
    
        lst = np.zeros((len(variables),len(scen_list),end_time))
    
        #Open the file set
        for s in range (0,len(num_list)): 
            pd.set_option('display.max_colwidth', -1)
            p_name = wdir + scen_list[i]+num_list[s]+"\\NECN-succession-log-short.csv"
            df = pd.read_csv(p_name)
     
            for j in range(0,len(variables)):
                v_name = variables[j]
                #aggregate
                lst[j,i,:] += df[v_name]



        #This will graph the average of each scenario
        lst[:,:,:] /= len(num_list)
        t = df["Time"]
    
        #ax.plot(t,lst[l,i,:], label=abbrvs_list[i],marker=marker_list[i],color="black",markevery=5)
        ax.plot(t,lst[l,i,:]/100,label=abbrvs_list[i],linestyle=style_list[i],color=color_list[i])
        print "scenario " + scen_list[i] + " mean " + str(np.mean(lst[l,i,:]))
    box = ax.get_position()
    #ax.set_position([box.x0, box.y0+.2, box.width, box.height*.8])
    ax.legend(loc='upper center',numpoints=1,mode="expand",ncol=len(scen_list),fontsize=10)#, bbox_to_anchor=(0.5, -0.2))
    plt.savefig(odir+ "\\"+v_name+"_avg_combined.png",dpi=300) 
    plt.savefig(odir+ "\\Figure2.pdf",dpi=300)  
   

#Lets not change above but if we want envelopes
plt.clf()
plt.close()
print "Generating combined plot with envelope"
fig, ax = plt.subplots()
plt.xlim(start_time,end_time)
plt.ylim(0,400)
for l in range(0,len(variables)):
    #plt.title("Total " + variables[l] +" by scenario")
    plt.ylabel("Aboveground biomass (Mg/ha)")
    plt.xlabel("Simulation year")
    for i in range(0,len(scen_list)):
    
        lst = np.zeros((len(variables),len(scen_list),end_time))
    
        #Open the file set
        for s in range (0,len(num_list)): 
            pd.set_option('display.max_colwidth', -1)
            p_name = wdir + scen_list[i]+num_list[s]+"\\NECN-succession-log-short.csv"
            df = pd.read_csv(p_name)
     
            for j in range(0,len(variables)):
                v_name = variables[j]
                #aggregate
                lst[j,i,:] = df[v_name]
                ax.plot(t,lst[l,i,:]/100,label=abbrvs_list[i],linestyle=style_list[i],color=color_list[i])


        #This will graph the average of each scenario
        lst[:,:,:] /= len(num_list)
        t = df["Time"]
    
        #ax.plot(t,lst[l,i,:], label=abbrvs_list[i],marker=marker_list[i],color="black",markevery=5)
        #ax.plot(t,lst[l,i,:]/100,label=abbrvs_list[i],linestyle=style_list[i],color=color_list[i])
        #print "scenario " + scen_list[i] + " mean " + str(np.mean(lst[l,i,:]))
    box = ax.get_position()
    #ax.set_position([box.x0, box.y0+.2, box.width, box.height*.8])
    ax.legend(loc='upper center',numpoints=1,mode="expand",ncol=len(scen_list),fontsize=10)#, bbox_to_anchor=(0.5, -0.2))
    plt.savefig(odir+ "\\"+v_name+"_avg_combined2.png",dpi=300)  


print "Script complete"

        
       
       
       


   


