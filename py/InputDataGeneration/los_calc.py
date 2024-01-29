#coding:Shift_Jis
import math
'''
�o�C�i���T�[�`
  value:�����l
  data:�����Ώۃ��X�g
'''
def bish(value, data):
    left = 0
    right = len(data) - 1
    while left <= right:
        mid = (left + right) // 2
        if value == data[mid]: # ��������
            return mid
        elif value > data[mid]:
            left = mid + 1
        else:
            right = mid - 1
    return -1 # �����o


'''
���HNW�̃����N�ڑ�����forward star�`���ɕϊ�
  nlink:�����N��
  nnode:�m�[�h��
  lfr:�n�_�m�[�hSEQ
  lto:�I�_�m�[�hSEQ
  jla:�����N�ڑ����i�}���j
  jlx:�����N�ڑ����i�����NSEQ�j
  lij:�����t���O
  nopass:�s�ʉ߃t���O
'''
def forwardstar_car(nlink, nnode, lfr, lto, jla, jlx, lij, nopass):
    #�e�m�[�h�̐ڑ������N�����Z�o
    for lx in range(nlink):
        if nopass[lx] == 1: #�ʍs�s��
            continue
        elif lij[lx] == -1: #�ʍs�s��
            continue
        elif lij[lx] == 0: #�����������N
            lf = lfr[lx]
            jla[lf + 1] = jla[lf + 1] + 1
            lt = lto[lx]
            jla[lt + 1] = jla[lt + 1] + 1
        elif lij[lx] == 1: #From��To
            lf = lfr[lx]
            jla[lf + 1] = jla[lf + 1] + 1
        elif lij[lx] == 2: #To��From
            lt = lto[lx]
            jla[lt + 1] = jla[lt + 1] + 1
    
    #�e�m�[�h�̐ڑ����̃|�C���^��ݒ�
    for nx in range(nnode):
        jla[nx + 1] = jla[nx + 1] + jla[nx]
    
    #�e�m�[�h�̐ڑ������N��ݒ�
    for lx in range(nlink):
        if nopass[lx] == 1: #�ʍs�s��
            continue
        elif lij[lx] == -1: #�ʍs�s��
            continue
        elif lij[lx] == 0: #�����������N
            lf = lfr[lx]
            jl = jla[lf]
            jlx[jl] = lx + 1
            jla[lf] = jla[lf] + 1
            lt = lto[lx]
            jl = jla[lt]
            jlx[jl] = -(lx + 1)
            jla[lt] = jla[lt] + 1
        elif lij[lx] == 1: #From��To
            lf = lfr[lx]
            jl = jla[lf]
            jlx[jl] = lx + 1
            jla[lf] = jla[lf] + 1
        elif lij[lx] == 2: #To��From
            lt = lto[lx]
            jl = jla[lt]
            jlx[jl] = -(lx + 1)
            jla[lt] = jla[lt] + 1
            
    #�e�m�[�h�̐ڑ������N��ݒ�ŕύX���ꂽ�e�m�[�h�̐ڑ������N�������ɖ߂�
    for lx in range(nlink):
        if nopass[lx] == 1: #�ʍs�s��
            continue
        elif lij[lx] == -1: #�ʍs�s��
            continue
        elif lij[lx] == 0: #�����������N
            lf = lfr[lx]
            jla[lf] = jla[lf] - 1
            lt = lto[lx]
            jla[lt] = jla[lt] - 1
        elif lij[lx] == 1: #From��To
            lf = lfr[lx]
            jla[lf] = jla[lf] - 1
        elif lij[lx] == 2: #To��From
            lt = lto[lx]
            jla[lt] = jla[lt] - 1
    return


