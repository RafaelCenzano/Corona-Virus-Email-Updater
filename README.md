# COVID-19 reporter

Simple project that requests and webscrapes website then sends email when new content is released.

CDC stopped updating the page

#### Requirements

create a secret.py with these variables:

```
import os

senderEmail = 'youremail@gmail.com' # has to be gmail
senderPassword = 'you app password'
recieverEmails = ['contact@domain.com', 'other@domain.com']
jsonFilePath = '/' + os.path.join('Users','jimdoe','Documents','Corona-Virus-Email-Updater','past.json')
```

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
