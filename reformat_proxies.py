import re
import os


def reformat_proxy(file_path):
    lines_list = []
    with open(file_path, 'r') as fp:
        lines_list = fp.readlines()
    lines_list = [re.sub(r'(<.*]\s)|>', '', a) for a in lines_list]
    with open(file_path, 'w') as fp:
        for line in lines_list:
            fp.write(line)


def proxybroker(limit=10, outfile='proxies.txt', types='HTTP'):
    try:
        if os.system(f'proxybroker find --type {types} -l {limit} --outfile {outfile}') != 0:
            raise Exception
    except:
        print(f'$$$$RUNTIME ERROR OCCURRED: Retrying in 5 seconds...')
        main()


def main():
    print(f'>>Fetching proxies...')
    proxybroker(100)
    print('DONE!')
    print(f'>>Reformatting proxies...')
    reformat_proxy('proxies.txt')
    print('DONE!')

main()