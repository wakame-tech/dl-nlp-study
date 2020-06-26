# dl-nlp-study
個人的な機械学習の知見、Tipsをまとめる

## 📚 contents
- mercari  
  [mercari-price-suggestion](https://www.kaggle.com/c/mercari-price-suggestion-challenge/overview)
- vtuber  
  doc2vec
- template  
  スニペット・テンプレート集

## 🔥 todo
- jupyter notebook
- streamlit
- bert(transformers)
- gpt2(transformers)
- [x] tensorboardx
- [x] pytorch-ignite template
- [x] japanese preprocessing
- VAE
- optuna
- [x] yml config
- kubeflow pipelines
- julia ml

## ⚙ 管理
### パス
大体こんなかんじ
```
/
  - dataset # データセット
  - src # ソースコード
  - logs # ログなど
```

ルートパスは環境変数にしてそこからの相対パス

### スクリプト
`Rakefile` で管理
```ruby
task :train do |t|
  sh 'ROOT=`pwd` python src/train.py'
end
```

学習は `rake train` で

### データセット
GoogleDriveとかに置いてスクリプトでダウンロードできるように

```sh
curl gdrive.sh | bash -s <FILE_ID>
```

でGoogleDrive上のファイルをダウンロードできる

### パラメータ
[Hydra](https://hydra.cc/) を使ってymlで管理.

```yml
# config.yml
train:
  dataset_path: ${env:ROOT}/dataset/xxx.pkl
  epoch: 100
```

取得は
```python
import hydra
from omegaconf import DictConfig

@hydra.main(config_path='config.yml')
def preprocess(cfg : DictConfig):
    print(cfg.pretty())
```

## 📈 学習
(WIP)

## 💻 デプロイ
(WIP)