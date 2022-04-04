import base64

f = open('/Users/maksimbuzov/Desktop/music_for_md.png', 'rb')
ls_f = base64.b64encode(f.read())
f.close()
str(ls_f)
ff = open('/Users/maksimbuzov/Desktop/base64.txt', 'wb')
ff.write(ls_f)
ff.close()
# print(str(ls_f))
