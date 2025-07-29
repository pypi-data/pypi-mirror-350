# FiuAI S3

一个支持阿里云OSS和MinIO的对象存储抽象包，提供了统一的接口来操作不同的对象存储服务。

## 特性

- 支持阿里云OSS和MinIO存储服务
- 统一的接口设计
- 工厂模式实现，易于扩展
- 完整的类型提示
- 详细的日志记录
- 异常处理机制

## 安装

```bash
pip install fiuai-s3
```

## 快速开始

### 初始化存储

```python
# file: utils/s3.py
from fiuai_s3 import ObjectStorageFactory
from config.app_config import get_settings

ObjectStorageFactory.initialize(
        # 初始化对象存储
        provider=get_settings().object_storage_config.provider,
        bucket_name=get_settings().object_storage_config.bucket_name,
        endpoint=get_settings().object_storage_config.endpoint,
        access_key=get_settings().object_storage_config.access_key,
        secret_key=get_settings().object_storage_config.secret_key,
        temp_dir=get_settings().object_storage_config.s3_temp_dir,
        use_https=get_settings().object_storage_config.s3_use_https
    
)
S3_Client = ObjectStorageFactory.get_instance()

```


### 使用存储实例

```python
# file: app.py
from utils.s3 import S3_Client

# 上传文件
S3_Client.upload_file("test.txt", b"Hello World")

# 下载文件
data = S3_Client.download_file("test.txt")

# 删除文件
S3_Client.delete_file("test.txt")

# 列出文件
files = S3_Client.list_files(prefix="test/")
```

## 配置参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| provider | str | 是 | - | 存储提供商，支持 "alicloud" 或 "minio" |
| bucket_name | str | 是 | - | 存储桶名称 |
| endpoint | str | 是 | - | 存储服务端点 |
| access_key | str | 是 | - | 访问密钥 |
| secret_key | str | 是 | - | 密钥 |
| temp_dir | str | 否 | "temp/" | 临时目录 |
| use_https | bool | 否 | False | 是否使用HTTPS |

## 开发

### 安装开发依赖

```bash
uv pip install .
```

### 运行测试

```bash
python -m pytest tests/
```

## 许可证

MIT License

## 作者

- liming (lmlala@aliyun.com)

## 贡献

欢迎提交 Issue 和 Pull Request！