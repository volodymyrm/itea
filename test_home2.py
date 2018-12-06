from home2 import monitor
import shutil
import os

def checker():

    for filename in os.listdir('source'):
        if os.path.exists(os.path.join('source', filename)):
            os.remove(os.path.join('source', filename))

    for filename in os.listdir('results'):
        if os.path.exists(os.path.join('results', filename)):
            os.remove(os.path.join('results', filename))

    for filename in os.listdir('errors'):
        if os.path.exists(os.path.join('errors', filename)):
            os.remove(os.path.join('errors', filename))

    shutil.copy('Norm1.txt', 'source')
    shutil.copy('Norm2.txt', 'source')
    shutil.copy('Bad_file1.txt', 'source')
    shutil.copy('Bad_file2.txt', 'source')
    shutil.copy('Presentation.odp', 'source')

    monitor('source', 'results', 'errors')

    source_files = os.listdir('source')
    result_files = os.listdir('results')
    error_files = os.listdir('errors')

    print('source_files list: ', source_files == ['Presentation.odp'])
    print('result_files list: ', result_files == ['Norm1.txt', 'Norm2.txt'])
    print('error_files list: ', error_files == ['Bad_file1.txt', 'Bad_file2.txt'])

    norm1 = open(os.path.join('results', 'Norm1.txt'), 'r')
    norm2 = open(os.path.join('results', 'Norm2.txt'), 'r')
    bad1 = open(os.path.join('errors', 'Bad_file1.txt'), 'r')
    bad2 = open(os.path.join('errors', 'Bad_file2.txt'), 'r')

    print('Norm1.txt value', norm1.read() == '6')
    print('Norm2.txt value', norm2.read() == '3')
    print('Bad_file1.txt value', bad1.read() == 'kfdsdfsdhf')
    print('Bad_file2.txt value', bad2.read() == '[a,2,3,]')

    norm1.close()
    norm2.close()
    bad1.close()
    bad2.close()

    for filename in os.listdir('results'):
        if os.path.exists(os.path.join('results', filename)):
            os.remove(os.path.join('results', filename))

    for filename in os.listdir('errors'):
        if os.path.exists(os.path.join('errors', filename)):
            os.remove(os.path.join('errors', filename))

checker()