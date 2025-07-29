### Thirteen GPU Scheduler

# Dashboard
<img width="1159" alt="image" src="https://user-images.githubusercontent.com/11758953/218321610-fc18957e-c6a7-4d26-8cb0-5b0017b54135.png">

![image](https://user-images.githubusercontent.com/11758953/218321614-a5c408cf-de15-41fe-a2fc-e314444d252d.png)

[http://54.180.160.135:2013/](http://54.180.160.135:2013/)

# Installation
```
pip install thirteen_gpu
```

### Job Submit


```
$ submit --user [USERNAME] --project [PROJECT_NAME] --path /path/to/project
```

예를 들어,
```
$ submit --user seilna --project my_project_test1 --path ~/Desktop/neural-quant
```

* `--project` 값은 기존 project name 과 겹치는 이름을 사용할 수 없다.
* `--path` 로 준 경로의 `config/runs/XXXX.json` 형태로 파일이 존재해야 함 (`config/generate_configs.py`) 를 통해 생성하면 된다.
* `submit` command 최초 1회 실행 시, 스케줄러 서버 접속 인증을 위해 비밀번호를 입력해야 한다. 비밀번호는 `thirteen123!` 이다.


### Job Delete
```
$ delete --user seilna --project [PROJECT_NAME]
```

