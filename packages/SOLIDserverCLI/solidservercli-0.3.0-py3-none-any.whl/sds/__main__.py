import os
import sys

"""
def convert_str_json(sparams: str) -> dict:
    import re
    print(f'---- {sparams}')

    if not sparams or sparams == "":
        return {}

    a = re.findall(r'((\w+)=(\w+|\"[^\"]+\")),?', sparams)
    if a:
        for g in a:
            print(g[1], g[2])


convert_str_json('a=12')
convert_str_json('a=12,b=1')
convert_str_json('a=12,b=1,c="test"')
convert_str_json('a=12,b=1,c="test,test"')
convert_str_json('a=12,b=1,c="test=test"')
exit()
"""

if not __package__:
    # Make CLI runnable from source tree with
    #    python src/package
    package_source_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, package_source_path)

if __name__ == "__main__":
    from sds.cli import main

    main()
