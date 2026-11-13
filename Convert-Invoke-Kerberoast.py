#!/usr/bin/python

import argparse
import os
import io
import re
import sys

def format_Data(fHandle, inputSamAccountName):
    fh = io.open(fHandle, 'r')
    SamAccountName = ''
    DistinguishedName = ''
    Hash = ''
    Hashes = []
    try:
        for line in fh:
            #Grab the SamAccountName
            if "SamAccountName" in line:
                stuff = line.split(':')
                SamAccountName = stuff[1].strip()
            #Grab the DistinguishedName
            if "DistinguishedName" in line:
                stuff = line.split(':')
                stuff = line.split(',')
                DistinguishedName = "{0}.{1}".format(stuff[-2].strip().replace('DC=',''),stuff[-1].strip().replace('DC=',''))
            #Grab Hash Line
            if "Hash" in line:
                stuff = line.split(' :')
                Hash += stuff[1].strip()
            #Grab Hash Line
            if "                       " in line:
                Hash += line.strip()
            if line == '\n' and (inputSamAccountName == None or SamAccountName in inputSamAccountName):
                print('[*] Adding {!r} to output file').format(SamAccountName)
                Hashes.append(re.sub(r'\*.*\*',"*{0}${1}$spn*$".format(SamAccountName,DistinguishedName), Hash))
                SamAccountName = ''
                DistinguishedName = ''
                Hash = ''
    except Exception, e:
        print >> sys.stderr, '[-] Error: %s \n Exiting...' % e

        sys.exit(1)
    
    if SamAccountName != '' and DistinguishedName != '' and  Hash != '': # Check if there ist still a hash element not appended 
        if inputSamAccountName == None or SamAccountName in inputSamAccountName:
            print('[*] Adding {!r} to output file').format(SamAccountName)
            Hashes.append(re.sub(r'\*.*\*',"*{0}${1}$spn*$".format(SamAccountName,DistinguishedName), Hash))
    
    print("[+] Created {0} entries.").format(len(Hashes))
    return Hashes


parser = argparse.ArgumentParser(description='Parser of Kerberoast output from Invoke-Kerberoast')

parser.add_argument('-f', action="store", dest="inputHandle", required=True, help = "Input file")
parser.add_argument('-w', action="store", dest="outputHandle", help = "Output file")
parser.add_argument('-a', action="store", dest="inputSamAccountName", nargs='*', help="Specify one or more SamAccountName(s) which will be extracted from a list of multiple hashes.")

parsed = parser.parse_args()

if(os.path.isfile(parsed.inputHandle)):

    print("[*] Opening file: {0}").format(parsed.inputHandle)
    output = format_Data(parsed.inputHandle, parsed.inputSamAccountName)
    if parsed.outputHandle:
        fOutput = open(parsed.outputHandle, 'w')
        for element in output:
            fOutput.write(element)
            fOutput.write('\n')
        fOutput.close()
        print("[+] Hashes written to: {0}".format(parsed.outputHandle))
    else:
        for element in output:
            print(element)
            print('\n')
else:
    print("Error opening file: {0}").format(parsed.inputHandle)
    exit()
