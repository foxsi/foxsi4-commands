#include <unordered_map>

struct MemData {
	uint8_t instruction;
	uint32_t addr;
	uint32_t data;
};
std::unordered_map<char, MemData> COMMAND_LOOKUP = {
	{0x82, (struct MemData){0x4d, 0x00, 0x00}},
	{0xA0, (struct MemData){0x4d, 0x07fb0000, 0x0c}},
	{0xA2, (struct MemData){0x4d, 0x07fb000c, 0x0c}},
	{0xA3, (struct MemData){0x4d, 0x07fb0018, 0xd8}},
	{0xA4, (struct MemData){0x4d, 0x07fb00f0, 0x0c}},
	{0xA5, (struct MemData){0x4d, 0x07fb00fc, 0x200}},
	{0xA6, (struct MemData){0x4d, 0x07fb0300, 0x0c}},
	{0xB0, (struct MemData){0x4d, 0x07fb030c, 0x08}},
	{0xB1, (struct MemData){0x4d, 0x07fb0314, 0x04}},
	{0xB2, (struct MemData){0x4d, 0x07fb0318, 0x04}},
	{0xB4, (struct MemData){0x4d, 0x07fb031c, 0x08}},
	{0xB5, (struct MemData){0x4d, 0x07fb0324, 0x04}},
	{0xB6, (struct MemData){0x4d, 0x07fb0328, 0x04}},
	{0x8E, (struct MemData){0x4d, 0x022b0314, 0x04}},
	{0x8F, (struct MemData){0x4d, 0x00, 0x00}},
	{0x40, (struct MemData){0x7d, 0x00, 0x00}},
	{0x42, (struct MemData){0x7d, 0x00, 0x00}},
	{0x44, (struct MemData){0x7d, 0x00, 0x00}},
	{0x45, (struct MemData){0x7d, 0x00, 0x00}},
	{0x10, (struct MemData){0x7d, 0x07fb0000, 0x00}},
	{0x11, (struct MemData){0x7d, 0x07fb0000, 0x00}},
	{0x12, (struct MemData){0x7d, 0x07fb0000, 0x00}},
	{0x13, (struct MemData){0x7d, 0x07fb0000, 0x00}},
	{0x14, (struct MemData){0x7d, 0x07fb0000, 0x00}},
	{0x15, (struct MemData){0x7d, 0x07fb0000, 0x00}},
	{0x16, (struct MemData){0x7d, 0x07fb0000, 0x00}},
	{0x21, (struct MemData){0x7d, 0x07fb0000, 0x00}},
	{0x70, (struct MemData){0x7d, 0x00, 0x00}},
	{0x71, (struct MemData){0x7d, 0x00, 0x00}},
	{0x72, (struct MemData){0x7d, 0x00, 0x00}},
	{0x73, (struct MemData){0x7d, 0x00, 0x00}},
	{0x74, (struct MemData){0x7d, 0x00, 0x00}},
	{0x78, (struct MemData){0x7d, 0x00, 0x00}},
};