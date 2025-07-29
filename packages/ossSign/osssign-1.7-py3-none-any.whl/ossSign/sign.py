from datetime import datetime, UTC
import base64
import hmac
import hashlib


# 获取当前日期
def get_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


# 获取当前时间
def get_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 获取当前GMT时间
def get_gmt_time() -> str:
    return datetime.now(UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")

# 拼接callback
def get_callback(oss_callback_url, oss_callback_body) -> str:
    oss_callback_url = oss_callback_url.replace("/", "\\/")
    callback = '{"callbackBodyType":"","callbackHost":"","callbackUrl":"' + oss_callback_url + '","callbackBody":"' + oss_callback_body + '"}'
    return base64.b64encode(callback.encode("utf-8")).decode()


# 计算阿里云OSS上传签名
def get_sign_v1(security_token, secret_access_key, access_key_id, bucket_name, object_path, object_name, date=None, callback=None) -> str:
    date = get_gmt_time() if date is None else date
    content_md5 = ""
    content_type = "application/octet-stream"
    canonicalized_resource = "/" + bucket_name + "/" + object_path + "/" + object_name
    if callback is None:
        sign_data = (
                "PUT"
                + "\n"
                + content_md5
                + "\n"
                + content_type
                + "\n"
                + date
                + "\n"
                + "x-oss-security-token:"
                + security_token
                + "\n"
                + canonicalized_resource
        )
    else:
        sign_data = (
            "PUT"
            + "\n"
            + content_md5
            + "\n"
            + content_type
            + "\n"
            + date
            + "\n"
            + "x-oss-callback:"
            + callback
            + "\n"
            + "x-oss-security-token:"
            + security_token
            + "\n"
            + canonicalized_resource
        )
    h = hmac.new(secret_access_key.encode("utf-8"), sign_data.encode(encoding="utf-8"), hashlib.sha1)
    signature = "OSS " + access_key_id + ":" + base64.b64encode(h.digest()).decode()
    return signature
