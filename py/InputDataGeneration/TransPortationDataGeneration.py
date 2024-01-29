#coding:Shift_Jis
import sys
import os
import csv
import pandas as pd
import geopandas as gpd
import datetime
import warnings
import los_car
import los_rail
import los_bus

warnings.simplefilter('ignore', FutureWarning)

curdir = os.getcwd()
#�t�H���_�\���̓Ǎ�
infile = curdir + '/Control_Input.txt'
rf = open(infile, 'r', encoding='Shift_Jis')
indir = rf.readline().rstrip('\n')
outdir = rf.readline().rstrip('\n')
cnvproj = rf.readline().rstrip('\n')

if os.path.isdir(indir) != True:
    print('�C���v�b�g�t�H���_:'+ indir + '������܂���')
    os.system('PAUSE')
    sys.exit()

if os.path.isdir(outdir) != True:
    print('�A�E�g�v�b�g�t�H���_:' + outdir + '������܂���')
    os.system('PAUSE')
    sys.exit()

path_ofile = outdir + '/Zone_TravelTime.csv' #�T�����ʏo�̓t�@�C��


#���W�n�̐ݒ�
src_proj = 'EPSG:6697' #�ϊ��O���W�n �ܓx�o�xJGD2011
dst_proj = 'EPSG:' + cnvproj #�ϊ�����W�n


#�]�[���f�[�^�͑S�@�ւŎg�p����̂ŁA��ɓǂݍ���
path_shp_zn = indir + '/Zone_Polygon.shp' #�]�[����shp
#�]�[���f�[�^�Ǎ�
if os.path.exists(path_shp_zn) != True:
    print('�]�[��shp:' + path_shp_zn + '������܂���')
    os.system('PAUSE')
    sys.exit()
print(datetime.datetime.now().time(),'�]�[���f�[�^�Ǎ��F' + path_shp_zn)
gdf = gpd.read_file(path_shp_zn)
#�]�[���f�[�^���f�[�^�t���[���ɕϊ�
df_zn = pd.DataFrame(gdf.iloc[:,:-1].values, columns = list(gdf.columns.values)[:-1] )


print(datetime.datetime.now().time(),'�S��LOS�쐬')
df_los_rail = los_rail.calc_los_rail(indir, outdir, src_proj, dst_proj, df_zn)


print(datetime.datetime.now().time(),'�o�XLOS�쐬')
df_los_bus = los_bus.calc_los_bus(indir, outdir, src_proj, dst_proj, df_zn)


print(datetime.datetime.now().time(),'������LOS�쐬')
df_los_car = los_car.calc_los_car(indir, outdir, src_proj, dst_proj, df_zn)

df_los = pd.concat([df_los_rail, df_los_bus, df_los_car], axis=1)
df_los.to_csv(path_ofile, encoding='Shift_Jis', index = False)

print(datetime.datetime.now().time(),'LOS�쐬�I��')
os.system('PAUSE')
