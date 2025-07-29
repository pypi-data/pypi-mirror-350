# predictionball

<a href="https://pypi.org/project/predictionball/">
    <img alt="PyPi" src="https://img.shields.io/pypi/v/predictionball">
</a>

A library for pulling in and normalising prediction market data.

## Dependencies :globe_with_meridians:

Python 3.11.6:

- [pandas](https://pandas.pydata.org/)
- [py-clob-client](https://github.com/Polymarket/py-clob-client)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [pydantic](https://docs.pydantic.dev/latest/)
- [requests](https://requests.readthedocs.io/en/latest/)
- [pyarrow](https://arrow.apache.org/docs/python/index.html)
- [sentence_transformers](https://sbert.net/)
- [scikit-learn](https://scikit-learn.org/)

## Raison D'être :thought_balloon:

`predictionball` aims to be a library that pulls in both historical and live prediction market data. It currently handles the following markets:

- [Polymarket](https://polymarket.com/)
- [Kalshi](https://kalshi.com/)
- [PredictIt](https://www.predictit.org/)

## Architecture :triangular_ruler:

`predictionball` is a functional library that does the following steps:

1. Pulls down different prediction markets.
2. Cluster the markets by event type.

## Installation :inbox_tray:

This is a python package hosted on pypi, so to install simply run the following command:

`pip install predictionball`

or install using this local repository:

`python setup.py install --old-and-unmanageable`

## Usage example :eyes:

The only way to access the data from `predictionball` is to use it as a python library.

### Python

To pull the models containing all the information, the following example can be used:

```python
from predictionball.pull import pull

models = pull()
```

This results in a dataframe where each game is represented by all its features.

## License :memo:

The project is available under the [MIT License](LICENSE).
