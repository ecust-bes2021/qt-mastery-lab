// crc_calculator.cpp
// CRC 计算器的实现

#include "crc_calculator.h"

CrcCalculator::CrcCalculator(const std::string &name)
    : _name(name)
    , _callCount(0)
{
}

std::string CrcCalculator::getName() const
{
    return _name;
}

// CRC8 实现
// 逐字节处理，每个字节逐位异或
// 多项式 0x07: 芯片通信中常用的 CRC8 标准
uint8_t CrcCalculator::crc8(const std::vector<uint8_t> &data) const
{
    uint8_t crc = 0x00;  // 初始值

    for (uint8_t byte : data) {
        crc ^= byte;  // 当前字节异或到 CRC 中

        // 逐位处理（8位）
        for (int i = 0; i < 8; ++i) {
            if (crc & 0x80) {
                // 最高位为1：左移后异或多项式
                crc = (crc << 1) ^ 0x07;
            } else {
                // 最高位为0：仅左移
                crc <<= 1;
            }
        }
    }

    ++_callCount;
    return crc;
}

// CRC16-CCITT 实现
// 多项式 0x1021: 广泛用于蓝牙、ZigBee、SD卡等协议
uint16_t CrcCalculator::crc16(const std::vector<uint8_t> &data) const
{
    uint16_t crc = 0xFFFF;  // 初始值

    for (uint8_t byte : data) {
        crc ^= (static_cast<uint16_t>(byte) << 8);  // 字节放到高8位

        for (int i = 0; i < 8; ++i) {
            if (crc & 0x8000) {
                crc = (crc << 1) ^ 0x1021;
            } else {
                crc <<= 1;
            }
        }
    }

    ++_callCount;
    return crc;
}

// 校验：重新计算 CRC16 并和期望值比较
bool CrcCalculator::verify(const std::vector<uint8_t> &data, uint16_t expected_crc16) const
{
    return crc16(data) == expected_crc16;
}

int CrcCalculator::getCallCount() const
{
    return _callCount;
}