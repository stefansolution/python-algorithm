from dct import  DCT 

in_img = "test_imgs/mountain.png"
msg = b"This is my secret"

out_img = "mountain_dct.png"


en = DCT(in_img)
en.DCTEn(msg, out_img)

dec = DCT(out_img)
secret  = dec.DCTDe().decode()

print(secret)






