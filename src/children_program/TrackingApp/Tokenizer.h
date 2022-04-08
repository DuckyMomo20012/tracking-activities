#ifndef _TOKENIZER_
#define _TOKENIZER_
#include<iostream>
#include<vector>
#include<string>
#include<sstream>


class Tokenizer {
public:
	static std::vector<std::string> split(std::string, std::string);
	static std::vector<int> convertToInt(std::string, std::string);
	static int smallestNumber(std::vector<int>);
	static std::vector<int> ThreeBiggestNumber(std::vector<int>);
};

class Integer {
public:
	static int parse(std::string);
	static bool tryParse(const std::string, int&);
	static std::string toString(std::vector<int>);
};

#endif // !_TOKENIZER_

