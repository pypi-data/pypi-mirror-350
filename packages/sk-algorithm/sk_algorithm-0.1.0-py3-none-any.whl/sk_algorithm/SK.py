# word="k"
def sk(word):
    li=[]
    for i in word:
        a=ord(i)
        e_num=a+3%26
        e_word=chr(e_num)
        li.append(e_word)
    e_string="".join(li)
    rli1=[]
    rli2=[]
    for j in range(len(e_string)):
        if j%2==0:
            rli1.append(e_string[j])
            li1="".join(rli1)
        else:
            rli2.append(e_string[j])
            li2="".join(rli2)
   
    full=li1+li2
    return full

def ks(word):
    le=len(word)
    mid=le//2

    n=0
    dli1=[]
    dli2=[]
    for j in range(len(word)):
        if len(word)%2==0:
            if n<mid:
                dli1.append(word[n])
                li1="".join(dli1)
                n+=1
            else:
                dli2.append(word[n])
                li2="".join(dli2)
                n+=1
        else:
            if n<=mid:
                dli1.append(word[n])
                li1="".join(dli1)
                n+=1
            else:
                dli2.append(word[n])
                li2="".join(dli2)
                n+=1
    new=[]
    if len(word)%2==0:
        for h in range(mid):
            new.append(dli1[h])
            new.append(dli2[h])
    else:
        for h in range(mid+1):
            if h==mid:
                new.append(dli1[h])
            else:
                new.append(dli1[h])
                new.append(dli2[h])
        


    d_full=[]
    for n in new:
        d_num=ord(n)
        num=d_num-3%26
        d_word=chr(num)
        d_full.append(d_word)
    de="".join(d_full)
    
    return de


# print(sk("this is encryption method"))
