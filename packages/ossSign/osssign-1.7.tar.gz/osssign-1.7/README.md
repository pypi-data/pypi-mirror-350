# 计算阿里云OSS文件上传签名

## 用法
> 说明：获取回调
>
> 方法：ossSign.GetCallback
>
> 入参：
> 
>> callback_url：回调地址
>> 
>> oss_callback_body：回调内容
> 
> 说明：计算签名
> 
> 方法：ossSign.GetSignV1
>
>> security_token：security_token
>> 
>> secret_access_key：secret_access_key
>> 
>> access_key_id：access_key_id
>> 
>> bucket_name：桶名称 
>>
>> object_path：文件对象路径
>>
>> object_name：文件对象名
>>
>> date：GMT时间，默认使用当前时间
>> 
>> callback：回调信息，默认不回调

## 打包
```shell
python setup.py sdist bdist_wheel
```

## 上传
### 安装依赖工具
```shell
pip install twine
```
### 上传到pypi（需要提前准备好账号）
```shell
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```