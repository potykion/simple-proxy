# simple-proxy

Service for bypass denied resources like this

![err](./err.png)

## Usage

```
http://127.0.0.1:8000/?url={URL}&key={KEY}
```

## Dev 

### Install

```
poetry install
```

### Create .env

```
KEY=1488
```

### Run

```
uvicorn main:app --reload
```

### Use

```
http://127.0.0.1:8000/?url=http://bugs.python.org/&key=1488
```

### In case of new dependencies 

```
poetry export -f requirements.txt > requirements.txt --without-hashes
```