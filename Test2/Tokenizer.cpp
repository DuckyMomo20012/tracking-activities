#include"Tokenizer.h"

std::vector<std::string> Tokenizer::split(std::string haystack, std::string needle) {
	std::vector<std::string> token;
	int start = 0;
	size_t foundPosition = haystack.find(needle, start);
	while (foundPosition!= std::string::npos) {
		token.push_back(haystack.substr(start, foundPosition-start));
		start = foundPosition + needle.size();
		foundPosition = haystack.find(needle, start);
	}
	token.push_back(haystack.substr(start, foundPosition - start));
	return token;
}

std::vector<int> Tokenizer::convertToInt(std::string haystack, std::string needle) {
	std::vector<int> token;
	std::vector<std::string> tokenString = Tokenizer::split(haystack, needle);
	for (auto e : tokenString) {
		int number;
		bool isSuccessful = Integer::tryParse(e, number);
		if (isSuccessful) {
			token.push_back(number);
		}
	}
	return token;
}

int Tokenizer::smallestNumber(std::vector<int> a) {
	int min = a[0];
	for (int i = 1; i < a.size(); i++)
		if (a[i] < min)min = a[i];
	return min;
}

std::vector<int> Tokenizer::ThreeBiggestNumber(std::vector<int>a) {
	int max = a[0], pos = 0;
	std::vector<int> result;
	for (int k = 0; k < 3; k++) {
		for (int i = 1; i < a.size(); i++)
			if (a[i] > max) {
				max = a[i]; pos = i;
			}
		a.erase(a.begin() + pos);
		result.push_back(max);
		max = a[0];
		pos = 0;
	}
	return result;
}

int Integer::parse(std::string value) {
	return stoi(value);
}

bool Integer::tryParse(const std::string value, int& number) {
	bool isValid = true;
	try {
		number = parse(value);
	}
	catch (const std::exception & ex) {
		isValid = false;
		std::cout << "Invalid format exception: " << ex.what() << std::endl;
	}
	return isValid;
}

std::string Integer::toString(std::vector<int> a) {
	std::stringstream writer;
	for (int i = 0; i < a.size(); i++)writer << a[i] << " ";
	return writer.str();
}