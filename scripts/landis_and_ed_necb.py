#Script to help analyze LANDIS-II and ED NECB outputs
#Created in 2020 by SF
#We are going to combine three previous scripts
#landis_necn.py for NEP through time
#ED_necn_graphs.py for NEP through time and NECB
#landis_necn_harvest_graphs.py for NECB

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
variables =["NEEC"]#["C_DeadWood"]#NEEC, SOMTC

#Much of this can probably be automated but let's start here

#################################################################
#                 END USER INPUT                                #
#################################################################

#START WITH LANDIS NEP


#Create main directory to save images created

odir = "C:\\Users\\sflanagan\\desktop\\model_comp_paper\\images\\necn_imgs"

if os.path.exists(odir):
    shutil.rmtree(odir)
os.makedirs(odir)

print "starting LANDIS NEP plots"  
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
    plt.ylabel("MgC/ha")
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
    plt.ylabel("Net ecosystem productivity MgC/ha)")
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
        lst[l,i,:] /= len(num_list)
        t = df["Time"]
    
        #ax.plot(t,lst[l,i,:], label=abbrvs_list[i],marker=marker_list[i],color="black",markevery=5)
        ax.plot(t,lst[l,i,:]/100*-1,label=abbrvs_list[i],linestyle=style_list[i],color=color_list[i])
        print "scenario " + scen_list[i] + " mean " + str(np.mean(lst[l,i,:]))
    box = ax.get_position()
    #ax.set_position([box.x0, box.y0+.2, box.width, box.height*.8])
    ax.legend(loc='upper center',numpoints=1,mode="expand",ncol=len(scen_list),fontsize=10)#, bbox_to_anchor=(0.5, -0.2))
    plt.savefig(odir+ "\\landis_"+v_name+"_avg_combined.png",dpi=300) 


##############################################################
#Now add the ED part
##############################################################
print "starting ED NEP plot"
inf = "C:\\Users\\sflanagan\\Desktop\\ED_output\\JWJERC\\NEP_graphs_final_for_scripts.csv"
inf2 = "C:\\Users\\sflanagan\\Desktop\\ED_output\\JWJERC\\Harvest_graphs_final_for_scripts.csv"
     
#open first file
df = pd.read_csv(inf)
df2 = pd.read_csv(inf2)


te = df["time"]

variable_names=["Pref","_20f","_50f","_100f","Excf"]

fig, ax = plt.subplots()
plt.xlim(start_time,end_time)
plt.xlabel("Simulation year")
plt.ylabel("Net ecosystem productivity (MgC/ha)")
#plt.ylim(0,max_agb)
print "Generating yearly necn plot"
for i in range(0,len(variable_names)):
    v= df[variable_names[i]]
    ax.plot(te,v,label=abbrvs_list[i],linestyle=style_list[i],color=color_list[i])

ax.legend(loc='lower center',numpoints=1,mode="expand",ncol=len(variable_names),fontsize=10)   
plt.savefig(odir+"\\ED_necn.png",dpi=300)


##############################################################
#Plot the two NEP parts together
##############################################################

print "generating combined NEP graph"

fig, (ax1, ax2) = plt.subplots(2, sharey = 'all')
ax1.set_ylim([-50,10])

#something going on for landis lst so just redo, think dividing too many times
for l in range(0,len(variables)):
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
        lst[l,i,:] /= len(num_list)
        t = df["Time"]

        ax1.plot(t,lst[l,i,:]/100*-1,label=abbrvs_list[i],linestyle=style_list[i],color=color_list[i])

#and ED
df = pd.read_csv(inf)
for i in range (0,5):
    v= df[variable_names[i]]
    ax2.plot(te,v,label=abbrvs_list[i],linestyle=style_list[i],color=color_list[i])

ax1.legend(loc='lower center',numpoints=1,mode="expand",ncol=len(scen_list),fontsize=10)#, bbox_to_anchor=(0.5, -0.2))   
fig.text(0.5, 0.04, 'Simulation year', ha='center', va='center')
fig.text(0.04, 0.5, 'Net ecosystem productivity (MgC/ha)', ha='center', va='center', rotation='vertical')
fig.text(.135,.12, "ED")
fig.text(.135,.61, "LANDIS-II")

