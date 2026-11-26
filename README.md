# hdmea-organoid-pipeline
From raw MaxWell HD-MEA recordings to network analysis: spike sorting, firing, bursts and synchrony in developing human brain organoids

## Data

Raw data is **not** stored in this repo (see `.gitignore`). Download it into `data/raw/`.

| File | Source | Size | Use |
|---|---|---|---|
| `maxone_record_000011.raw.h5` | GIN `NeuralEnsemble/ephy_testing_data`, path `maxwell/MaxOne_data/Record/000011/data.raw.h5` | 18 MB | Test file for loading + spike sorting |

Download:
    curl -L -o data/raw/maxone_record_000011.raw.h5 https://gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/master/maxwell/MaxOne_data/Record/000011/data.raw.h5
