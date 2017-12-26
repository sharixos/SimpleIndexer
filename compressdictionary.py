
def compress(ifname, osinglefile, ostringfile):
    ifile = open(ifname)
    ofile = open(osinglefile, 'wb')
    ofile2 = open(ostringfile, 'w')

    pos = 0
    for line in ifile:
        sp = line.split()
        ofile2.write(sp[0])
        out = []
        out.append(int(sp[1]))
        out.append(int(sp[2]))
        out.append(pos)
        for i in range(3):
            ofile.write(bytes(((out[i])&255,)))
            ofile.write(bytes(((out[i]>>8)&255,)))
            ofile.write(bytes(((out[i]>>16)&255,)))
            ofile.write(bytes(((out[i]>>24)&255,)))
        pos += len(sp[0])

def uncompress(singlefile, stringfile, ofname):
    isingle = open(singlefile,'rb')
    istring = open(stringfile)
    ofile = open(ofname, 'w')

    data = isingle.read()
    strdata = istring.read()
    lines = int(isingle.tell()/12)
    arr = []
    for i in range(int(lines)):
        for j in range(3):
            v = 0
            v = (v | int(data[i*12+j*4+3])) << 8
            v = (v | int(data[i*12+j*4+2])) << 8
            v = (v | int(data[i*12+j*4+1])) << 8
            v = (v | int(data[i*12+j*4+0]))
            arr.append(v)
    for i in range(lines-1):
        length = arr[i*3+5] - arr[i*3+2]
        term = strdata[0:length]
        strdata = strdata[length:]
        strid = str(arr[i*3+0])
        strfq = str(arr[i*3+1])
        ofile.write(term + ' '*(20-len(term)) + ' '+ strid + ' '*(4-len(strid))+ ' ' + strfq + ' '*(4-len(strfq))+'\n')
    strid = str(arr[lines*3-3])
    strfq = str(arr[lines*3-2])
    ofile.write(strdata + ' '*(20-len(strdata)) + ' '+ strid + ' '*(4-len(strid))+ ' ' + strfq + ' '*(4-len(strfq))+'\n')

dictionary = 'data/index/dictionary.txt'
single = 'data/index/dictionary.single'
string = 'data/index/dictionary.string'
unsingle = 'data/index/dictionary.unsingle'

print('------------ dictionary compressed and uncompressed--------------')
print("dictionary compressed to file: ")
print('    '+single + ' and ' + string)

compress(dictionary, single, string)
uncompress(single, string,unsingle)

print("and uncompressed file is:")
print('    '+unsingle)
print('-----------------------------------------------------------------')