def scatter_plot_clones(data, add_pseudo_count=True, savename=None):
    import matplotlib.pyplot as plt
    import numpy as np
    samps = data.columns

    n = len(samps)

    # c_x = np.clip(np.random.randint(-10, 20, size=500), a_min=0, a_max=100) / 1.
    # c_y = np.clip(np.random.randint(-10, 20, size=500), a_min=0, a_max=100) / 1.
    # add_pseudo_count = True
    fig, axs = plt.subplots(nrows=n, ncols=n, figsize=(20, 10), sharex='all', sharey='all')
    for i, samp1 in enumerate(samps):
        for j, samp2 in enumerate(samps):
            if i <= j:
                axs[i, j].axis('off')
            else: #i>j

                D = data[[samp1, samp2]].dropna(how='all').fillna(0)
                #print(D)

                c_x = D[samp2].to_numpy()
                c_y = D[samp1].to_numpy()

                x_norm = np.sum(c_x)
                y_norm = np.sum(c_y)

                M = 2 * sum((c_x / x_norm) * (c_y / y_norm)) / (sum((c_x / x_norm) ** 2) + sum((c_y / y_norm) ** 2))

                # print(samp1)
                # print(c_x)
                # print(samp2)
                # print(c_y)
                # print(M)

                c_x[c_x == 0] = add_pseudo_count / 3.
                c_x = c_x / x_norm
                c_y[c_y == 0] = add_pseudo_count / 3.
                c_y = c_y / y_norm

                sc = axs[i, j].scatter(c_x, c_y, c='k', s=5)
                if add_pseudo_count:
                    axs[i, j].plot([1 / (2 * x_norm), 1 / (2 * x_norm), 1], [1, 1 / (2 * y_norm), 1 / (2 * y_norm)], 'k--', lw=1)

                axs[i, j].set_yscale('log')
                axs[i, j].set_xscale('log')

                axs[i, j].set_yticklabels([])
                axs[i, j].set_xticklabels([])


                plt.text(0.8, 0.8, "{:.2f}".format(M), transform=axs[i, j].transAxes)

                if j == 0:
                    axs[i, j].set_ylabel(samp1)
                if i == n-1:
                    axs[i, j].set_xlabel(samp2)
    plt.tight_layout()
    if savename:
        plt.savefig(savename)
#%% clones stacked plots - function
def draw_clone_bars(data_dict, dict_order=None, ll=0.5, bk_th=0.0008, save_name=None, hatched=False, title=None, create_new = True):
    import seaborn as sns
    import matplotlib.pyplot as plt
    # data_dict is a dict of dict, first level is samples and second is clones, value is fractional size: data_dict[samp1][clone]=0.0001
    # ll is lower limit for y axis (fraction of sequences)
    # bk_th is the threshold for clone size that would be part of black bar
    # save_name is the name of the file to save the plot, None would not save
    # hatched - if True it would use twice the same colors, but hatch them the second time, so you get twice the number of clones colored
    n_large_clones = 12 # how many different clones will be colored
    clrs = sns.color_palette('Paired', n_colors=n_large_clones) #palette for the clones
    if hatched: #if using hatching, add all colors twice
        clrs = clrs[:-1]*2
        n_large_clones *= 2
    clrs = clrs + [(1,1,1)] #add one color more color for non colored clones (white)

    all_large_clones_dict = {} #dict for the largest clones over all samples, values would be fractional size
    for sample in data_dict:
        all_large_clones_dict = {c: max(all_large_clones_dict.get(c,0), data_dict[sample].get(c,0))
                                 for c in set(sorted(data_dict[sample],key=data_dict[sample].get,)[-n_large_clones:]
                                              + list(all_large_clones_dict.keys()))}
    all_large_clones = {c: i for i,c in enumerate(sorted(all_large_clones_dict,key=all_large_clones_dict.get,)[-n_large_clones:])}
    # this dict has the largest clones found, but value now is index of color to be used in clrs list

    if create_new:
        fig = plt.figure(figsize=(20,10))
    if not dict_order:
        dict_order = data_dict.keys()
    for j,samp in enumerate(dict_order):
        b = 0 # bottom of current bar
        t = 0 # top of current bar
        for c in sorted(data_dict[samp], key=data_dict[samp].get,): #loop over all clones in sample from small to large
            if b == 0 and data_dict[samp].get(c,0) < bk_th: #as long as clones are smaller than threshold
                t += data_dict[samp].get(c,0) #add them together to top
            else:
                if b == 0:
                    plt.bar(j, t, color = 'black', edgecolor='black') # use one black bar for all clones below threshold
                    b = t #advance bottom to where top was
                color_index = all_large_clones.get(c, n_large_clones) # get correct color for next clone
                plt.bar(j, data_dict[samp].get(c, 0), bottom=b, color=clrs[color_index],
                        edgecolor='black', hatch='x' if hatched and n_large_clones / 2 <= color_index < n_large_clones else '')
                b += data_dict[samp].get(c,0)
    samp_labels = ['\n'.join(str(x).split('_')) for x in dict_order]
    plt.xticks(range(len(samp_labels)), samp_labels, rotation=0)
    plt.ylabel('fraction of all sequences')
    plt.ylim([ll,1])
    if title:
        plt.title(title)
    if save_name:
        plt.savefig(save_name)
    #plt.show()


#%%
