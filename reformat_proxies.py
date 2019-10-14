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
    os.system(f'proxybroker find --type {types} -l {limit} --outfile {outfile}')


def main():
    print(f'>>Fetching proxies...')
    try:
        proxybroker(100)
    except RuntimeError:
        print(f'$$$$RUNTIME ERROR OCCURRED: Retrying in 5 seconds...')
        main()
    print('DONE!')
    print(f'>>Reformatting proxies...')
    reformat_proxy('proxies.txt')
    print('DONE!')

main()