'''
�_�C�N�X�g���@�ɂ�鎩����LOS�p�̍ŒZ�o�H�T��
  ndin:�T���n�_�m�[�h
  nnode:�m�[�h��
  minv:�ŒZ�o�H�R�X�g
  lfr:�n�_�m�[�hSEQ
  lto:�I�_�m�[�hSEQ
  lvp:�n�_�m�[�hSEQ
  lvm:�I�_�m�[�hSEQ
  jla:�����N�ڑ����i�}���j
  jlx:�����N�ڑ����i�����NSEQ�j
  nxt:�ŒZ�o�H�ڑ��m�[�h
  lno:�ŒZ�o�H�ڑ������N�ԍ�
'''
def dijkstra_car(ndin, nnode, minv, lfr, lto, lvp, lvm, jla, jlx, nxt, lno):
    #������
    mx = nnode + 1
    lbl = [mx] * nnode
    npo = [mx] * nnode
    no = ndin #�n�_
    minv[no] = 0 #�n�_�̃R�X�g
    lbl[no] = -1 #�n�_�͒T����
    nxt[no] = 0 #�n�_�͐ڑ���Ȃ�
    nmin = mx #�ŏ��R�X�g�m�[�h
    nmax = mx #�ő�R�X�g�m�[�h

    while True:
        #�����N�̌������l�����ăR�X�g�v�Z
        for jl in range(jla[no], jla[no + 1]):
            ln = jlx[jl]
            if ln == 0: #�ʍs�s��
                continue
            elif ln > 0: #From��To
                nx = lto[ln - 1]
                if lbl[nx] < 0: #�o�H�m��ς݃m�[�h
                    continue
                else:
                    lv = minv[no] + lvp[ln - 1]
            elif ln < 0: #To��From
                nx = lfr[abs(ln) - 1]
                if lbl[nx] < 0: #�o�H�m��ς݃m�[�h
                    continue
                else:
                    lv = minv[no] + lvm[abs(ln) - 1]

            if lv < minv[nx]:
                if nmin == mx: #�T�����W������
                    nmax = nx
                    nmin = nx
                    npo[nx] = mx #�m�[�hnx���R�X�g���������m�[�h�͂Ȃ�
                elif nmin == nx: #�ŏ��R�X�g�m�[�h�̃R�X�g���X�V
                    pass
                else:
                    if minv[nx] == math.inf: #���Y�m�[�h�����߂ĒT�����ꂽ �R�X�g���ő�Ɖ���
                        nn = nmax
                    else:
                        nn = npo[nx]
                        if nmax == nx: #�ő�R�X�g�̃m�[�h�̃R�X�g���X�V�@�R�X�g���ő傩��1�O�ɂȂ�Ɖ���
                            nmax = npo[nx]
                        else: #nx�����o���đO����q���ς�
                            np = lbl[nx]
                            npo[np] = npo[nx]    
                        lbl[nn] = lbl[nx]

                    while True: #�T���m�[�h�̌q�����m�肳����
                        if minv[nn] > lv:
                            nn = npo[nn]
                            if nn == mx:
                                lbl[nx] = nmin
                                npo[nmin] = nx
                                nmin = nx
                                npo[nx] = mx
                                break
                        else:
                            lbl[nx] = lbl[nn]
                            lbl[nn] = nx
                            npo[nx] = nn
                            if lbl[nx] == mx:
                                nmax = nx
                            else:
                                nj = lbl[nx]
                                npo[nj] = nx
                            break

                minv[nx] = lv
                nxt[nx] = no
                lno[nx] = ln
            else:
                continue


        if nmin == mx: #�S�m�[�h�̌o�H���肵�����ߒT���I��
            break
        else: #�ŏ��R�X�g�����܂����m�[�h�𖢊m��m�[�h���X�g������o��
            no = nmin
            nmin = lbl[no]
            lbl[no] = -1
            if nmin != mx:
                npo[nmin] = mx
    return


'''
�S��NW�ƃo�XNW�p�̃����N�ڑ�����forward star�`���ɕϊ�
  nlink:�����N��
  nnode:�m�[�h��
  lfr:�n�_�m�[�hSEQ
  lto:�I�_�m�[�hSEQ
  jla:�����N�ڑ����i�}���j
  jlx:�����N�ڑ����i�����NSEQ�j
  lij:�����t���O
'''
def forwardstar(nlink, nnode, lfr, lto, jla, jlx, lij):
    #�e�m�[�h�̐ڑ������N�����Z�o
    for lx in range(nlink):
        if lij[lx] == -1: #�ʍs�s��
            continue
        elif lij[lx] == 0: #�����������N
            lf = lfr[lx]
            jla[lf + 1] = jla[lf + 1] + 1
            lt = lto[lx]
            jla[lt + 1] = jla[lt + 1] + 1
        elif lij[lx] == 1: #From��To
            lf = lfr[lx]
            jla[lf + 1] = jla[lf + 1] + 1
        elif lij[lx] == 2: #To��From
            lt = lto[lx]
            jla[lt + 1] = jla[lt + 1] + 1
    
    #�e�m�[�h�̐ڑ����̃|�C���^��ݒ�
    for nx in range(nnode):
        jla[nx + 1] = jla[nx + 1] + jla[nx]
    
    #�e�m�[�h�̐ڑ������N��ݒ�
    for lx in range(nlink):
        if lij[lx] == -1: #�ʍs�s��
            continue
        elif lij[lx] == 0: #�����������N
            lf = lfr[lx]
            jl = jla[lf]
            jlx[jl] = lx + 1
            jla[lf] = jla[lf] + 1
            lt = lto[lx]
            jl = jla[lt]
            jlx[jl] = -(lx + 1)
            jla[lt] = jla[lt] + 1
        elif lij[lx] == 1: #From��To
            lf = lfr[lx]
            jl = jla[lf]
            jlx[jl] = lx + 1
            jla[lf] = jla[lf] + 1
        elif lij[lx] == 2: #To��From
            lt = lto[lx]
            jl = jla[lt]
            jlx[jl] = -(lx + 1)
            jla[lt] = jla[lt] + 1
            
    #�e�m�[�h�̐ڑ������N��ݒ�ŕύX���ꂽ�e�m�[�h�̐ڑ������N�������ɖ߂�
    for lx in range(nlink):
        if lij[lx] == -1: #�ʍs�s��
            continue
        elif lij[lx] == 0: #�����������N
            lf = lfr[lx]
            jla[lf] = jla[lf] - 1
            lt = lto[lx]
            jla[lt] = jla[lt] - 1
        elif lij[lx] == 1: #From��To
            lf = lfr[lx]
            jla[lf] = jla[lf] - 1
        elif lij[lx] == 2: #To��From
            lt = lto[lx]
            jla[lt] = jla[lt] - 1
    return


