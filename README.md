# PMAblast

1、安装依赖库

```bash
pip3 install requests,argparse,threadpool
```

2、使用说明

```bash
python PMAblast.py -u "http://192.168.101.233/phpmyadmin/" -l root -P pass.txt
```

![image-20201229144853002](/images/image-20201229144853002.png)

多线程爆破,默认为10线程

```
python PMAblast.py -u "http://192.168.101.233/phpmyadmin/" -l root -P pass.txt -T 20
```

3、登陆检测原理

登陆成功后头部会携带Set-Cookie字段，进行判断。

![image-20201229145237847](/images/image-20201229145237847.png)