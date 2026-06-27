// crc_calculator.h
// CRC 计算器 —— 纯 C++ 实现，不依赖任何框架
// 这个类稍后会通过 pybind11 暴露给 Python 使用

#ifndef CRC_CALCULATOR_H
#define CRC_CALCULATOR_H

#include <cstdint>
#include <vector>
#include <string>

// CRC 计算器类
// 提供 CRC8 和 CRC16 两种校验算法
// 芯片通信中最常用的数据完整性校验方式
class CrcCalculator
{
public:
    // 构造函数
    // name: 给这个计算器实例取个名字（方便调试/日志）
    CrcCalculator(const std::string &name);

    // 获取计算器名称
    std::string getName() const;

    // CRC8 计算
    // data: 输入字节数组
    // 返回: 1 字节校验值
    // 算法: 多项式 0x07（x^8 + x^2 + x + 1），初始值 0x00
    uint8_t crc8(const std::vector<uint8_t> &data) const;

    // CRC16 计算（CCITT）
    // data: 输入字节数组
    // 返回: 2 字节校验值
    // 算法: 多项式 0x1021，初始值 0xFFFF
    uint16_t crc16(const std::vector<uint8_t> &data) const;

    // 校验数据完整性
    // data: 原始数据
    // expected_crc16: 期望的 CRC16 值
    // 返回: true = 校验通过，false = 数据被篡改
    bool verify(const std::vector<uint8_t> &data, uint16_t expected_crc16) const;

    // 获取调用次数（演示 pybind11 暴露只读属性）
    int getCallCount() const;

private:
    std::string _name;

    // 记录 crc8/crc16 被调用的总次数
    // 用于演示：C++ 端的状态能被 Python 端观察到
    mutable int _callCount = 0;
};

#endif // CRC_CALCULATOR_H