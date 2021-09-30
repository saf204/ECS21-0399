#Script to help analyze LANDIS-II harvest outputs
#Created by Steve Flanagan, 2017
#Plots of biomass harvest (avg) will be saved to a new folder "harvest_imgs"
#stored in whatever is specified by the user as the wdir
#If outputs are not renamed they will be overwritten 
#Might get warnings if you have "harvest_imgs open - just run again

#import arcpy
import matplotlib.pyplot as plt
import pandas as pd
import os, shutil 


#################################################################
#                  START USER INPUT                             #
#################################################################
#Set the output path
wdir = "C:\\Users\\sflanagan\\desktop\\landis_runs\\100m_final\\Output\\"#"C:\\Users\\sflanagan\\desktop\\landis_runs\\100m\\Output\\final_hopefully\\"

#List the scenarios you want to examine
scen_list = ["pf_500yrs4","pf_500yrs2"] #["base_case","rep_0"]  

#start, end, step of time
start_time = 0
end_time = 301 #add 1
max_agb = 2000  #Now really Mg removed

#Number of management areas and species
num_areas = 5
species =["quervirg","pinupalu","nyssbifl","pinuelli","querfalc","querhemi",
          "querinca","querlaev","quermarg","quernigr","querstel",
          "taxoasce"]

#Much of this can probably be automated but let's start here

#################################################################
#                 END USER INPUT                                #
#################################################################

#Create main directory to save images created
odir = wdir+"harvest_imgs"
if os.path.exists(odir):
    shutil.rmtree(odir)
os.makedirs(odir)

  
#Open the harvest-summary-log file and loop through desired scenarios
for i in range(0,len(scen_list)):
    print "Generating plots for " + scen_list[i]
    
    #Create subdirectories if needed
    if len(scen_list)==1 and i==0:
        print "Plots for one scenario"
    else:
        odir = wdir+"harvest_imgs" + "\\" + scen_list[i]
        os.makedirs(odir)

    #Open the file 
    pd.set_option('display.max_colwidth', -1)
    p_name = wdir + scen_list[i]+"\\Harvest\\Harvest-summary-log.csv"
    df = pd.read_csv(p_name)

    #just because using code and this will help not miss a change
    ff=df
     
    #Go through by management area and get biomass harvested
    for k in range(1,num_areas+1):
        
        rf = ff[ff.ManagementArea==k]
        
        #Want all on one graph
        plt.clf()
        fig, ax = plt.subplots()
        plt.xlim(start_time,end_time)
        plt.ylim(0,max_agb)
        plt.ylabel("Removed (Mg)")
        plt.xlabel("Time (yr)")

        #Get time and biomass harvest for each management area
        for j in range (0,len(species)):

            s_name = "BiomassHarvestedMg_" +species[j]
            
            #Need slices this time
            t = rf["Time"]
            v = rf[s_name]
            ax.plot(t,v, label = species[j])
            
        # Put a legend to the right of the current axis
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.savefig(odir+ "\\managementArea_"+str(k)+".png") 
        plt.close()


print "Script complete"

        
       
       
       


   


