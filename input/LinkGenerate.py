"""This file help fixing url in version released
If there are new versions, first add in "released.json" to reuse again in the future, then change version need to test
in "input.json" and run this file, url in "input.json" will be generated automatically"""
import json


def loadInputData(file_name):
    f = open(file_name)
    _inp = json.load(f)
    f.close()
    return _inp


def writeInputData(_inp):
    f = open("input.json", "w")
    json.dump(_inp, f, indent=3)
    f.close()


if __name__ == "__main__":
    dst = loadInputData('input.json')
    src = loadInputData('released.json')
    for t in ['market', 'sqe']:
        for n in ['client', 'wakeup', 'dictation']:
            version = dst[t][n][0]
            for r in src[n]:
                if version == r[0]:
                    dst[t][n][1] = r[1]
                    break
    writeInputData(dst)