'''
�_�C�N�X�g���@�ɂ��S���H���ʍŒZ�o�H�T��
  ndin:�T���n�_�m�[�h
  nnode:�m�[�h��
  minv:�ŒZ�o�H�R�X�g
  lfr:�n�_�m�[�hSEQ
  lto:�I�_�m�[�hSEQ
  lvp:�n�_�m�[�hSEQ
  lvm:�I�_�m�[�hSEQ
  jla:�����N�ڑ����i�}���j
  jlx:�����N�ڑ����i�����NSEQ�j
  nxt:�ŒZ�o�H�ڑ��m�[�h
  lno:�ŒZ�o�H�ڑ������N�ԍ�
  lktype:�����N���
'''
def dijkstra_rail_line(ndin, nnode, minv, lfr, lto, lvp, lvm, jla, jlx, nxt, lno, lktype):
    #������
    mx = nnode + 1
    lbl = [mx] * nnode
    npo = [mx] * nnode
    no = ndin #�n�_
    minv[no] = 0 #�n�_�̃R�X�g
    lbl[no] = -1 #�n�_�͒T����
    nxt[no] = 0 #�n�_�͐ڑ���Ȃ�
    nmin = mx #�ŏ��R�X�g�m�[�h
    nmax = mx #�ő�R�X�g�m�[�h

    while True:
        #�����N�̌������l�����ăR�X�g�v�Z
        for jl in range(jla[no], jla[no + 1]):
            ln = jlx[jl]
            if lno[no] != 0: #lno[no]��0�̂Ƃ��Alktype[- 1]�ƂȂ邽�߁A�Ō�̗v�f�̎Q�Ƃ������
                if lktype[abs(lno[no]) - 1] == 2 and lktype[abs(ln) - 1] == 2: continue #���H���抷�����N���g��Ȃ���Ԏ�ʂ̏抷���֎~
                if lktype[abs(lno[no]) - 1] == 2 and lktype[abs(ln) - 1] == 3: continue #�w�_�~�[�m�[�h�֓��Y�w�_�~�[�����N���g��Ȃ���Ԃ��֎~
                if lktype[abs(lno[no]) - 1] == 3 and lktype[abs(ln) - 1] == 2: continue #�w�_�~�[�m�[�h�֓��Y�w�_�~�[�����N���g��Ȃ��~�Ԃ��֎~
                if lktype[abs(lno[no]) - 1] == 3 and lktype[abs(ln) - 1] == 3: continue #�����̗�Ԏ�ʂ��܂������H���抷���֎~
            if ln == 0: #�ʍs�s��
                continue
            elif ln > 0: #From��To
                nx = lto[ln - 1]
                if lbl[nx] < 0: #�o�H�m��ς݃m�[�h
                    continue
                else:
                    lv = minv[no] + lvp[ln - 1]
            elif ln < 0: #To��From
                nx = lfr[abs(ln) - 1]
                if lbl[nx] < 0: #�o�H�m��ς݃m�[�h
                    continue
                else:
                    lv = minv[no] + lvm[abs(ln) - 1]

            if lv < minv[nx]:
                if nmin == mx: #�T�����W������
                    nmax = nx
                    nmin = nx
                    npo[nx] = mx #�m�[�hnx���R�X�g���������m�[�h�͂Ȃ�
                elif nmin == nx: #�ŏ��R�X�g�m�[�h�̃R�X�g���X�V
                    pass
                else:
                    if minv[nx] == math.inf: #���Y�m�[�h�����߂ĒT�����ꂽ �R�X�g���ő�Ɖ���
                        nn = nmax
                    else:
                        nn = npo[nx]
                        if nmax == nx: #�ő�R�X�g�̃m�[�h�̃R�X�g���X�V�@�R�X�g���ő傩��1�O�ɂȂ�Ɖ���
                            nmax = npo[nx]
                        else: #nx�����o���đO����q���ς�
                            np = lbl[nx]
                            npo[np] = npo[nx]    
                        lbl[nn] = lbl[nx]

                    while True: #�T���m�[�h�̌q�����m�肳����
                        if minv[nn] > lv:
                            nn = npo[nn]
                            if nn == mx:
                                lbl[nx] = nmin
                                npo[nmin] = nx
                                nmin = nx
                                npo[nx] = mx
                                break
                        else:
                            lbl[nx] = lbl[nn]
                            lbl[nn] = nx
                            npo[nx] = nn
                            if lbl[nx] == mx:
                                nmax = nx
                            else:
                                nj = lbl[nx]
                                npo[nj] = nx
                            break

                minv[nx] = lv
                nxt[nx] = no
                lno[nx] = ln
            else:
                continue


        if nmin == mx: #�S�m�[�h�̌o�H���肵�����ߒT���I��
            break
        else: #�ŏ��R�X�g�����܂����m�[�h�𖢊m��m�[�h���X�g������o��
            no = nmin
            nmin = lbl[no]
            lbl[no] = -1
            if nmin != mx:
                npo[nmin] = mx
    return


