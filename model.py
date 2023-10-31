from random import randint
a=list()
for i in range(10):
  a.insert(i,randint(1,100))
  
for i in range(10):
  print(a[i],end='\n')
