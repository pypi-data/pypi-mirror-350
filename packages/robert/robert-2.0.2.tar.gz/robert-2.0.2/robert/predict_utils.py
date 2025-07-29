#####################################################.
#     This file stores functions from PREDICT       #
#####################################################.

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from robert.utils import (
    categorical_transform,
    get_graph_style,
    pearson_map,
    graph_reg,
    graph_clas,
    )


def test_csv(self,Xy_test_df,descs_model,params_df):
    """
    Separates the test databases into X and y. This allows to merge test external databases that 
    contain different columns with internal test databases coming from GENERATE
    """

    y_test_df = pd.DataFrame()
    
    try:
        X_test_df = Xy_test_df[descs_model]
    except KeyError:
        # this might fail if the initial categorical variables have not been transformed
        try:
            self.args.log.write(f"\n   x  There are missing descriptors in the test set! Looking for categorical variables converted from CURATE")
            Xy_test_df = categorical_transform(self,Xy_test_df,'predict')
            X_test_df = Xy_test_df[descs_model]
            self.args.log.write(f"   o  The missing descriptors were successfully created")
        except KeyError:
            self.args.log.write(f"   x  There are still missing descriptors in the test set! The following descriptors are needed: {descs_model}")
            self.args.log.finalize()
            sys.exit()

    if params_df['y'][0] in Xy_test_df:
        y_test_df = Xy_test_df[params_df['y'][0]]

    return X_test_df, y_test_df


def plot_predictions(self, params_dict, Xy_data, path_n_suffix):
    '''
    Plot graphs of predicted vs actual values for train, validation and test sets
    '''

    set_types = [f"{params_dict['repeat_kfolds']}x {params_dict['kfold']}-fold CV",'test']
    
    graph_style = get_graph_style()
    
    self.args.log.write(f"\n   o  Saving graphs in:")

    if params_dict['type'].lower() == 'reg':
        # Plot graph with all sets
        _ = graph_reg(self,Xy_data,params_dict,set_types,path_n_suffix,graph_style)
        # Plot CV average ± SD graph of validation or test set
        _ = graph_reg(self,Xy_data,params_dict,set_types,path_n_suffix,graph_style,sd_graph=True)
        if 'y_external' in Xy_data and not Xy_data['y_external'].isnull().values.any() and len(Xy_data['y_external']) > 0:
            # Plot CV average ± SD graph of external set
            set_type = 'external'
            _ = graph_reg(self,Xy_data,params_dict,set_type,path_n_suffix,graph_style,csv_test=True,sd_graph=True)

    elif params_dict['type'].lower() == 'clas':
        for set_type in set_types:
            _ = graph_clas(self,Xy_data,params_dict,set_type,path_n_suffix)
        if 'y_external' in Xy_data and not Xy_data['y_external'].isnull().values.any() and len(Xy_data['y_external']) > 0:
            set_type = 'external'
            _ = graph_clas(self,Xy_data,params_dict,set_type,path_n_suffix,csv_test=True)

    return graph_style


