import argparse
from model.finetuning import TokenClassifier
from model.manager import read_config, get_output_path

def train(config_path):
    config = read_config(config_path=config_path)
    config['save_path'] = get_output_path(config=config)
    tokenClassifier = TokenClassifier(config=config, mode='train')
    tokenClassifier.load_data()
    tokenClassifier.load_model()
    tokenClassifier.train()

def eval(config_path):
    config = read_config(config_path=config_path)
    tokenClassifier = TokenClassifier(config=config, mode='eval')
    tokenClassifier.load_data()
    tokenClassifier.load_model()
    tokenClassifier.eval()

def predict(config_path):
    config = read_config(config_path=config_path)
    tokenClassifier = TokenClassifier(config=config, mode='predict')
    tokenClassifier.load_data()
    tokenClassifier.load_model()
    tokenClassifier.predict()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train a model with the specified config file.")

    # Add an argument for the config file path
    parser.add_argument('--train', type=str, help='Path to the training config file')
    parser.add_argument('--eval', type=str, help='Path to the evaluation config file')
    parser.add_argument('--predict', type=str, help='Path to the prediction config file')

    # Parse the arguments
    args = parser.parse_args()
    #read the config file
   
    if args.train:
        train(args.train)
    elif args.eval:
        eval(args.eval)
    elif args.predict:
        predict(args.predict)
   