__version__ = "0.0.1"
__copyright__ = "Copyright 2025"
__license__ = "GPL-3.0"
__developer__ = "Jianfeng Sun"
__maintainer__ = "Jianfeng Sun"
__email__ = "jianfeng.sunmt@gmail.com"


import time
import numpy as np
from tresor.library.SingleLocus import SingleLocus as simuip
from tresor.pcr.Amplify import Amplify as pcr
from tresor.sequencing.Calling import Calling as seq
from tresor.pcr.Subsampling import Subsampling
from tresor.util.sequence.fastq.Write import write as wfastq
from tresor.util.Console import Console


class SingleLocus:

    def __init__(
            self,
            len_params,
            seq_num,
            is_sv_umi_lib,
            is_sv_seq_lib,
            is_sv_primer_lib,
            is_sv_adapter_lib,
            is_sv_spacer_lib,
            working_dir,
            condis,
            sim_thres,
            permutation,

            seq_error,
            err_route,
            pcr_error,
            pcr_nums,
            err_num_met,
            use_seed,
            seed,

            ampl_rate,
            sv_fastq_fp,

            seq_sub_spl_number=None,
            seq_sub_spl_rate=1/3,

            verbose=False,
            **kwargs,
    ):
        self.len_params = len_params
        self.seq_num = seq_num
        self.is_sv_umi_lib = is_sv_umi_lib
        self.is_sv_seq_lib = is_sv_seq_lib
        self.is_sv_primer_lib = is_sv_primer_lib
        self.is_sv_adapter_lib = is_sv_adapter_lib
        self.is_sv_spacer_lib = is_sv_spacer_lib

        self.working_dir = working_dir
        self.condis = condis
        self.sim_thres = sim_thres
        self.permutation = permutation

        self.err_route = err_route
        self.ampl_rate = ampl_rate
        self.pcr_error = pcr_error
        self.seq_error = seq_error
        self.err_num_met = err_num_met
        self.use_seed = use_seed
        self.seed = seed

        self.pcr_nums = pcr_nums

        self.seq_sub_spl_number = seq_sub_spl_number
        self.seq_sub_spl_rate = seq_sub_spl_rate
        self.sv_fastq_fp = sv_fastq_fp

        self.pcr = pcr
        self.seq = seq
        self.wfastq = wfastq
        self.subsampling = Subsampling()

        self.kwargs = kwargs

        self.console = Console()
        self.console.verbose = verbose
        self.verbose = verbose

        ### +++++++++++++++ block: generate sequencing library +++++++++++++++
        self.console.print('===>Sequencing library generation starts')
        self.sequencing_library = simuip(
            len_params=self.len_params,
            seq_num=self.seq_num,
            is_seed=self.use_seed,
            working_dir=self.working_dir,
            condis=self.condis,
            sim_thres=self.sim_thres,
            permutation=self.permutation,
            is_sv_umi_lib=self.is_sv_umi_lib,
            is_sv_seq_lib=self.is_sv_seq_lib,
            is_sv_primer_lib=self.is_sv_primer_lib,
            is_sv_adapter_lib=self.is_sv_adapter_lib,
            is_sv_spacer_lib=self.is_sv_spacer_lib,
            verbose=self.verbose,
            mode=self.kwargs['mode'],
            material_params=self.kwargs['material_params'] if 'material_params' in self.kwargs.keys() else None,
            seq_params=self.kwargs['seq_params'] if 'seq_params' in self.kwargs.keys() else None,
        ).pooling()
        self.console.print('===>Sequencing library has been generated')

    def generate(self, ):
        """

        [['1' '1' '0']
         ['1' '1' '1']
         ['1' '1' '2']
         ...
         ['1' '1' '48']
         ['1' '1' '49']]
        Returns
        -------

        """
        ### +++++++++++++++ block: PCR amplification: Preparation +++++++++++++++
        self.console.print('===>PCR amplification starts...')
        self.console.print('======>Assign parameters...')
        # print(np.array(self.sequencing_library))
        time_arr = []
        satime = time.time()
        for i, pcr_num_i in enumerate(self.pcr_nums):
            self.console.print('======>{}. PCR cycle number: {}'.format(i, pcr_num_i))
            pcr_ampl_params = {
                'read_lib_fpn': self.working_dir + 'sequencing_library.txt',

                'data': np.array(self.sequencing_library[0]),
                'ampl_rate': self.ampl_rate,
                'pcr_error': self.pcr_error,
                'pcr_num': pcr_num_i,

                'err_route': self.err_route,
                'err_num_met': self.err_num_met,
                'use_seed': self.use_seed,
                'seed': self.seed,
                'recorder_nucleotide_num': [],
                'recorder_pcr_err_num': [],
                'recorder_pcr_read_num': [],

                'seq_sub_spl_number': self.seq_sub_spl_number,
                'seq_sub_spl_rate': self.seq_sub_spl_rate,

                'pcr_deletion': False,
                'pcr_insertion': False, # False True
                'pcr_del_rate': 2.4*10e-6,
                'pcr_ins_rate': 7.1*10e-7,

                'verbose': self.verbose,
            }
            # pcr_ampl_params['data']
            # [['GGGAAATTTAAACCCTTTAAAGGGAAAAAAGGGCCC' '0' 'init']
            #  ['GGGTTTAAACCCCCCCCCGGGAAATTTTTTGGGTTT' '1' 'init']
            #  ['AAATTTGGGCCCGGGAAAGGGCCCAAAAAAGGGAAA' '2' 'init']
            #  ...
            #  ['CCCAAAAAAGGGCCCAAAGGGCCCTTTGGGGGGCCC' '48' 'init']
            #  ['TTTTTTAAATTTAAAAAAGGGAAAGGGGGGGGGCCC' '49' 'init']]
            # print(pcr_ampl_params['data'][:, 1:3])
            # print(pcr_ampl_params)
            if pcr_ampl_params['err_route'] == 'bftree':
                pcr_ampl_params['data'] = pcr_ampl_params['data'][:, 1:3]
            if pcr_ampl_params['err_route'] == 'sptree':
                pcr_ampl_params['data'] = pcr_ampl_params['data'][:, 1:3]
            if pcr_ampl_params['err_route'] == 'mutation_table_minimum' or pcr_ampl_params['err_route'] == 'mutation_table_complete':
                # print(pcr_ampl_params['data'][:, 0])
                def calc_len(a):
                    return len(a)
                vfunc = np.vectorize(calc_len)
                # [[36] vfunc(pcr_ampl_params['data'][:, 0])[:, np.newaxis]
                #  [36]
                #  [36]
                #  ...
                #  [36]
                #  [36]]
                pcr_ampl_params['data'] = np.hstack((
                    vfunc(pcr_ampl_params['data'][:, 0])[:, np.newaxis],
                    pcr_ampl_params['data'][:, 1:3],
                ))
                # print(pcr_ampl_params['data'])
                # pcr_ampl_params['data']
                # [['36' '0' 'init']
                #  ['36' '1' 'init']
                #  ['36' '2' 'init']
                #  ...
                #  ['36' '48' 'init']
                #  ['36' '49' 'init']]
                col_0 = np.array([[1] for _ in range(pcr_ampl_params['data'].shape[0])])
                mut_info_table = np.hstack((col_0, col_0))
                col_2 = pcr_ampl_params['data'][:, 1].astype(str)[:, np.newaxis]
                mut_info_table = np.hstack((mut_info_table, col_2))
                pcr_ampl_params['mut_info'] = mut_info_table
                # print(mut_info_table)
                # pcr_ampl_params['mut_info'] = np.empty(shape=[0, 3])
                # print(pcr_ampl_params['mut_info'])

            ### +++++++++++++++ block: PCR amplification: simulation +++++++++++++++
            pcr_stime = time.time()
            pcr = self.pcr(pcr_params=pcr_ampl_params).np()
            # print(pcr.keys())
            self.console.print('======>PCR amplification completes in {}s'.format(time.time() - pcr_stime))
            # print(pcr['data'])
            # print(pcr['data'].shape)

            ### +++++++++++++++ block: Subsampling: sequencing depth or rate +++++++++++++++
            # print(pcr['data'])
            # print(pcr['data'].shape)
            if pcr_ampl_params['err_route'] == 'bftree':
                pcr['data'] = self.subsampling.bftree(pcr_dict=pcr)
            # print(pcr['data'])
            # print(pcr['data'].shape)

            if pcr_ampl_params['err_route'] == 'sptree':
                pcr['data'] = self.subsampling.sptree(pcr_dict=pcr)

            if pcr_ampl_params['err_route'] == 'mutation_table_minimum':
                pcr['data'] = self.subsampling.mutation_table_minimum(pcr_dict=pcr)

            if pcr_ampl_params['err_route'] == 'mutation_table_complete':
                pcr['data'] = self.subsampling.mutation_table_complete(pcr_dict=pcr)

            ### +++++++++++++++ block: Sequencing: parameters +++++++++++++++
            self.console.print('======>Sequencing starts')
            seq_params = {
                'data': pcr['data'],

                'seq_error': self.seq_error,
                'err_num_met': self.err_num_met,
                'use_seed': self.use_seed,
                'seed': self.seed,
                'verbose': self.verbose,

                'seq_sub_spl_number': self.seq_sub_spl_number,
                'seq_sub_spl_rate': self.seq_sub_spl_rate,

                'seq_deletion': False,
                'seq_insertion': False,  # False True
                'seq_del_rate': 2.4 * 10e-6,
                'seq_ins_rate': 7.1 * 10e-7,
            }
            seq = self.seq(seq_params=seq_params).np()
            self.console.print('=========>Sequencing has completed')
            print('======>simulation completes in {}s'.format(time.time() - satime))
            time_arr.append(time.time() - satime)

            self.console.print('=========>Reads write to files in FastQ format')
            self.wfastq().togz(
                list_2d=seq['data'],
                sv_fp=self.sv_fastq_fp,
                fn='pcr_num_' + str(i),
                # fn='pcr_num_' + "{:.2f}".format(pcr_num_i),
                symbol='-',
            )
            del seq
        eatime = time.time()
        self.console.print('=========>Total time: {:.3f}s'.format(eatime - satime))
        self.console.print('=========>FastQ file is saved')
        self.console.print('======>Simulation completes')
        return {
            'time_arr': time_arr
        }