def save_predictions(self,Xy_data,model_data,suffix_title):
    '''
    Saves CSV files with the different sets and their predicted results
    '''

    # save CV and test results as a single df
    Xy_train, Xy_test = pd.DataFrame(Xy_data['names_train']), pd.DataFrame(Xy_data['names_test'])
    for col in Xy_data['X_train']:
        Xy_train[col] = Xy_data['X_train'][col].tolist()
        Xy_test[col] = Xy_data['X_test'][col].tolist()
    Xy_train[model_data['y']] = Xy_data['y_train'].tolist()
    Xy_train[f"{model_data['y']}_pred"] = Xy_data['y_pred_train']
    Xy_train[f"{model_data['y']}_pred_sd"] = Xy_data['y_pred_train_sd']

    Xy_test[model_data['y']] = Xy_data['y_test'].tolist()
    Xy_test[f"{model_data['y']}_pred"] = Xy_data['y_pred_test']
    Xy_test[f"{model_data['y']}_pred_sd"] = Xy_data['y_pred_test_sd']

    df_results = pd.concat([Xy_train, Xy_test], axis=0)

    # add column with sets
    train_list = ['CV' for _ in Xy_data['y_train']]
    test_list = ['Test' for _ in Xy_data['y_test']]
    col_set = train_list + test_list
    df_results['Set'] = col_set

    # save results as CSV
    base_csv_name = f"PREDICT/{model_data['model']}_{suffix_title}"
    base_csv_path = f"{Path(os.getcwd()).joinpath(base_csv_name)}"
    path_n_suffix = f'{base_csv_path}'
    _ = df_results.to_csv(f'{base_csv_path}.csv', index = None, header=True)

    # prints
    print_preds = f'   o  Saving CSV databases with predictions and their SD in:'   
    print_preds += f'\n      -  Predicted results of starting dataset: {base_csv_name}.csv'

    if self.args.csv_test != '':            
        # saves prediction for external test in --csv_test
        Xy_external = pd.DataFrame(Xy_data['names_external'])

        for col in Xy_data['X_external']:
            Xy_external[col] = Xy_data['X_external'][col].tolist()
            Xy_external[col] = Xy_data['X_external'][col].tolist()

        if 'y_external' in Xy_data:
            Xy_external[model_data['y']] = Xy_data['y_external'].tolist()
        Xy_external[f"{model_data['y']}_pred"] = Xy_data['y_pred_external']
        Xy_external[f"{model_data['y']}_pred_sd"] = Xy_data['y_pred_external_sd']

        path_external = Path(os.getcwd()).joinpath('PREDICT/csv_test/')
        Path(path_external).mkdir(exist_ok=True, parents=True)
        csv_name_external = f'{os.path.basename(self.args.csv_test).split(".csv")[0]}_{model_data["model"]}_{suffix_title}.csv'
        name_external = f"{path_external}/{csv_name_external}"

        _ = Xy_external.to_csv(name_external, index = None, header=True)
        print_preds += f'\n      -  External set with predicted results: PREDICT/csv_test/{csv_name_external}'

    self.args.log.write(print_preds)

    # store the names of the datapoints
    name_points = {}
    if model_data['names'] != '':
        if model_data['names'].lower() in Xy_train: # accounts for upper/lowercase mismatches
            model_data['names'] = model_data['names'].lower()
        if model_data['names'].upper() in Xy_train:
            model_data['names'] = model_data['names'].upper()
        if model_data['names'] in Xy_train:
            name_points['train'] = df_results[model_data['names']][df_results.Set == 'CV']
            name_points['test'] = df_results[model_data['names']][df_results.Set == 'Test']

    return path_n_suffix, name_points, Xy_data


