# COVID-19 reporter

Simple project that requests and webscrapes website then sends email when new content is released.

#### Requirements

[Use a virtualenv to create an isolated enviorment](https://virtualenv.pypa.io/en/latest/)

Run the make command to install requirements

```
make
```

or with pip manually

```
pip3 install -r requirements.txt
```

## Running the program

Run description

```
make run
```

or with python manually

```
python3 run.py
```

## Authors

* [**Rafael Cenzano**](https://github.com/RafaelCenzano)

## License

This project's license here: [LICENSE](LICENSE)


This Readme was created with [pystarter](https://github.com/RafaelCenzano/PyStarter)

```
pip3 install pystarter
```

## Example Email:

```
Hello,

Update: 3/9/20 10:53 AM

CDC Updated March 9, 2020

Total cases: 423
157.9268292682927% increase in cases in U.S.

Total deaths: 19
72.72727272727273% increase in deaths in U.S.

States reporting cases: 35 (includes District of Columbia)
84.21052631578947% increase in states with cases in U.S.

- COVID-19 Reporter
                         
```