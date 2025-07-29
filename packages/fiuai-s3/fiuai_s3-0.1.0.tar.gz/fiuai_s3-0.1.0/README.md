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
from fiuai_s3 import ObjectStorageFactory

# 初始化MinIO存储
ObjectStorageFactory.initialize(
    provider="minio",
    bucket_name="dev",
    endpoint="http://127.0.0.1:19000",
    access_key="devdevdev",
    secret_key="devdevdev",
    temp_dir="temp/",
    use_https=False
)

# 或者初始化阿里云OSS存储
ObjectStorageFactory.initialize(
    provider="alicloud",
    bucket_name="your-bucket",
    endpoint="oss-cn-hangzhou.aliyuncs.com",
    access_key="your-access-key",
    secret_key="your-secret-key",
    temp_dir="temp/",
    use_https=True
)
```

### 使用存储实例

```python
# 获取存储实例
storage = ObjectStorageFactory.get_instance()

# 上传文件
storage.upload_file("test.txt", b"Hello World")

# 下载文件
data = storage.download_file("test.txt")

# 删除文件
storage.delete_file("test.txt")

# 列出文件
files = storage.list_files(prefix="test/")
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
pip install -r requirements.txt
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