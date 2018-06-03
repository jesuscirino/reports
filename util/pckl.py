
import pickle
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("file", help="print pickle file", type=str)
args   = parser.parse_args()
FILE   = args.file
RES    = {'Tag Abuse':0,
           'None':0,
        'Plagiarism':0,
        'Copy Paste':0,
        'Photoplagiarism':0}
 
with open(FILE, 'rb') as f:
    d = pickle.load(f)
    for k, v in d.items():
        if v['date'] < '2018-05-09-59-59-00'and v['date'] > '2018-05-09-00-00-00':
        #if v['date'] < '2018-01-01-00-00-00':
            #RES[v['reason']] += 1
            #print(v['date'])
            print('{} --- {}'.format(k,v))
            print('\n/////////')
    print('*****')
    print('*****')
 
print (RES)
