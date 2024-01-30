from scipy import stats

x = [1, 2, 3, 4]
y = [1, 3, 2, 1]

slope1, intercept, r, p, std_err = stats.linregress(x, y)
print(slope1)
print(r)
print(stats.linregress(x, y))
print(type(stats.linregress(x, y)))
"""
def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, x))
print(mymodel)
"""