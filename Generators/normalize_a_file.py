# say I have a file having list of numbers, i want to normalized output
# ex: file has [2
# 3,
# 4]
# sum = 2 + 3 + 4
# output should be [(2/sum)*100,(3/sum)*100,(4/sum)*100 ]


# a generator that will yeild ints from input file
def read_file(name):
    with open(name, 'r') as f:
        for line in f:
            yield int(line)

# As generators returns an iterator


def print_generator_values(numbers):
    flag = True
    for i in numbers:
        flag = False
        print(i)
    if flag:
        print("no numbers found, iterator is empty")

it = read_file("mynums.txt")
# it is a generator object , lets see what it contains
print_generator_values(it)
print("lets try one more time")
print_generator_values(it)

# As we can see second time iterator is already empty or exhausted.
# so basically a iterator can be executed only once.
# now lets come to the problem

def normalize(numbers):
    total = sum(numbers)
    print("sum is " + total.__str__())
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

# In normalize method once sum runs on numbers, numbers will be exhaused. then value in numbers will not work as expected.

it = read_file("mynums.txt")
res = normalize(it) # this res will be empty list
print(res)

# one thing that can be done is keeping a copy of it in normalize

def normalize_keep_copy(numbers):
    numbers = list(numbers) # here we are converting iterator to list so eventually again this code can fail coz of out of memory if numbers are so many
    total = sum(numbers)
    print("sum is " + total.__str__())
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

it = read_file("mynums.txt")
res = normalize_keep_copy(it) # this res will be empty list
print(res)


print("getting new interator can be an option: ...")
# what we can do is we can send read_file("mynums.txt") as input to normalize function and it will get new iterator
# while doing addition and while iterating

def normalize_passed_read_file(get_iter):
    total = sum(get_iter())
    result = []
    for value in get_iter():
        percent = 100 * value / total
        result.append(percent)
    return result

percentages = normalize_passed_read_file(lambda : read_file("mynums.txt"))
print(percentages)

#Even better way to achieve the same result is using a class that implements iterator protocol.
# read iterators readme.md to understand better

# Basically when we try to run over a iterator ,__iter__ method is called.

print("created a new container class, where __iter__ itself yields data")
class ReadFileGenerator(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def __iter__(self):
        with open(self.file_name) as f:
            for line in f:
                yield int(line)
it = ReadFileGenerator("mynums.txt")
percentages = normalize(it)
print(percentages)

# So what ever we send list, array etc are all containers which python knows how to traverse.
# what we did above is defined one of our own container and used __iter method to tell it to yield results one after another.
# In this case at the time of sum __iter__ method will be called at it will yield line by line, and sum method will keep using it and doing sum.
# once its yielded it will be consumed then only next yield will happen.
# next while accessing each number in for loop, again second item iter method will get called and all are yielded again , and for loop will keep using that yielded value one by one.
# to generate results. Remeber this yielding and consumption are sequential.