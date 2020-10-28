# Press the green button in the gutter to run the script.
from .core import Data

if __name__ == '__main__':
    print('go go go!')
    #data = pd.read_csv('./data/USDA_Food_Database.csv')

    data = Data()
    data.read_data('./data/USDA_Food_Database.csv')
    print(data.data)





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
