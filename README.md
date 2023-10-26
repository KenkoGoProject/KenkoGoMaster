KenkoGo 是一个不跨平台、不可扩展、不高性能的消息调度系统。

KenkoGoMaster 是 KenkoGo 的核心组成部分，它负责调度所有的消息，
正如它的名字 `Master(大师)` 一样，消息流转的全部逻辑在这里完成。

## 功能支持

- [ ] 应用主动注册
- [ ] 模拟对话
- [ ] 应用部署
- [ ] 应用运行器部署
- [ ] 数据统计(发言频率、调用频率、数据库占用、活跃用户数量、文件系统占用)
- [ ] 实时数据(系统类型、内存占用、处理器占用)
- [ ] 本地文件系统管理
- [ ] 消息国际化
- [ ] 消息链路追踪
- [ ] 数据库管理
- [ ] 日志记录

## 快速开始

使用 Docker

```shell
docker pull kenkogo/kenkogo-master:latest
docker run -d --name kenkogo-master -p 17680:17680 kenkogo/kenkogo-master:latest
```

## 从源码构建

### 克隆仓库

```shell
git clone https://github.com/KenkoGoProject/KenkoGoMaster.git
cd KenkoGoMaster
```

### 安装依赖

使用 Python 3.11, 有必要时请使用虚拟环境。

```shell
pip install -r requirements.txt
```

### 运行

```shell
python main.py
```

或者在 Docker 中运行

```shell
docker build -t kenkogo-master .
docker run -t --name kenkogo-master -p 17680:17680 kenkogo-master
```

## 原理解释

### 客户端状态机

客户端在 **Master** 上有若干状态。

#### 已断开

客户端未连接到Master。

#### 已连接，未注册

客户端已经连接到Master，但是还没有注册为应用。

此时客户端可主动执行以下操作：

- 注册：客户端向Master发送注册请求，注册为应用
- 断开连接：客户端主动断开与Master的连接

此时客户端可接收以下消息：

- 注册成功：Master向客户端发送注册成功消息，客户端进入`已注册，暂停调度`状态
- 注册失败：Master向客户端发送注册失败消息，客户端维持`已连接，未注册`状态

#### 已注册，暂停调度

客户端已经注册为应用，但是还没有被调度。

此时客户端可主动执行以下操作：

- 断开连接：客户端主动断开与Master的连接，Master将会将客户端标记为`已断开`状态

此时客户端可接收以下消息：

- 开始调度：Master向客户端发送开始调度消息，客户端进入`已注册，正在调度`状态

#### 已注册，正在调度

客户端已经注册为应用，并且正在被调度。

此时客户端可接收以下消息：

- 暂停调度：Master向客户端发送暂停调度消息，客户端进入`已注册，暂停调度`状态


### 应用常规注册步骤

#### 应用启动

应用启动后，需要向 Master 发起 WebSocket 连接，请求头暂未做要求。
当建立起 WebSocket 连接后，客户端应当持续发送 `ping` 消息，以保持连接。

#### 发送注册请求

在应用未注册时，Master 可能会在预期外断开连接，
所以应用应当在建立 WebSocket 连接后立即发送注册请求。

请求消息内容应当满足以下格式。
在一个 Master 的生命周期内，应用名称允许重复。

```json
{
  "type": "register",
  "data": {
    "name": "应用名称",
    "version": "应用版本",
    "description": "应用描述",
    "author": "应用作者"
  }
}
```

发送一次注册请求后，应用应当等待 Master 的响应，
若多次发送注册请求，Master 将忽略后续的请求。

等待 Master 鉴权通过后，返回应用的唯一标识符。

```json
{
  "type": "register",
  "data": {
    "success": true,
    "id": "应用唯一标识符"
  }
}
```

#### 发送心跳

应用应当在每 30 秒内发送一次心跳消息，以保持连接。

```json
{
  "type": "heartbeat"
}
```

#### 等待消息调度

当应用注册成功后，Master 将会向应用发送消息调度请求。

```json
{
  "type": "message",
  "data": {
    "id": "消息唯一标识符",
    "content": "消息内容"
  }
}
```


## 感谢

- [FastAPI集成Socket.io坑点汇集和技术选型](https://blog.csdn.net/wangsenling/article/details/128568432)