'''
�S���H���ʒT���o�H�̏o��
  iz:�o���n
  jz:�ړI�n
  nxt:�ŒZ�o�H�ڑ��m�[�h
  lno:�ŒZ�o�H�ڑ������N�ԍ�
  ir:�ŒZ�o�H�̃����N��
  ndtb:�ŒZ�o�H�m�[�h���X�g
  lktb:�ŒZ�o�H�����N���X�g
  lktype:�����N���
  lkexp:��Ԏ��
  lkfreq:�^�s�{��
'''
def rotout_rail_line(iz, jz, nxt, lno, ndtb, lktb, lktype, lkexp, lkfreq):
    ierr = 0
    ir = 0
    hon = 999
    railtype = 1
    nx = jz
    ndtb.append(nx)
    while nx != iz: #�ړI�n����o���n�܂Œǂ�������
        ir = ir + 1
        if nxt[nx] == -1:
            ierr = 999
            break
        else:
            ln = lno[nx]
            if lktype[abs(ln) - 1] == 1:
                if lkexp[abs(ln) - 1] != 1:
                    railtype = lkexp[abs(ln) - 1]
                hon = min(hon, lkfreq[abs(ln) - 1])
            lktb.append(ln)
            nx = nxt[nx]
            ndtb.append(nx)
    return ierr, ir, railtype, hon  #�G���[,�����N��,��Ԏ��,�^�s�{��


