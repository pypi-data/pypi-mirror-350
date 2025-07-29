import matplotlib
import numpy as np
import multiprocessing

matplotlib.rcParams['webagg.open_in_browser'] = False
matplotlib.use('webagg')

import matplotlib.pyplot as plt
from matplotlib.pyplot import *

def show_figure_(figure):
    figure.show()
    plt.show(block=False)

# 这是一个全局列表
figures = []
current_progress = None

def show(figure=None):
    if figure is None:
        figure = plt.gcf()
    
    if not figure in figures:
        figures.append(figures)
    else:
        figures.pop(figures.index(figure))
        figures.append(figure)
    global current_progress
    if current_progress is not None:
        # 停止当前进程，并释放
        current_progress.terminate()
    current_progress = multiprocessing.Process(target=show_figure_, kwargs=dict(figure=figure))
    current_progress.start()