def print_predict(self,Xy_data,model_data,suffix_title):
    '''
    Prints results of the predictions for all the sets
    '''
    
    print_results = f"\n   o  Summary of results {model_data['model']}_{suffix_title}:"
    set_print = 'CV (train+valid.):Test'

    # get number of points and proportions
    n_train = len(Xy_data['y_train'])
    n_test = len(Xy_data['y_test'])
    n_points = f'{n_train}:{n_test}'
    print_results += f"\n      -  Points {set_print} = {n_points}"

    total_points = n_train + n_test
    prop_train = round(n_train*100/total_points)
    prop_test = round(n_test*100/total_points)
    prop_print = f'{prop_train}:{prop_test}'
    print_results += f"\n      -  Proportion {set_print} = {prop_print}"
    
    n_descps = len(Xy_data['X_train'].keys())
    print_results += f"\n      -  Number of descriptors = {n_descps}"
    print_results += f"\n      -  Proportion (train+valid.) points:descriptors = {n_train}:{n_descps}"

    # print results and save dat file
    CV_type = f"{model_data['repeat_kfolds']}x {model_data['kfold']}-fold CV"
    if model_data['type'].lower() == 'reg':
        print_results += f"\n      -  {CV_type} : R2 = {Xy_data['r2_train']:.2}, MAE = {Xy_data['mae_train']:.2}, RMSE = {Xy_data['rmse_train']:.2}"
        print_results += f"\n      -  Test : R2 = {Xy_data['r2_test']:.2}, MAE = {Xy_data['mae_test']:.2}, RMSE = {Xy_data['rmse_test']:.2}"
        print_results += f"\n      -  Average SD in test set = {np.mean(Xy_data['y_pred_test_sd']):.2}"
        print_results += f"\n      -  y range of dataset (train+valid.) = {float(Xy_data['pred_min']):.2} to {float(Xy_data['pred_max']):.2}, total {float(Xy_data['pred_range']):.2}"
        if 'y_external' in Xy_data and not Xy_data['y_external'].isnull().values.any() and len(Xy_data['y_external']) > 0:
            print_results += f"\n      -  External test : R2 = {Xy_data['r2_external']:.2}, MAE = {Xy_data['mae_external']:.2}, RMSE = {Xy_data['rmse_external']:.2}"

    elif model_data['type'].lower() == 'clas':
        print_results += f"\n      -  {CV_type} : Accur. = {Xy_data['acc_train']:.2}, F1 score = {Xy_data['f1_train']:.2}, MCC = {Xy_data['mcc_train']:.2}"
        if 'y_pred_test' in Xy_data and not Xy_data['y_test'].isnull().values.any() and len(Xy_data['y_test']) > 0:
            print_results += f"\n      -  Test : Accur. = {Xy_data['acc_test']:.2}, F1 score = {Xy_data['f1_test']:.2}, MCC = {Xy_data['mcc_test']:.2}"
        if 'y_external' in Xy_data and not Xy_data['y_external'].isnull().values.any() and len(Xy_data['y_external']) > 0:
            print_results += f"\n      -  External test : Accur. = {Xy_data['acc_external']:.2}, F1 score = {Xy_data['f1_external']:.2}, MCC = {Xy_data['mcc_external']:.2}"

    self.args.log.write(print_results)


def pearson_map_predict(self,Xy_data,params_dir):
    '''
    Plots the Pearson map and analyzes correlation of descriptors.
    '''

    corr_matrix = pearson_map(self,Xy_data['X_train'],'predict',params_dir=params_dir)

    corr_dict = {'descp_1': [],
                 'descp_2': [],
                 'r': []
    }
    for i,descp in enumerate(corr_matrix.columns):
        for j,val in enumerate(corr_matrix[descp]):
            if i < j and np.abs(val) > 0.8:
                corr_dict['descp_1'].append(corr_matrix.columns[i])
                corr_dict['descp_2'].append(corr_matrix.columns[j])
                corr_dict['r'].append(val)

    print_corr = f'      Ideally, variables should show low correlations.' # no initial \n, it's a new log.write
    if len(corr_dict['descp_1']) == 0:
        print_corr += f"\n      o  Correlations between variables are acceptable"
    else:
        abs_r_list = list(np.abs(corr_dict['r']))
        abs_max_r = max(abs_r_list)
        max_r = corr_dict['r'][abs_r_list.index(abs_max_r)]
        max_descp_1 = corr_dict['descp_1'][abs_r_list.index(abs_max_r)]
        max_descp_2 = corr_dict['descp_2'][abs_r_list.index(abs_max_r)]
        if abs_max_r > 0.84:
            print_corr += f"\n      x  WARNING! High correlations observed (up to r = {max_r:.2} or R2 = {max_r*max_r:.2}, for {max_descp_1} and {max_descp_2})"
        elif abs_max_r > 0.71:
            print_corr += f"\n      x  WARNING! Noticeable correlations observed (up to r = {max_r:.2} or R2 = {max_r*max_r:.2}, for {max_descp_1} and {max_descp_2})"

    self.args.log.write(print_corr)
