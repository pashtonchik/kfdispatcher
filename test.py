a = 200

while True:
    a -= 1
    try:
        if not a:
            print(a)
            break
    except:
        print(10000)