import shutil
import os
import io
import sys
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():

        path = r'D:\temp\acg temp\temp\幼驯染\197'
        f = os.listdir(path)
        print(f)


if __name__ == '__main__':
    main()