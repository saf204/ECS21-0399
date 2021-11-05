#Script to help analyze LANDIS-II and ED NEE and Eddy Flux measurements at Jones Center
#Created by Steve Flanagan, 2019
#Graphs will be saved to a new folder "temp_imgs" stored in whatever is specified by the user as the wdir
#If outputs are not renamed they will be overwritten 
#Might get warnings if you have "temp_imgs open - just run again

#import arcpy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, shutil 

##THIS IS NOT AUTOMATED RIGHT NOW - I AM GOING TO SPECIFIC DIRECTORIES FOR THE FILES I NEED
##SF 4/9/2020

scenario = "flux_2009_to2013_1"

#Create main directory to save images created
wdir = "C:\\Users\\sflanagan\\desktop\\flux\\"
odir = "C:\\Users\\sflanagan\\desktop\\model_comp_paper\\images\\flux_imgs"
if os.path.exists(odir):
    shutil.rmtree(odir)
os.makedirs(odir)

#open all the files
lname = "C:\\Users\\sflanagan\\desktop\\landis_runs\\flux\\Output\\"  + scenario + "\\NECN-succession-monthly-log.csv"
ldf = pd.read_csv(lname)
fdf = pd.read_csv(wdir+"JC010-01-exchange.csv")
ename = "C:\\Users\\sflanagan\\Desktop\\ED_output\\JWJERC\\flux_compare_file.csv"
edf = pd.read_csv(ename)


'''
The Following part of the code was used to look at the yearly average, not the five year time interval
Changes were also made in LANDIS to match the ecoregions used, hence the range is 4-6 to match ecoregions
4 and 5 where the three towers were positioned. This will run if you un-comment it, but be carefule with
those changes 


#Start manipulating the flux data to get to yearly and monthly values, five years of unique values
flux_modified = np.zeros((3,5,12))
for tower in range (1,4):
    fdft = fdf.loc[fdf['Site'] == tower]
    for year in range (2009,2014):
        fdfy = fdft.loc[fdft['Year']==year]
        for month in range (1,13):
            fdfm = fdfy.loc[fdfy['Month']==month]
            flux_modified[tower-1,year-2009,month-1] = fdfm['NEE'].mean()*8.63 #converion to landis units, see notebook



#and get the first five years of the monthly landis data, keeping ecoregions seperate for now
landis_modified = np.zeros((2,5,12))
for ecoregion in range (4,6):
    ldft = ldf.loc[ldf['EcoregionIndex'] == ecoregion]
    for year in range (1,6):
        ldfy = ldft.loc[ldft['Time']==year]
        for month in range (1,13):
            ldfm = ldfy.loc[ldfy['Month']==month]
            landis_modified[ecoregion-4,year-1,month-1] = ldfm['avgNEE']

#print "towers have " + str(flux_modified[:,4,4])
#print "landis has " + str(landis_modified[:,4,:])

landis_yrmean = landis_modified.mean(axis=1)
flux_yrmean = flux_modified.mean(axis=1)

month = [1,2,3,4,5,6,7,8,9,10,11,12]
fig, ax = plt.subplots()
for eco in range (0,2):
    ax.plot(month,landis_yrmean[eco,:],label=eco)
    
for tower in range (0,3):
    ax.plot(month,flux_yrmean[tower,:],color="black",label=tower)
plt.legend()
plt.show()
plt.clf()
plt.close()
'''

#These images are used for the publication. 
#This grabs the yearly flux data - 3 towers, 12 months for 5 years   
flux_modified = np.zeros((3,60))
for tower in range (1,4):
    fdft = fdf.loc[fdf['Site'] == tower]
    count=0
    for year in range (2009,2014):
        fdfy = fdft.loc[fdft['Year']==year]
        for month in range (1,13):
            fdfm = fdfy.loc[fdfy['Month']==month]
            flux_modified[tower-1,count] = fdfm['NEE'].mean()*8.63*44.0/12.0 #converion to landis units, see notebook
            count+=1



#This grabs the yearly LANDIS data, 9 ecoregions with 12 months for 5 years   
landis_modified = np.zeros((9,60))
for ecoregion in range (0,9):
    ldft = ldf.loc[ldf['EcoregionIndex'] == ecoregion]
    count=0
    for year in range (1,6):
        ldfy = ldft.loc[ldft['Time']==year]
        for month in range (1,13):
            ldfm = ldfy.loc[ldfy['Month']==month]
            landis_modified[ecoregion,count] = ldfm['avgNEE']
            count+=1


#Plot ALL towers and ecoregions            
month = [1,2,3,4,5,6,7,8,9,10,11,12,12,14,15,16,17,18,19,20,21,22,23,24,25,26,27,
         28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,
         53,54,55,56,57,58,59,60]
fig, ax = plt.subplots()
for eco in range (0,9):
    ax.plot(month,landis_modified[eco,:],label=eco)
    
