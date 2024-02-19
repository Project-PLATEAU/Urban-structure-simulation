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

def calc_los_car(indir, outdir, src_proj, dst_proj, df_zn):
    warnings.simplefilter('ignore', FutureWarning)

    #�g�p�t�@�C�����w��
    path_shp_link = indir + '/Road_NW.shp' #���HNW�����N��shp
    path_shp_node = indir + '/Road_Node.shp' #���HNW�m�[�h��shp


    if os.path.exists(path_shp_link) != True:
        print('���HNW�����Nshp:' + path_shp_link + '������܂���')
        print('������LOS�쐬���X�L�b�v���܂�')
        df_los = los_dmy(df_zn)
        return df_los
    if os.path.exists(path_shp_node) != True:
        print('���HNW�m�[�hshp:' + path_shp_node + '������܂���')
        print('������LOS�쐬���X�L�b�v���܂�')
        df_los = los_dmy(df_zn)
        return df_los


    print(datetime.datetime.now().time(),'�f�[�^�Ǎ��J�n')
    #���HNW�����Nshp�Ǎ�
    #if os.path.exists(path_shp_link) != True:
    #    print('���HNW�����Nshp:' + path_shp_link + '������܂���')
    #    os.system('PAUSE')
    #    sys.exit()
    print(datetime.datetime.now().time(),'���HNW�����N�Ǎ��F' + path_shp_link)
    gdf = gpd.read_file(path_shp_link)
    #�����N�f�[�^���f�[�^�t���[���ɕϊ�
    df_road_nw_link = pd.DataFrame(gdf.iloc[:,:-1].values, columns = list(gdf.columns.values)[:-1])
    col_name = df_road_nw_link.columns.values


    #���HNW�����N�̃f�[�^�̕⊮
    fill_values = {col_name[4]: 0.0, col_name[5]: 0, col_name[6]: 9, col_name[7]: 1.0, col_name[8]: 0, col_name[9]: 0, col_name[10]: 0, col_name[11]: 2.0}
    df_road_nw_link_tmp = df_road_nw_link.fillna(fill_values)
    df_road_nw_link = df_road_nw_link_tmp.copy()


    #���HNW�m�[�hshp�Ǎ�
    #if os.path.exists(path_shp_node) != True:
    #    print('���HNW�m�[�hshp:' + path_shp_node + '������܂���')
    #    os.system('PAUSE')
    #    sys.exit()
    print(datetime.datetime.now().time(),'���HNW�m�[�h�Ǎ��F' + path_shp_node)
    gdf = gpd.read_file(path_shp_node)
    #�m�[�h�f�[�^���f�[�^�t���[���ɕϊ�
    df_road_nw_node = pd.DataFrame(gdf.iloc[:,:-1].values, columns = list(gdf.columns.values)[:-1] )


    print(datetime.datetime.now().time(),'�f�[�^�Ǎ��I��')
    print(datetime.datetime.now().time(),'������LOS�v�Z�J�n')

    #���ӌ�_�̏���
    lst_link_dmy = []
    lst_link_dmy_node1 = []
    lst_link_dmy_node2 = []
    lst_link_dmy_data = ['0', '0', '0', 1.0, 0, 0, 10, 30.0, 0, 1, 0, 4] #���̑���
    for i in range(len(df_road_nw_node)):
        if df_road_nw_node.iloc[i, 3] == '000000':
            continue
        if df_road_nw_node.iloc[i, 0] > df_road_nw_node.iloc[i, 3] + df_road_nw_node.iloc[i, 4]:
            continue   
        lst_link_dmy.append(lst_link_dmy_data)
        lst_link_dmy_node1.append(df_road_nw_node.iloc[i, 0])
        lst_link_dmy_node2.append(df_road_nw_node.iloc[i, 3] + df_road_nw_node.iloc[i, 4])
    df_link_dmy = pd.DataFrame(lst_link_dmy, columns = col_name)
    df_link_dmy.iloc[:, 1] = lst_link_dmy_node1
    df_link_dmy.iloc[:, 2] = lst_link_dmy_node2


    #���HNW�̃����N�Ƌ��ӌ�_�����N������
    df_road_nw = pd.concat([df_road_nw_link, df_link_dmy], axis=0, ignore_index=True)


    #�m�[�hSEQ�̍쐬(�ꎞ�l)
    nam = list(set(pd.concat([df_road_nw.iloc[:, 1],df_road_nw.iloc[:, 2]])))
    nam.sort()

    lf = []
    for i in df_road_nw.iloc[:, 1]:
        lf.append(nam.index(i))
    df_road_nw['From�m�[�hSEQ'] = lf

    lt = []
    for i in df_road_nw.iloc[:, 2]:
        lt.append(nam.index(i))
    df_road_nw['To�m�[�hSEQ'] = lt
    col_name = df_road_nw.columns.values


    #�]�[���A�N�Z�X�����N�̍쐬����
    #�m�[�h�����ꓹ�m�[�h����ʓ��m�[�h���𔻒f
    linknum_in = [0] * (len(nam)) #�m�[�h�ɓ����Ă��郊���N��
    linknum_out = [0] * (len(nam)) #�m�[�h�ɏo�Ă��������N��
    for i in range(len(df_road_nw)):
        if df_road_nw.iloc[i, 8] == 1: #���ꓹ�����N
            continue
        if df_road_nw.iloc[i, 9] == 1: #�A�N�Z�X�s�����N
            continue
        if df_road_nw.iloc[i, 4] == 1: #�ʍs�s�����N
            continue
        
        if df_road_nw.iloc[i, 5] == 0: #������
            linknum_out[df_road_nw.iloc[i, 12]] = linknum_out[df_road_nw.iloc[i, 12]] + 1
            linknum_in[df_road_nw.iloc[i, 13]] = linknum_in[df_road_nw.iloc[i, 13]] + 1
            linknum_in[df_road_nw.iloc[i, 12]] = linknum_in[df_road_nw.iloc[i, 12]] + 1
            linknum_out[df_road_nw.iloc[i, 13]] = linknum_out[df_road_nw.iloc[i, 13]] + 1
        elif df_road_nw.iloc[i, 5] == 1: #From��To
            linknum_out[df_road_nw.iloc[i, 12]] = linknum_out[df_road_nw.iloc[i, 12]] + 1
            linknum_in[df_road_nw.iloc[i, 13]] = linknum_in[df_road_nw.iloc[i, 13]] + 1
        elif df_road_nw.iloc[i, 5] == 2: #To��From
            linknum_in[df_road_nw.iloc[i, 12]] = linknum_in[df_road_nw.iloc[i, 12]] + 1
            linknum_out[df_road_nw.iloc[i, 13]] = linknum_out[df_road_nw.iloc[i, 13]] + 1
        else:
            continue

    #�o����ł���m�[�h�Ƀt���O�𗧂Ă�
    connect = [0] * (len(nam))
    for i in range(len(nam)):
        if linknum_in[i] > 0 and linknum_out[i] > 0:
            connect[i] = 1


    #�]�[���A�N�Z�X�����N�̍쐬
    lst_link_acs = []
    lst_link_acs_node1 = []
    lst_link_acs_node2 = []
    lst_link_acs_dist = []
    lst_link_acs_node1_seq = []
    lst_link_acs_node2_seq = []
    lst_link_acs_data = ['0', '0', '0', 99999.0, 0, 0, 11, 30.0, 0, 1, 0, 4, 0, 0]
    transformer = pyproj.Transformer.from_crs(src_proj, dst_proj)
    #���W�ϊ�
    node_x, node_y = transformer.transform(df_road_nw_node.iloc[:, 1], df_road_nw_node.iloc[:, 2])
    zn_x, zn_y = transformer.transform(df_zn.iloc[:, 1], df_zn.iloc[:, 2])
    #�m�[�h�̈ʒu�֌W���w�K
    node_xy_array = np.array([node_x, node_y]).T
    knn_num = 100 #�T���m�[�h��
    knn_model = NearestNeighbors(n_neighbors = knn_num, algorithm = 'ball_tree').fit(node_xy_array)

    for i in range(len(df_zn)):
        zn_xy = [zn_x[i], zn_y[i]]
        knn_dists, knn_results = knn_model.kneighbors([zn_xy])
        #�T�����ʂ���A�N�Z�X��t���Ă����m�[�h��I��ŃA�N�Z�X�����N���쐬
        for ix in range(knn_num):
            nx = knn_results[:,ix][0]
            nx = los_calc.bish(df_road_nw_node.iloc[nx, 0], nam)
            if connect[nx] == 0:
                continue
            lst_link_acs.append(lst_link_acs_data)
            lst_link_acs_node1.append(str(i))
            lst_link_acs_node2.append(nam[nx])
            lst_link_acs_dist.append(knn_dists[:,ix][0])
            lst_link_acs_node1_seq.append(i)
            lst_link_acs_node2_seq.append(nx + len(df_zn))
            break
    df_link_acs = pd.DataFrame(lst_link_acs, columns = col_name)
    df_link_acs.iloc[:, 1] = lst_link_acs_node1
    df_link_acs.iloc[:, 2] = lst_link_acs_node2
    df_link_acs.iloc[:, 3] = lst_link_acs_dist
    df_link_acs.iloc[:, 12] = lst_link_acs_node1_seq
    df_link_acs.iloc[:, 13] = lst_link_acs_node2_seq


    #�]�[����SEQ�����HNW�̃m�[�h�����O�ɗ���悤�ɂ��炷
    df_road_nw.iloc[:, 12] = df_road_nw.iloc[:, 12] + len(df_zn)
    df_road_nw.iloc[:, 13] = df_road_nw.iloc[:, 13] + len(df_zn)


    #���HNW�ƃ]�[���A�N�Z�X������
    df_road_nw = pd.concat([df_road_nw, df_link_acs], axis=0, ignore_index=True)


    #���H��ʂɂ�鑬�x�ݒ�
    for i in range(len(df_road_nw)):
        if df_road_nw.iloc[i, 6] == 1: #���������ԍ���
            df_road_nw.iloc[i, 7] = 80.0
        elif df_road_nw.iloc[i, 6] == 2: #�s�s�������H
            df_road_nw.iloc[i, 7] = 60.0
        elif df_road_nw.iloc[i, 6] == 3: #��ʍ���
            if df_road_nw.iloc[i, 8] == 1:
                df_road_nw.iloc[i, 7] = 60.0
            else:
                df_road_nw.iloc[i, 7] = 50.0
        elif df_road_nw.iloc[i, 6] == 4: #��v�n�����i�s���{�����j
            df_road_nw.iloc[i, 7] = 40.0
        elif df_road_nw.iloc[i, 6] == 5: #��v�n�����i�w��s���j
            df_road_nw.iloc[i, 7] = 40.0
        elif df_road_nw.iloc[i, 6] == 6: #��ʓs���{����
            df_road_nw.iloc[i, 7] = 40.0
        elif df_road_nw.iloc[i, 6] == 7: #�w��s�̈�ʎs��
            df_road_nw.iloc[i, 7] = 30.0
        elif df_road_nw.iloc[i, 6] == 9: #���̑��̓��H
            df_road_nw.iloc[i, 7] = 30.0
        elif df_road_nw.iloc[i, 6] == 0: #������
            df_road_nw.iloc[i, 7] = 30.0
        else: #�]�[���A�N�Z�X�A���ӌ�_��
            df_road_nw.iloc[i, 7] = 30.0


    #�����N�ڑ�����forward star�`���ɕϊ�
    #������
    jla = [0] * (len(nam) + len(df_zn) + 1)
    jlx = [0] * (len(df_road_nw) * 2)
    los_calc.forwardstar_car(len(df_road_nw), len(nam) + len(df_zn), list(df_road_nw.iloc[:, 12]), list(df_road_nw.iloc[:, 13]), jla, jlx, list(df_road_nw.iloc[:, 5]), list(df_road_nw.iloc[:, 4]))


    #�����N�R�X�g�̐ݒ�
    lcost = df_road_nw.iloc[:, 3] / 1000.0 / df_road_nw.iloc[:, 7] * 60.0

    lvp = lcost
    lvm = lcost

    df_los = pd.DataFrame(columns=['Travel_Time_Car'])

    #�o�H�T���̏�����
    for iz in range(len(df_zn)):
        ndin = iz #�T���N�_
        minv = [math.inf] * (len(nam) + len(df_zn))
        nxt = [-1] * (len(nam) + len(df_zn))
        lno = [0] * (len(nam) + len(df_zn))

        #�_�C�N�X�g���@�ɂ��ŒZ�o�H�T��
        los_calc.dijkstra_car(ndin, len(nam) + len(df_zn), minv, list(df_road_nw.iloc[:, 12]), list(df_road_nw.iloc[:, 13]), lvp, lvm, jla, jlx, nxt, lno)

        df_los_zn = pd.DataFrame(list(np.round(minv[:len(df_zn)], 1)), columns=['Travel_Time_Car'])
        df_los = pd.concat([df_los, df_los_zn], axis=0, ignore_index=True)

    df_los = df_los.replace(math.inf, 9999.0)
    print(datetime.datetime.now().time(),'������LOS�v�Z�I��')
    return df_los


def los_dmy(df_zn):
    df_los = pd.DataFrame(columns=['Travel_Time_Car'])
    
    for iz in range(len(df_zn)):
        lst_los = []
        for jz in range(len(df_zn)):
            if iz == jz:
                lst_los.append([0,0])
            else:
                lst_los.append([9999.0])

        df_los_zn = pd.DataFrame(lst_los, columns=['Travel_Time_Car'])
        df_los = pd.concat([df_los, df_los_zn], axis=0, ignore_index=True)
    return df_los