'''
�_�C�N�X�g���@�ɂ��S���̑S�w�Ԃ̍ŒZ�o�H�T��
  ndin:�T���n�_�m�[�h
  nnode:�m�[�h��
  minv:�ŒZ�o�H�R�X�g
  lfr:�n�_�m�[�hSEQ
  lto:�I�_�m�[�hSEQ
  lvp:�n�_�m�[�hSEQ
  lvm:�I�_�m�[�hSEQ
  jla:�����N�ڑ����i�}���j
  jlx:�����N�ڑ����i�����NSEQ�j
  nxt:�ŒZ�o�H�ڑ��m�[�h
  lno:�ŒZ�o�H�ڑ������N�ԍ�
  lktype:�����N���
'''
def dijkstra_rail(ndin, nnode, minv, lfr, lto, lvp, lvm, jla, jlx, nxt, lno, lktype):
    #������
    mx = nnode + 1
    lbl = [mx] * nnode
    npo = [mx] * nnode
    no = ndin #�n�_
    minv[no] = 0 #�n�_�̃R�X�g
    lbl[no] = -1 #�n�_�͒T����
    nxt[no] = 0 #�n�_�͐ڑ���Ȃ�
    nmin = mx #�ŏ��R�X�g�m�[�h
    nmax = mx #�ő�R�X�g�m�[�h

    while True:
        #�����N�̌������l�����ăR�X�g�v�Z
        for jl in range(jla[no], jla[no + 1]):
            ln = jlx[jl]
            if lno[no] != 0: #lno[no]��0�̂Ƃ��Alktype[- 1]�ƂȂ邽�߁A�Ō�̗v�f�̎Q�Ƃ������
                if lktype[abs(lno[no]) - 1] == 1 and lktype[abs(ln) - 1] == 1: continue #�܂�Ԃ���Ԃ��֎~
                if lktype[abs(lno[no]) - 1] == 4 and lktype[abs(ln) - 1] == 4: continue #�抷�����N�̘A�����֎~
            if ln == 0: #�ʍs�s��
                continue
            elif ln > 0: #From��To
                nx = lto[ln - 1]
                if lbl[nx] < 0: #�o�H�m��ς݃m�[�h
                    continue
                else:
                    lv = minv[no] + lvp[ln - 1]
            elif ln < 0: #To��From
                nx = lfr[abs(ln) - 1]
                if lbl[nx] < 0: #�o�H�m��ς݃m�[�h
                    continue
                else:
                    lv = minv[no] + lvm[abs(ln) - 1]

            if lv < minv[nx]:
                if nmin == mx: #�T�����W������
                    nmax = nx
                    nmin = nx
                    npo[nx] = mx #�m�[�hnx���R�X�g���������m�[�h�͂Ȃ�
                elif nmin == nx: #�ŏ��R�X�g�m�[�h�̃R�X�g���X�V
                    pass
                else:
                    if minv[nx] == math.inf: #���Y�m�[�h�����߂ĒT�����ꂽ �R�X�g���ő�Ɖ���
                        nn = nmax
                    else:
                        nn = npo[nx]
                        if nmax == nx: #�ő�R�X�g�̃m�[�h�̃R�X�g���X�V�@�R�X�g���ő傩��1�O�ɂȂ�Ɖ���
                            nmax = npo[nx]
                        else: #nx�����o���đO����q���ς�
                            np = lbl[nx]
                            npo[np] = npo[nx]    
                        lbl[nn] = lbl[nx]

                    while True: #�T���m�[�h�̌q�����m�肳����
                        if minv[nn] > lv:
                            nn = npo[nn]
                            if nn == mx:
                                lbl[nx] = nmin
                                npo[nmin] = nx
                                nmin = nx
                                npo[nx] = mx
                                break
                        else:
                            lbl[nx] = lbl[nn]
                            lbl[nn] = nx
                            npo[nx] = nn
                            if lbl[nx] == mx:
                                nmax = nx
                            else:
                                nj = lbl[nx]
                                npo[nj] = nx
                            break

                minv[nx] = lv
                nxt[nx] = no
                lno[nx] = ln
            else:
                continue


        if nmin == mx: #�S�m�[�h�̌o�H���肵�����ߒT���I��
            break
        else: #�ŏ��R�X�g�����܂����m�[�h�𖢊m��m�[�h���X�g������o��
            no = nmin
            nmin = lbl[no]
            lbl[no] = -1
            if nmin != mx:
                npo[nmin] = mx
    return


