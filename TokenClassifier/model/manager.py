import os
import shutil
import json
import matplotlib.pyplot as plt
import pandas as pd

RESULT_PATH = 'results'
LOSS_PATH = 'loss'

def read_config(config_path):
    config_file = open(config_path, 'r')
    config = json.load(config_file)
    config_file.close()
    return config

def save_relation_types(relation_types, path):
    path = os.path.join(path, 'relation_types.json')
    with open(path, 'w') as f:
        json.dump(relation_types, f)
        
def get_output_path(config):
    directory = config['save_path']
    name = config['model']
    folders = []
    for item in os.listdir(directory):
        current_path = os.path.join(directory, item)
        if os.path.isdir(current_path):
            try:
                id = int(item.split('_')[0])
                if len(os.listdir(current_path)) == 0:
                    remove_folder(current_path)
                else:
                    folders.append(id)
            except:
                remove_folder(current_path)

    if len(folders) == 0:
        model_path = os.path.join(directory, '0_' + name)
    else:
        folders = sorted(folders)
        last_id = folders[-1]
        model_path = os.path.join(directory, str(last_id + 1) + '_' + name)
    os.makedirs(model_path)
    #os.makedirs(os.path.join(model_path,RESULT_PATH))
    #os.makedirs(os.path.join(model_path,LOSS_PATH))
    return model_path

def remove_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
    except OSError as e:
        print(f"Error: {folder_path} : {e.strerror}")

def update_config(model_path, config_):
    config_path = os.path.join(model_path, 'config.json')
    config = read_config(config_path)
    for k,v in config_.items():
        config[k] = v
    with open(config_path, 'w') as f:
        json.dump(config, f)



def plot_loss(loss, output_path, title):
    if not os.path.exists(os.path.join(output_path, LOSS_PATH)):
        os.makedirs(os.path.join(output_path, LOSS_PATH))
    pd.DataFrame(loss).to_csv(os.path.join(output_path, LOSS_PATH, title + '.csv'))
    plt.figure(figsize=(10, 6))
    for k,v in loss.items():
        plt.plot(v, label=k)
    # Add title and labels
    plt.title('loss over epochs')
    plt.xlabel('Epochs')
    plt.ylabel('loss')
    # Add a legend
    plt.legend()
    # save the plot
    output_path = os.path.join(output_path, LOSS_PATH, title + '.png')
    plt.savefig(output_path)
    plt.close()

def getResultPaths(train_path, prediction_path,  threshold):
    
    prediction_name = prediction_path.split('/')[-1].split('.')[0]
    result_path = os.path.join(train_path, RESULT_PATH, prediction_name +  '_thr_' + str(threshold))
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    prediction_path = os.path.join(result_path, "predictions.json")
    return result_path, prediction_path

def getPredictionPath(result_path, prediction_path):
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    prediction_name = prediction_path.split('/')[-1].split('.')[0]
    prediction_path = os.path.join(result_path, prediction_name + '_predictions.json')
    return prediction_path

def save_predictions(predictions, prediction_path):
    with open(prediction_path, 'w') as f:
        json.dump(predictions, f)

