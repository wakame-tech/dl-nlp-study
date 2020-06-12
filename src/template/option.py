from argparse import ArgumentParser
import datetime
import uuid


def exp_hash() -> str:
    date, hsh = f'{datetime.datetime.now():%m%d}', str(uuid.uuid4())[-6:]
    return f'{date}{hsh}'


def parse_options(root: str):
    """
    学習・デモに必要なオプションを作成

    Parameters
    ----------
    root: str
        プロジェクトのルートパス

    Returns
    -------
    options: object
    """
    parser = ArgumentParser()
    hsh = exp_hash()
    
    print(f'root: {root}, exp hash: {hsh}')
    
    parser.add_argument('--name', type=str, default='chat-bot',
                        help='project name')
    parser.add_argument('--experiment_hash', type=str, default=hsh,
                        help='experiment id')
    parser.add_argument('--dry_run', action='store_true',
                        help='only define models')

    options = parser.parse_args()

    return options