'''
�S�w�ԒT���o�H�̏o��
  iz:�o���n
  jz:�ړI�n
  nxt:�ŒZ�o�H�ڑ��m�[�h
  lno:�ŒZ�o�H�ڑ������N�ԍ�
  ir:�ŒZ�o�H�̃����N��
  ndtb:�ŒZ�o�H�m�[�h���X�g
  lktb:�ŒZ�o�H�����N���X�g
  lst_station:�w�R�[�h
  len_agency:���Ǝ҃R�[�h�̕�����
  df_rail_nw:�S��NW
  df_rail_fare_dist:�^���e�[�u��(����)
  df_rail_fare_sec:�^���e�[�u��(������)
'''
def rotout_rail(iz, jz, nxt, lno, ndtb, lktb, lst_station, len_agency, df_rail_nw, df_rail_fare_dist, df_rail_fare_sec):
    ierr = 0
    ir = 0
    tim_rail = 0.0
    tim_wait = 0.0
    fare_rail = 0.0
    dist_ope = 0.0 #�c�ƃL��
    dist_fare = 0.0 #�^���v�Z�L��
    fareflg = 0 #�����t���O
    
    nx = jz
    ista = ''
    jsta = lst_station[jz]
    ndtb.append(nx)
    while nx != iz: #�ړI�n����o���n�܂Œǂ�������
        ir = ir + 1
        if nxt[nx] == -1:
            ierr = 999
            break
        else:
            ln = lno[nx]
            lktb.append(ln)

            
            #�������Ԃ�ςݏグ
            if ln > 0:
                tim_rail += df_rail_nw.iloc[ln - 1, 7]
            else:
                tim_rail += df_rail_nw.iloc[abs(ln) - 1, 8]
            
            if df_rail_nw.iloc[abs(ln) - 1, 3] == 4: #�抷�����N
                if ir == 1: #�Ōオ�抷���֎~
                    tim_rail = 9999.0
                    tim_wait = 0.0
                    fare_rail = 9999.0
                    return ierr, ir, tim_rail, tim_wait, fare_rail
                if lst_station[nx][0:len_agency] == lst_station[nxt[nx]][0:len_agency]: #���ꎖ�Ǝ҂̏抷
                    pass
                else:
                    #�^���v�Z
                    fare_rail += calc_fare_rail(ista, jsta, fareflg, dist_ope, dist_fare, df_rail_fare_dist, df_rail_fare_sec, len_agency)
                    
                    #������
                    dist_ope = 0.0
                    dist_fare = 0.0
                    fareflg = 0
                    jsta = lst_station[nxt[nx]]
            else: #���������N
                if ln > 0:
                    #��ԑ҂����Ԃ̐ςݏグ
                    if df_rail_nw.iloc[ln - 1, 9] > 0: #�^�s�{�����Ȃ��ꍇ�͑҂����Ԃ��v�Z���Ȃ�
                        tim_wait += 60.0 / df_rail_nw.iloc[ln - 1, 9] / 2.0
                else:
                    #��ԑ҂����Ԃ̐ςݏグ
                    if df_rail_nw.iloc[abs(ln) - 1, 10] > 0: #�^�s�{�����Ȃ��ꍇ�͑҂����Ԃ��v�Z���Ȃ�
                        tim_wait += 60.0 / df_rail_nw.iloc[abs(ln) - 1, 10] / 2.0
                    
                #�^���v�Z�̂��߂̋����ςݏグ
                dist_ope += df_rail_nw.iloc[abs(ln) - 1, 5]
                if df_rail_nw.iloc[abs(ln) - 1, 6] == 0.0:
                    dist_fare += df_rail_nw.iloc[abs(ln) - 1, 5]
                else:
                    dist_fare += df_rail_nw.iloc[abs(ln) - 1, 6]
                
                #����or�n������@0:�����l,1:�����̂�,2:�n���̂�,3:����+�n��
                if fareflg == 0:
                    if df_rail_nw.iloc[abs(ln) - 1, 6] == 0.0:
                        fareflg = 1
                    else:
                        fareflg = 2
                elif fareflg == 1:
                    if df_rail_nw.iloc[abs(ln) - 1, 6] == 0.0:
                        pass
                    else:
                        fareflg = 3
                elif fareflg == 2:
                    if df_rail_nw.iloc[abs(ln) - 1, 6] == 0.0:
                        fareflg = 3
                    else:
                        pass
                else:
                    pass
                
                ista = lst_station[nxt[nx]]
            nx = nxt[nx]
            ndtb.append(nx)
            
    if df_rail_nw.iloc[abs(ln) - 1, 3] == 4: #�ŏ����抷���֎~
        tim_rail = 9999.0
        tim_wait = 0.0
        fare_rail = 9999.0
    else: #�ŏI��ԋ�Ԃ̉^���v�Z
        fare_rail += calc_fare_rail(ista, jsta, fareflg, dist_ope, dist_fare, df_rail_fare_dist, df_rail_fare_sec, len_agency)
    return ierr, ir, tim_rail, tim_wait, fare_rail  #�G���[,�����N��,��������,��ԑ҂�����,�^��


'''
�S���^���v�Z
  ista:��ԉw�R�[�h
  jsta:�~�ԉw�R�[�h
  fareflg:���p�H���t���O
  dist_ope:�c�ƃL��
  dist_fare:�^���v�Z�L��
  fare_rail:�^��
  df_rail_fare_dist:�^���e�[�u��(����)
  df_rail_fare_sec:�^���e�[�u��(������)
  len_agency:���Ǝ҃R�[�h�̕�����
'''
def calc_fare_rail(ista, jsta, fareflg, dist_ope, dist_fare, df_rail_fare_dist, df_rail_fare_sec, len_agency):
    fare = 0.0
    if (df_rail_fare_sec.iloc[:, 5] == ista + jsta).any(): #��ԉ^���e�[�u�����m�F
        fare = df_rail_fare_sec[df_rail_fare_sec.iloc[:, 5] == ista + jsta].iloc[0, 2]
    elif (df_rail_fare_sec.iloc[:, 5] == jsta + ista).any(): #��ԉ^���e�[�u�����m�F
        fare = df_rail_fare_sec[df_rail_fare_sec.iloc[:, 5] == jsta + ista].iloc[0, 2]
    else: #�΋����^���e�[�u�����m�F
        if (dist_ope == 0) or (len(df_rail_fare_dist) == 0): #�S��NW�ɋ����f�[�^���Ȃ��������͋����уe�[�u�����Ȃ��ꍇ�͉^�����v�Z���Ȃ�
            return fare
        else:
            if ista[0:len_agency] == '1'.zfill(len_agency): #JR
                if fareflg == 1: #�����̂�
                    fare = df_rail_fare_dist[(df_rail_fare_dist.iloc[:, 0] == ista[0:len_agency]) & \
                                             (df_rail_fare_dist.iloc[:, 1] == 1) & \
                                             (df_rail_fare_dist.iloc[:, 2] == math.ceil(dist_ope))].iloc[0, 3]
                elif fareflg == 2: #�n���̂�
                    fare = df_rail_fare_dist[(df_rail_fare_dist.iloc[:, 0] == ista[0:len_agency]) & \
                                             (df_rail_fare_dist.iloc[:, 1] == 2) & \
                                             (df_rail_fare_dist.iloc[:, 2] == math.ceil(dist_ope))].iloc[0, 3]
                else: #����+�n��
                    if dist_ope <= 10.0:
                        fare = df_rail_fare_dist[(df_rail_fare_dist.iloc[:, 0] == ista[0:len_agency]) & \
                                                 (df_rail_fare_dist.iloc[:, 1] == 2) & \
                                                 (df_rail_fare_dist.iloc[:, 2] == math.ceil(dist_ope))].iloc[0, 3]
                    else:
                        fare = df_rail_fare_dist[(df_rail_fare_dist.iloc[:, 0] == ista[0:len_agency]) & \
                                                 (df_rail_fare_dist.iloc[:, 1] == 1) & \
                                                 (df_rail_fare_dist.iloc[:, 2] == math.ceil(dist_fare))].iloc[0, 3]
            else:
                fare = df_rail_fare_dist[(df_rail_fare_dist.iloc[:, 0] == ista[0:len_agency]) & \
                                         (df_rail_fare_dist.iloc[:, 2] == math.ceil(dist_ope))].iloc[0, 3]
    return fare


