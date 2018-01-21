from forest_model import *
import json
from tqdm import tqdm
import time
import scipy as sp
import seaborn as sns
from multiprocessing import Pool


def get_density(args):
    """
    Calculation the car flow for default CA
    :param args: density
    :return: measurements
    """
    sp.random.seed()
    cur_density = args
    print('Density: ', cur_density)
    samples = 4
    st = time.time()
    model = ForestModel()
    model._param_treeDensity = cur_density
    model.reset()
    results = []
    print('Current density is: ', cur_density)
    for _ in tqdm(range(samples)):
        "Getting new random initial row"
        model.reset()
        for i in range(250):
            model.step()
        #     For additional INFO change HERE
        if cur_density == 0.0:
            results.append(0)
        else:
            results.append(model.measurements['Dead'][-1] / model.measurements['Trees'][0])
    print('Elapsed time: ', time.time() - st)
    return cur_density, results


def plot_graphs(file_name='ResultsMeasure.raw', feature='Ignited', data=False):
    if not data:
        with open(file_name) as data_file:
            RESULT = json.load(data_file)
    else:
        RESULT = data
    f, ax = plt.subplots(figsize=(12, 8))
    # sns.tsplot(..., ax=ax)
    sns.tsplot(RESULT[feature], legend=True, condition=feature, color='r')
    # sns.tsplot(np.array([0.3]*3000), color='g')
    # sns.tsplot(np.array([0.4] * 3000), color='g')
    # ATTENTION!!! HERE you can set the critical range
    ax.axhline(y=.3, xmin=0.75, xmax=1, color='lightgrey', linestyle='--', label='Range of real values')
    ax.axhline(y=.35, xmin=0.75, xmax=1, color='lightgrey', linestyle='--')
    if feature == 'Ignited':
        sns.tsplot(RESULT['Border'], legend=True, condition='Fire Border', color='Blues_d')
    if feature == 'Border':
        sns.tsplot(RESULT['Ignited'], legend=True, condition='Ignited', color='Blues_d')
    sns.set(font_scale=1.5)
    plt.setp(ax.get_legend().get_texts(), fontsize='16')  # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize='22')  # for legend title
    # sns.pointplot(x=np.array(range(len(RESULT[target][state]))), y=RESULT[target][state])
    # sns.tsplot(time='lambda', value='Transient len',
    #            data=to_plot, ci="sd")
    _text = 'Steps'
    ax.set(xlabel=_text, ylabel=feature + ', #')
    plt.legend()
    # plt.savefig('Entropy50.png', bbox_inches='tight', dpi=1200)
    plt.show()


if __name__ == '__main__':
    # ------ PART 0 - Model with GUI ------
    # test = ForestModel()
    # gui = GUI(test)
    # gui.start()

    # ------ PART I - Calculate different measurements ------
    # test = ForestModel()
    # for i in range(250):
    #     print(i)
    #     test.step()
    # RESULT = test.measurements
    # try:
    #     with open('ResultsMeasure.raw', 'w') as outfile:
    #         json.dump(RESULT, outfile)
    # except:
    #     pass
    # plot_graphs(feature='Dead', data=RESULT)
    # plot_graphs(feature='Border', data=RESULT)

    # ------ PART II - Calculate different features for specific density values ------
    # start = time.time()
    # density = np.linspace(0, 1, 32)
    # # ----MAGIC HERE----
    # # PARALLEL VERSION
    # p = Pool(8)
    # RESULT = p.map(get_density, density)
    # p.close()
    # print(RESULT)
    # end = time.time()
    # print('TOTAL TIME: ', end - start, 's')
    # with open('ResultsDensity.raw', 'w') as outfile:
    #     json.dump(RESULT, outfile)

    # ------ PART III - PLOT Results ------
    with open('ResultsDensity.raw') as data_file:
        data = json.load(data_file)
    #     TODO change size here for comparing with font-size in the Report
    sns.set(font_scale=1.5)
    sns.set_style("whitegrid")
    _to_plot = {'x': [],
                'y': []}
    for denc in data:
        _to_plot['x'].extend([denc[0]] * len(denc[1]))
        _to_plot['y'].extend(denc[1])

    f, ax = plt.subplots(figsize=(12, 8))
    plt.scatter(_to_plot['x'], _to_plot['y'], alpha=0.4, color='red')
    _text = 'Density'
    ax.set(xlabel=_text, ylabel='Burned trees')
    plt.xticks([x for x in np.linspace(0, 1, 11)])
    plt.legend()
    # plt.show()
    plt.savefig('TreeDensity.png', bbox_inches='tight', dpi=1200)
