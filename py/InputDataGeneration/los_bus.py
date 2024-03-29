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

def calc_los_bus(indir, outdir, src_proj, dst_proj, df_zn):
    warnings.simplefilter('ignore', FutureWarning)

    #�g�p�t�@�C�����w��
    tim_limit = 15.0 #�҂����Ԃ̏��
    tim_load = 15.0 #�抷����
    tim_ope = 15.0 #�^�s����
    tim_wait = 3.0 #�����҂����ԁi�����\�ɍ��킹�ăo�X��ɍs���̂ŉ^�s�{���Ƃ͊֌W�Ȃ��ݒ�j

    #�g�p�t�@�C�����w��
    path_bus_stop = indir + '/Bus_Stop.csv' #�o�X�ʒu
    path_bus_nw = indir + '/Bus_NW.csv' #�o�XNW
    path_bus_fare = indir + '/Bus_Fare.csv' #�^���e�[�u��
    path_shp_zn = indir + '/Zone_Polygon.shp' #�]�[����shp


    if os.path.exists(path_bus_stop) != True:
        print('�o�X��R�[�h:' + path_bus_stop + '������܂���')
        print('�o�XLOS�쐬���X�L�b�v���܂�')
        df_los = los_dmy(df_zn)
        return df_los
    if os.path.exists(path_bus_nw) != True:
        print('�o�XNW:' + path_bus_nw + '������܂���')
        print('�o�XLOS�쐬���X�L�b�v���܂�')
        df_los = los_dmy(df_zn)
        return df_los
    if os.path.exists(path_bus_fare) != True:
        print('�o�X�^���e�[�u��:' + path_bus_fare + '������܂���')
        print('�o�XLOS�쐬���X�L�b�v���܂�')
        df_los = los_dmy(df_zn)
        return df_los


    print(datetime.datetime.now().time(),'�f�[�^�Ǎ��J�n')
    #�o�X��R�[�h�Ǎ�
    #if os.path.exists(path_bus_stop) != True:
    #    print('�o�X��R�[�h:' + path_bus_stop + '������܂���')
    #    os.system('PAUSE')
    #    sys.exit()
    print(datetime.datetime.now().time(),'�o�X��R�[�h�Ǎ��F' + path_bus_stop)
    dtype_bus_stop = {0: str, 1: str, 2: float, 3: float, 4: str}
    df_bus_stop = pd.read_csv(path_bus_stop, encoding='shift-jis',dtype=dtype_bus_stop) 
    col_bus_stop_name = df_bus_stop.columns.values
    df_bus_stop['id'] = df_bus_stop['agency_id'] + '_' + df_bus_stop['stop_id']
    df_bus_stop = df_bus_stop.sort_values('id').reset_index(drop=True)
    lst_bus_stop = list(df_bus_stop .iloc[:, -1])


    #�o�XNW�f�[�^�Ǎ�
    #if os.path.exists(path_bus_nw) != True:
    #    print('�o�XNW:' + path_bus_nw + '������܂���')
    #    os.system('PAUSE')
    #    sys.exit()
    print(datetime.datetime.now().time(),'�o�XNW�Ǎ��F' + path_bus_nw)
    dtype_bus_nw = {0: str, 1: str, 2: str, 3: str, 4: str, 5: float, 6: float}
    df_bus_nw_tmp = pd.read_csv(path_bus_nw, encoding='shift-jis',dtype=dtype_bus_nw) 
    col_name_bus = df_bus_nw_tmp.columns.values

    #�o�XNW�f�[�^�̕⊮
    fill_values = {col_name_bus[5]: 0.0, col_name_bus[6]: 0.0}
    df_bus_nw_tmp = df_bus_nw_tmp.fillna(fill_values)
    df_bus_nw_tmp = df_bus_nw_tmp.copy()


    #�o�X�^���e�[�u���̓Ǎ�
    #if os.path.exists(path_bus_fare) != True:
    #    print('�o�X�^���e�[�u��:' + path_bus_fare + '������܂���')
    #    os.system('PAUSE')
    #    sys.exit()
    print(datetime.datetime.now().time(),'�o�X�^���e�[�u���Ǎ��F' + path_bus_fare)
    dtype_bus_fare = {0: str, 1: str, 2: str, 3: str, 4: float}
    df_bus_fare_tmp = pd.read_csv(path_bus_fare, encoding='shift-jis',dtype=dtype_bus_fare) 
    df_bus_fare_tmp['id'] = df_bus_fare_tmp.iloc[:, 0] + '_' + df_bus_fare_tmp.iloc[:, 1] + '_' +  df_bus_fare_tmp.iloc[:, 2] + '_' +  df_bus_fare_tmp.iloc[:, 3]
    df_bus_fare = df_bus_fare_tmp.sort_values('id').reset_index(drop=True)


    print(datetime.datetime.now().time(),'�f�[�^�Ǎ��I��')
    print(datetime.datetime.now().time(),'�o�XLOS�v�Z�J�n')


    #��ԃp�^�[�����X�g�̍쐬
    lst_line = list(set(df_bus_nw_tmp.iloc[:, 0] + '_' + df_bus_nw_tmp.iloc[:, 1] + '_' + df_bus_nw_tmp.iloc[:, 2]))
    lst_line.sort()


    #�抷�\�o�X��̔���
    connect = np.full((len(df_bus_stop), len(df_bus_stop)), 1) - np.eye(len(df_bus_stop))
    np.eye(len(df_bus_stop))
    lst_bus = list(df_bus_stop.iloc[:, -1])

    for line in lst_line:
        #��ԃp�^�[����NW�̐ݒ�
        df_bus_line = df_bus_nw_tmp[df_bus_nw_tmp.iloc[:, 0] + '_' + df_bus_nw_tmp.iloc[:, 1] + '_' + df_bus_nw_tmp.iloc[:, 2] == line].copy() #��ԃp�^�[���ʂɒ��o
        df_bus_line = df_bus_line.reset_index(drop=True) #�C���f�b�N�X�������p�����̂ŐU�蒼��
        jigyo = df_bus_line.iloc[0, 0]
        rosen = df_bus_line.iloc[0, 1]

        #�o�X��̏d���폜
        nam_bus_line = list(set(pd.concat([df_bus_line.iloc[:, 3], df_bus_line.iloc[:, 4]])))
        nam_bus_line.sort()

        #������ԃp�^�[���Ɋ܂܂��o�X��Ԃ͏抷�s��
        for ibus in nam_bus_line:
            i = lst_bus.index(jigyo + '_' + ibus)
            for jbus in nam_bus_line:
                j = lst_bus.index(jigyo + '_' + jbus)
                connect[i, j] = 0


    #���W�ϊ�
    transformer = pyproj.Transformer.from_crs(src_proj, dst_proj)
    bus_stop_x, bus_stop_y = transformer.transform(df_bus_stop.iloc[:, 2], df_bus_stop.iloc[:, 3])

    #�m�[�h�̈ʒu�֌W���w�K
    bus_stop_xy_array = np.array([bus_stop_x, bus_stop_y]).T
    knn_num = len(df_bus_stop) #�T���m�[�h��
    knn_model = NearestNeighbors(n_neighbors = knn_num, algorithm = 'ball_tree').fit(bus_stop_xy_array)

    #�o�X��ʂɐڑ��o�X���T�� �ЂƂ܂������o�X�₩�ŐU�蕪����
    lst_connect_same = []
    lst_connect_dif = []
    for ibus in range(len(df_bus_stop)):
        bus_stop_xy = [bus_stop_x[ibus], bus_stop_y[ibus]]
        knn_dists, knn_results = knn_model.kneighbors([bus_stop_xy])

        lst_connect_bus_same = []
        lst_connect_bus_dif = []
        nn = 0
        for ix in range(0, knn_num):
            if knn_dists[:,ix][0] > 100: #100m�܂ł͓���o�X��Ƃ݂Ȃ�
                break
            else:
                #�抷���
                jbus = knn_results[:,ix][0]
                if connect[ibus, jbus] == 1: #����H���̃o�X��łȂ�
                    if df_bus_stop.iloc[ibus, 4] == df_bus_stop.iloc[jbus, 4]: #���ꖼ�̂̏ꍇ�͓���o�X��ƔF�߂�
                        lst_connect_bus_same.append(jbus)
                    else:
                        lst_connect_bus_dif.append([jbus, knn_dists[:,ix][0]])
        if lst_connect_bus_same == []: #�������g���܂߂�
            lst_connect_bus_same.append(ibus)
        lst_connect_same.append(lst_connect_bus_same)
        lst_connect_dif.append(lst_connect_bus_dif)
        
    #��v�w���̃^�[�~�i����100m�ȏ㗣�ꂽ�����o�X����܂Ƃ߂�
    for ir in range(3): #�Ƃ肠����3��
        for ibus in range(len(df_bus_stop)):
            for jbus in lst_connect_same[ibus]:
                lst_connect_same[ibus] = list(set(lst_connect_same[ibus] + lst_connect_same[jbus]))
                lst_connect_same[ibus].sort()

    #�ʖ��o�X�₪�����o�X��̓���H���̃o�X��ł͂Ȃ����m�F
    for ibus in range(len(df_bus_stop)):
        for jbus in lst_connect_same[ibus]:
            lst_del = []
            for kbus in lst_connect_dif[ibus]:
                for lbus in lst_connect_same[kbus[0]]:
                    if connect[jbus, lbus] == 0:
                        lst_del.append(kbus)
                        break
            for kbus in lst_del:
                lst_connect_dif[ibus].remove(kbus)


    #�����o�X��ɏ]���āA�ʖ��o�X����܂Ƃ߂�
    for ibus in range(len(df_bus_stop)):
        for jbus in lst_connect_same[ibus]:
            if ibus != jbus:
                lst_connect_dif[ibus] = lst_connect_dif[ibus] + lst_connect_dif[jbus]

    for ibus in range(len(df_bus_stop)):
        lst_connect_dif[ibus].sort(key=lambda x: (x[1], x[0]))


    #�ʖ��o�X��̐ڑ��\�������� �ʖ��o�X��ǂ���������H���ɂȂ��i����H���ɂ���ꍇ�͋߂������̗p�j
    for ibus in range(len(df_bus_stop)):
        flg = [1] * len(lst_connect_dif[ibus])
        lst_del = []
        for jx, jbus in enumerate(lst_connect_dif[ibus][:-1]):
            for kbus in lst_connect_same[jbus[0]]:
                for lx, lbus in enumerate(lst_connect_dif[ibus][jx+1:], 1):
                    if flg[jx + lx] == 1:
                        for mbus in lst_connect_same[lbus[0]]:
                            if connect[kbus, mbus] == 0:
                                flg[jx + lx] = 0
                                lst_del.append(lbus)
                                break
        for i in range(len(lst_del)):
            lst_connect_dif[ibus].remove(lst_del[i])


    #�ʖ��o�X�₪1�̎��́A����o�X��Ƃ݂Ȃ��@��������ꍇ�͕ʃo�X��Ƃ��ď抷�\�Ƃ���
    for ibus in range(len(df_bus_stop)):
        if lst_connect_same[ibus][0] == ibus:
            if len(lst_connect_dif[ibus]) == 0:
                pass
            elif len(lst_connect_dif[ibus]) == 1:
                ix = lst_connect_dif[ibus][0][0]
                if ix < ibus: #���ɏ����ς݂̂͂��Ȃ̂ɑ��݁�ix�ŕ����ڑ�����\��������
                    lst_connect_dif[ibus] = []
                elif len(lst_connect_dif[ix]) > 1: #�ڑ����肪�����ڑ�����\������
                    lst_connect_dif[ibus] = []
                elif lst_connect_same[ix][0] < ibus: #���ɏ����ς�
                    lst_connect_dif[ibus] = []
                else:
                    for i in range(len(lst_connect_same[ix])):
                        ii = lst_connect_same[ix][i]
                        lst_connect_same[ibus].append(ii) #����o�X��Ƃ��Ă܂Ƃ߂�
                        if i > 0:
                            lst_connect_same[ii] = []
                            lst_connect_same[ii].append(ibus)
                            lst_connect_dif[ii] = []
                    lst_connect_same[ix] = []
                    lst_connect_same[ix].append(ibus)
                    lst_connect_dif[ix] = []
                    lst_connect_dif[ibus] = []
            else:
                for i in range(len(lst_connect_dif[ibus])):
                    lst_connect_dif[ibus][i] = lst_connect_dif[ibus][i][0] #���X�g���狗�����폜
        else:
            lst_connect_same[ibus] = [lst_connect_same[ibus][0]]
            lst_connect_dif[ibus] = []
        
        lst_connect_same[ibus].sort()


    #��ԃp�^�[���ʂɌo�H�T�� �o�X�Ԃ̕��Ϗ��v���ԂƉ^�s�{�����Z�o
    col_name = ['line_id', 'stop_id1', 'stop_id2', 'travel_time', 'fare', 'frequency','seq1','seq2']
    df_bus_line_los = pd.DataFrame(columns=col_name) #��ԃp�[�^����LOS�p�̃f�[�^�t���[��

    lst_bus = list(df_bus_stop.iloc[:, -1])

    for line in lst_line:
        #��ԃp�^�[����NW�̐ݒ�
        df_bus_line = df_bus_nw_tmp[df_bus_nw_tmp.iloc[:, 0] + '_' + df_bus_nw_tmp.iloc[:, 1] + '_' + df_bus_nw_tmp.iloc[:, 2] == line].copy() #��ԃp�^�[���ʂɒ��o
        df_bus_line = df_bus_line.reset_index(drop=True) #�C���f�b�N�X�������p�����̂ŐU�蒼��
        jigyo = df_bus_line.iloc[0, 0]
        rosen = df_bus_line.iloc[0, 1]

        #�o�X��̏d���폜
        nam_bus_line = list(set(pd.concat([df_bus_line.iloc[:, 3], df_bus_line.iloc[:, 4]])))
        nam_bus_line.sort()

        #���v���Ԍv�Z ��ԃp�^�[���ň�����Ȃ̂ŁA�o�H�T�������ɒP���ɐςݏグ
        tim_line = np.full((len(nam_bus_line), len(nam_bus_line)), 9999.0)
        for i in range(len(df_bus_line)):
            tim = 0.0
            ibus = nam_bus_line.index(df_bus_line.iloc[i, 3])
            for j in range(i + 1, len(df_bus_line) + 1):
                tim = tim + df_bus_line.iloc[j - 1, 5] / 10.0
                jbus = nam_bus_line.index(df_bus_line.iloc[j - 1, 4])
                tim_line[ibus, jbus] = min(tim_line[ibus, jbus], tim) #������o������W��������̂ŁA�Z�����ɂ܂Ƃ߂�

        #�^�������߂āA��ԃp�^�[����LOS���쐬
        lst_dmy = []
        for i, ibus in enumerate(nam_bus_line):
            for j, jbus in enumerate(nam_bus_line):
                if (tim_line[i, j] < 9999.0) and (i != j): #�T���s�\��2�x�o�Ă���o�X�������
                    if len(df_bus_fare) > 0:
	                    ix = los_calc.bish(jigyo + '_' + rosen + '_' + ibus + '_' + jbus, df_bus_fare.iloc[:,-1])
	                    if ix != -1:
	                        fare = df_bus_fare.iloc[ix, -2]
	                        ii = lst_bus.index(jigyo + '_' + ibus)
	                        ii = lst_connect_same[ii][0]
	                        jj = lst_bus.index(jigyo + '_' + jbus)
	                        jj = lst_connect_same[jj][0]
	                        #��ԃp�^�[���ʂȂ̂ŉ^�s�{���͒�ԃp�^�[����1��
	                        if round(tim_line[i, j], 0) == 0.0:
	                            tim = 0.5
	                        else:
	                            tim = round(tim_line[i, j], 0)
	                        lst_dmy.append([line,ibus,jbus,tim,fare,df_bus_line.iloc[0, 6],ii,jj])
                    else: #�^���e�[�u�����Ȃ��ꍇ
	                        ii = lst_bus.index(jigyo + '_' + ibus)
	                        ii = lst_connect_same[ii][0]
	                        jj = lst_bus.index(jigyo + '_' + jbus)
	                        jj = lst_connect_same[jj][0]
	                        #��ԃp�^�[���ʂȂ̂ŉ^�s�{���͒�ԃp�^�[����1��
	                        if round(tim_line[i, j], 0) == 0.0:
	                            tim = 0.5
	                        else:
	                            tim = round(tim_line[i, j], 0)
	                        lst_dmy.append([line,ibus,jbus,tim,0,df_bus_line.iloc[0, 6],ii,jj])
        df_bus_line_los = pd.concat([df_bus_line_los, pd.DataFrame(lst_dmy, columns = col_name)], axis=0, ignore_index=True)


    #�n����LOS���W�񂷂�
    df_bus_line_los['frequency_tmp'] = np.maximum(1, df_bus_line_los['frequency'].values)
    df_bus_line_los['sumtime'] = df_bus_line_los['travel_time'] * df_bus_line_los['frequency_tmp']
    df_bus_line_los['sumfare'] = df_bus_line_los['fare'] * df_bus_line_los['frequency_tmp']
    df_bus_nw = df_bus_line_los.groupby(['seq1','seq2'])[['sumtime', 'sumfare', 'frequency', 'frequency_tmp']].sum()
    df_bus_nw['travel_time'] = df_bus_nw['sumtime'] / df_bus_nw['frequency_tmp']
    df_bus_nw['fare'] = df_bus_nw['sumfare'] / df_bus_nw['frequency_tmp']
    df_bus_nw['type'] = 1
    col_name = ['seq1', 'seq2', 'travel_time', 'fare', 'frequency', 'type']
    df_bus_nw = df_bus_nw.reset_index().reindex(columns=col_name)


    #�抷�����N��ݒ�
    lst_dmy = []
    col_name = ['seq1', 'seq2', 'travel_time', 'fare', 'frequency', 'type']
    for ibus in range(len(df_bus_stop)):
        for jbus in lst_connect_dif[ibus]:
            lst_dmy.append([ibus,jbus,0,0,0,0])
            df_bus_trans = pd.DataFrame(lst_dmy, columns=col_name)


    #�o�X���LOS�Ə抷�����N����������NW���쐬
    df_bus_nw = pd.concat([df_bus_nw, df_bus_trans], axis=0, ignore_index=True)


    #print(datetime.datetime.now().time(),'�S�o�X��ԒT��')
    #�o�X��ԒT��
    #�m�[�hSEQ�̍쐬
    nam_bus = list(set(pd.concat([df_bus_nw.iloc[:,0],df_bus_nw.iloc[:,1]])))
    #�m�[�hSEQ���Z�b�g
    lf = []
    for i in range(0, len(df_bus_nw)):
        lf.append(nam_bus.index(df_bus_nw.iloc[i, 0]))
    df_bus_nw['From�m�[�hSEQ'] = lf
    lt = []
    for i in range(0, len(df_bus_nw)):
        lt.append(nam_bus.index(df_bus_nw.iloc[i, 1]))
    df_bus_nw['To�m�[�hSEQ'] = lt

    jla = [0] * (len(nam_bus) + 1)
    jlx = [0] * (len(df_bus_nw) * 2)
    lij = list(df_bus_nw.iloc[:, 5])
    los_calc.forwardstar(len(df_bus_nw), len(nam_bus), list(df_bus_nw.iloc[:, -2]), list(df_bus_nw.iloc[:, -1]), jla, jlx, lij)

    #�����N�R�X�g�̐ݒ�
    #��Ԏ���
    lvp = df_bus_nw.iloc[:, 2].copy()
    lvm = df_bus_nw.iloc[:, 2].copy()
    #�҂����Ԃ����Z
    lvp += np.minimum(tim_limit, np.divide(60.0 * tim_ope / 2.0, df_bus_nw.iloc[:, 4], out=np.zeros_like(df_bus_nw.iloc[:, 4], dtype=np.float64), where=(df_bus_nw.iloc[:, 5] == 1) & (df_bus_nw.iloc[:, 4] == 0)))
    lvm += np.minimum(tim_limit, np.divide(60.0 * tim_ope / 2.0, df_bus_nw.iloc[:, 4], out=np.zeros_like(df_bus_nw.iloc[:, 4], dtype=np.float64), where=(df_bus_nw.iloc[:, 5] == 1) & (df_bus_nw.iloc[:, 4] == 0)))
    #�ނ�݂ɏ抷�𑝂₳�Ȃ��悤�ɏ抷����
    lvp += [ n * tim_load for n in list(df_bus_nw.iloc[:, 5]) ]
    lvm += [ n * tim_load for n in list(df_bus_nw.iloc[:, 5]) ]

    #�o�H�T��
    tim_bus = np.full(len(df_bus_stop) ** 2, 9999.0).reshape(len(df_bus_stop), len(df_bus_stop))
    tim_bus_wait = np.full(len(df_bus_stop) ** 2, 0.0).reshape(len(df_bus_stop), len(df_bus_stop))
    tim_bus_wait_hatu = np.full(len(df_bus_stop) ** 2, 0.0).reshape(len(df_bus_stop), len(df_bus_stop))
    fare_bus = np.full(len(df_bus_stop) ** 2, 9999.0).reshape(len(df_bus_stop), len(df_bus_stop))

    lst_key = list(range(len(df_bus_nw)))
    lst_travel_time = df_bus_nw['travel_time'].to_list()
    lst_fare = df_bus_nw['fare'].to_list()
    lst_frequency = df_bus_nw['frequency'].to_list()
    lst_type = df_bus_nw['type'].to_list()

    dct_travel_time = dict(zip(lst_key, lst_travel_time))
    dct_fare = dict(zip(lst_key, lst_fare))
    dct_frequency = dict(zip(lst_key, lst_frequency))
    dct_type = dict(zip(lst_key, lst_type))


    #��p�Ȃ��ōs����o�X��Ԃ�LOS���Z�b�g
    for i in range(len(df_bus_nw) - len(df_bus_trans)):
        ibus = df_bus_nw.iloc[i, 0]
        jbus = df_bus_nw.iloc[i, 1]
        tim_bus[ibus, jbus] = df_bus_nw.iloc[i, 2]
        if df_bus_nw.iloc[i, 4] != 0:
            tim_bus_wait[ibus, jbus] = min(60.0 * tim_ope / df_bus_nw.iloc[i, 4] / 2.0, tim_limit)
            tim_bus_wait_hatu[ibus, jbus] = min(60.0 * tim_ope / df_bus_nw.iloc[i, 4] / 2.0, tim_limit)
        fare_bus[ibus, jbus] = df_bus_nw.iloc[i, 3]

    for ibus in range(len(nam_bus)):
        ndin = ibus #�T���N�_
        minv = [math.inf] * len(nam_bus)
        nxt = [-1] * len(nam_bus)
        lno = [0] * len(nam_bus)

        #�_�C�N�X�g���@�ɂ��ŒZ�o�H�T��
        los_calc.dijkstra_bus(ndin, len(nam_bus), minv, list(df_bus_nw.iloc[:, -2]), list(df_bus_nw.iloc[:, -1]), lvp, lvm, jla, jlx, nxt, lno, list(df_bus_nw.iloc[:, -3]))

        for jbus in range(len(nam_bus)):
            if ibus == jbus: continue
            if tim_bus[nam_bus[ibus], nam_bus[jbus]] < 9999.0: continue #��p�Ȃ��ōs����o�X��Ԃ͒T�����Ȃ�
            ndtb = []
            lktb = []
            ierr, ir, tim_bus[nam_bus[ibus], nam_bus[jbus]], tim_bus_wait[nam_bus[ibus], nam_bus[jbus]], tim_bus_wait_hatu[nam_bus[ibus], nam_bus[jbus]], fare_bus[nam_bus[ibus], nam_bus[jbus]] = los_calc.rotout_bus(ibus, jbus, nxt, lno, ndtb, lktb, dct_travel_time, dct_fare, dct_frequency, dct_type, tim_limit, tim_ope)


    #�o�X�A�N�Z�X�Z�o
    znbus = [] #�]�[���ʃA�N�Z�X�o�X�̃��X�g
    dist_znbus = [] #�]�[���ʃA�N�Z�X�o�X�ւ̋������X�g
    transformer = pyproj.Transformer.from_crs(src_proj, dst_proj)
    #���W�ϊ�
    zn_x, zn_y = transformer.transform(df_zn.iloc[:, 1], df_zn.iloc[:, 2])

    for zn in range(0, len(df_zn)):
        zn_xy = [zn_x[zn], zn_y[zn]]
        knn_dists, knn_results = knn_model.kneighbors([zn_xy])

        lst_bus = []
        lst_dist = []

        #�ő�5km�܂�500m�P�ʂŔ͈͂��L���āA�A�N�Z�X����w�����
        maxdist = math.ceil(knn_dists[:,0][0] / 500) #�Ŋ��w
        if maxdist > 5:
            pass
        else:
            for ix in range(0, knn_num):
                if knn_dists[:,ix][0] / 500 > maxdist:
                    break
                else:
                    lst_bus.append(knn_results[:,ix][0])
                    lst_dist.append(knn_dists[:,ix][0])
        znbus.append(lst_bus)
        dist_znbus.append(lst_dist)


    #�]�[����LOS���v�Z
    #�o�͗p�̃f�[�^�t���[��������
    df_los = pd.DataFrame(columns=['Travel_Time_Bus', 'Waiting_Time_Bus', 'Access_Time_Bus', 'Egress_Time_Bus', 'Fare_Bus'])
    lst_jz = df_zn.iloc[:, 0]

    for iz in range(0, len(df_zn)):
        lst_los = []
        for jz in range(0, len(df_zn)):
            sumtim = 9999.0
            min_i = len(df_bus_stop)
            min_j = len(df_bus_stop)
            if iz == jz:
                lst_los.append([0.0,0.0,0.0,0.0,0.0])
            else:
                for i, bus_acs in enumerate(znbus[iz]):
                    for j, bus_egr in enumerate(znbus[jz]):
                        ibus = lst_connect_same[bus_acs][0]
                        jbus = lst_connect_same[bus_egr][0]
                        if sumtim > tim_bus[ibus, jbus] + tim_bus_wait[ibus, jbus] + \
                                    dist_znbus[iz][i] * math.sqrt(2) / 80.0 + \
                                    dist_znbus[jz][j] * math.sqrt(2) / 80.0:
                            sumtim = tim_bus[ibus, jbus] + tim_bus_wait[ibus, jbus] + \
                                    dist_znbus[iz][i] * math.sqrt(2) / 80.0 + \
                                    dist_znbus[jz][j] * math.sqrt(2) / 80.0
                            min_i = i
                            min_j = j
                if sumtim == 9999.0:
                    lst_los.append([9999.0,9999.0,9999.0,9999.0,9999.0])
                else:
                    ibus = lst_connect_same[znbus[iz][min_i]][0]
                    jbus = lst_connect_same[znbus[jz][min_j]][0]
                    lst_los.append([round(tim_bus[ibus, jbus], 1),round(tim_bus_wait[ibus, jbus] - tim_bus_wait_hatu[ibus, jbus] + tim_wait, 1),round(dist_znbus[iz][min_i] * math.sqrt(2) / 80.0, 1),round(dist_znbus[jz][min_j] * math.sqrt(2) / 80.0, 1),round(fare_bus[ibus, jbus], 1)])

        df_los_zn = pd.DataFrame(lst_los, columns=['Travel_Time_Bus', 'Waiting_Time_Bus', 'Access_Time_Bus', 'Egress_Time_Bus', 'Fare_Bus'])
        df_los = pd.concat([df_los, df_los_zn], axis=0, ignore_index=True)

    print(datetime.datetime.now().time(),'�o�XLOS�v�Z�I��')
    return df_los


def los_dmy(df_zn):
    df_los = pd.DataFrame(columns=['Travel_Time_Bus', 'Waiting_Time_Bus', 'Access_Time_Bus', 'Egress_Time_Bus', 'Fare_Bus'])
    
    for iz in range(0, len(df_zn)):
        lst_los = []
        for jz in range(0, len(df_zn)):
            if iz == jz:
                lst_los.append([0.0,0.0,0.0,0.0,0.0])
            else:
                lst_los.append([9999.0,9999.0,9999.0,9999.0,9999.0])

        df_los_zn = pd.DataFrame(lst_los, columns=['Travel_Time_Bus', 'Waiting_Time_Bus', 'Access_Time_Bus', 'Egress_Time_Bus', 'Fare_Bus'])
        df_los = pd.concat([df_los, df_los_zn], axis=0, ignore_index=True)
    return df_los
