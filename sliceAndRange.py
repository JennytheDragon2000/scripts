
import sys
print('\n')
l = ['a', 'b', 'c', 'd', 'e', 'f']
#add one space to the left of each element in the list
print([f' {i}' for i in l])


#compare slicing and indexing with range()

#get values from command line
# sliceStart = int(sys.argv[1])
# sliceStop = int(sys.argv[2])
# sliceStep = int(sys.argv[3])

# rangeStart = int(sys.argv[4])
# rangeStop = int(sys.argv[5])
# rangeStep = int(sys.argv[6])

sliceStart = 10 
sliceStop = -10
sliceStep = -1

rangeStart = 5
rangeStop = -1
rangeStep = -1

sliceObject = slice(sliceStart, sliceStop, sliceStep)
rangeList = range(rangeStart, rangeStop, rangeStep)

def sliceUsingRange(rangeStart, rangeStop, rangeStep=1):
    print([f'{l[i]}' for i in rangeList],  "<==================== using range", f"{rangeStart}, {rangeStop}, {rangeStep}")


#print the positive incex of l
print([ f' {i}' for i in range(len(l))])
#print the nexgative index of l
print([ f'{i}' for i in range(-len(l), 0)])
print("\n")


print(l[sliceObject], "<====================       slice", f"{sliceStart}, {sliceStop}, {sliceStep}")
sliceUsingRange(rangeStart, rangeStop, rangeStep)