for tower in range (0,3):
    ax.plot(month,flux_modified[tower,:],color="black",label=tower)
plt.legend()
plt.savefig(odir+"\\landis_monthly_all_towers_and_ecoregions.png")
#plt.show()
plt.clf()
plt.close()


#Plot the AVERAGE of ALL towers and ecoregions
#Average of eco regions and tower
landis_ecomean = landis_modified.mean(axis=0)
flux_towermean = flux_modified.mean(axis=0)
fig, ax = plt.subplots()
ax.set_ylim([-150,250])
ax.plot(month,landis_ecomean[:],label="Model",color="black")   
ax.plot(month,flux_towermean[:],color="black",label="Tower",linestyle="dashed")
plt.ylabel(' gC/m$^2$')
plt.xlabel("January 2009 - Devember 2013 by Month")
plt.title("Monthly Model Predicted and Flux Tower NEE")
plt.legend(loc=3)
plt.savefig(odir+"\\landis_monthly_average_of_all_towers_and_ecoregions.png")
#plt.show()
plt.clf()
plt.close()


#Plot the YEARLY value of all towers and ecoregions
landisyr = np.zeros((5))
fluxyr = np.zeros((5))
yr=np.zeros((5))
count=0
for x in range (2009,2014):
    yr[count] = x
    count+=1
    
for x in range (0,60):
    landisyr[x/12] += landis_ecomean[x]
    fluxyr[x/12] += flux_towermean[x]

landisyr[:]/12.0
fluxyr[:]/12.0

print "LANDIS average NEE all ecoregions " + str(landisyr.mean(axis=0))
#print fluxyr

fig, ax = plt.subplots()
ax.ticklabel_format(useOffset=False,style="plain")
ax.xaxis.set_ticks(np.arange(2009, 2014, 1))
ax.plot(yr,landisyr[:],label="Model")   
ax.plot(yr,fluxyr[:],color="black",label="Tower")
ax.axhline(y=landisyr.mean(axis=0),color="blue",linestyle="dashed",label="Model Average")   
ax.axhline(y=fluxyr.mean(axis=0),color="black",linestyle="dashed",label="Tower Average") 
plt.ylabel(' gC/m$^2$yr')
plt.xlabel("Year")
plt.title("Yearly Model Predicted and Flux Tower NEE")
plt.legend(loc="lower left")
plt.savefig(odir+"\\landis_yearly_all_ecoregions.png")
#plt.show()

plt.clf()
plt.close()


##################################################################
#REPEAT for only the two LANDIS ecoregions we want
##################################################################

landis_modified = np.zeros((2,60))
for ecoregion in range (3,5):
    ldft = ldf.loc[ldf['EcoregionIndex'] == ecoregion]
    count=0
    for year in range (1,6):
        ldfy = ldft.loc[ldft['Time']==year]
        for month in range (1,13):
            ldfm = ldfy.loc[ldfy['Month']==month]
            landis_modified[ecoregion-3,count] = ldfm['avgNEE']
            count+=1

month = [1,2,3,4,5,6,7,8,9,10,11,12,12,14,15,16,17,18,19,20,21,22,23,24,25,26,27,
         28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,
         53,54,55,56,57,58,59,60]
fig, ax = plt.subplots()

for eco in range (0,2):
    ax.plot(month,landis_modified[eco,:])
for tower in range (0,3):
    ax.plot(month,flux_modified[tower,:],color="black",label=tower)
plt.legend()
plt.savefig(odir+"\\landis_monthly_two_ecoregions.png")
#plt.show()
plt.clf()
plt.close()


#Plot the AVERAGE of the twoecoregions
#Average of eco regions and tower
landis_ecomean = landis_modified.mean(axis=0)
flux_towermean = flux_modified.mean(axis=0)
fig, ax = plt.subplots()
ax.set_ylim([-150,250])
ax.plot(month,landis_ecomean[:],label="Model",color="black")   
ax.plot(month,flux_towermean[:],color="black",label="Tower",linestyle="dashed")
plt.ylabel(' gC/m$^2$')
plt.xlabel("January 2009 - Devember 2013 by Month")
plt.title("Monthly Model Predicted and Flux Tower NEE")
plt.legend(loc=3)
plt.savefig(odir+"\\landis_monthly_average_two_ecoregions.png")
#plt.show()
plt.clf()
plt.close()


#Plot the YEARLY value of two ecoregions
landisyr = np.zeros((5))
fluxyr = np.zeros((5))
yr=np.zeros((5))
count=0
for x in range (2009,2014):
    yr[count] = x
    count+=1
    
for x in range (0,60):
    landisyr[x/12] += landis_ecomean[x]
    fluxyr[x/12] += flux_towermean[x]

landisyr[:]/12.0
fluxyr[:]/12.0


