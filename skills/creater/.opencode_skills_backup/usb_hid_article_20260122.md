---
title: "USB-HID：那个让键盘鼠标「即插即用」的神秘协议"
date: 2026-01-22
tags: [USB, HID, 人机交互, 嵌入式]
description: 聊聊USB-HID协议的实际使用体验、踩坑经验和实用建议
---

记得第一次在嵌入式项目里要做一个自定义键盘的时候，我整个人都是懵的——这年头做个键盘还得跟USB协议打交道？以前以为插上就能用是天经地义的事，直到自己写代码才发现，这里面的水真的很深。

## 说USB-HID之前，先聊聊它解决了什么问题

在没有HID协议之前，如果你想做个键盘或者鼠标，得自己写驱动程序。PS/2接口那时候还能凑合用，但随着USB普及，设备厂商就疯了——总不能让每个鼠标都自带驱动吧？

USB-IF（USB开发者论坛）这帮人就想了个办法：定义一个**人机接口设备类**（Human Interface Device，简称HID）。这个协议的核心思想是：**设备自己描述自己会发送什么数据，主机按照这个描述来解析**。这样操作系统只需要一个通用的HID驱动，就能支持所有符合规范的键盘、鼠标、手柄，甚至是那些奇奇怪怪的USB脚垫、指纹识别器。

## HID协议最让人头疼的地方

说实话，我第一次看HID报告描述符（Report Descriptor）的时候，内心是崩溃的。这玩意儿不是普通的结构体，而是一串字节流，每个字节都有特定的含义，组合起来描述数据的组织方式。

举个简单的例子，一个标准的3键鼠标报告描述符大概长这样：

```c
// 0x05, 0x01,        // Usage Page (Desktop)
// 0x09, 0x02,        // Usage (Mouse)
// 0xA1, 0x01,        // Collection (Application)
// 0x09, 0x01,        //   Usage (Pointer)
// 0xA1, 0x00,        //   Collection (Physical)
// 0x05, 0x09,        //     Usage Page (Buttons)
// 0x19, 0x01,        //     Usage Minimum (1)
// 0x29, 0x03,        //     Usage Maximum (3)
// 0x15, 0x00,        //     Logical Minimum (0)
// 0x25, 0x01,        //     Logical Maximum (1)
// 0x95, 0x03,        //     Report Count (3)
// 0x75, 0x01,        //     Report Size (1)
// 0x81, 0x02,        //     Input (Data, Var, Abs)
// 0x95, 0x01,        //     Report Count (1)
// 0x75, 0x05,        //     Report Size (5)
// 0x81, 0x01,        //     Input (Constant)
// 0x05, 0x01,        //     Usage Page (Desktop)
// 0x09, 0x30,        //     Usage (X)
// 0x09, 0x31,        //     Usage (Y)
// 0x15, 0x81,        //     Logical Minimum (-127)
// 0x25, 0x7F,        //     Logical Maximum (127)
// 0x75, 0x08,        //     Report Size (8)
// 0x95, 0x02,        //     Report Count (2)
// 0x81, 0x06,        //     Input (Data, Var, Rel)
// 0xC0,              //   End Collection
// 0xC0               // End Collection
```

这堆十六进制数看起来像是天书，但实际上是有规律的：
- 每个项以一个前缀字节开始，指示项的类型和长度
- Usage Page告诉我们这是什么类型的设备（桌面设备、游戏控制器等）
- 那些0xA1、0x05什么的，其实是变长编码，读多了也就习惯了

## 用HIDAPI库省心多了