'''
�_�C�N�X�g���@�ɂ��S�o�X��Ԃ̍ŒZ�o�H�T��
  ndin:�T���n�_�m�[�h
  nnode:�m�[�h��
  minv:�ŒZ�o�H�R�X�g
  lfr:�n�_�m�[�hSEQ
  lto:�I�_�m�[�hSEQ
  lvp:�n�_�m�[�hSEQ
  lvm:�I�_�m�[�hSEQ
  jla:�����N�ڑ����i�}���j
  jlx:�����N�ڑ����i�����NSEQ�j
  nxt:�ŒZ�o�H�ڑ��m�[�h
  lno:�ŒZ�o�H�ڑ������N�ԍ�
  lktype:�����N���
'''
def dijkstra_bus(ndin, nnode, minv, lfr, lto, lvp, lvm, jla, jlx, nxt, lno, lktype):
    #������
    mx = nnode + 1
    lbl = [mx] * nnode
    npo = [mx] * nnode
    no = ndin #�n�_
    minv[no] = 0 #�n�_�̃R�X�g
    lbl[no] = -1 #�n�_�͒T����
    nxt[no] = 0 #�n�_�͐ڑ���Ȃ�
    nmin = mx #�ŏ��R�X�g�m�[�h
    nmax = mx #�ő�R�X�g�m�[�h

    while True:
        #�����N�̌������l�����ăR�X�g�v�Z
        for jl in range(jla[no], jla[no + 1]):
            ln = jlx[jl]
            if lno[no] != 0: #lno[no]��0�̂Ƃ��Alktype[- 1]�ƂȂ邽�߁A�Ō�̗v�f�̎Q�Ƃ������
                if lktype[abs(lno[no]) - 1] == 0 and lktype[abs(ln) - 1] == 0: continue #�抷�����N�̘A�����֎~
            if ln == 0: #�ʍs�s��
                continue
            elif ln > 0: #From��To
                nx = lto[ln - 1]
                if lbl[nx] < 0: #�o�H�m��ς݃m�[�h
                    continue
                else:
                    lv = minv[no] + lvp[ln - 1]
            elif ln < 0: #To��From
                nx = lfr[abs(ln) - 1]
                if lbl[nx] < 0: #�o�H�m��ς݃m�[�h
                    continue
                else:
                    lv = minv[no] + lvm[abs(ln) - 1]

            if lv < minv[nx]:
                if nmin == mx: #�T�����W������
                    nmax = nx
                    nmin = nx
                    npo[nx] = mx #�m�[�hnx���R�X�g���������m�[�h�͂Ȃ�
                elif nmin == nx: #�ŏ��R�X�g�m�[�h�̃R�X�g���X�V
                    pass
                else:
                    if minv[nx] == math.inf: #���Y�m�[�h�����߂ĒT�����ꂽ �R�X�g���ő�Ɖ���
                        nn = nmax
                    else:
                        nn = npo[nx]
                        if nmax == nx: #�ő�R�X�g�̃m�[�h�̃R�X�g���X�V�@�R�X�g���ő傩��1�O�ɂȂ�Ɖ���
                            nmax = npo[nx]
                        else: #nx�����o���đO����q���ς�
                            np = lbl[nx]
                            npo[np] = npo[nx]    
                        lbl[nn] = lbl[nx]

                    while True: #�T���m�[�h�̌q�����m�肳����
                        if minv[nn] > lv:
                            nn = npo[nn]
                            if nn == mx:
                                lbl[nx] = nmin
                                npo[nmin] = nx
                                nmin = nx
                                npo[nx] = mx
                                break
                        else:
                            lbl[nx] = lbl[nn]
                            lbl[nn] = nx
                            npo[nx] = nn
                            if lbl[nx] == mx:
                                nmax = nx
                            else:
                                nj = lbl[nx]
                                npo[nj] = nx
                            break

                minv[nx] = lv
                nxt[nx] = no
                lno[nx] = ln
            else:
                continue


        if nmin == mx: #�S�m�[�h�̌o�H���肵�����ߒT���I��
            break
        else: #�ŏ��R�X�g�����܂����m�[�h�𖢊m��m�[�h���X�g������o��
            no = nmin
            nmin = lbl[no]
            lbl[no] = -1
            if nmin != mx:
                npo[nmin] = mx
    return


