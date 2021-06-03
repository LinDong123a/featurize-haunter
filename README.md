# FeaturizeHaunter: featurize.cn实例抢占脚本

[featurize.cn](https://featurize.cn)是一个GPU服务器租赁平台，该平台的GPU租赁价格是比较实惠的，提供的服务使用体验也比较好，唯一的缺点就是服务器的数量实在是不多，每次要用到的时候都抢不到，头疼之下写了该工具，用于该平台下服务器的自动租赁。

## 特点

* 多GPU同时抢占，并提供优先级
* 同时抢占多台机器 

## 安装方式

```shell
pip install 
```

## 使用说明

### Token获取

该工具使用了[featurize.cn](https://featurize.cn)提供的[featurize](https://pypi.org/project/featurize/)进行实例的查询与租用，使用该工具需要先生成开发者token，生成方式可前往[featurize的设置界面](https://featurize.cn/dashboard/settings)后，点击【开发者】->【生成/重置令牌即可】

### 同时指定多GPU进行抢占

当我们要同时抢占2080Ti和3090时，我们先通过[featurize.cn](https://featurize.cn)的实例列表确定平台上的GPU名称，比如平台上2080Ti的全称为GeForce RTX 2080 Ti，3090的全称为GeForce RTX 3090，于是对应的命令行为：

```shell
featurize-haunter --token {token} --gpus "GeForce RTX 2080 Ti,GeForce RTX 3090"
```

上述命令中，{token}为在【Token获取】部分获得的token，在进行租赁时，当同时发现2080 Ti和3090的实例时，会优先租用3090，默认租赁1个实例

### 同时指定多GPU多机器

```shell
featurize-haunter --token {token} --gpus "GeForce RTX 2080 Ti,GeForce RTX 3090" -n 5
```

上述命令会在成功租赁到5个实例后停止。

### 消息提示

为了在租赁完成或者出错时有方式提示，还提供了音频通知

```shell
featurize-haunter --token {token} --gpus "GeForce RTX 2080 Ti,GeForce RTX 3090" -n 5 --notification music
```

上述命令将会在成功租赁一个实例或者出错时播放不同的音效。


> 在macos下，如果执行时报没有AppKit的错，则执行`pip install PyObjC`

## TODO

* [] 增加email提醒机制 
* [] 引入多线程，实现更高效的并发
