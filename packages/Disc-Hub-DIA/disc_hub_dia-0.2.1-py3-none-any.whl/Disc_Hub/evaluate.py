import numpy as np
import matplotlib.pyplot as plt

def calculate_fdr(df, col_score):
    # FDR calculation based on decoy
    df_sorted = df.sort_values(by=col_score, ascending=False, ignore_index=True)
    target_num = (df_sorted.decoy == 0).cumsum()
    decoy_num = (df_sorted.decoy == 1).cumsum()
    target_num[target_num == 0] = 1
    df_sorted['q_pr'] = decoy_num / target_num
    df_sorted['q_pr'] = df_sorted['q_pr'][::-1].cummin()
    ids_report_fdr = sum((df_sorted.q_pr < 0.01) & (df_sorted.decoy == 0))
    print(f'Ids at report 1% FDR ({col_score}): {ids_report_fdr}')

    # Determine species
    df_sorted = df_sorted[~df_sorted['protein_names'].isna()].copy()
    df_sorted['species'] = 'HUMAN'
    df_sorted.loc[df_sorted['protein_names'].str.contains('ARATH'), 'species'] = 'ARATH'
    df_sorted.loc[df_sorted['protein_names'].str.contains('HUMAN'), 'species'] = 'HUMAN'

    # FDR calculation based on plants
    df_sorted = df_sorted[df_sorted['decoy'] == 0].reset_index(drop=True)
    df_sorted = df_sorted.sort_values(by=col_score, ascending=False, ignore_index=True)
    target_num = (df_sorted.species == 'HUMAN').cumsum()
    decoy_num = (df_sorted.species == 'ARATH').cumsum()
    target_num[target_num == 0] = 1
    df_sorted['q_pr_external'] = decoy_num / target_num
    df_sorted['q_pr_external'] = df_sorted['q_pr_external'][::-1].cummin()
    ids_external_fdr = sum((df_sorted.q_pr_external < 0.01) & (df_sorted.decoy == 0))
    print(f'Ids at external 1% FDR ({col_score}): {ids_external_fdr}')

    # Calculate plot data
    #fdr_v = np.arange(0.0005, 0.05, 0.001)
    fdr_v = np.arange(0.0005, 0.05, 0.001)
    external_fdr_v_left, external_fdr_v_right = [], []
    report_fdr_v = []
    id_num_v = []
    for fdr in fdr_v:
        # Relation between report_fdr and external_fdr
        report_fdr_v.append(fdr)
        df_temp = df_sorted[df_sorted['q_pr'] < fdr]
        external_fdr_v_right.append(df_temp['q_pr_external'].max())

        # Relation between external_fdr and identified number
        external_fdr_v_left.append(fdr)
        df_temp = df_sorted[(df_sorted['q_pr_external'] < fdr) & (df_sorted.decoy == 0)]
        id_num_v.append(df_temp['pr_id'].nunique())

    external_fdr_v_left = np.array(external_fdr_v_left)
    external_fdr_v_right = np.array(external_fdr_v_right)
    id_num_v = np.array(id_num_v)

    return external_fdr_v_left, external_fdr_v_right, report_fdr_v, id_num_v, ids_report_fdr, ids_external_fdr


def plot_ids_and_fdr(df, col_score1, col_score2, save_path):
    # Calculate FDR data for predicted_prob
    external_fdr_v_left1, external_fdr_v_right1, report_fdr_v1, id_num_v1, ids_report_fdr1, ids_external_fdr1 = calculate_fdr(
        df, col_score1)

    # Calculate FDR data for cscore_pr_run
    external_fdr_v_left2, external_fdr_v_right2, report_fdr_v2, id_num_v2, ids_report_fdr2, ids_external_fdr2 = calculate_fdr(
        df, col_score2)

    # Plot the data
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax2.plot(np.linspace(0, 0.05, 100), np.linspace(0, 0.05, 100), linestyle='--', color='grey')

    # Plot curves for predicted_prob (blue)
    ax2.plot(external_fdr_v_right1, report_fdr_v1, label=col_score1, color='blue')
    ax1.plot(external_fdr_v_left1, id_num_v1, label=col_score1, color='blue', linewidth=3)

    # Plot curves for cscore_pr_run (red)
    ax2.plot(external_fdr_v_right2, report_fdr_v2, label=col_score2, color='red')
    ax1.plot(external_fdr_v_left2, id_num_v2, label=col_score2, color='red', linewidth=3)

    # Set axis labels and styles
    ax1.set_xlabel('External  FDR', fontsize=22)
    ax1.set_ylabel('#Precursors', color='black', fontsize=20)
    ax2.set_ylabel('Report  FDR', color='red', fontsize=20)
    ax1.tick_params(axis='y', labelcolor='black', labelsize=15)
    ax2.tick_params(axis='y', labelcolor='red', labelsize=15)

    # Display legend
    plt.legend(fontsize=15,  loc='best')

    # Add text annotation in the bottom-right corner
    text = (
        f'Ids at report 1% FDR ({col_score1}): {ids_report_fdr1}\n'
        f'Ids at external 1% FDR ({col_score1}): {ids_external_fdr1}\n'
        f'Ids at report 1% FDR ({col_score2}): {ids_report_fdr2}\n'
        f'Ids at external 1% FDR ({col_score2}): {ids_external_fdr2}'
    )
    plt.text(0.95, 0.05, text, transform=ax1.transAxes, fontsize=10, verticalalignment='bottom',
             horizontalalignment='right', bbox=dict(facecolor='white', alpha=0.8))

    # Save the plot
    if save_path:
        plt.savefig(save_path, dpi=300,  bbox_inches='tight') #bbox_extra_artists=(legend,),
        print(f"Plot saved as {save_path}")
    plt.show()