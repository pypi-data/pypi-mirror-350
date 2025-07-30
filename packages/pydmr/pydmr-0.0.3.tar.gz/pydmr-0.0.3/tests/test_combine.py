import os

import numpy as np
import pydmr


def test_concat():

    data1 = {
        'time': ['Acquisition times', 'sec', 'float'],
        'signal': ['Acquired signals', 'sec', 'float'],
        'FA': ['Flip angle', 'deg', 'float'],
        'TR': ['Repetition time', 'msec', 'float'],
    }
    data2 = {
        'time': ['Acquisition times', 'sec', 'float'],
        'signal': ['Acquired signals', 'sec', 'float'],
        'FA': ['Flip angle', 'deg', 'float'],
        'TR': ['Repetition time', 'msec', 'float'],
    }
    rois1 = {
        '001': {
            'Baseline': {
                'time': [1,2,3,4],
                'signal': [5,6,7,8],
            },
            'Followup': {
                'time': [9,10,11],
                'signal':[12,13,14],
            },
        },
    }
    rois2 = {
        '002': {
            'Baseline': {
                'time': [10,20,30,40],
                'signal':[50,60,70,80],
            },
            'Followup': {
                'time': [90,100,110],
                'signal':[120,130,140],
            },
        },
    }
    pars1 = {
        '001': {
            'Baseline': {
                'FA': 50,
                'TR': 5.4,
            },
            'Followup': {
                'FA': 40,
                'TR': 5.4,
            },
        },
    }
    pars2 = {
        '002': {
            'Baseline': {
                'FA': 45,
                'TR': 5.4,
            },
            'Followup': {
                'FA': 50,
                'TR': 5.4,
            },
        },
    }

    dmr = {'data':data1, 'pars':pars1, 'rois':rois1}
    file1 = os.path.join(os.getcwd(), 'test1.dmr')
    pydmr.write(file1, dmr, 'nest')

    dmr = {'data':data2, 'pars':pars2, 'rois':rois2}
    file2 = os.path.join(os.getcwd(), 'test2.dmr')
    pydmr.write(file2, dmr, 'nest')

    # concatenate
    file = os.path.join(os.getcwd(), 'test.dmr')
    pydmr.concat([file1, file2], file)

    # read
    dmr_concat = pydmr.read(file, format='nest')

    assert np.array_equal(
        dmr_concat['data']['FA'],
        ['Flip angle', 'deg', 'float'],
    )
    assert np.array_equal(
        dmr_concat['rois']['001']['Baseline']['signal'],
        [5, 6, 7, 8],
    )
    assert np.array_equal(
        dmr_concat['rois']['001']['Followup']['signal'],
        [12, 13, 14],
    )
    assert dmr_concat['pars']['001']['Followup']['FA'] == 40
    assert dmr_concat['pars']['002']['Followup']['FA'] == 50

    # Cleanup
    os.remove(file1 + '.zip')
    os.remove(file2 + '.zip')
    os.remove(file + '.zip')



if __name__ == "__main__":

    test_concat()

    print('All combine tests passed!!')