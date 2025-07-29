hw-oa 
# 项目文档

## 本地运行项目
uvicorn hw_oa_server.main:app --reload
## 安装twine
uv pip install twine
## 发布项目
创建 ~/.pypirc，内容如下
```
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = **** #这个在pypi网站上获取个人的token
```
uv build # 构建，完成后会生成目录 dist，下面放着压缩包
cd /d/workspace/mcp/hwoa_mcp_server/hw_oa #项目所在路径
export PYTHONIOENCODING=utf-8  # 设置 Python 输出编码
twine upload dist/* # 配置 ～/.pypirc后不需要手动输入密码
## 测试
更新 pip install --upgrade  hw-oa
本地运行  uv run hw-oa
如果没问题说明发布成功
[uvicorn参考文档](https://www.uvicorn.org/deployment/)

## 项目描述
- 由cicd工具生成模板
