import os,tqdm,glob
import numpy as np
from scipy.interpolate import interp1d

''' training disp input '''
def get_filename(filepath_disp_training,filepath_vs_training,dataset_type):
    filename_dispersion_total = []
    filename_vs_total = []
    key_total = []
    if dataset_type == "train":
        if os.path.exists(filepath_disp_training) and os.path.exists(filepath_vs_training):

            files_disp = os.listdir(filepath_disp_training)

            # read inputs
            for file in files_disp:

                key = file[2:-4]  # add group disp and phase disp
#                 print(key)
                filename_disp = filepath_disp_training + file

                filename_vs = filepath_vs_training + file
#                 print(filename_vs)
                if os.path.exists(filename_vs) and os.path.exists(filename_disp):
                    filename_dispersion_total.append(filename_disp)

                    filename_vs_total.append(filename_vs)

                    key_total.append(file[0:-4])

            return np.array(filename_dispersion_total), np.array(filename_vs_total), np.array(key_total)
        else:
            print('Input file path is not exist, check the input path!')
            return None, None, None

def gaussian_map(vel,vel_axis,radius=0.1):
    rows  = vel_axis.shape[0]
    cols  = vel.shape[0]
    vel_map = np.zeros((rows,cols))
    for i in range(cols):
        vel_temp = vel[i]
        x_gaussian = gaussian(vel_temp, vel_axis, r=radius)
        vel_map[:, i] = x_gaussian
    return vel_map

def gaussian(vel,vel_axis,r=0.1):
    x_gaussian = np.exp(-((vel_axis-vel)**2)/(2*r**2))
    return x_gaussian

# filepath_disp_training = 'rawData/Shenetal2013_disp_pg_real/'
# filepath_vs_training   = 'rawData/Shenetal2013_Vs/'
# os.system("rm -rf Input_disp_combine_gaussian_map  && mkdir Input_disp_combine_gaussian_map  ")
# r=0.1
# disp_names,vs_names,keys_names = get_filename(filepath_disp_training,filepath_vs_training,'train')
# vel_axis = np.linspace(2,5,num=60)

# for i in tqdm.tqdm(range(len(keys_names))):
#     vel_pg=np.loadtxt(disp_names[i])
#     freqs  = vel_pg[:,0] #vel_pg = vel_pg[:,1:3]     # np.delete(a,0,axis=1)
#     vel_p = vel_pg[:,1]
#     vel_g = vel_pg[:,1]
#     # vel_g = vel_pg[:,2]
#     vs_syn=np.loadtxt(vs_names[i])
#     depths = vs_syn[:,0]
#     vel_vs = vs_syn[:,1]
#     vel_map_p= gaussian_map(vel_p,vel_axis,radius=r)
#     vel_map_g= gaussian_map(vel_g,vel_axis,radius=r)
#     # vs_map_syn = gaussian_map(vel_vs,vel_axis,radius=r)
#     name_pg = './Input_disp_combine_gaussian_map/'+ keys_names[i] + '.npy'
#     np.save(name_pg,np.array([vel_map_p,vel_map_g]))



''' training vs input '''
# filepath_vs = './rawData/Shenetal2013_Vs/'
# depth_spacing=0.5# 1,2,5,6,10
# depth_max = 150

# if depth_spacing in [0.5,1,2,5,6,10]:
#     depth = np.arange(0,depth_max+depth_spacing,depth_spacing)
# os.system('rm -rf Input_Vs && mkdir Input_Vs')

# count = 0
# for lat in np.arange(0,180,0.1):
#     for lon in np.arange(0,360,0.1):
#         key = "%.2f"%lat+ "_"+"%.2f"%lon
#         key_name = key + '.txt'
#         file_vs = filepath_vs + key_name
#         if  os.path.exists(file_vs):
#             temp = np.loadtxt(file_vs); 
#             if len(temp)>1:
#                 count =count +1
#                 print(count,key_name)
#                 depth_temp=temp[:,0]; vs_temp = temp[:,1]
#                 fl = interp1d(depth_temp, vs_temp, kind='slinear')
#                 vs = fl(depth)
#                 # for using those data to predict dispersion curve comparing the vs from cnn
#                 vs_out = np.array([depth,vs])
#                 np.save("Input_Vs/"+key,vs_out.T)



''' Prediction disp input '''
import pandas as pd

grInDir = 'rawData/Shenetal2016_disp_pg_real_dat/InputPhaseData'
phInDir = 'rawData/Shenetal2016_disp_pg_real_dat/InputPhaseData'
outDir  = 'Input_predict'

grPers = set([os.path.split(v)[1].split('.')[0] for v in glob.glob(f'{grInDir}/*.dat')])
phPers = set([os.path.split(v)[1].split('.')[0] for v in glob.glob(f'{phInDir}/*.dat')])

pers = list(phPers & grPers); pers.sort(key= lambda a: float(a))
pers = pers[:17]

dispDict = {}

for iper,per in enumerate(pers):
    print(f'Period = {per}s')
    dfGrv = pd.read_csv(f'{grInDir}/{per}.dat',header=None,names=['Lon','Lat','Grv','Grv_Uncer'],delimiter=' ')
    dfPhv = pd.read_csv(f'{phInDir}/{per}.dat',header=None,names=['Lon','Lat','Phv','Phv_Uncer'],delimiter=' ')
    df = pd.merge(dfPhv,dfGrv,left_on=['Lon','Lat'],right_on=['Lon','Lat'])
    for row in df.iterrows():
        row = row[1]; pid = f'{row["Lat"]:.2f}_{row["Lon"]:.2f}'
        if pid not in dispDict:
            dispDict[pid] = np.nan*np.ones((len(pers),5))
        dispDict[pid][iper,:] = np.array([float(per),row['Phv'],row['Phv_Uncer'],row['Grv'],row['Grv_Uncer']])

os.makedirs(outDir,exist_ok=True)
for k,v in tqdm.tqdm(dispDict.items()):
    if np.any(np.isnan(v)):
        continue
    np.savetxt(f'{outDir}/{k}.txt',v,fmt='%10.5f')
