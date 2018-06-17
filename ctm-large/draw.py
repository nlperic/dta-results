import matplotlib.pyplot as plt
import pandas as pd
import os
import arrow as ar
import time
plt.style.use('ggplot')


def read_paths(any_pf_path):
    df = pd.read_csv(any_pf_path, header=None)
    paths = list(df[1].unique())
    # num_int = max(df[0]+1)
    num_int = 110
    return num_int, paths


def read_data_paths(data_dir):
    files = os.listdir(data_dir)
    files.sort()
    return files


def read_df(data_dir,file):
    df = pd.read_csv(data_dir+file, header=None)
    return df


def get_od_spec_paths(paths, origin, destination):
    odp = [p for p in paths if p.startswith(origin) and p.endswith(destination)]
    return odp


def draw_path_tt(df_tt_path, df_pf_path, od_paths, num_t):
    pf_map = {}
    tt_map = {}
    for path in od_paths:
        tts, pfs = [], []
        for t in range(num_t):
            ts_tts = df_tt_path[(df_tt_path[0]==t)&(df_tt_path[1] == path)][2].values
            tts.append(ts_tts[0])
            ts_pfs = df_pf_path[(df_pf_path[0] == t) & (df_pf_path[1] == path)][2].values
            if not ts_pfs:
                ts_pfs = [0.0]
            pfs.append(ts_pfs[0])
        pf_map[path] = pfs
        tt_map[path] = tts
    plt.figure()
    for path in od_paths:
        plt.plot(list(range(num_t)), tt_map[path], label=path)
    plt.xlabel('assignment interval')
    plt.ylabel('path travel time (simulation step)')
    plt.legend(bbox_to_anchor=(0.40, 1.00), loc=2, borderaxespad=0.)
    # plt.ylim(240, 290)
    timestep = ar.now().format('YYYYMMDD-HHmmss-S')
    fig_name = './draw/' + timestep + '_tt.pdf'
    plt.savefig(fig_name, dpi=400, bbox_inches='tight')
    plt.clf()
    for path in od_paths:
        plt.plot(list(range(num_t)), pf_map[path], label=path)
    plt.xlabel('assignment interval')
    plt.ylabel('path flow (vph)')
    plt.legend(bbox_to_anchor=(1.0, 1.00), loc=2, borderaxespad=0.)
    timestep = ar.now().format('YYYYMMDD-HHmmss-S')
    fig_name = './draw/' + timestep + '_pf.pdf'
    time.sleep(0.1)
    plt.savefig(fig_name, dpi=400, bbox_inches='tight')



pf_dir = './pf/'
tt_dir = './path_tt/'
pf_files = read_data_paths(pf_dir)
pf_files.sort()
tt_files = read_data_paths(tt_dir)
tt_files.sort()
num, pt = read_paths('./path_collection.txt')
origins = ['N001', 'N004']
destinations = ['N002', 'N003']


os.system('rm -rf ./draw/*')
for o in origins:
    for d in destinations:
        od_paths = get_od_spec_paths(pt, o, d)
        df_pf = read_df(pf_dir, pf_files[-2])
        df_tt = read_df(tt_dir, tt_files[-2])
        draw_path_tt(df_tt, df_pf, od_paths, num)

# o = origins[0]
# d = destinations[0]
# od_paths = get_od_spec_paths(pt,o,d)
#
# df_pf = read_df(pf_dir, pf_files[0])
# df_tt = read_df(tt_dir, tt_files[0])
# draw_path_tt(df_tt,df_pf,od_paths, num)
