from forest_model import *
import json
import seaborn as sns


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
    # test = ForestModel()
    # gui = GUI(test)
    # gui.start()
    test = ForestModel()
    for i in range(200):
        print(i)
        test.step()
    RESULT = test.measurements
    try:
        with open('ResultsMeasure.raw', 'w') as outfile:
            json.dump(RESULT, outfile)
    except:
        pass
    plot_graphs(feature='Dead', data=RESULT)
    plot_graphs(feature='Border', data=RESULT)
