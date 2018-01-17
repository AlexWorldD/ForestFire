from forest_model import *

if __name__ == '__main__':
    test = ForestModel()
    for _ in range(10):
        test.step()
        print(test.grid)
    print('t')
