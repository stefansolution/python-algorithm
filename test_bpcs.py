import bpcs

alpha = 0.45
vslfile = 'Temp\\raw_image1.png'
msgfile = 'AnyTextGreaterThan300Chars' # can be any type of file
encfile = 'Temp\\raw_image1_test_bpcs.png'
msgfile_decoded = 'Temp\\tmp.txt'

bpcs.encode(vslfile, msgfile, encfile, alpha) # embed msgfile in vslfile, write to encfile
msg = bpcs.decode(encfile, msgfile_decoded, alpha) # recover message from encfile
print(msg)