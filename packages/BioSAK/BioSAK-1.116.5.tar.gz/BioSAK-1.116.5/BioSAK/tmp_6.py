
gbk_file = '/Users/songweizhi/Desktop/SMP/Host_tree_Sponge/combined_COI_sponge_3AXHW8PS013-Alignment_formatted_ref_accession/tmp/FR848901.1.gbk'

def get_origin_seq_from_gbk(gbk_file):

    after_origin_line = False
    before_slash_line = True
    concatenated_seq = ''
    for each_line in open(gbk_file):
        each_line = each_line.strip()
        if each_line == 'ORIGIN':
            after_origin_line = True
        if each_line == '//':
            before_slash_line = False
        if (after_origin_line is True) and (before_slash_line is True):
            if each_line != 'ORIGIN':
                each_line_split = each_line.split(' ')
                seq_str = ''.join(each_line_split[1:])
                seq_str = seq_str.upper()
                concatenated_seq += seq_str

    return concatenated_seq
