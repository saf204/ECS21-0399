#Script to help analyze LANDIS-II biomass outputs
#Created by Steve Flanagan, 2017
#Plots of biomass (avg) will be saved to a new folder "temp_imgs_multruns"
#stored in whatever is specified by the user as the wdir
#If outputs are not renamed they will be overwritten 
#Might get warnings if you have "temp_imgs_multruns open - just run again

#import arcpy
import matplotlib.pyplot as plt
import pandas as pd
import os, shutil 
import numpy as np
from osgeo import gdal


#################################################################
#                  START USER INPUT                             #
#################################################################
#Set the output path
wdir = "C:\\Users\\sflanagan\\desktop\\landis_runs\\100m_final\\Output\\"

#List the scenarios you want to examine
#scen_list = ["pf_300yrs","wf_20_300yrs","wf_100_300yrs","wf_50_300yrs","nf_300yrs"]#"wfs_1000yrs"]
#scen_list = ["pf_300yrs","wf_20_allsame_300yrs","wf_50_allsame_300yrs","wf_100_allsame_300yrs","nf_300yrs"]
scen_list = ["pf_ottmer_300yrs","wf_20_ottmer_300yrs","wf_50_ottmer_300yrs","wf_100_ottmer_300yrs","nf_300yrs"]
#and the numbers for the runs
num_list =["1","2","3","4","5"]

#start, end, step of time
start_time = 0
end_time = 301 #add 1
time_step = 5 #of output file
max_agb = 30000  #g/m2
eco_max = 20000


#Number of regions and species
num_regions = 9
species =["pinupalu","quervirg","nyssbifl","pinuelli","querfalc","querhemi",
          "querinca","querlaev","quernigr","querstel","quermarg",
          "taxoasce"]

### ADDED FOR SUBPLOITS, can probably ignore - 5 scenarios, 2 species, 61 values right now
splot_arry = np.zeros((5,2,61))
#Much of this can probably be automated but let's start here

#################################################################
#                 END USER INPUT                                #
#################################################################

#Create main directory to save images created
odir = wdir+"temp_imgs_multruns"
if os.path.exists(odir):
    shutil.rmtree(odir)
os.makedirs(odir)

  
#Open the spp-log file and loop through desired scenarios
for i in range(0,len(scen_list)):
    print "Generating plots for " + scen_list[i]
    lst = np.zeros((12,61))
    mnmx = np.zeros((12,61,5))
    
    #Create subdirectories if needed
    if len(scen_list)==1 and i==0:
        oedir = odir+"\\ecoregions"
        os.makedirs(oedir)
    else:
        odir = wdir+"temp_imgs_multruns" + "\\" + scen_list[i]
        oedir = odir+"\\ecoregions"
        os.makedirs(odir)
        os.makedirs(oedir)

    #Open the file set 
    for s in range(0,len(num_list)):

        pd.set_option('display.max_colwidth', -1)
        p_name = wdir + scen_list[i]+ num_list[s] + "\\spp-biomass-log.csv"
        df = pd.read_csv(p_name)
     
        #Remove ecoregions with NaN values
        ff = df[df.NumActiveSites != 0].astype(float, raise_on_error=False)

        #Get weights that we will need later
        total_sites =0 
        for z in range (0, num_regions):
            num_s = ff.iat[z,2]
            total_sites+= num_s

    
        #Go through by species and get AGB
        for j in range(0,len(species)):
        
            s_name = "AboveGroundBiomass_" +species[j]

            # Species agb is actually a string so convert it to numeric
            # And then reinsert in the dataframe
            f2 = pd.to_numeric(ff[s_name], errors='coerce')
            ff[s_name]=f2
        
            #Get time and biomass for each ecoregion
            for k in range (1,num_regions+1):

                r_name = "eco" +str(k)
                rf = ff[ff['EcoName'].str.contains(r_name)]
                
                rf.plot("Time",s_name)
                plt.ylabel("AGB (g/m2)")
                #plt.ylim(0,eco_max)
                plt.xlabel("Time (yr)")
                plt.title(s_name + " " + r_name)
                plt.savefig(oedir+"\\"+s_name+"_"+r_name+"_"+num_list[s]+".png")
                plt.close()
                
            #Get time and total biomass summed over all ecoregions
            #Need to weight by number of sites
            ff[s_name+'weighted_agb'] = ff['NumActiveSites']*ff[s_name]/float(total_sites)
            nf = ff.groupby(["Time"])[s_name+"weighted_agb"].sum().reset_index()
            ws = nf[s_name+"weighted_agb"]
            lst[j,:] += ws
            mnmx[j,:,s] = ws
            
    #Now Plot by total biomass by species
    t=nf["Time"]
    for p in range(0,len(species)):
        for f in range(0,end_time/time_step+1):
            vy = lst[p,f]
            lst[p,f] = vy/5.0
       
    plt.clf()
    

    for q in range(0,len(species)):
        fig, ax = plt.subplots()
        plt.ylabel("AGB (g/m2)")
        plt.xlabel("Time (yr)")
        plt.ylim(0,10000)
        s_name = species[q]
      
        ax.plot(t,lst[q,:], label=species[q])
        #plt.show()

        plt.savefig(odir+ "\\"+s_name+".png")
        plt.close()

        print "scenario " +scen_list[i] + " species " +species[q] +" at time zero " + str(lst[q,0])  
    




    #one figure with all species
    plt.clf()
    fix, ax = plt.subplots(nrows=4, ncols=3, sharex ='all' , sharey = 'all',figsize=(15,15))
    
    plt.ylabel("AGB (g/m2)")
    plt.xlabel("Time (yr)")
    plt.ylim(0,10000)
    for q in range (0,len(species)):    
        ax[q%4,q%3].plot(t,lst[q,:], label=species[q])
        ax[q%4,q%3].set_title(species[q])
    plt.savefig(odir+ "\\12.png")
    plt.clf()






    #And do them all on one graph
    plt.close('all')
    fig, ax = plt.subplots()
    plt.ylabel("AGB (g/m2)")
    plt.xlabel("Simulation Year (yr)")
    plt.title("AGB values seperated by longleaf and all other species")
    plt.xlim(start_time,end_time)
    plt.ylim(0,max_agb)
    #with min and max
    nmax = np.zeros((12,61))
    nmin = np.zeros((12,61))
    amtr = np.zeros((12,61))


    #Only put this in to get min and mac
    for b in range(0,12):
        for v in range(0,61):
            max = 0
            min = 10000000
            gave = 0
            for l in range(0,5):
                getV = mnmx[b,v,l]
                if getV > max:
                    max = getV
                if getV < min:
                    min = getV
                gave += getV
            nmax[b,v] = max
            nmin[b,v] = min
            amtr[b,v] = gave/5.0
            #print max, min

    for q in range(0,len(species)):    
       

        if q==0:
            ax.plot(t,lst[q,:], label="longleaf",color="black",marker="v")
            ax.plot(t,nmax[q,:], label=species[q]+ "max")
            ax.plot(t,nmin[q,:], label=species[q]+"min")
            #ax.plot(t,amtr[q,:], label=species[q]+"avg")
            splot_arry[i,q,:]=lst[q,:]
        else:
            w = lst[q,:]
            z+=w
            r = nmax[q,:]
            s+=r
            c = nmin[q,:]
            p+=c
    ax.plot(t,z, label="other species",color="black",marker="s") 
    ax.plot(t,s, label="other species"+"max") 
    ax.plot(t,p, label="other species"+"min")
    splot_arry[i,1,:] = z
    # Put a legend to the right of the current axis
    box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='upper right',numpoints=1,fontsize=10)#, bbox_to_anchor=(0.5, -0.2))
    plt.savefig(odir+ "\\combined.png")
     
    plt.close()
    