fig, ax = plt.subplots()
ax.ticklabel_format(useOffset=False,style="plain")
ax.xaxis.set_ticks(np.arange(2009, 2014, 1))
ax.plot(yr,landisyr[:],label="Model")   
ax.plot(yr,fluxyr[:],color="black",label="Tower")
ax.axhline(y=landisyr.mean(axis=0),color="blue",linestyle="dashed",label="Model Average")   
ax.axhline(y=fluxyr.mean(axis=0),color="black",linestyle="dashed",label="Tower Average") 
plt.ylabel(' gC/m$^2$yr')
plt.xlabel("Year")
plt.title("Yearly Model Predicted and Flux Tower NEE")
plt.legend(loc="lower left")
plt.savefig(odir+"\\landis_yearly_two_ecoregions.png")
#plt.show()

plt.clf()
plt.close()




#####NOW DO ED #####
edvalues = edf['PF_nep1']*-83    #This is what the yearly value would be if that month was representaive 
                             #So, convert from kg/m2 to g but then divide by 12 and change sign for NEE                        
                        

flux_towermean = flux_modified.mean(axis=0)
fig, ax = plt.subplots()
plt.ylim=(-150,250)
ax.plot(month,edvalues,label="Model",color="black")   
ax.plot(month,flux_towermean[:],color="black",label="Tower",linestyle="dashed")
plt.ylabel(' gC/m$^2$')
plt.xlabel("Month")
plt.title("Monthly Model Predicted and Flux Tower NEE")
plt.legend(loc="upper right")
plt.savefig(odir+"\\monthly_ed.png")
#plt.show()

plt.clf()
plt.close()


edyr = np.zeros((5))

for x in range (0,60):
    edyr[x/12] += edvalues[x]
    

edyr[:]/12.0


fig, ax = plt.subplots()
ax.ticklabel_format(useOffset=False,style="plain")
ax.xaxis.set_ticks(np.arange(2009, 2014, 1))
ax.plot(yr,edyr[:],label="Model")   
ax.plot(yr,fluxyr[:],color="black",label="Tower")
ax.axhline(y=edyr.mean(axis=0),color="blue",linestyle="dashed",label="Model Average")  
ax.axhline(y=fluxyr.mean(axis=0),color="black",linestyle="dashed",label="Tower Average") 
plt.ylabel(' gC/m$^2$yr')
plt.xlabel("Year")
plt.title("Yearly Model Predicted and Flux Tower NEE")
plt.legend(loc="lower center")
plt.savefig(odir+"\\yearly_ed.png")
#plt.show()

plt.clf()
plt.close()



#Put both images in one plot

fig, (ax1, ax2) = plt.subplots(2, sharey = 'all')
fig.suptitle("Monthly Model Predicted and Flux Tower NEE")
ax1.text(57,200,"A")
ax2.text(57,200, "B")
#ax1.set( ylabel =' Monthly gC/m$^2$')
ax1.set( ylabel =' Monthly MgC/ha')
plt.xlabel("Simulation month")

#DIVIDING BY 100 for Mg/ha instead of G/m2
for q in range (0,2):
    if q==0:
        ax1.plot(month,landis_ecomean[:]/100.0,label="Model",color="black")   
        ax1.plot(month,flux_towermean[:]/100.0,color="black",label="Tower",linestyle="dashed") 
        ax1.legend(loc = "upper left")
        
    if q==1:
        ax2.plot(month,edvalues/100.0,label="Model",color="black")   
        ax2.plot(month,flux_towermean[:]/100.0,color="black",label="Tower",linestyle="dashed")
plt.savefig(odir+"\\flux_final.png",dpi=300)
odir = "C:\\Users\\sflanagan\\desktop\\model_comp_paper\\images\\final_images"        
plt.savefig(odir+"\\flux_final.png",dpi=300)
#plt.show()
plt.clf()
plt.close()


#Put all on one graph
fig, ax = plt.subplots()
ax.set_ylim(-1.5,3)
ax.plot(month,landis_ecomean[:]/100.0,label="LANDIS-II",color="black",linestyle="dashed")   
ax.plot(month,flux_towermean[:]/100.0,color="black",label="Data")
ax.plot(month,edvalues/100.0,label="ED",color="black", linestyle="dotted")  
ax.set_ylim=(-1.5,4)
plt.ylabel('NEE MgC/ha')
plt.xlabel("Month")
plt.legend(loc="best")
plt.savefig(odir+"\\flux_one_plot.png", dpi=300)
plt.savefig(odir+"\\figure2.pdf", dpi=300)
#plt.show()

plt.clf()
plt.close()


#Print the average values for each scenario
print "LANDIS average NEE tower ecoregions " + str(landisyr.mean(axis=0))
print "ED average NEE " + str(edyr.mean(axis=0))
print "Flux average NEE" + str(fluxyr.mean(axis=0))

print "Script complete"

        
       
       
       


   