plt.savefig("C:\\Users\\sflanagan\\desktop\\model_comp_paper\\images\\final_images\\landis_and_ED_NEP.png", dpi=300)
plt.savefig("C:\\Users\\sflanagan\\desktop\\model_comp_paper\\images\\final_images\\figure4.pdf", dpi=300)
plt.clf()


################################################################################
#Now do LANDIS NECP. This was a pain so just copy and past the code
#As I re-use variables in many of my scripts I think I will just need
#to be careful with the ED and COMBINE part
################################################################################ 

print "starting LANDIS NECB graphs"
#Max values for harvest, so for us 300yrs/every 2 yrs *6 management areas
harv_rows = 900
#No easy way to do arrays of changing size, will need to change if statement below too if alter
hrvp = np.zeros((harv_rows))
hrv20 = np.zeros((harv_rows/10))
hrv50 = np.zeros((harv_rows/25))
hrv100 = np.zeros((harv_rows/50))

#start, end, step of time
start_time = 0
end_time = 301 #add 1
time_step = 2
max_agb = 32000  #g/m2

#Open the necn file and loop through desired scenarios storing values in an array  
lst = np.zeros((len(scen_list),end_time))

for i in range(0,len(scen_list)):
    for s in range (0,len(num_list)): 
        pd.set_option('display.max_colwidth', -1)
        p_name = wdir + scen_list[i]+num_list[s]+"\\NECN-succession-log-short.csv"
        df = pd.read_csv(p_name)
        lst[i,:] += df["NEEC"]

lst /=float(len(num_list))    


#And the harvest files
for j in range(0,len(scen_list)-1):
    for s in range (0,len(num_list)):
        p_name = wdir + scen_list[j]+num_list[s]+"\\Harvest\\Harvest-summary-log.csv"
        nf=pd.read_csv(p_name)
        if j ==0:
            hrvp[:]+=nf["TotalBiomassHarvested"]
        elif j==1:
            hrv20[:]+=nf["TotalBiomassHarvested"]
        elif j==2:
            hrv50[:]+=nf["TotalBiomassHarvested"]
        elif j==3:
            hrv100[:]+=nf["TotalBiomassHarvested"]

#average harvest but also convert units to NECB units (mult by .04)
hrvp/=float(len(num_list))
hrv20/=float(len(num_list))
hrv50/=float(len(num_list))
hrv100/=float(len(num_list))

hrvp*=.04
hrv20*=.04
hrv50*=.04
hrv100*=.04

#new arrays for plotting
time = np.zeros((end_time/time_step+1))
nee = np.zeros((len(scen_list),end_time/time_step+1))
hrvt = np.zeros((len(scen_list),end_time/time_step+1))

#probably can combine but do all seperate for now
for a in range(0,end_time,time_step):
    time[a/time_step] = a


fig, ax = plt.subplots()
plt.xlim(start_time,end_time)
for f in range(0,len(scen_list)):
    adder = 0
    for b in range(0,end_time):
        adder += lst[f,b]
        if b%time_step==0 and b>0:
            nee[f,b/time_step] += adder
    #print adder
    #print nee[f,:]
    ax.plot(time,-1.0*nee[f,:]/100, label=abbrvs_list[f],linestyle=style_list[f],color=color_list[f])

plt.title("Cumulative NECB Modeled by scenario")
plt.xlabel("Simulation Year (yr)")
plt.ylabel("NECB (MgC/ha)")
ax.legend(loc='lower center',numpoints=1,mode="expand",ncol=len(scen_list),fontsize=10)
plt.savefig(odir+ "\\landis_nee_only.png") 
   
#print nee[1,30]
#print time[30]
#print nee.shape
#print time.shape


#boy this section is ugly, fix if have time.  NOTE DID.  Still not universal for can change time_step
def fill_zeros_with_last(arr):
    prev = np.arange(len(arr))
    prev[arr == 0] = 0
    prev = np.maximum.accumulate(prev)
    return arr[prev]


