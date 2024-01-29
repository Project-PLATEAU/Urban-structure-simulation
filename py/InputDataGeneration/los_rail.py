#coding:Shift_Jis
import sys
import os
import csv
import numpy as np
import pandas as pd
import geopandas as gpd
import math
import datetime
from shapely.geometry import Point
from sklearn.neighbors import NearestNeighbors
import pyproj
import los_calc
import warnings

def calc_los_rail(indir, outdir, src_proj, dst_proj, df_zn):
    warnings.simplefilter('ignore', FutureWarning)

    #�g�p�t�@�C�����w��
    path_station = indir + '/Rail_Station.csv' #�w�ʒu
    path_rail_nw = indir + '/Rail_NW.csv' #�S��NW
    path_rail_fare_dist = indir + '/Rail_Fare_Dist.csv' #�^���e�[�u���i�΋����j
    path_rail_fare_sec = indir + '/Rail_Fare_Table.csv' #�^���e�[�u���i�����ԁj

    print(datetime.datetime.now().time(),'�f�[�^�Ǎ��J�n')
    #�w�R�[�h�Ǎ�
    if os.path.exists(path_station) != True:
        print('�w�R�[�h:' + path_station + '������܂���')
        os.system('PAUSE')
        sys.exit()
    print(datetime.datetime.now().time(),'�w�R�[�h�Ǎ��F' + path_station)
    dtype_station = {0: str, 1: str, 2: str, 3: str, 4: float, 5: float, 6: str, 7: int}
    df_station = pd.read_csv(path_station, encoding='shift-jis',dtype=dtype_station) 
    col_station_name = df_station.columns.values
    lst_station = list(df_station.iloc[:, 0])


    #�S��NW�f�[�^�Ǎ�
    if os.path.exists(path_rail_nw) != True:
        print('�S��NW:' + path_rail_nw + '������܂���')
        os.system('PAUSE')
        sys.exit()
    print(datetime.datetime.now().time(),'�S��NW�Ǎ��F' + path_rail_nw)
    dtype_rail_nw = {0: str, 1: str, 2: str, 3: int, 4: int, 5: float, 6: float, 7: float, 8: float, 9: float, 10: float}
    df_rail_nw_tmp = pd.read_csv(path_rail_nw, encoding='shift-jis',dtype=dtype_rail_nw) 
    col_name_rail = df_rail_nw_tmp.columns.values


    #�S��NW�f�[�^�̕⊮
    fill_values = {col_name_rail[5]: 0.0, col_name_rail[6]: 0.0, col_name_rail[7]: 0.0, col_name_rail[8]: 0.0, col_name_rail[9]: 0.0, col_name_rail[10]: 0.0}
    df_rail_nw_tmp = df_rail_nw_tmp.fillna(fill_values)
    df_rail_nw_tmp = df_rail_nw_tmp.copy()


    #�S���^���e�[�u���i�΋����j�̓Ǎ�
    if os.path.exists(path_rail_fare_dist) != True:
        print('�S���^���e�[�u���i�΋����j:' + path_rail_fare_dist + '������܂���')
        os.system('PAUSE')
        sys.exit()
    print(datetime.datetime.now().time(),'�S���^���e�[�u���i�΋����j�Ǎ��F' + path_rail_fare_dist)
    dtype_rail_fare_dist = {0: str, 1: int, 2: int, 3: float, 4: str}
    df_rail_fare_dist = pd.read_csv(path_rail_fare_dist, encoding='shift-jis',dtype=dtype_rail_fare_dist) 


    #�S���^���e�[�u���i�����ԁj�̓Ǎ�
    if os.path.exists(path_station) != True:
        print('�S���^���e�[�u���i�����ԁj:' + path_station + '������܂���')
        os.system('PAUSE')
        sys.exit()
    print(datetime.datetime.now().time(),'�S���^���e�[�u���i�����ԁj�Ǎ��F' + path_station)
    dtype_rail_fare_sec = {0: str, 1: str, 2: float, 3: str, 4: str}
    df_rail_fare_sec = pd.read_csv(path_rail_fare_sec, encoding='shift-jis',dtype=dtype_rail_fare_sec) 
    df_rail_fare_sec['ID'] = df_rail_fare_sec.iloc[:, 0] + df_rail_fare_sec.iloc[:, 1]

    print(datetime.datetime.now().time(),'�f�[�^�Ǎ��I��')
    print(datetime.datetime.now().time(),'�S��LOS�v�Z�J�n')


    #�H�����X�g�̍쐬
    lst_line = list(set(df_station.iloc[:, 1] + df_station.iloc[:, 2]))
    lst_line.sort()

    df_rail_nw = pd.DataFrame(columns=col_name_rail) #�H���ʂɉw�ԑ��������NW�̂��߂̋�̃f�[�^�t���[��
    nlink = 0
    #�H���ʂɌo�H�T�� �w�Ԃ̕��Ϗ��v���ԂƉ^�s�{�����Z�o
    for line in lst_line:
        #�����̒T��
        #�T��NW�̐ݒ�
        df_rail_line = df_rail_nw_tmp[(df_rail_nw_tmp[col_name_rail[1]].str[:len(line)] == line) & (df_rail_nw_tmp[col_name_rail[3]] <= 3)].copy() #�H���ʂɒ��o
        df_rail_line = df_rail_line.reset_index(drop=True) #�C���f�b�N�X�������p�����̂ŐU�蒼��

        #�m�[�hSEQ�̍쐬
        #�w�_�~�[�m�[�h
        nam_rail_line_0 = list(set(pd.concat([df_rail_line[df_rail_line[col_name_rail[1]].str[-1] == '0'].iloc[:, 1], df_rail_line[df_rail_line[col_name_rail[2]].str[-1] == '0'].iloc[:, 2]])))
        nam_rail_line_0.sort()
        #�w�m�[�h
        nam_rail_line_1 = list(set(pd.concat([df_rail_line[df_rail_line[col_name_rail[1]].str[-1] != '0'].iloc[:, 1], df_rail_line[df_rail_line[col_name_rail[2]].str[-1] != '0'].iloc[:, 2]])))
        nam_rail_line_1.sort()
        #�m�[�h���X�g
        nam_rail_line = nam_rail_line_0 + nam_rail_line_1
        nam_rail_line

        lf = []
        for i in df_rail_line.iloc[:, 1]:
            lf.append(nam_rail_line.index(i))
        df_rail_line['From�m�[�hSEQ'] = lf

        lt = []
        for i in df_rail_line.iloc[:, 2]:
            lt.append(nam_rail_line.index(i))
        df_rail_line['To�m�[�hSEQ'] = lt
        col_name_rail_line = df_rail_line.columns.values

        #�����N�ڑ�����forward star�`���ɕϊ�
        #������
        jla = [0] * (len(nam_rail_line) + 1)
        jlx = [0] * (len(df_rail_line) * 2)
        lij = [0] * len(df_rail_line)
        los_calc.forwardstar(len(df_rail_line), len(nam_rail_line), list(df_rail_line.iloc[:, 11]), list(df_rail_line.iloc[:, 12]), jla, jlx, lij)

        #�c�ƃL��
        #�����N�R�X�g�̐ݒ�
        lvp = df_rail_line.iloc[:, 5]
        lvm = df_rail_line.iloc[:, 5]

        #�o�H�T��
        dist_line1 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))

        for iz in range(len(nam_rail_line_0)):
            ndin = iz #�T���N�_
            minv = [math.inf] * len(nam_rail_line)
            nxt = [-1] * len(nam_rail_line)
            lno = [0] * len(nam_rail_line)

            #�_�C�N�X�g���@�ɂ��ŒZ�o�H�T��
            los_calc.dijkstra_rail_line(ndin, len(nam_rail_line), minv, list(df_rail_line.iloc[:, 11]), list(df_rail_line.iloc[:, 12]), lvp, lvm, jla, jlx, nxt, lno, list(df_rail_line.iloc[:, 3]))
            dist_line1[iz] = minv[:len(nam_rail_line_0)]

        #���Z�L��
        #�����N�R�X�g�̐ݒ�
        lvp = df_rail_line.iloc[:, 6]
        lvm = df_rail_line.iloc[:, 6]

        #�o�H�T��
        dist_line2 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))

        for iz in range(len(nam_rail_line_0)):
            ndin = iz #�T���N�_
            minv = [math.inf] * len(nam_rail_line)
            nxt = [-1] * len(nam_rail_line)
            lno = [0] * len(nam_rail_line)

            #�_�C�N�X�g���@�ɂ��ŒZ�o�H�T��
            los_calc.dijkstra_rail_line(ndin, len(nam_rail_line), minv, list(df_rail_line.iloc[:, 11]), list(df_rail_line.iloc[:, 12]), lvp, lvm, jla, jlx, nxt, lno, list(df_rail_line.iloc[:, 3]))
            dist_line2[iz] = minv[:len(nam_rail_line_0)]
        
        
        hv = 99990.0 #�o�H�T���̂��߂�high value
        #�e�w��ԏ�ԁi�}�s���������N�Ȃ��j�̒T��
        #From��To���̒T��
        #�T��NW�̐ݒ�
        df_rail_line = df_rail_nw_tmp[(df_rail_nw_tmp[col_name_rail[1]].str[:len(line)] == line) & (df_rail_nw_tmp[col_name_rail[3]] <= 3)].copy()
        df_rail_line = df_rail_line.reset_index(drop=True)

        #�}�s�����N�Ƀn�C�o�����[
        df_rail_line.loc[df_rail_line[col_name_rail[4]] == 2,  col_name_rail[7]] = hv
        df_rail_line.loc[df_rail_line[col_name_rail[4]] == 2,  col_name_rail[8]] = hv
        #�e�w���������N��To��From�Ƀn�C�o�����[
        df_rail_line.loc[(df_rail_line[col_name_rail[3]] == 1) & (df_rail_line[col_name_rail[4]] == 1),  col_name_rail[8]] = hv

        #�m�[�hSEQ���Z�b�g
        df_rail_line['From�m�[�hSEQ'] = lf
        df_rail_line['To�m�[�hSEQ'] = lt

        #�����N�R�X�g�̐ݒ�
        lvp = df_rail_line.iloc[:, 7] / 10.0
        lvm = df_rail_line.iloc[:, 8] / 10.0

        #�o�H�T��
        tim_line11 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        railtype_line11 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        hon_line11 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        for iz in range(len(nam_rail_line_0)):
            ndin = iz #�T���N�_
            minv = [math.inf] * len(nam_rail_line)
            nxt = [-1] * len(nam_rail_line)
            lno = [0] * len(nam_rail_line)

            #�_�C�N�X�g���@�ɂ��ŒZ�o�H�T��
            los_calc.dijkstra_rail_line(ndin, len(nam_rail_line), minv, list(df_rail_line.iloc[:, 11]), list(df_rail_line.iloc[:, 12]), lvp, lvm, jla, jlx, nxt, lno, list(df_rail_line.iloc[:, 3]))
            tim_line11[iz] = minv[:len(nam_rail_line_0)]

            #�o�H�T�����ʂ���^�s�{�����v�Z
            for jz in range(len(nam_rail_line_0)):
                if iz == jz: continue
                if minv[jz] >= hv / 10: continue
                ndtb = []
                lktb = []
                ierr, ir, railtype, hon = los_calc.rotout_rail_line(iz, jz, nxt, lno, ndtb, lktb, list(df_rail_line.iloc[:, 3]), list(df_rail_line.iloc[:, 4]), list(df_rail_line.iloc[:, 9]))
                if hon != 999: railtype_line11[iz, jz] = railtype
                if hon != 999: hon_line11[iz, jz] = hon

        tim_line11 = np.where(tim_line11 >= hv / 10, 0, tim_line11)
        tim_line11 = np.where(tim_line11 == 0, 0, tim_line11 - 2) #�w�_�~�[�����N�̏��v���Ԃ�����

        #To��From���̒T��
        #�T��NW�̐ݒ�
        df_rail_line = df_rail_nw_tmp[(df_rail_nw_tmp[col_name_rail[1]].str[:len(line)] == line) & (df_rail_nw_tmp[col_name_rail[3]] <= 3)].copy()
        df_rail_line = df_rail_line.reset_index(drop=True)

        #�}�s�����N�Ƀn�C�o�����[
        df_rail_line.loc[df_rail_line[col_name_rail[4]] == 2,  col_name_rail[7]] = hv
        df_rail_line.loc[df_rail_line[col_name_rail[4]] == 2,  col_name_rail[8]] = hv
        #�e�w���������N��From��To�Ƀn�C�o�����[
        df_rail_line.loc[(df_rail_line[col_name_rail[3]] == 1) & (df_rail_line[col_name_rail[4]] == 1),  col_name_rail[7]] = hv

        #�m�[�hSEQ���Z�b�g
        df_rail_line['From�m�[�hSEQ'] = lf
        df_rail_line['To�m�[�hSEQ'] = lt

        #�����N�R�X�g�̐ݒ�
        lvp = df_rail_line.iloc[:, 7] / 10.0
        lvm = df_rail_line.iloc[:, 8] / 10.0

        #�o�H�T��
        tim_line12 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        railtype_line12 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        hon_line12 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        for iz in range(len(nam_rail_line_0)):
            ndin = iz #�T���N�_
            minv = [math.inf] * len(nam_rail_line)
            nxt = [-1] * len(nam_rail_line)
            lno = [0] * len(nam_rail_line)

            #�_�C�N�X�g���@�ɂ��ŒZ�o�H�T��
            los_calc.dijkstra_rail_line(ndin, len(nam_rail_line), minv, list(df_rail_line.iloc[:, 11]), list(df_rail_line.iloc[:, 12]), lvp, lvm, jla, jlx, nxt, lno, list(df_rail_line.iloc[:, 3]))
            tim_line12[iz] = minv[:len(nam_rail_line_0)]

            #�o�H�T�����ʂ���^�s�{�����v�Z
            for jz in range(len(nam_rail_line_0)):
                if iz == jz: continue
                if minv[jz] >= hv / 10: continue
                ndtb = []
                lktb = []
                ierr, ir, railtype, hon = los_calc.rotout_rail_line(iz, jz, nxt, lno, ndtb, lktb, list(df_rail_line.iloc[:, 3]), list(df_rail_line.iloc[:, 4]), list(df_rail_line.iloc[:, 10]))
                if hon != 999: railtype_line12[iz, jz] = railtype
                if hon != 999: hon_line12[iz, jz] = hon

        tim_line12 = np.where(tim_line12 >= hv / 10, 0, tim_line12)
        tim_line12 = np.where(tim_line12 == 0, 0, tim_line12 - 2)

        tim_line1 = tim_line11 + tim_line12
        railtype_line1 = railtype_line11 + railtype_line12
        hon_line1 = hon_line11 + hon_line12


        #�e�w��ԏ�ԁi�}�s���������N����j�̒T��
        #From��To���̒T��
        #�T��NW�̐ݒ�
        df_rail_line = df_rail_nw_tmp[(df_rail_nw_tmp[col_name_rail[1]].str[:len(line)] == line) & (df_rail_nw_tmp[col_name_rail[3]] <= 3)].copy()
        df_rail_line = df_rail_line.reset_index(drop=True)

        #�}�s�w�_�~�[�����N�̏�ԑ��Ƀn�C�o�����[
        df_rail_line.loc[(df_rail_line[col_name_rail[3]] == 2) & (df_rail_line[col_name_rail[4]] == 2),  col_name_rail[7]] = hv
        #�e�w���������N��To��From�Ƀn�C�o�����[
        df_rail_line.loc[(df_rail_line[col_name_rail[3]] == 1) & (df_rail_line[col_name_rail[4]] == 1),  col_name_rail[8]] = hv
        #�}�s���������N��To��From�Ƀn�C�o�����[
        df_rail_line.loc[(df_rail_line[col_name_rail[3]] == 1) & (df_rail_line[col_name_rail[4]] == 2),  col_name_rail[8]] = hv

        #�m�[�hSEQ���Z�b�g
        df_rail_line['From�m�[�hSEQ'] = lf
        df_rail_line['To�m�[�hSEQ'] = lt

        #�����N�R�X�g�̐ݒ�
        lvp = df_rail_line.iloc[:, 7] / 10.0
        lvm = df_rail_line.iloc[:, 8] / 10.0

        #�o�H�T��
        tim_line21 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        railtype_line21 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        hon_line21 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        for iz in range(len(nam_rail_line_0)):
            ndin = iz #�T���N�_
            minv = [math.inf] * len(nam_rail_line)
            nxt = [-1] * len(nam_rail_line)
            lno = [0] * len(nam_rail_line)

            #�_�C�N�X�g���@�ɂ��ŒZ�o�H�T��
            los_calc.dijkstra_rail_line(ndin, len(nam_rail_line), minv, list(df_rail_line.iloc[:, 11]), list(df_rail_line.iloc[:, 12]), lvp, lvm, jla, jlx, nxt, lno, list(df_rail_line.iloc[:, 3]))
            tim_line21[iz] = minv[:len(nam_rail_line_0)]

            #�o�H�T�����ʂ���^�s�{�����v�Z
            for jz in range(len(nam_rail_line_0)):
                if iz == jz: continue
                if minv[jz] >= hv / 10: continue
                ndtb = []
                lktb = []
                ierr, ir, railtype, hon = los_calc.rotout_rail_line(iz, jz, nxt, lno, ndtb, lktb, list(df_rail_line.iloc[:, 3]), list(df_rail_line.iloc[:, 4]), list(df_rail_line.iloc[:, 9]))
                if hon != 999: railtype_line21[iz, jz] = railtype
                if hon != 999: hon_line21[iz, jz] = hon
                if railtype == 1: #�}�s�Ȃ��Ɠ�������
                    hon_line21[iz, jz] = 0
                    tim_line21[iz, jz] = 0

        tim_line21 = np.where(tim_line21 >= hv / 10, 0, tim_line21)
        tim_line21 = np.where(tim_line21 == 0, 0, tim_line21 - 2) #�w�_�~�[�����N�̏��v���Ԃ�����

        #To��From���̒T��
        #�T��NW�̐ݒ�
        df_rail_line = df_rail_nw_tmp[(df_rail_nw_tmp[col_name_rail[1]].str[:len(line)] == line) & (df_rail_nw_tmp[col_name_rail[3]] <= 3)].copy()
        df_rail_line = df_rail_line.reset_index(drop=True)

        #�}�s�w�_�~�[�����N�̏�ԑ��Ƀn�C�o�����[
        df_rail_line.loc[(df_rail_line[col_name_rail[3]] == 2) & (df_rail_line[col_name_rail[4]] == 2),  col_name_rail[7]] = hv
        #�e�w���������N��From��To�Ƀn�C�o�����[
        df_rail_line.loc[(df_rail_line[col_name_rail[3]] == 1) & (df_rail_line[col_name_rail[4]] == 1),  col_name_rail[7]] = hv
        #�}�s���������N��From��To�Ƀn�C�o�����[
        df_rail_line.loc[(df_rail_line[col_name_rail[3]] == 1) & (df_rail_line[col_name_rail[4]] == 2),  col_name_rail[7]] = hv

        #�m�[�hSEQ���Z�b�g
        df_rail_line['From�m�[�hSEQ'] = lf
        df_rail_line['To�m�[�hSEQ'] = lt

        #�����N�R�X�g�̐ݒ�
        lvp = df_rail_line.iloc[:, 7] / 10.0
        lvm = df_rail_line.iloc[:, 8] / 10.0

        #�o�H�T��
        tim_line22 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        railtype_line22 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        hon_line22 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        for iz in range(len(nam_rail_line_0)):
            ndin = iz #�T���N�_
            minv = [math.inf] * len(nam_rail_line)
            nxt = [-1] * len(nam_rail_line)
            lno = [0] * len(nam_rail_line)

            #�_�C�N�X�g���@�ɂ��ŒZ�o�H�T��
            los_calc.dijkstra_rail_line(ndin, len(nam_rail_line), minv, list(df_rail_line.iloc[:, 11]), list(df_rail_line.iloc[:, 12]), lvp, lvm, jla, jlx, nxt, lno, list(df_rail_line.iloc[:, 3]))
            tim_line22[iz] = minv[:len(nam_rail_line_0)]

            #�o�H�T�����ʂ���^�s�{�����v�Z
            for jz in range(len(nam_rail_line_0)):
                if iz == jz: continue
                if minv[jz] >= hv / 10: continue
                ndtb = []
                lktb = []
                ierr, ir, railtype, hon = los_calc.rotout_rail_line(iz, jz, nxt, lno, ndtb, lktb, list(df_rail_line.iloc[:, 3]), list(df_rail_line.iloc[:, 4]), list(df_rail_line.iloc[:, 10]))
                if hon != 999: railtype_line22[iz, jz] = railtype
                if hon != 999: hon_line22[iz, jz] = hon
                if railtype == 1: #�}�s�Ȃ��Ɠ�������
                    hon_line22[iz, jz] = 0
                    tim_line22[iz, jz] = 0

        tim_line22 = np.where(tim_line22 >= hv / 10, 0, tim_line22)
        tim_line22 = np.where(tim_line22 == 0, 0, tim_line22 - 2)

        tim_line2 = tim_line21 + tim_line22
        railtype_line2 = railtype_line21 + railtype_line22
        hon_line2 = hon_line21 + hon_line22


        #�}�s��ԏ�Ԃ̒T��
        #From��To���̒T��
        #�T��NW�̐ݒ�
        df_rail_line = df_rail_nw_tmp[(df_rail_nw_tmp[col_name_rail[1]].str[:len(line)] == line) & (df_rail_nw_tmp[col_name_rail[3]] <= 3)].copy()
        df_rail_line = df_rail_line.reset_index(drop=True)

        #�e�w�w�_�~�[�����N�̏�ԑ��Ƀn�C�o�����[
        df_rail_line.loc[(df_rail_line[col_name_rail[3]] == 2) & (df_rail_line[col_name_rail[4]] == 1),  col_name_rail[7]] = hv
        #�e�w���������N��To��From�Ƀn�C�o�����[
        df_rail_line.loc[(df_rail_line[col_name_rail[3]] == 1) & (df_rail_line[col_name_rail[4]] == 1),  col_name_rail[8]] = hv
        #�}�s���������N��To��From�Ƀn�C�o�����[
        df_rail_line.loc[(df_rail_line[col_name_rail[3]] == 1) & (df_rail_line[col_name_rail[4]] == 2),  col_name_rail[8]] = hv

        #�m�[�hSEQ���Z�b�g
        df_rail_line['From�m�[�hSEQ'] = lf
        df_rail_line['To�m�[�hSEQ'] = lt

        #�����N�R�X�g�̐ݒ�
        lvp = df_rail_line.iloc[:, 7] / 10.0
        lvm = df_rail_line.iloc[:, 8] / 10.0

        #�o�H�T��
        tim_line31 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        railtype_line31 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        hon_line31 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        for iz in range(len(nam_rail_line_0)):
            ndin = iz #�T���N�_
            minv = [math.inf] * len(nam_rail_line)
            nxt = [-1] * len(nam_rail_line)
            lno = [0] * len(nam_rail_line)

            #�_�C�N�X�g���@�ɂ��ŒZ�o�H�T��
            los_calc.dijkstra_rail_line(ndin, len(nam_rail_line), minv, list(df_rail_line.iloc[:, 11]), list(df_rail_line.iloc[:, 12]), lvp, lvm, jla, jlx, nxt, lno, list(df_rail_line.iloc[:, 3]))
            tim_line31[iz] = minv[:len(nam_rail_line_0)]

            #�o�H�T�����ʂ���^�s�{�����v�Z
            for jz in range(len(nam_rail_line_0)):
                if iz == jz: continue
                if minv[jz] >= hv / 10: continue
                ndtb = []
                lktb = []
                ierr, ir, railtype, hon = los_calc.rotout_rail_line(iz, jz, nxt, lno, ndtb, lktb, list(df_rail_line.iloc[:, 3]), list(df_rail_line.iloc[:, 4]), list(df_rail_line.iloc[:, 9]))
                if hon != 999: railtype_line31[iz, jz] = railtype
                if hon != 999: hon_line31[iz, jz] = hon

        tim_line31 = np.where(tim_line31 >= hv / 10, 0, tim_line31)
        tim_line31 = np.where(tim_line31 == 0, 0, tim_line31 - 2) #�w�_�~�[�����N�̏��v���Ԃ�����

        #To��From���̒T��
        #�T��NW�̐ݒ�
        df_rail_line = df_rail_nw_tmp[(df_rail_nw_tmp[col_name_rail[1]].str[:len(line)] == line) & (df_rail_nw_tmp[col_name_rail[3]] <= 3)].copy()
        df_rail_line = df_rail_line.reset_index(drop=True)

        #�e�w�w�_�~�[�����N�̏�ԑ��Ƀn�C�o�����[
        df_rail_line.loc[(df_rail_line[col_name_rail[3]] == 2) & (df_rail_line[col_name_rail[4]] == 1),  col_name_rail[7]] = hv
        #�e�w���������N��From��To�Ƀn�C�o�����[
        df_rail_line.loc[(df_rail_line[col_name_rail[3]] == 1) & (df_rail_line[col_name_rail[4]] == 1),  col_name_rail[7]] = hv
        #�}�s���������N��From��To�Ƀn�C�o�����[
        df_rail_line.loc[(df_rail_line[col_name_rail[3]] == 1) & (df_rail_line[col_name_rail[4]] == 2),  col_name_rail[7]] = hv

        #�m�[�hSEQ���Z�b�g
        df_rail_line['From�m�[�hSEQ'] = lf
        df_rail_line['To�m�[�hSEQ'] = lt

        #�����N�R�X�g�̐ݒ�
        lvp = df_rail_line.iloc[:, 7] / 10.0
        lvm = df_rail_line.iloc[:, 8] / 10.0

        #�o�H�T��
        tim_line32 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        railtype_line32 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        hon_line32 = np.zeros((len(nam_rail_line_0), len(nam_rail_line_0)))
        for iz in range(len(nam_rail_line_0)):
            ndin = iz #�T���N�_
            minv = [math.inf] * len(nam_rail_line)
            nxt = [-1] * len(nam_rail_line)
            lno = [0] * len(nam_rail_line)

            #�_�C�N�X�g���@�ɂ��ŒZ�o�H�T��
            los_calc.dijkstra_rail_line(ndin, len(nam_rail_line), minv, list(df_rail_line.iloc[:, 11]), list(df_rail_line.iloc[:, 12]), lvp, lvm, jla, jlx, nxt, lno, list(df_rail_line.iloc[:, 3]))
            tim_line32[iz] = minv[:len(nam_rail_line_0)]

            #�o�H�T�����ʂ���^�s�{�����v�Z
            for jz in range(len(nam_rail_line_0)):
                if iz == jz: continue
                if minv[jz] >= hv / 10: continue
                ndtb = []
                lktb = []
                ierr, ir, railtype, hon = los_calc.rotout_rail_line(iz, jz, nxt, lno, ndtb, lktb, list(df_rail_line.iloc[:, 3]), list(df_rail_line.iloc[:, 4]), list(df_rail_line.iloc[:, 10]))
                if hon != 999: railtype_line32[iz, jz] = railtype
                if hon != 999: hon_line32[iz, jz] = hon

        tim_line32 = np.where(tim_line32 >= hv / 10, 0, tim_line32)
        tim_line32 = np.where(tim_line32 == 0, 0, tim_line32 - 2)

        tim_line3 = tim_line31 + tim_line32
        railtype_line3 = railtype_line31 + railtype_line32
        hon_line3 = hon_line31 + hon_line32

        #�e�T�����ʂ���^�s�{�����v�Z
        hon_line = np.maximum(hon_line1, hon_line2) + hon_line3

        #�e�T�����ʂ��珊�v���Ԃ��v�Z �^�s�{���f�[�^�Ȃ��ɑΉ��i�^�s�{��1�{�Ƃ��Čv�Z�j
        np_dmy = np.ones((len(nam_rail_line_0), len(nam_rail_line_0)))
        sumtim = tim_line1 * np.maximum(hon_line1, np_dmy) + tim_line2 * np.maximum(hon_line2, np_dmy) + tim_line3 * np.maximum(hon_line3, np_dmy)
        hon_line1 = np.maximum(hon_line1, np.divide(tim_line1, tim_line1, out=np.zeros_like(tim_line1, dtype=np.float64), where=tim_line1 != 0))
        hon_line2 = np.maximum(hon_line2, np.divide(tim_line2, tim_line2, out=np.zeros_like(tim_line2, dtype=np.float64), where=tim_line2 != 0))
        hon_line3 = np.maximum(hon_line3, np.divide(tim_line3, tim_line3, out=np.zeros_like(tim_line3, dtype=np.float64), where=tim_line3 != 0))
        sumhon = hon_line1 + hon_line2 + hon_line3

        tim_line = np.divide(sumtim, sumhon, out=np.zeros_like(sumtim, dtype=np.float64), where=sumhon != 0)

        lst_dmy = []
        for i in range(len(nam_rail_line_0)):
            for j in range(len(nam_rail_line_0)):
                if i < j:
                    nlink += 1
                    lst_dmy.append([str(nlink), nam_rail_line_0[i], nam_rail_line_0[j], 1, 1, round(dist_line1[i, j], 1), round(dist_line2[i, j], 1), tim_line[i, j], tim_line[j, i], hon_line[i, j], hon_line[j, i]])
        df_rail_nw_dmy = pd.DataFrame(lst_dmy, columns=col_name_rail)
        df_rail_nw = pd.concat([df_rail_nw, df_rail_nw_dmy], axis=0, ignore_index=True)
    
    df_rail_nw_dmy = df_rail_nw_tmp[df_rail_nw_tmp[col_name_rail[3]] == 4].copy() #�抷�����N�ɒ��o
    df_rail_nw_dmy.iloc[:,7] = df_rail_nw_dmy.iloc[:,7] / 10
    df_rail_nw_dmy.iloc[:,8] = df_rail_nw_dmy.iloc[:,8] / 10
    df_rail_nw = pd.concat([df_rail_nw, df_rail_nw_dmy], axis=0, ignore_index=True)
    df_rail_nw.iloc[:,1] = df_rail_nw.iloc[:,1].str[:len(lst_station[0])]
    df_rail_nw.iloc[:,2] = df_rail_nw.iloc[:,2].str[:len(lst_station[0])]


    #�m�[�hSEQ���Z�b�g
    lf = []
    for i in df_rail_nw.iloc[:, 1]:
        lf.append(lst_station.index(i))
    df_rail_nw['From�m�[�hSEQ'] = lf

    lt = []
    for i in df_rail_nw.iloc[:, 2]:
        lt.append(lst_station.index(i))
    df_rail_nw['To�m�[�hSEQ'] = lt
    col_name_rail_nw = df_rail_nw.columns.values

    #�����N�ڑ�����forward star�`���ɕϊ�
    #������
    jla = [0] * (len(lst_station) + 1)
    jlx = [0] * (len(df_rail_nw) * 2)
    lij = [0] * len(df_rail_nw)
    los_calc.forwardstar(len(df_rail_nw), len(lst_station), list(df_rail_nw.iloc[:, 11]), list(df_rail_nw.iloc[:, 12]), jla, jlx, lij)

    #�����N�R�X�g�̐ݒ�
    #��Ԏ���
    lvp = df_rail_nw.iloc[:, 7].copy()
    lvm = df_rail_nw.iloc[:, 8].copy()
    #�҂����Ԃ����Z
    lvp += np.divide(30.0, df_rail_nw.iloc[:, 9], out=np.zeros_like(df_rail_nw.iloc[:, 9], dtype=np.float64), where=(df_rail_nw.iloc[:, 3] == 1) & (df_rail_nw.iloc[:, 9] != 0))
    lvm += np.divide(30.0, df_rail_nw.iloc[:, 10], out=np.zeros_like(df_rail_nw.iloc[:, 10], dtype=np.float64), where=(df_rail_nw.iloc[:, 3] == 1) & (df_rail_nw.iloc[:, 10] != 0))


    #�o�H�T��
    tim_rail = np.zeros((len(lst_station), len(lst_station)))
    tim_rail_wait = np.zeros((len(lst_station), len(lst_station)))
    fare_rail = np.zeros((len(lst_station), len(lst_station)))
    len_agency = len(df_station.iloc[0, 1])

    for iz in range(len(lst_station)):
        ndin = iz #�T���N�_
        minv = [math.inf] * len(lst_station)
        nxt = [-1] * len(lst_station)
        lno = [0] * len(lst_station)

        #�_�C�N�X�g���@�ɂ��ŒZ�o�H�T��
        los_calc.dijkstra_rail(ndin, len(lst_station), minv, list(df_rail_nw.iloc[:, 11]), list(df_rail_nw.iloc[:, 12]), lvp, lvm, jla, jlx, nxt, lno, list(df_rail_nw.iloc[:, 3]))
    
        #�o�H�T�����ʂ��珊�v���ԁi�������ԂƑ҂����ԁj�Ɖ^�����v�Z
        for jz in range(len(lst_station)):
            if iz == jz: continue
            ndtb = []
            lktb = []
            ierr, ir, tim_rail[iz, jz], tim_rail_wait[iz, jz], fare_rail[iz, jz] = los_calc.rotout_rail(iz, jz, nxt, lno, ndtb, lktb, lst_station, len_agency, df_rail_nw, df_rail_fare_dist, df_rail_fare_sec)


    #�w�A�N�Z�X�Z�o
    znsta = [] #�]�[���ʃA�N�Z�X�w�̃��X�g
    dist_znsta = [] #�]�[���ʃA�N�Z�X�w�ւ̋������X�g
    transformer = pyproj.Transformer.from_crs(src_proj, dst_proj)
    #���W�ϊ�
    sta_x, sta_y = transformer.transform(df_station.iloc[:, 4], df_station.iloc[:, 5])
    zn_x, zn_y = transformer.transform(df_zn.iloc[:, 1], df_zn.iloc[:, 2])
    #�m�[�h�̈ʒu�֌W���w�K
    sta_xy_array = np.array([sta_x, sta_y]).T
    knn_num = len(df_station) #�T���m�[�h��
    knn_model = NearestNeighbors(n_neighbors = knn_num, algorithm = 'ball_tree').fit(sta_xy_array)

    for zn in range(len(df_zn)):
        zn_xy = [zn_x[zn], zn_y[zn]]
        knn_dists, knn_results = knn_model.kneighbors([zn_xy])

        lst_sta = []
        lst_dist = []

        #�ő�10km�܂�1km�P�ʂŔ͈͂��L���āA�A�N�Z�X����w�����
        maxdist = math.ceil(knn_dists[:,0][0] / 1000) #�Ŋ��w
        if maxdist > 10:
            pass
        else:
            for ix in range(knn_num):
                if knn_dists[:,ix][0] / 1000 > maxdist:
                    break
                else:
                    lst_sta.append(knn_results[:,ix][0])
                    lst_dist.append(knn_dists[:,ix][0])
        znsta.append(lst_sta)
        dist_znsta.append(lst_dist)


    #�]�[����LOS���v�Z
    #�o�͗p�̃f�[�^�t���[��������
    df_los = pd.DataFrame(columns=['zone_code_o', 'zone_code_d', 'Travel_Time_Rail', 'Waiting_Time_Rail', 'Access_Time_Rail', 'Egress_Time_Rail', 'Fare_Rail'])
    lst_jz = df_zn.iloc[:, 0]

    for iz in range(len(df_zn)):
        lst_los = []
        for jz in range(len(df_zn)):
            sumtim = 9999.0
            min_i = len(df_station)
            min_j = len(df_station)
            if iz == jz:
                lst_los.append([0,0,0,0,0,0,0])
            else:
                for i, sta_acs in enumerate(znsta[iz]):
                    for j, sta_egr in enumerate(znsta[jz]):
                        if sta_acs == sta_egr: continue
                        if sumtim > tim_rail[sta_acs, sta_egr] + tim_rail_wait[sta_acs, sta_egr] + \
                                    dist_znsta[iz][i] * math.sqrt(2) / 80.0 + \
                                    dist_znsta[jz][j] * math.sqrt(2) / 80.0:
                            sumtim = tim_rail[sta_acs, sta_egr] + tim_rail_wait[sta_acs, sta_egr] + \
                                    dist_znsta[iz][i] * math.sqrt(2) / 80.0 + \
                                    dist_znsta[jz][j] * math.sqrt(2) / 80.0
                            min_i = i
                            min_j = j
                if sumtim == 9999.0:
                    lst_los.append([0,0,9999.0,9999.0,9999.0,9999.0,9999.0])
                else:
                    lst_los.append([0,0,tim_rail[znsta[iz][min_i],znsta[jz][min_j]],tim_rail_wait[znsta[iz][min_i], znsta[jz][min_j]],round(dist_znsta[iz][min_i] * math.sqrt(2) / 80.0, 1),round(dist_znsta[jz][min_j] * math.sqrt(2) / 80.0, 1),fare_rail[znsta[iz][min_i], znsta[jz][min_j]]])

        df_los_zn = pd.DataFrame(lst_los, columns=['zone_code_o', 'zone_code_d', 'Travel_Time_Rail', 'Waiting_Time_Rail', 'Access_Time_Rail', 'Egress_Time_Rail', 'Fare_Rail'])
        df_los_zn.iloc[:, 0] = lst_jz[iz]
        df_los_zn.iloc[:, 1] = lst_jz
        df_los = pd.concat([df_los, df_los_zn], axis=0, ignore_index=True)

    print(datetime.datetime.now().time(),'�S��LOS�v�Z�I��')
    return df_los
