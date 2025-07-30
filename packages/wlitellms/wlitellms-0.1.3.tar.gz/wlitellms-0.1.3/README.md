# wlitellms

Fork from langmanus's llms

## 编译

- 环境配置

```
conda create -n wlitellms python=3.12
conda activate wlitellms
```

- 安装依赖

```
pip install -e .
```

- 执行编译

```
python setup.py sdist bdist_wheel
```

- 发布

```
twine upload dist/*
```
