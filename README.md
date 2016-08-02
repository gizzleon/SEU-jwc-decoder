﻿# SEU-jwc-decoder 说明文档

---
## 更新记录

 - 2016/08/02 - decoder v1.0 诞生


---

## 简介
这是一个专门为SEU教务处系统的验证码设计的识别器，正确率能维持在36%左右。目前所知使用该种验证码的地方有学生在线系统与学生选课系统。

识别器用python2.7开发，并使用了pytesser的OCR功能。设计思路请参见[这里][1]。

## 使用说明
 1. 请将所有`.py`的文件(`testing.py`除外)放入目录，在需要使用的脚本中`import decoder`；
 2. 用opencv的`cv2.imread(<filename>, 0)`读入验证码图像，请注意**第二个参数为0**；
 3. 调用方法`decoder.imageToString(img)`方法，参数为第二步所得的`ndarray`类型图像数组，结果将返回仅含数字的字符串，若无法识别则会返回空字符串；
 4. `testing.py`文件为对该识别器的测试程序，目前仅能在**选课未开放时**正常运行。请修改`testRange`为你想测试的次数。运行结束后会输出识别正确、识别出不正确的四位数以及识别失败（包括超时）三种情况的次数统计。

##  可以改进的地方

 - 在填充干扰线、滤波、取阈值等操作时改变相关参数有可能小程度提升识别的准确率（可以参考[设计思路][1]）
 - 如果能够将数字的变形还原，应该可以大幅提升准确率
 
## 其他

没有错→_→我写这个识别器的目的就是为了实现选课系统的自动登录。此外，任何能获取源码的人都可以使用或对其进行修改。如果有任何的想法，欢迎来交流XD


  [1]: http://blog.csdn.net/sinat_35287833/article/details/52091611