写原生HID协议确实不是人干的活。好在有[HIDAPI](https://github.com/libusb/hidapi)这个跨平台库，它封装了底层细节，让开发者可以专注于业务逻辑。

我在项目里用过这个库，总体感受是：**真的省心，但也有些坑要注意**。

首先是枚举设备，这个过程比我想象的复杂。HIDAPI会遍历所有HID设备，返回一个链表，每个节点包含设备的详细信息：

```c
#include <hidapi.h>
#include <stdio.h>

int main(void) {
    // 初始化库
    hid_init();
    
    // 枚举所有HID设备（VID=0和PID=0表示匹配所有）
    struct hid_device_info *devs = hid_enumerate(0x0, 0x0);
    struct hid_device_info *cur_dev = devs;
    
    while (cur_dev) {
        printf("设备: %ls - %ls\n",
               cur_dev->manufacturer_string,
               cur_dev->product_string);
        printf("VID:PID = %04x:%04x\n",
               cur_dev->vendor_id,
               cur_dev->product_id);
        printf("Usage Page: 0x%hx\n", cur_dev->usage_page);
        cur_dev = cur_dev->next;
    }
    
    // 记得释放内存
    hid_free_enumeration(devs);
    hid_exit();
    return 0;
}
```

这里有个大坑：**枚举完一定要调用`hid_free_enumeration`释放内存**。我之前有次写测试程序忘了这茬，内存直接炸了。

打开设备后，就可以读写数据了。HID设备通过**中断传输**来交换数据，这种方式延迟低，适合实时输入设备：

```c
// 打开指定设备
hid_device *handle = hid_open(0x046D, 0xC01D, NULL); // Logitech鼠标
if (!handle) {
    printf("打开设备失败: %ls\n", hid_error(NULL));
    return -1;
}

// 设置非阻塞模式
hid_set_nonblocking(handle, 1);

unsigned char buf[65]; // HID报告第一个字节是报告ID

// 读取输入报告（鼠标移动、按键状态等）
int res = hid_read(handle, buf, sizeof(buf));
if (res > 0) {
    printf("收到 %d 字节数据\n", res);
    // buf[0] = 按键状态
    // buf[1] = X轴移动
    // buf[2] = Y轴移动
    // buf[3] = 滚轮
}

// 发送输出报告（比如控制键盘LED）
unsigned char report[65] = {0};
report[0] = 0x00; // 报告ID
report[1] = 0x01; // 数据
hid_write(handle, report, 65);

hid_close(handle);
```

## 踩坑经验总结

在做USB-HID项目的过程中，我踩过不少坑，说几个印象最深的：

**坑一：报告描述符写错一点点，整个设备就不工作**。有次我把Usage Page写错了（把0x01写成了0x02），结果设备枚举成功后，系统始终收不到数据。调试了半天才发现是描述符的问题。建议用USB分析仪或者hidrd工具验证描述符的正确性。

**坑二：HIDAPI在不同平台的行为不一致**。Windows上用hid.dll，Linux上用hidraw， macOS上用IOHidManager。有时候同一段代码在Windows下正常，到Linux下就出问题。比如Linux下需要设备有写权限才能发送输出报告，这个权限问题让我折腾了一整天。

**坑三：报告ID的坑**。HID报告可以有ID也可以没有ID。有ID的话，数据第一个字节是报告ID；没有ID的话，整个报告都是数据。HIDAPI的`hid_write`函数期望第一个字节是报告ID（即使是0），如果你的设备不用报告ID，这里就容易搞混。

**坑四：蓝牙HID和USB HID不一样**。是的，你没看错，蓝牙也有HID协议（Bluetooth HID Profile），但它和USB HID用的是不同的协议栈。如果你的设备要同时支持USB和蓝牙，需要分别实现两套协议。

## 什么情况下该用HID

如果你要做的设备属于以下几类，HID协议基本上是最佳选择：

- 键盘、鼠标、触摸板这些传统输入设备
- 游戏手柄、摇杆、踏板等游戏控制器
- 工业控制面板、POS机键盘
- 需要即插即用、跨平台兼容的设备

如果你的设备数据传输量大、延迟要求不高，那可能用CDC（虚拟串口）或者自定义的USB类更合适。HID的优势在于即插即用和低延迟，代价是报告大小和频率有限制。

## 用下来的感受

HID协议整体来说是个设计得很聪明的协议，它让「即插即用」成为可能。但对于开发者来说，确实有一定的学习曲线。报告描述符那套东西，第一次接触会觉得反人类，但用多了也就习惯了。

最让我欣慰的是，HIDAPI这个库把跨平台的脏活累活都封装好了，让我可以专注于应用逻辑。如果你正要做HID相关的项目，建议先花时间把HID协议的基本概念搞清楚，然后用HIDAPI来写代码，会省事很多。

---

*关于USB-HID，你有什么想问的或者想分享的经验吗？欢迎在评论区聊聊。*