#let's play with subplots now
#Unfortunately didn't put all in one big array like I did for necn_harvest_graphs
#but this runs quick so add a subplot matrix to save above values
fig, ax = plt.subplots(nrows=3, ncols=2, sharex = 'all', sharey='all')
ax1 = ax[0,0]
ax2 = ax[0,1]
ax3 = ax[1,0]
ax4 = ax[1,1]
ax5 = ax[2,0]

'''
ax1.set_title("2yr RxFire")
ax2.set_title("20yr WF")
ax3.set_title("50yr WF")
ax4.set_title("100yr WF")
ax5.set_title("Fire Exclusion")
'''
ax1.text(25, 250, "A", size=16)
ax2.text(25, 250, "B", size=16)
ax3.text(25, 250, "C", size=16)
ax4.text(25, 250, "D", size=16)
ax5.text(25, 250, "E", size=16)


ax[-1,-1].axis('off')


plt.ylabel("Aboveground biomass (Mg/ha)")
plt.xlabel("Simulation year")
#plt.title("AGB values seperated by longleaf and all other species")
plt.xlim(start_time,end_time)
plt.ylim(0,max_agb/100)

for i in range(0,5):
    if i==0:
        ax1.plot(t,splot_arry[i,0,:]/100, label="longleaf",color='#377eb8')
        ax1.plot(t,splot_arry[i,1,:]/100, label="other species",color='#ff7f00') 
    elif i==1:
        ax2.plot(t,splot_arry[i,0,:]/100, label="longleaf",color='#377eb8')
        ax2.plot(t,splot_arry[i,1,:]/100, label="other species",color='#ff7f00') 
        ax2.legend(loc='upper right',numpoints=1,fontsize=10)
    elif i==2:
        ax3.plot(t,splot_arry[i,0,:]/100, label="longleaf",color='#377eb8')
        ax3.plot(t,splot_arry[i,1,:]/100, label="other species",color='#ff7f00') 
    elif i==3:
        ax4.plot(t,splot_arry[i,0,:]/100, label="longleaf",color='#377eb8')
        ax4.plot(t,splot_arry[i,1,:]/100, label="other species",color='#ff7f00') 
    elif i==4:
        ax5.plot(t,splot_arry[i,0,:]/100, label="longleaf",color='#377eb8')
        ax5.plot(t,splot_arry[i,1,:]/100, label="other species",color='#ff7f00') 
  
        
fig.text(0.5, 0.04, 'Simulation year', ha='center', va='center')
fig.text(0.04, 0.5, 'Aboveground biomass (Mg/ha)', ha='center', va='center', rotation='vertical')
plt.savefig(wdir+"temp_imgs_multruns"+"\\subplotcombined.png", dpi=300)
plt.savefig(wdir+"temp_imgs_multruns"+"\\Figure3.pdf", dpi=300)
     
plt.close()


print "Script complete"

       
       
     