'''
�S�o�X��ԒT���o�H�̏o��
  iz:�o���n
  jz:�ړI�n
  nxt:�ŒZ�o�H�ڑ��m�[�h
  lno:�ŒZ�o�H�ڑ������N�ԍ�
  ir:�ŒZ�o�H�̃����N��
  ndtb:�ŒZ�o�H�m�[�h���X�g
  lktb:�ŒZ�o�H�����N���X�g
  dct_travel_time:���v����
  dct_fare:�^��
  dct_frequency:�^�s�{��
  dct_type:�����N�^�C�v
  tim_limit:�҂����Ԃ̏��
  tim_ope:�^�s����
'''
def rotout_bus(iz, jz, nxt, lno, ndtb, lktb, dct_travel_time, dct_fare, dct_frequency, dct_type, tim_limit, tim_ope):
    ierr = 0
    ir = 0
    tim = 0.0
    tim_wait = 0.0
    tim_wait_hatu = 0.0
    fare = 0.0
    
    nx = jz
    ndtb.append(nx)
    while nx != iz: #�ړI�n����o���n�܂Œǂ�������
        ir = ir + 1
        if nxt[nx] == -1:
            ierr = 999
            tim = 9999.0
            tim_wait = 0.0
            tim_wait_hatu = 0.0
            fare = 9999.0
            return ierr, ir, tim, tim_wait, tim_wait_hatu, fare
        else:
            ln = lno[nx]
            lktb.append(ln)

            
            #���ԁA�^����ςݏグ
            if ln > 0:
                tim += dct_travel_time[ln - 1]
                fare += dct_fare[ln - 1]
            else:
                tim += dct_travel_time[abs(ln) - 1]
                fare += dct_fare[abs(ln) - 1]
            
            if dct_type[abs(ln) - 1] == 0: #�抷�����N
                if ir == 1: #�Ōオ�抷���֎~
                    tim = 9999.0
                    tim_wait = 0.0
                    tim_wait_hatu = 0.0
                    fare = 9999.0
                    return ierr, ir, tim, tim_wait, tim_wait_hatu, fare
            else: #���������N
                if ln > 0:
                    #��ԑ҂����Ԃ̐ςݏグ
                    if dct_frequency[ln - 1] != 0:
                        tim_wait += min(60.0 * tim_ope / dct_frequency[ln - 1] / 2.0, tim_limit)
                else:
                    #��ԑ҂����Ԃ̐ςݏグ
                    if dct_frequency[abs(ln) - 1] != 0:
                        tim_wait += min(60.0 * tim_ope / dct_frequency[abs(ln) - 1] / 2.0, tim_limit)
            nx = nxt[nx]
            ndtb.append(nx)
            
    if dct_type[abs(ln) - 1] == 0: #�ŏ����抷���֎~
        tim = 9999.0
        tim_wait = 0.0
        tim_wait_hatu = 0.0
        fare = 9999.0
        return ierr, ir, tim, tim_wait, tim_wait_hatu, fare

    if ln > 0:
        if dct_frequency[ln - 1] != 0:
                tim_wait_hatu = min(60.0 * tim_ope / dct_frequency[ln - 1] / 2.0, tim_limit)
    else:
        if dct_frequency[abs(ln) - 1] != 0:
                tim_wait_hatu = min(60.0 * tim_ope / dct_frequency[abs(ln) - 1] / 2.0, tim_limit)
    
    return ierr, ir, tim, tim_wait, tim_wait_hatu, fare #�G���[,�����N��,��������,��ԑ҂�����,�����҂�����,�^��
