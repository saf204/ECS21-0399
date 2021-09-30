#Script to help analyze LANDIS-II biomass outputs
#Created by Steve Flanagan, 2017
#Plots of biomass (avg) will be saved to a new folder "hw_sw_imgs"
#stored in whatever is specified by the user as the wdir
#If outputs are not renamed they will be overwritten 
#Might get warnings if you have "hw_sw_imgs open - just run again

#import arcpy
import matplotlib.pyplot as plt
import pandas as pd
import os, shutil 


#################################################################
#                  START USER INPUT                             #
#################################################################
#Set the output path
wdir = "C:\\Users\\sflanagan\\desktop\\landis_runs\\100m_final\\Output\\"
#"C:\\Users\\sflanagan\\desktop\\landis_runs\\100m\\Output\\final_hopefully\\"

#List the scenarios you want to examine
scen_list = ["pf_300yrs1","wf_20_300yrs1","wf_100_300yrs1","wf_50_300yrs1","nf_300yrs1","wf_100_allsame_300yrs2","wfs_1000yrs1"] 

#start, end, step of time
start_time = 0
end_time = 301 #add 1
time_step = 10
max_agb = 27000  #g/m2
eco_max = 10000  #for adjusting eco max agb without changing combined graph

#Number of regions and species
num_regions = 9
species =["pinupalu","quervirg","nyssbifl","pinuelli","querfalc","querhemi",
          "querinca","querlaev","quernigr","querstel","quermarg",
          "taxoasce"]

#Much of this can probably be automated but let's start here

#################################################################
#                 END USER INPUT                                #
#################################################################

#Create main directory to save images created
odir = wdir+"hw_sw_imgs"
if os.path.exists(odir):
    shutil.rmtree(odir)
os.makedirs(odir)

  
#Open the spp-log file and loop through desired scenarios
for i in range(0,len(scen_list)):
    print "Generating plots for " + scen_list[i]
    
    #Create subdirectories if needed
    if len(scen_list)==1 and i==0:
        oedir = odir+"\\ecoregions"
        os.makedirs(oedir)
    else:
        odir = wdir+"hw_sw_imgs" + "\\" + scen_list[i]
        oedir = odir+"\\ecoregions"
        os.makedirs(odir)
        os.makedirs(oedir)

    #Open the file 
    pd.set_option('display.max_colwidth', -1)
    p_name = wdir + scen_list[i]+"\\spp-biomass-log.csv"
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

        # Species agb is actually a sting so convert it to numeric
        # And then reinsert in the dataframe
        f2 = pd.to_numeric(ff[s_name], errors='coerce')
        ff[s_name]=f2
        
        #Get time and biomass for each ecoregion
        for k in range (1,num_regions+1):

            r_name = "eco" +str(k)
            rf = ff[ff['EcoName'].str.contains(r_name)]

            rf.plot("Time",s_name)
            plt.ylabel("AGB (g/m2)")
            plt.ylim(0,eco_max)
            plt.xlabel("Time (yr)")
            plt.title(s_name + " " + r_name)
            plt.savefig(oedir+"\\"+s_name+r_name+".png")
            plt.close()

        #Get time and total biomass summed over all ecoregions
        #Need to weight by number of sites
        ff[s_name+'weighted_agb'] = ff['NumActiveSites']*ff[s_name]/float(total_sites)
        nf = ff.groupby(["Time"])[s_name+"weighted_agb"].sum().reset_index()
        
        ##########################
        #temp removal of start
        #nf = nf[nf.Time !=0]
        ##########################

        nf.plot("Time",s_name+"weighted_agb")
        plt.ylim(0,max_agb)
        plt.ylabel("AGB (g/m2)")
        plt.xlabel("Time (yr)")
        plt.savefig(odir+ "\\"+s_name+".png")
        plt.close()

    
    #Now do them all on one graph
    plt.clf()
    fig, ax = plt.subplots()
    plt.xlim(start_time,end_time)
    plt.ylim(0,max_agb)
    plt.ylabel("AGB (g/m2)")
    plt.xlabel("Time (yr)")
    
    for j in range(0,len(species)):

        s_name = "AboveGroundBiomass_" +species[j]
         
        nf = ff.groupby(["Time"])[s_name+"weighted_agb"].sum().reset_index()

        ############################
        #temp removal of start
        #nf = nf[nf.Time !=0]
        ############################

        #Need slices this time
        if j==0:
            t = nf["Time"]
            v = nf[s_name+"weighted_agb"]
            ax.plot(t,v, label = species[j])
        else:
            w = nf[s_name+"weighted_agb"]
            z +=w
   
    ax.plot(t,z, label = "hardwoods")
    # Put a legend to the right of the current axis
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(odir+ "\\combined.png")


    #And also ecoregions
    for k in range (1,num_regions+1):
        plt.close()
        fig, ax = plt.subplots()
        plt.xlim(start_time,end_time)
        plt.ylim(0,max_agb)
        plt.ylabel("AGB (g/m2)")
        plt.xlabel("Time (yr)")

        r_name = "eco" +str(k)
        rf = ff[ff['EcoName'].str.contains(r_name)]

        for j in range(0,len(species)):

            s_name = "AboveGroundBiomass_" +species[j]

            #Need slices this time
            t = rf["Time"]
            v = rf[s_name]
            ax.plot(t,v, label = species[j])

        # Put a legend to the right of the current axis
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.savefig(oedir+ "\\"+r_name+"_combined.png")


print "Script complete"

        
       
       
       


   


