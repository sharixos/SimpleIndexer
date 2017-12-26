import math

def gamma(num):
    num_bin = bin(num).replace('0b','')
    return '1' * (len(num_bin) - 1) + '0' + num_bin[1:]

def ungamma(thestr):
    mid = thestr.find('0')
    return int(math.pow(2,mid)) + int(thestr[mid:],2)

def compress(ifname, ofname):
    ifile = open(ifname)
    ofile = open(ofname, 'wb')
    for line in ifile:
        binstr = ''
        docnos = line.split()
        lvalue = int(docnos[0])
        binstr += gamma(lvalue + 1)
        for docno in docnos[1:]:
            binstr += gamma(int(docno) - lvalue)
            lvalue = int(docno)
        while len(binstr)>=8:
            out = int(binstr[0:8],2)
            ofile.write(bytes((out,)))
            binstr = binstr[8:]
        if len(binstr) != 0:
            binstr += '1'*(8-len(binstr))
            out = int(binstr,2)
            ofile.write(bytes((out,)))
        ofile.write(bytes((255,))) # line end flag
    
def uncompress(ifname, ofname):
    ifile = open(ifname, 'rb')
    ofile = open(ofname, 'w')

    ifdata = ifile.read()
    ifsize = ifile.tell()
    binstr = ''
    x = 0
    while x<ifsize:
        if ifdata[x]==255:
            if x+1<ifsize and ifdata[x+1]==255:
                binstr += '1'*8
                x += 1
            p0 = binstr.find('0')
            lvalue = ungamma(binstr[0:p0*2+1]) - 1
            binstr = binstr[p0*2+1:]
            ofile.write(str(lvalue)+' ')
            p0 = binstr.find('0')
            while p0>-1:
                lvalue += ungamma(binstr[0:p0*2+1])
                ofile.write(str(lvalue)+' ')
                binstr = binstr[p0*2+1:]
                p0 = binstr.find('0')
            ofile.write('\n')
            binstr = ''
        else:
            code = bin(ifdata[x]).replace('0b','')
            binstr += '0'*(8-len(code)) + code
        x += 1

inverted = 'data/index/inverted.txt'
gammafile = 'data/index/inverted.gamma'
ungammafile = 'data/index/inverted.ungamma'

print('--------- inverted index compressed and uncompressed------------')
print("inverted index compressed to file: ")
print('    '+gammafile)

compress(inverted, gammafile)
uncompress(gammafile, ungammafile)

print("and uncompressed file is:")
print('    '+ungammafile)
print('-----------------------------------------------------------------')