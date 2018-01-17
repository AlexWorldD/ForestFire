from forest_model import *

if __name__ == '__main__':
    test = ForestModel()
    for i in range(100):
        test.step()
        print(i, test.grid)
    print('t')
