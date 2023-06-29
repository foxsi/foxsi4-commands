#include <unordered_map>

struct MemData {
	uint8_t instruction;
	uint32_t addr;
	uint32_t data;
};
std::unordered_map<char, MemData> COMMAND_LOOKUP = {
	{0x82, (struct MemData){0x4d, 0x00, 0x00}},
	{0x88, (struct MemData){0x4d, 0x00, 0x00}},
	{0x89, (struct MemData){0x4d, 0x00, 0x00}},
	{0x8A, (struct MemData){0x4d, 0x00, 0x00}},
	{0x8B, (struct MemData){0x4d, 0x00, 0x00}},
	{0x8E, (struct MemData){0x4d, 0x38000244, 0x04}},
	{0x9F, (struct MemData){0x4d, 0x38000248, 0x04}},
	{0x9A, (struct MemData){0x4d, 0x00, 0x0c}},
	{0x9C, (struct MemData){0x4d, 0x380001f4, 0x04}},
	{0x9D, (struct MemData){0x4d, 0x380001f0, 0x04}},
	{0xA1, (struct MemData){0x4d, 0x00, 0x02}},
	{0xA4, (struct MemData){0x4d, 0x00, 0x00}},
	{0xA8, (struct MemData){0x4d, 0x00, 0x00}},
	{0x98, (struct MemData){0x4d, 0x38000100, 0x04}},
	{0x92, (struct MemData){0x4d, 0x00, 0x00}},
	{0x93, (struct MemData){0x4d, 0x00, 0x00}},
	{0xB8, (struct MemData){0x4d, 0x00, 0x02}},
	{0xB5, (struct MemData){0x4d, 0x00, 0x01}},
	{0xB6, (struct MemData){0x4d, 0x00, 0x01}},
	{0xB7, (struct MemData){0x4d, 0x00, 0x02}},
	{0xB9, (struct MemData){0x4d, 0x00, 0x01}},
	{0x40, (struct MemData){0x7d, 0x00, 0x00}},
	{0x42, (struct MemData){0x7d, 0x00, 0x00}},
	{0x44, (struct MemData){0x7d, 0x00, 0x00}},
	{0x45, (struct MemData){0x7d, 0x00, 0x00}},
	{0x77, (struct MemData){0x7d, 0x00, 0x00}},
	{0x61, (struct MemData){0x7d, 0x00, 0x00}},
	{0x62, (struct MemData){0x7d, 0x00, 0x00}},
	{0x63, (struct MemData){0x7d, 0x00, 0x00}},
	{0x24, (struct MemData){0x7d, 0x00, 0x00}},
	{0x25, (struct MemData){0x7d, 0x00, 0x00}},
	{0x18, (struct MemData){0x7d, 0x38000040, 0x00}},
	{0x1F, (struct MemData){0x7d, 0x38000044, 0x00}},
	{0x10, (struct MemData){0x7d, 0x38000048, 0x00}},
	{0x11, (struct MemData){0x7d, 0x00, 0x00}},
	{0x12, (struct MemData){0x7d, 0x38000050, 0x00}},
	{0x13, (struct MemData){0x7d, 0x38000054, 0x00}},
	{0x14, (struct MemData){0x7d, 0x00, 0x00}},
	{0x15, (struct MemData){0x7d, 0x00, 0x00}},
	{0x16, (struct MemData){0x7d, 0x00, 0x00}},
	{0x17, (struct MemData){0x7d, 0x00, 0x00}},
	{0x1A, (struct MemData){0x7d, 0x00, 0x00}},
	{0x1C, (struct MemData){0x7d, 0x00, 0x00}},
	{0x1D, (struct MemData){0x7d, 0x00, 0x00}},
	{0x3A, (struct MemData){0x7d, 0x00, 0x00}},
	{0x3B, (struct MemData){0x7d, 0x00, 0x00}},
	{0x39, (struct MemData){0x7d, 0x00, 0x00}},
	{0x70, (struct MemData){0x7d, 0x00, 0x00}},
	{0x71, (struct MemData){0x7d, 0x00, 0x00}},
	{0x72, (struct MemData){0x7d, 0x00, 0x00}},
	{0x73, (struct MemData){0x7d, 0x00, 0x00}},
	{0x74, (struct MemData){0x7d, 0x00, 0x00}},
	{0x78, (struct MemData){0x7d, 0x00, 0x00}},
};