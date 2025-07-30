__version__ = "0.0.1"
__copyright__ = "Copyright 2025"
__license__ = "GPL-3.0"
__developer__ = "Jianfeng Sun"
__maintainer__ = "Jianfeng Sun"
__email__ = "jianfeng.sunmt@gmail.com"


import time
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from tresor.util.random.Sampling import Sampling as ranspl
from tresor.util.random.Number import Number as rannum
from tresor.util.file.Writer import Writer as pfwriter
from tresor.util.file.Folder import Folder as crtfolder
from tresor.util.sequence.symbol.Single import Single as dnasgl
from tresor.util.Hamming import Hamming
from tresor.read.umi.Design import Design as dumi
from tresor.read.seq.Design import Design as dseq
from tresor.read.primer.Design import Design as dprimer
from tresor.read.adapter.Design import Design as dadapter
from tresor.read.spacer.Design import Design as dspacer
from tresor.util.Console import Console
from tresor.util.sequence.Fasta import Fasta as sfasta
from tresor.util.Kit import tactic6


class Gene:

    def __init__(
            self,
            gspl,
            len_params,

            is_seed=False,

            working_dir='./simu/',
            condis=['umi'],
            sim_thres=3,
            permutation=0,
            is_sv_umi_lib=True,
            is_sv_seq_lib=True,
            is_sv_primer_lib=True,
            is_sv_adapter_lib=True,
            is_sv_spacer_lib=True,
            verbose=True,
            **kwargs,
    ):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines all its attributes.

        Parameters
        ----------
        gspl
            Generate the gene_map and gspl_arr
        len_params
            Set the length of each part of the sequence
        fasta_cdna_fpn
            Specify the fasta file containing the cdna sequences
        is_seed
            Determine whether the simulation is for seed or not
        working_dir
            Specify the working directory
        condis
            Determine the type of simulation
        sim_thres
            Control the similarity threshold of the simulated sequences
        permutation
            Determine the number of permutations
        is_sv_umi_lib
            Control whether to save the umi library
        is_sv_seq_lib
            Determine whether the sequence library is simulated or not
        is_sv_primer_lib
            Determine whether to use the primer library or not
        is_sv_adapter_lib
            Determine whether the adapter library is saved
        is_sv_spacer_lib
            Determine whether to simulate the spacer library
        verbose
            Control the output of the console
        **kwargs
            Pass a variable number of keyword arguments to a function

            Generate the gene_map, which is a dictionary of genes and their corresponding index

        Returns
        -------

            The instance of the class

        Doc Author
        ----------
            Trelent
        """
        self.pfwriter = pfwriter()
        self.ranspl = ranspl()
        self.rannum = rannum()
        self.dnasgl = dnasgl()
        self.crtfolder = crtfolder()
        self.gspl = gspl
        self.dumi = dumi
        self.dseq = dseq
        self.dprimer = dprimer
        self.dadapter = dadapter
        self.dspacer = dspacer
        self.working_dir = working_dir
        self.len_params = len_params
        self.is_seed = is_seed
        self.is_sv_umi_lib = is_sv_umi_lib
        self.is_sv_seq_lib = is_sv_seq_lib
        self.is_sv_primer_lib = is_sv_primer_lib
        self.is_sv_adapter_lib = is_sv_adapter_lib
        self.is_sv_spacer_lib = is_sv_spacer_lib
        self.condis = condis
        self.sim_thres = sim_thres
        self.permutation = permutation
        self.dna_map = self.dnasgl.todict(nucleotides=self.dnasgl.get(universal=True), reverse=True)
        self.crtfolder.osmkdir(working_dir)


        self.gene_map = {k: v for k, v in enumerate(self.gspl.index)}
        # print(self.gene_map)
        csr_ = coo_matrix(self.gspl)
        self.gspl_arr = np.transpose([
            csr_.row.tolist(),
            csr_.col.tolist(),
            csr_.data.tolist(),
        ]).astype(int)
        self.gspl_arr = self.gspl_arr[self.gspl_arr[:, 0] == 0]
        # print(self.gspl_arr)

        self.kwargs = kwargs
        # print(self.kwargs)

        if not self.kwargs['material_params']:
            self.kwargs['material_params'] = {}
            self.kwargs['material_params']['fasta_cdna_fpn'] = None

        self.console = Console()
        self.console.verbose = verbose

    def pooling(self, ):
        """

        Attributes
        ----------
        condi_map
            {'umi': ['alone', '1'], 'primer': ['alone', '1'], 'spacer': ['alone', '1'], 'adapter': ['alone', '1'], 'seq': ['alone', '2']}

        Returns
        -------

        """
        self.console.print("======>Sequencing library preparation starts")
        stime = time.time()
        sequencing_library = []
        umi_pool = []
        umi_cnt = 0

        ### +++++++++++++++ block: condition map +++++++++++++++
        condi_map = {}
        for condi in self.condis:
            condi_arr = condi.split("_")
            condi_map[condi_arr[0]] = []
        for condi in self.condis:
            condi_arr = condi.split("_")
            if len(condi_arr) == 1:
                condi_map[condi_arr[0]].append('alone')
            else:
                condi_map[condi_arr[0]].append(condi_arr[1])
        self.console.print("======>Condition map: {}".format(condi_map))
        condi_keys = condi_map.keys()

        ### +++++++++++++++ block: select CDNA from a reference ome +++++++++++++++
        if 'seq' in condi_keys and self.kwargs['material_params']['fasta_cdna_fpn']:
            self.console.print("======>Read CDNAs from a reference ome")
            fastq_ref_arr = sfasta().get_from_gz(
                fasta_fpn=self.kwargs['material_params']['fasta_cdna_fpn'],
            )
            if self.kwargs['mode'] == 'short_read':
                df_fastq_ref = pd.DataFrame(fastq_ref_arr)
                # print(df_fastq_ref)
                df_fastq_ref = df_fastq_ref.rename(columns={0: 'name', 1: 'seq'})
                df_fastq_ref['len'] = df_fastq_ref['seq'].apply(lambda x: len(x))
                df_fastq_ref = df_fastq_ref.loc[df_fastq_ref['len'] > 2 * self.len_params['seq']]
                # print(df_fastq_ref)
                seq_cdna_map = tactic6(
                    arr_2d=df_fastq_ref[['name', 'seq']].values.tolist()
                )
                cdna_ids = [*seq_cdna_map.keys()]
            else:
                seq_cdna_map = tactic6(
                    arr_2d=fastq_ref_arr
                )
                cdna_ids = [*seq_cdna_map.keys()]
            self.console.print("======>There are {} genes in the reference genome".format(len(cdna_ids)))

        ### +++++++++++++++ block: generate each read +++++++++++++++
        for x, gs in enumerate(self.gspl_arr):
            sample = gs[0]
            gene = gs[1]
            seq_num = gs[2]

            if 'seq' in condi_keys and self.kwargs['material_params']['fasta_cdna_fpn']:
                cdna_seqs_sel_maps = {}
                for i, seq_i in enumerate(condi_map['seq']):
                    cdna_ids_sel = self.ranspl.uniform(
                        data=cdna_ids,
                        num=seq_num,
                        use_seed=self.is_seed,
                        seed=i + 100000 + (x+1)*100000,
                        replace=True,
                    )
                    ### cdna_ids_sel
                    # ['ENST00000526369.3', ..., 'ENST00000531461.5', 'ENST00000635785.1']
                    # ['ENST00000581517.1', ..., 'ENST00000490527.1', 'ENST00000453971.1']
                    # ...
                    # ['ENST00000519955.1', ..., 'ENST00000527746.5', 'ENST00000360135.8']
                    u = []
                    for ii in cdna_ids_sel:
                        if self.kwargs['mode'] == 'long_read':
                            u.append(seq_cdna_map[ii])
                        elif self.kwargs['mode'] == 'short_read':
                            # @@ if a random number extending to the end of the reference CDNA sequence
                            # leads to a length of sequence, which is shorter than the required short
                            # read length, then we directly use the whole reference CDNA sequence.
                            cdna_short_read_ran_id = self.rannum.uniform(
                                low=0,
                                high=len(seq_cdna_map[ii]) - self.len_params['seq'],
                                num=1,
                                use_seed=self.is_seed,
                                seed=(i - 100000 + (x + 1) * 100000),
                            )
                            if (cdna_short_read_ran_id[0] + self.len_params['seq']) > len(seq_cdna_map[ii]):
                                u.append(seq_cdna_map[ii][0:self.len_params['seq']])
                            else:
                                u.append(seq_cdna_map[ii][cdna_short_read_ran_id[0]:(cdna_short_read_ran_id[0]+self.len_params['seq'])])
                    cdna_seqs_sel_maps[seq_i] = u
                    # print(cdna_seqs_sel_maps)
                    # print(len(cdna_seqs_sel_maps))
                    self.pfwriter.generic(
                        df=cdna_ids_sel,
                        sv_fpn=self.working_dir + 'cdna_ids_' + seq_i + '_s_' + str(sample) + '_g_' + str(
                            gene) + '.txt',
                    )

            for id in np.arange(seq_num):
                self.console.print("======>Read {} generation".format(id + 1))
                read_struct_ref = {}
                ### +++++++++++++++ block: generate umis +++++++++++++++
                if 'umi' in condi_keys:
                    self.console.print("=========>UMI generation start")
                    for umi_mark_id, umi_mark_suffix in enumerate(condi_map['umi']):
                        # print(umi_mark_id, id + self.permutation * seq_num + umi_cnt + umi_mark_id + 100000000)
                        umi_mark = '_' + umi_mark_suffix if umi_mark_suffix != 'alone' else ''
                        self.console.print("============>UMI condition {}: {}".format(umi_mark_id, 'umi' + umi_mark))
                        umi_flag = False
                        while not umi_flag:
                            umi_seed = id + self.permutation * seq_num + umi_cnt + (umi_mark_id + 1) * 100000000 + (x+1)*100000
                            umip = self.dumi(
                                dna_map=self.dna_map,
                                umi_unit_pattern=self.len_params['umi' + umi_mark]['umi_unit_pattern'],
                                pseudorandom_num=self.rannum.uniform(
                                    low=0,
                                    high=4,
                                    num=self.len_params['umi' + umi_mark]['umi_unit_len'],
                                    use_seed=self.is_seed,
                                    seed=umi_seed,
                                ),
                            )
                            umi_i = umip.reoccur(is_sv=False)
                            edh = np.array([Hamming().general(umi_i, j) for j in umi_pool])
                            # for j in umi_pool:
                            #     if hamming().general(umi_i, j) < self.sim_thres:
                            #         print(umi_i, j)
                            if len(edh[edh < self.sim_thres]) == 0:
                                # print(len(edh[edh < self.sim_thres]))
                                umi_pool.append(umi_i)
                                read_struct_ref['umi' + umi_mark] = umi_i
                                umi_flag = True
                                umip.write(
                                    res=umi_i,
                                    lib_fpn=self.working_dir + 'umi' + umi_mark + '_s_' + str(sample) + '_g_' + str(gene) + '.txt',
                                    is_sv=self.is_sv_umi_lib)
                                umip.write(
                                    res=str(umi_seed),
                                    lib_fpn=self.working_dir + 'umi' + umi_mark + '_s_' + str(sample) + '_g_' + str(gene) + '_seeds.txt',
                                    is_sv=self.is_sv_umi_lib,
                                )
                            else:
                                # print(id)
                                umi_cnt += 1

                ### +++++++++++++++ block: generate seqs +++++++++++++++
                if 'seq' in condi_keys:
                    self.console.print("=========>Sequence generation start")
                    for seq_mark_id, seq_mark_suffix in enumerate(condi_map['seq']):
                        seq_mark = '_' + seq_mark_suffix if seq_mark_suffix != 'alone' else ''
                        self.console.print("============>Sequence condition {}: {}".format(seq_mark_id, 'seq' + seq_mark))
                        if self.kwargs['material_params']['fasta_cdna_fpn']:
                            seq_i = self.dseq(
                                cdna_seq=cdna_seqs_sel_maps[seq_mark_suffix][id],
                            ).cdna(
                                lib_fpn=self.working_dir + 'seq' + seq_mark  + '_s_' + str(sample) + '_g_' + str(gene) + '.txt',
                                is_sv=self.is_sv_seq_lib,
                            )
                            # print(seq_i)
                        else:
                            seq_seed = id + self.permutation * seq_num + 8000000 + (seq_mark_id+1) * 200000000 + (x+1)*100000
                            pseq = self.dseq(
                                dna_map=self.dna_map,
                                pseudorandom_num=self.rannum.uniform(
                                    low=0,
                                    high=4,
                                    num=self.len_params['seq' + seq_mark],
                                    use_seed=self.is_seed,
                                    seed=seq_seed,
                                ),
                            )
                            seq_i = pseq.general(
                                lib_fpn=self.working_dir + 'seq' + seq_mark  + '_s_' + str(sample) + '_g_' + str(gene) + '.txt',
                                is_sv=self.is_sv_seq_lib,
                            )
                            pseq.write(
                                res=str(seq_seed),
                                lib_fpn=self.working_dir + 'seq' + seq_mark + '_s_' + str(sample) + '_g_' + str(gene) + '_seeds.txt',
                                is_sv=self.is_sv_seq_lib,
                            )
                        read_struct_ref['seq' + seq_mark] = seq_i

                ### +++++++++++++++ block: generate primers +++++++++++++++
                if 'primer' in condi_keys:
                    self.console.print("=========>Primer generation start")
                    for primer_mark_id, primer_mark_suffix in enumerate(condi_map['primer']):
                        primer_mark = '_' + primer_mark_suffix if primer_mark_suffix != 'alone' else ''
                        self.console.print("============>Primer condition {}: {}".format(primer_mark_id, 'primer' + primer_mark))
                        primer_seed = id + self.permutation * seq_num + 8000000 + (primer_mark_id + 1) * 300000000 + (x+1)*100000
                        pprimer = self.dprimer(
                            dna_map=self.dna_map,
                            pseudorandom_num=self.rannum.uniform(
                                low=0,
                                high=4,
                                num=self.len_params['primer' + primer_mark],
                                use_seed=self.is_seed,
                                seed=primer_seed,
                            ),
                        )
                        primer_i = pprimer.general(
                            lib_fpn=self.working_dir + 'primer' + primer_mark + '_s_' + str(sample) + '_g_' + str(gene) + '.txt',
                            is_sv=self.is_sv_primer_lib),
                        pprimer.write(
                            res=str(primer_seed),
                            lib_fpn=self.working_dir + 'primer' + primer_mark + '_s_' + str(sample) + '_g_' + str(gene) + '_seeds.txt',
                            is_sv=self.is_sv_primer_lib,
                        )
                        read_struct_ref['primer' + primer_mark] = primer_i

                ### +++++++++++++++ block: generate adapters +++++++++++++++
                if 'adapter' in condi_keys:
                    self.console.print("=========>Adapter generation start")
                    for adapter_mark_id, adapter_mark_suffix in enumerate(condi_map['adapter']):
                        adapter_mark = '_' + adapter_mark_suffix if adapter_mark_suffix != 'alone' else ''
                        self.console.print("============>Adapter condition {}: {}".format(adapter_mark_id, 'adapter' + adapter_mark))
                        adapter_seed = id + self.permutation * seq_num + 8000000 + (adapter_mark_id+1) * 400000000 + (x+1)*100000
                        padapter = self.dadapter(
                            dna_map=self.dna_map,
                            pseudorandom_num=self.rannum.uniform(
                                low=0,
                                high=4,
                                num=self.len_params['adapter' + adapter_mark],
                                use_seed=self.is_seed,
                                seed=adapter_seed,
                            ),
                        )
                        adapter_i = padapter.general(
                            lib_fpn=self.working_dir + 'adapter' + adapter_mark + '_s_' + str(sample) + '_g_' + str(gene) + '.txt',
                            is_sv=self.is_sv_adapter_lib,
                        )
                        padapter.write(
                            res=str(adapter_seed),
                            lib_fpn=self.working_dir + 'adapter' + adapter_mark + '_s_' + str(sample) + '_g_' + str(gene) + '_seeds.txt',
                            is_sv=self.is_sv_adapter_lib,
                        )
                        read_struct_ref['adapter' + adapter_mark] = adapter_i

                ### +++++++++++++++ block: generate spacers +++++++++++++++
                if 'spacer' in condi_keys:
                    self.console.print("=========>Spacer generation start")
                    for spacer_mark_id, spacer_mark_suffix in enumerate(condi_map['spacer']):
                        spacer_mark = '_' + spacer_mark_suffix if spacer_mark_suffix != 'alone' else ''
                        self.console.print("============>Spacer condition {}: {}".format(spacer_mark_id, 'spacer' + spacer_mark))
                        spacer_seed = id + self.permutation * seq_num + 8000000 + (spacer_mark_id+1) * 500000000 + (x+1)*100000
                        pspacer = self.dspacer(
                            dna_map=self.dna_map,
                            pseudorandom_num=self.rannum.uniform(
                                low=0,
                                high=4,
                                num=self.len_params['spacer' + spacer_mark],
                                use_seed=self.is_seed,
                                seed=spacer_seed,
                            ),
                        )
                        spacer_i = pspacer.general(
                            lib_fpn=self.working_dir + 'spacer' + spacer_mark + '_s_' + str(sample) + '_g_' + str(gene) + '.txt',
                            is_sv=self.is_sv_spacer_lib,
                        )
                        pspacer.write(
                            res=str(spacer_seed),
                            lib_fpn=self.working_dir + 'spacer' + spacer_mark + '_s_' + str(sample) + '_g_' + str(gene) + '_seeds.txt',
                            is_sv=self.is_sv_spacer_lib,
                        )
                        read_struct_ref['spacer' + spacer_mark] = spacer_i

                ### +++++++++++++++ block: Custom-designed sequences +++++++++++++++
                if 'custom' in condi_keys:
                    for custom_mark_id, custom_mark_suffix in enumerate(condi_map['custom']):
                        custom_mark = '_' + custom_mark_suffix if custom_mark_suffix != 'alone' else ''
                        self.console.print("============>Custom-designed condition {}: {}".format(custom_mark_id, 'custom' + custom_mark))
                        read_struct_ref['custom' + custom_mark] = self.kwargs['seq_params']['custom' + custom_mark]

                read_struct_pfd_order = {condi: read_struct_ref[condi] for condi in self.condis}
                sequencing_library.append([
                    self.paste([*read_struct_pfd_order.values()]),
                    str(id) + '*s*' + str(sample) + '*g*' + str(gene) + '*',
                    'init',
                ])
        # print(umi_cnt)
        # print(umi_pool)
        self.pfwriter.generic(df=sequencing_library, sv_fpn=self.working_dir + 'sequencing_library.txt')
        etime = time.time()
        self.console.print("===>Time for sequencing library preparation: {:.3f}s".format(etime-stime))
        return sequencing_library

    def paste(self, read_struct=[]):
        return ''.join(read_struct)


if __name__ == "__main__":
    from tresor.path import to

    from tresor.gsample.FromSimulator import fromSimulator

    gspl = fromSimulator(
        R_root='D:/Programming/R/R-4.3.2/',
        num_samples=2,
        num_genes=20,
        simulator='spsimseq',
    ).run()

    p = Gene(
        gspl=gspl,
        len_params={
            'umi': {
                'umi_unit_pattern': 3,
                'umi_unit_len': 12,
            },
            'umi_1': {
                'umi_unit_pattern': 3,
                'umi_unit_len': 12,
            },
            'seq': 100,
            'seq_2': 100,
            'adapter': 10,
            'adapter_1': 10,
            'primer': 10,
            'primer_1': 10,
            'spacer': 10,
            'spacer_1': 10,
        },
        seq_params={
            'custom': 'BAGC',
            'custom_1': 'V',
        },
        material_params={
            'fasta_cdna_fpn': to('data/Homo_sapiens.GRCh38.cdna.all.fa.gz'),  # None False
        },
        is_seed=True,

        working_dir=to('data/simu/'),

        # condis=['umi'],
        # condis=['umi', 'seq'],
        condis=['umi', 'custom', 'seq', 'custom_1'],

        # condis=['umi', 'primer', 'primer_1', 'spacer', 'spacer_1', 'adapter', 'adapter_1', 'seq', 'seq_2', 'umi_1'],
        sim_thres=3,
        permutation=0,

        mode='short_read',  # long_read short_read

        verbose=False,
    )

    p.pooling()