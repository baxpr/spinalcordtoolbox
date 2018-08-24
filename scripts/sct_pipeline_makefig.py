#!/usr/bin/env python
# -*- coding: utf-8
#
# Generate figure from the output of sct_pipeline.
#
# Copyright (c) 2018 Polytechnique Montreal <www.neuro.polymtl.ca>
# Author: Julien Cohen-Adad
# Created: 2018-05-21
# License: https://github.com/neuropoly/spinalcordtoolbox/blob/master/LICENSE

# TODO: generalize this code for other things than Dice

from __future__ import absolute_import

import argparse


def get_parser():
    parser = argparse.ArgumentParser(
        description='Generate figure from the output of sct_pipeline.')
    parser.add_argument("-i", "--input",
                        help="Pickle file(s) generated by sct_pipeline. You can input several files, separated by space.",
                        nargs='+',
                        required=True)
    parser.add_argument("-l", "--label",
                        help="Label name for each pickle data.",
                        nargs='+',
                        required=True)
    parser.add_argument("-v", "--verbose",
                        help="Verbose: 0 = no verbosity, 1 = verbose (default).",
                        choices=('0', '1'),
                        type=int,
                        default=1)
    return parser


def main(args):
    import io
    import sct_utils as sct
    import pickle
    import numpy as np
    import matplotlib.pyplot as plt

    sct.start_stream_logger()

    # make sure number of inputs and labels are the same
    if len(arguments.input) != len(arguments.label):
        raise RuntimeError("Mismatch between # of files and labels")

    # fs = 10  # font size
    nb_plots = args.input.__len__()

    list_data = []
    text_results = []  # numerical results to display inside the figure
    for fname_pickle in args.input:
        df = pickle.load(io.open(fname_pickle, "rb"))
        # filter lines based on status. For status definition, see sct_pipeline
        # Note: the > 0 test is to filter out NaN
        df_dice = df.query("(status != 200) & (status != 201) & (dice > 0 )")["dice"]
        list_data.append(df_dice.get_values())
        # compute statistics
        count_passed = df.status[df.status == 0].count()
        count_failed = df.status[df.status == 99].count()
        count_crashed_run = df.status[df.status == 1].count()
        count_crashed_integrity = df.status[df.status == 2].count()
        count_total = count_passed + count_failed + count_crashed_run + count_crashed_integrity
        text_results.append('\n'.join(["PASS: {}/{}".format(count_passed, count_total),
                                       "FAIL: {}".format(count_failed),
                                       "CRASH_RUN: " + str(count_crashed_run),
                                       "CRASH_INTEGRITY: " + str(count_crashed_integrity)]))

    pos = np.arange(nb_plots)

    # plot fig
    fig, ax = plt.subplots(1)

    plt.violinplot(list_data, pos, points=100, widths=0.8, showmeans=True, showextrema=True, showmedians=True,
                   bw_method=0.5)
    plt.grid(axis='y')
    plt.ylabel('Dice coefficient')
    plt.xticks(pos, args.label)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ylim = ax.get_ylim()
    for i in range(nb_plots):
        plt.text(i + 0.02, ylim[0] + 0.01, text_results[i], horizontalalignment='left', verticalalignment='bottom')
    plt.savefig('violin_plot.png')


if __name__ == '__main__':
    parser = get_parser()
    arguments = parser.parse_args()
    main(arguments)
