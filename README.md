# Test online store for Taproot Assets Protocol on Bitcoin Testnet Blockchain

An implementation of online store that accepts Taproot Assets powered by [Tiramisu wallet](https://testnet.tarowallet.net/) API,

This online store [is currently deployed here](https://tapd-store.tarowallet.net) 

## Installation and execution

```
pip install requirements.txt

gunicorn --bind 0.0.0.0:5000 app:app
```