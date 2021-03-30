# Vefui
> Vue Element-UI Form
> A small exe package plan.

## required

+ chrome **For WEB View**
+ python3.7+

## Used

1. clone this repository
2. create a new python venv py3.7+
3. write you package and package

## Component
> Form Component

- [x] input
    - [x] range
- [x] textarea
- [x] file upload
- [x] select
    - [x] single
    - [x] multi
- [x] date 
- [x] datetime
- [x] slider
- [x] switch


## Build exe package
> package with pyinstaller
```shell script
# python -m vefui <app_dir> <web_dir>
python -m vefui example\hello.py vefui\dist
```