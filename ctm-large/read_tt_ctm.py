import os
from network.link import Edge
from network.node import Vertex
from network.graph import Graph
from network.utilities import Stream
import arrow as ar
import sys
import pandas as pd




def read_paths(any_pf_path):
    df = pd.read_csv(any_pf_path, header=None)
    paths = list(df[1].unique())
    paths.sort()
    # num_int = max(df[0]+1)
    num_int = 25
    return num_int, paths


def calculate_delay_operator(net_path, fit_path, any_pf_path, rec_dir, path_tt_dir):
    nt = Graph('NG Network')
    nt.assign_step = 1
    nt.veh_unit = 100
    os.system('rm -rf {}/*'.format(path_tt_dir))
    st = Stream()
    st.set_net_path(net_path)
    st.read_network_data(nt)
    st.set_fit_path(fit_path)
    if fit_path != '':
        st.fit_rsv_data(nt)
    nt.init_cost()
    asg_ints, paths = read_paths(any_pf_path)
    files = os.listdir(rec_dir)
    files.sort()

    lasttwo = files[-3:]
    for file in lasttwo:
        nt.update_cost(rec_dir+file)
        list_path_tt = []
        for t in range(asg_ints):
            for p in paths:
                path_tt = collect_path_cost(nt, p, t)
                entry = '{},{},{}'.format(t,p,path_tt)
                list_path_tt.append(entry)
        str_towrite = '\n'.join(list_path_tt)
        filename = path_tt_dir + '{}.txt'.format(ar.now().format('YYYYMMDD-HHmmss-S'))
        if os.name == 'nt':
            os.system('type nul> {}'.format(filename))
        else:
            os.system('touch {}'.format(filename))
        with open(filename, 'w') as f:
            f.write(str_towrite)


def collect_path_cost(nt, path, start_time):
    nodes = path.split()
    edgeofnodes = list(zip(nodes[:-1], nodes[1:]))
    anchor_time = start_time
    path_tt = 0
    for i in edgeofnodes:
        tt_i = nt.edgefullset[i].getcost(anchor_time)
        anchor_time = start_time+path_tt
        path_tt += tt_i
    return path_tt

# if __name__ == '__main__':
    # get_sample_files('./path_flows/','./records/', '../tests/nyg_mfd_fit.json')
        # net_dir = '../tests/nyg_mac_network_180126.csv'
        # fit_dir = '../tests/nyg_mfd_fit.json'
        # rec_data_dir = '../data/records/'
        # pf_data_dir = '../data/pf/'

# print(read_paths('./path_flows/20180501-022015-5.txt'))


if __name__ == '__main__':
    calculate_delay_operator('./nyg_network.csv','','./path_collection.txt','./records/','./path_tt/')