plt.clf()
fig, ax = plt.subplots()        
for f in range(0,len(scen_list)):
    adder = 0
    if f==0:
        for b in range(0,harv_rows):
            adder += hrvp[b]
            if b%(6)==0:
                hrvt[f,b/6*2/time_step] = adder
    if f==1:
        for b in range(0,harv_rows/10):
            adder += hrv20[b]
            if b%6==0 and b>0:
                hrvt[f,b/6*20/time_step] = adder
    if f==2:
        for b in range(0,harv_rows/25):
            adder += hrv50[b]
            if b%6==0 and b>0:
                hrvt[f,b/6*50/time_step] = adder
    if f==3:
        for b in range(0,harv_rows/50):
            adder += hrv100[b]
            if b%6==0 and b>0:
                hrvt[f,b/6*100/time_step] = adder
    hrvt[f,((end_time-1)/time_step)]=adder
    #print adder
    #print hrvt[f,:]
    hrvt[f,:] = fill_zeros_with_last(hrvt[f,:])
    #print hrvt[f,:]
    ax.plot(time,-1*hrvt[f,:]/100, label=abbrvs_list[f],linestyle=style_list[f],color=color_list[f])
    
plt.title("Cumulative Harvest by scenario")
plt.xlabel("Simulation Year (yr)")
plt.ylabel("Harvest (MgC/m2)")
ax.legend(loc='lower center',numpoints=1,mode="expand",ncol=len(scen_list),fontsize=10)
plt.savefig(odir+ "\\landis_harvest_only.png") 
       


#and combined
plt.clf()
fig, ax = plt.subplots()
plt.title("Cumulative NEEC by scenario")
plt.xlabel("Simulation Year (yr)")
plt.ylabel("NEEC (gC/m2)")

for h in range(0,len(scen_list)):
    ax.plot(time,hrvt[h,:]+nee[h,:], label=abbrvs_list[h],linestyle=style_list[h],color=color_list[h])#marker=marker_list[h]
ax.axhline(y=0,color="black")
ax.legend(loc='upper center',numpoints=1,mode="expand",ncol=len(scen_list),fontsize=10)
plt.savefig(odir+ "\\landis_combined.png") 

#and flipped
plt.clf()
fig, ax = plt.subplots()
plt.title("Cumulative NECB by scenario")
plt.xlabel("Simulation Year (yr)")
plt.ylabel("NECB (MgC/ha)")

for h in range(0,len(scen_list)):
    ax.plot(time,-1.0*(hrvt[h,:]+nee[h,:])/100, label=abbrvs_list[h],linestyle=style_list[h],color=color_list[h])#marker=marker_list[h]
ax.axhline(y=0,color="black")
ax.legend(loc='lower center',numpoints=1,mode="expand",ncol=len(scen_list),fontsize=10)
plt.savefig(odir+ "\\landis_combined_necb.png") 


#and as subplots
plt.clf()
fix, ax = plt.subplots(nrows=3, ncols=1, sharex ='all', figsize=(8,8))
ax1 = ax[0]
ax1.set_ylim(-100,600)
ax1.text(10, 400, "A", size=16)
ax2 = ax[1]
ax2.text(10, -500, "B", size=16)
ax3 = ax[2]
ax3.text(10, -180, "C", size=16)

ax1.set_title("Cumulative model calculated net ecosystem productivity")
ax2.set_title("Cumulative biomass removed from fire")
ax3.set_title("Cumulative net ecosystem carbon balance")

plt.xlabel("Simulation year")
plt.xlim(0,300)
ax2.set_ylabel("MgC/ha")
for h in range (0, len(scen_list)):
    mult=.81
    if h==0:
        mult=.3
    ax1.plot(time,-1.0*nee[h,:]/100, label=abbrvs_list[h],linestyle=style_list[h],color=color_list[h])
    ax2.plot(time,-1*hrvt[h,:]*mult/100, label=abbrvs_list[h],linestyle=style_list[h],color=color_list[h])
    ax3.plot(time,-1*(hrvt[h,:]*mult+nee[h,:])/100, label=abbrvs_list[h],linestyle=style_list[h],color=color_list[h])
    ax1.legend(loc='upper center',numpoints=1,mode="expand",ncol=len(scen_list),fontsize=10)

fig.text(0.4, 0.5, 'NECB (gC/m2)', ha='center', va='center', rotation='vertical')
plt.savefig(odir+ "\\landis_subplots.png") 


#and do non cumulative
plt.clf()   
fig, ax = plt.subplots()
time2 = np.zeros((end_time))
#plt.title("Yearly NEP by scenario")
plt.xlabel("Simulation year")

plt.ylabel("Net ecosystem productivity (MgC/ha)")
for w in range (0,end_time):
    time2[w]=w
for f in range (0,len(scen_list)):
    ax.plot(time2,-1*lst[f,:]/100, label=abbrvs_list[f],linestyle=style_list[f],color=color_list[f])
ax.legend(loc='lower center',numpoints=1,mode="expand",ncol=len(scen_list),fontsize=10)
plt.savefig(odir+ "\\landis_yearly.png") 


################################################################################
#Now do ED NECP
################################################################################ 
print "starting ED NECB graphs"

df = pd.read_csv(inf)
df2 = pd.read_csv(inf2)

plt.clf()
fix, ax = plt.subplots(nrows=3, ncols=1, sharex ='all', figsize=(8,8))
ax1 = ax[0]
ax1.set_ylim(-100,1000)
ax1.text(10, 400, "A", size=16)
ax2 = ax[1]
ax2.text(10, -500, "B", size=16)
ax3 = ax[2]
ax3.text(10, -180, "C", size=16)

ax1.set_title("Cumulative model calculated net ecosystem productivity")
ax2.set_title("Cumulative biomass removed from fire")
ax3.set_title("Cumulative net ecosystem carbon balance")

plt.xlabel("Simulation year")
plt.xlim(0,300)
ax2.set_ylabel("MgC/ha")
v1 = ["sPref","s_20f","s_50f","s_100f","sExcf"]
v2 = ["pf_sumf","_20f_sum", "_50f_sum", "_100f_sum","sf_sumf"]	
v3 = ["fp","f20","f50","f100","fs"]
for h in range (0, len(variable_names)):
    n = df[v1[h]]
    ha = df2[v2[h]]
    f = df2[v3[h]]
    ax1.plot(t,n, label=abbrvs_list[h],linestyle=style_list[h],color=color_list[h])
    ax2.plot(t,ha, label=abbrvs_list[h],linestyle=style_list[h],color=color_list[h])
    ax3.plot(t,f, label=abbrvs_list[h],linestyle=style_list[h],color=color_list[h])
    ax1.legend(loc='upper center',numpoints=1,mode="expand",ncol=len(variable_names),fontsize=10)

fig.text(0.4, 0.5, 'NECB (gC/m2)', ha='center', va='center', rotation='vertical')
plt.savefig(odir+ "\\ed_subplots_necn.png", dpi=300) 

################################################################################
#LANDIS and ED NECP Combined
################################################################################ 
print "starting combined NECP plot"

fig, (ax1, ax2) = plt.subplots(2, sharey = 'all')
#ax1.set_ylim([-50,10])
for h in range (0,5):
    #ED needs
    n = df[v1[h]]
    ha = df2[v2[h]]
    f = df2[v3[h]]
    #Landis needs
    mult=.81
    if h==0:
        mult=.3
    ax1.plot(time,-1*(hrvt[h,:]*mult+nee[h,:])/100, label=abbrvs_list[h],linestyle=style_list[h],color=color_list[h])
    ax2.plot(t,f, label=abbrvs_list[h],linestyle=style_list[h],color=color_list[h])

ax1.legend(loc='upper center',numpoints=1,mode="expand",ncol=len(scen_list),fontsize=10)#, bbox_to_anchor=(0.5, -0.2))   
fig.text(0.5, 0.04, 'Simulation year', ha='center', va='center')
fig.text(0.04, 0.5, 'Cumulative NECB (MgC/ha)', ha='center', va='center', rotation='vertical')
fig.text(.135,.41, "ED")
fig.text(.135,.8, "LANDIS-II")

plt.savefig("C:\\Users\\sflanagan\\desktop\\model_comp_paper\\images\\final_images\\landis_and_ED_NECB.png", dpi=300)
plt.savefig("C:\\Users\\sflanagan\\desktop\\model_comp_paper\\images\\final_images\\figure5.pdf", dpi=300)
plt.clf()

print "Script complete"