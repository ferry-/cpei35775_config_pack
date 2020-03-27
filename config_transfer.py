#!/usr/bin/python3

import sys
import requests

URL= "http://%s/cgi-bin/firmwarecfg"

def usage():
    print("Usage: %s down host" % sys.argv[0])
    print("       %s up host config.bin" % sys.argv[0])

def main():
    if len(sys.argv) in (3, 4):
        op = sys.argv[1].strip().lower()
        host = sys.argv[2]

        if op == "down":
            r = requests.post(URL % host, files={ 'a': None }, data={ "config":"Download" })
            if r.status_code == 200:
                config = r.content
                sys.stdout.buffer.write(config)
                print("success", file=sys.stderr)
            else:
                print("failed (code %d). try logging in the web interface first" % r.status_code, file=sys.stderr)

        elif op == "up":
            input_file = open(sys.argv[3], "rb")
            r = requests.post(URL % host, files={'UploadConfigFile': ('UploadConfigFile', input_file, "application/octet-stream")}, data={"Submit23":"Import"})
            print(r)
            if r.ok:
                print(r.text)
            else:
                print(r.text)
                print("failed. try logging in the web interface first", file=sys.stderr)

        else:
            usage()

    else:
        usage()

if __name__ == "__main__":
    main()