if __name__ == "__main__":
    from tresor.path import to

    p = SingleLocus(
        # initial sequence generation
        len_params={
            'umi': {
                'umi_unit_pattern': 3,
                'umi_unit_len': 12,
            },
            'seq': 100,
        },
        seq_params={
            'custom': 'AAGC',
            'custom_1': 'A',
        },
        material_params={
            'fasta_cdna_fpn': to('data/Homo_sapiens.GRCh38.cdna.all.fa.gz'),  # None False
        },
        seq_num=50,
        working_dir=to('data/simu/'),

        is_sv_umi_lib=True,
        is_sv_seq_lib=True,
        is_sv_primer_lib=True,
        is_sv_adapter_lib=True,
        is_sv_spacer_lib=True,
        condis=['umi'],
        # condis=['umi', 'seq'],
        # condis=['umi', 'custom', 'seq', 'custom_1'],
        sim_thres=3,
        permutation=0,

        # PCR amplification
        ampl_rate=0.9,
        err_route='sptree', # bftree sptree err1d err2d mutation_table_minimum mutation_table_complete
        pcr_error=1e-4,
        pcr_nums=np.arange(1, 18 + 1, 1),
        err_num_met='nbinomial',
        seq_error=0.01,
        seq_sub_spl_number=30, # None 200
        seq_sub_spl_rate=0.333,
        use_seed=True,
        seed=1,

        verbose=False, # True

        mode='short_read',  # long_read short_read

        sv_fastq_fp=to('data/simu/'),
    )
    print(p.generate())