import csv
import os
import random
#这里的样本都是按二倍体来的
def count_convert_to_state(par_1_count_A, par_1_count_a, par_2_count_A, par_2_count_a,
                           sam_1_count_A, sam_1_count_a, sam_2_count_A, sam_2_count_a,
                           sam_3_count_A, sam_3_count_a, sam_4_count_A, sam_4_count_a):
    def get_genotype(count_A, count_a):
        total = count_A + count_a
        prob_A = count_A / total
        return 'A' if random.random() < prob_A else 'a'

    def get_diploid_genotype(count_A, count_a):
        allele1 = get_genotype(count_A, count_a)
        allele2 = get_genotype(count_A, count_a)
        return ''.join(sorted([allele1, allele2]))

    def determine_state(sam_genotype, par1_genotype, par2_genotype):
        if par1_genotype == par2_genotype:
            return random.choice([0, 1, 2])
        count_par1 = sam_genotype.count(par1_genotype)
        count_par2 = sam_genotype.count(par2_genotype)
        if count_par1 == 2:
            return 0
        elif count_par2 == 2:
            return 1
        elif count_par1 == 1 and count_par2 == 1:
            return 2
        return -1

    # 获取父母的基因型
    par1_genotype = get_genotype(par_1_count_A, par_1_count_a)
    par2_genotype = get_genotype(par_2_count_A, par_2_count_a)

    # 获取并计算每个样本的状态
    states = []
    for count_A, count_a in [(sam_1_count_A, sam_1_count_a), (sam_2_count_A, sam_2_count_a),
                             (sam_3_count_A, sam_3_count_a), (sam_4_count_A, sam_4_count_a)]:
        sam_genotype = get_diploid_genotype(count_A, count_a)
        state = determine_state(sam_genotype, par1_genotype, par2_genotype)
        states.append(state)

    return states


def process_panel_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        for row in reader:
            position = row[1]
            par_1_count_A = int(row[2])
            par_1_count_a = int(row[3])
            par_2_count_A = int(row[4])
            par_2_count_a = int(row[5])
            sam_1_count_A = int(row[7])
            sam_1_count_a = int(row[8])
            sam_2_count_A = int(row[9])
            sam_2_count_a = int(row[10])
            sam_3_count_A = int(row[11])
            sam_3_count_a = int(row[12])
            sam_4_count_A = int(row[13])
            sam_4_count_a = int(row[14])

            # 获得样本的状态
            states = count_convert_to_state(par_1_count_A, par_1_count_a, par_2_count_A, par_2_count_a,
                                            sam_1_count_A, sam_1_count_a, sam_2_count_A, sam_2_count_a,
                                            sam_3_count_A, sam_3_count_a, sam_4_count_A, sam_4_count_a)

            # 写入位置和状态
            writer.writerow([position] + states)


def process_all_panels(directory):
    # List all files in the directory
    for filename in os.listdir(directory):
        if filename.startswith("example") and filename.endswith(".panel"):
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(directory, filename.replace("example", "state").replace(".panel", ".panel"))
            process_panel_file(input_file, output_file)

# 使用实际的目录路径
directory = 'E:/毕业设计/ancestryhmm/example_chromosome_panel'
process_all_panels(directory)