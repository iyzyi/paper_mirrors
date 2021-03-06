> 本文转载自：https://jingyan.baidu.com/article/0f5fb0990bba086d8334eaf6.html，版权归原作者所属哦~

大致原理就是有一个需要解密的ZIP而且不知道密码，但幸运的是有ZIP包里一个已知文件，将已知文件进行ZIP加密后和待解密的ZIP里已知文件进行hex对比，两者的区别就是ZIP加密的三个key。

## [](javascript:;)工具/原料

  * 电脑

  * ZIP加密压缩包

## [](javascript:;)方法/步骤

  1. 比如待解密的ZIP包内有两个文件，如下所示：

[![ZIP明文攻击获得加密压缩包内文件](https://imgsa.baidu.com/exp/w=500/sign=88ebdd98df62853592e0d221a0ee76f2/18d8bc3eb13533fa91303444a2d3fd1f40345bd1.jpg)](http://jingyan.baidu.com/album/0f5fb0990bba086d8334eaf6.html?picindex=1)

  2. 但是目前有003.jpg文件，将003.jpg进行单独压缩，如下所示：

[![ZIP明文攻击获得加密压缩包内文件](https://imgsa.baidu.com/exp/w=500/sign=e740c9efc3ea15ce41eee00986013a25/203fb80e7bec54e7d2aabd74b3389b504fc26a12.jpg)](http://jingyan.baidu.com/album/0f5fb0990bba086d8334eaf6.html?picindex=2)

  3. 可以看到两个压缩包文件内的003.jpg文件的CRC32值是一样的，下面就可以使用Advanced Zip Password Recovery来进行破解，网上下载该软件进行安装，选择攻击类型为Plain-text模式，如下所示：

[![ZIP明文攻击获得加密压缩包内文件](https://imgsa.baidu.com/exp/w=500/sign=04b6a770cc5c1038247ecec28210931c/d4628535e5dde7117d09e49cadefce1b9c166185.jpg)](http://jingyan.baidu.com/album/0f5fb0990bba086d8334eaf6.html?picindex=3)

  4. 点击start，开始对比筛选key，速度很快，一会就解密成功，如下所示：

[![ZIP明文攻击获得加密压缩包内文件](https://imgsa.baidu.com/exp/w=500/sign=34fdf553c33d70cf4cfaaa0dc8ddd1ba/7a899e510fb30f2409644b69c295d143ac4b03d9.jpg)](http://jingyan.baidu.com/album/0f5fb0990bba086d8334eaf6.html?picindex=4)

  5. 筛选很快，完成后会出现三个加密密钥，点击后面导出，即可将加密的ZIP包另存为空白的ZIP包，如下所示：

[![ZIP明文攻击获得加密压缩包内文件](https://imgsa.baidu.com/exp/w=500/sign=e92aab81bcfd5266a72b3c149b199799/1f178a82b9014a909ee2e1d7a3773912b21beef8.jpg)](http://jingyan.baidu.com/album/0f5fb0990bba086d8334eaf6.html?picindex=5)

[![ZIP明文攻击获得加密压缩包内文件](https://imgsa.baidu.com/exp/w=500/sign=d0dda9dde350352ab16125086343fb1a/9a504fc2d56285350ff3744b9aef76c6a7ef634d.jpg)](http://jingyan.baidu.com/album/0f5fb0990bba086d8334eaf6.html?picindex=6)

  6. 简单来说，ZIP明文攻击就是利用已知文件找加密密钥，利用密钥来解锁其它加密文件，因为ZIP压缩包里的所有文件都是使用同一个加密密钥来加密的。

