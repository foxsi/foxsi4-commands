#include <unordered_map>

struct MemData {
	uint8_t instruction;
	uint32_t addr;
	uint32_t data;
};
std::unordered_map<char, MemData> COMMAND_LOOKUP = {
	{0x80, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x81, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x82, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x88, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x89, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x8a, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x8b, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x98, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x9a, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x9c, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x9d, (struct MemData){0b00000000, 0x00, 0x0}},
	{0xa1, (struct MemData){0b00000000, 0x00, 0x0}},
	{0xa4, (struct MemData){0b00000000, 0x00, 0x0}},
	{0xa8, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x92, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x93, (struct MemData){0b00000000, 0x00, 0x0}},
	{0xb8, (struct MemData){0b00000000, 0x00, 0x0}},
	{0xb5, (struct MemData){0b00000000, 0x00, 0x0}},
	{0xb6, (struct MemData){0b00000000, 0x00, 0x0}},
	{0xb7, (struct MemData){0b00000000, 0x00, 0x0}},
	{0xb9, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x40, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x42, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x44, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x45, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x77, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x61, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x62, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x63, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x24, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x25, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x18, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x1a, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x1c, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x1d, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x12, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x13, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x39, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x70, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x71, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x72, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x73, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x74, (struct MemData){0b00000000, 0x00, 0x0}},
	{0x78, (struct MemData){0b00000000, 0x00, 0x0}},
};