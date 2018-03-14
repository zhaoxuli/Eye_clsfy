import random
import argparse 

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('fn_caffelist', type=str, help='[in]')
    parser.add_argument('fn_mxnetlist', type=str, help='[out]')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    #if source_base_folder[-1] != os.sep:
    #    source_base_folder += os.sep
    #    
    #if remove_path[-1] != os.sep:
    #    remove_path += os.sep

    args = parse_args()

    lines = open(args.fn_caffelist).readlines()
    lines = map(lambda x: x.strip(), lines)
    img_list = map(lambda x: x.split(), lines)
    
    lst_list = []
    idx = 0
    for img_name, img_class in img_list:
        out_line = '%d\t%s\t%s' % (idx, img_class, img_name)
        lst_list.append(out_line)
        idx += 1
        
    random.seed(100)
    random.shuffle(lst_list)
   
    out_f = open(args.fn_mxnetlist, 'w') 
    for a in lst_list:
        out_f.write(a + '\n')
        
    out_f.truncate(out_f.tell()-1)
    out_f.close()
