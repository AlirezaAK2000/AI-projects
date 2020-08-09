"""
main file for running project
"""
from pre_processing_tools import get_data, read_test
from learning_tools import learn, test, learn_landas
from app_constants import LANDAS

if __name__ == '__main__':
    lines_train = get_data('Train_data.rtf')
    model = learn(lines_train)
    lines_test, labels = read_test(['Test_data.rtf', 'labels.rtf'])
    print(test(lines_test, labels, model)(LANDAS))
