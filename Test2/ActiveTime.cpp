#include"ActiveTime.h"
#include<algorithm>


Time::Time()
{
	
	time_t now = time(0);
	tm* ltm = localtime(&now);
	_hour = ltm->tm_hour;
	_minute = ltm->tm_min;
}

Time::Time(int hour, int minute)
{
	_hour = hour;
	_minute = minute;
}

void Time::mod(int hour, int minute)
{
	_hour = hour;
	_minute = minute;
}

std::string Time::toString()
{
	std::stringstream s;
	s << _hour << ":" << _minute;
	return s.str();
}

Time Time::sub(Time t) {
	int disMin = (_hour * 60 + _minute) - (t.Hour() * 60 - t.Minute());
	Time newTime(disMin / 60, disMin % 60);
	return newTime;
}

std::string Time::fileName()
{
	std::stringstream s;
	s << _hour << "." << _minute;
	return s.str();
}

ActiveTime::ActiveTime()
{
	_duration = 0;
	_interrupt_time = 0;
	_sum = 0;
	isDuration = false;
	isInterruptTime = false;
	isSum = false;
}

ActiveTime::ActiveTime(Time from, Time to)
{
	_from = from;
	_to = to;
}

std::string ActiveTime::toString()
{
	std::stringstream s;
	s << "F" << _from.toString() << " T" << _to.toString();
	if (isDuration)s << " D" << _duration;
	if (isInterruptTime)s << " I" << _interrupt_time;
	if (isSum)s << " S" << _sum;
	return s.str();
}



Time getTime()
{
	Time now = Time();
	return now;
}

void readFile(std::string filename, std::vector<ActiveTime>& listActiveTime)
{
	std::ifstream file(filename);
	while (!file.eof()) {
		ActiveTime newActiveTime;
		std::string line;
		std::getline(file, line);
		if (line == "")continue;
		if (line.length() < 9)continue;
		std::vector<std::string> activeTimeS = Tokenizer::split(line, " ");
		for (int i = 0; i < activeTimeS.size(); i++) {
			std::string s1 = activeTimeS[i].substr(0, 1);
			std::string s2 = activeTimeS[i].substr(1, activeTimeS[i].length() - 1);
			if (s1 == "F" || s1 == "B") {
				std::vector<std::string> timeString = Tokenizer::split(s2, ":");
				int newHour;
				int newMin;
				Time newTime;
				bool isSuccessful = Integer::tryParse(timeString[0], newHour);
				bool isSuccessful2 = Integer::tryParse(timeString[1], newMin);
				if (isSuccessful == isSuccessful2 && isSuccessful == true) {
					newTime.mod(newHour, newMin);
				}
				newActiveTime.setFrom(newTime);
			}
			if (s1 == "T" || s1 == "E") {
				std::vector<std::string> timeString = Tokenizer::split(s2, ":");
				int newHour;
				int newMin;
				Time newTime;
				bool isSuccessful = Integer::tryParse(timeString[0], newHour);
				bool isSuccessful2 = Integer::tryParse(timeString[1], newMin);
				if (isSuccessful == isSuccessful2 && isSuccessful == true) {
					newTime.mod(newHour, newMin);
				}
				newActiveTime.setTo(newTime);
			}
			if (s1 == "D") {
				int newDuration;
				bool isSuccessful = Integer::tryParse(s2, newDuration);
				if (isSuccessful == true) {
					newActiveTime.setDuration(newDuration);
					newActiveTime.isDuration = true;
				}
			}
			if (s1 == "I") {
				int newInterrupt;
				bool isSuccessful = Integer::tryParse(s2, newInterrupt);
				if (isSuccessful == true) {
					newActiveTime.setInterruptTime(newInterrupt);
					newActiveTime.isInterruptTime = true;
				}
			}
			if (s1 == "S") {
				int newSum;
				bool isSuccessful = Integer::tryParse(s2, newSum);
				if (isSuccessful == true) {
					newActiveTime.setSum(newSum);
					newActiveTime.isSum = true;
				}
			}
		}
		listActiveTime.push_back(newActiveTime);
	}

	file.close();

}


void writeStartTimeToFile(std::string filename, Time activeTime) {
	std::ofstream file(filename, std::ofstream::app);

	file << std::endl << "B" << activeTime.toString() << " ";

	file.close();
}

void writeEndTimeToFile(std::string filename, Time activeTime) {
	std::ofstream file(filename, std::ofstream::app);

	file << "E" << activeTime.toString();

	file.close();
}

bool isInUseTime(Time now, std::vector<ActiveTime> listActiveTime) {
	bool check = false;
	for (auto e : listActiveTime) {
		if (e.From().convertToMin() <= now.convertToMin() && now.convertToMin() <= e.To().convertToMin()) {
			check = true;
			break;
		}
	}
	return check;
}

bool isInThisTime(Time now, ActiveTime e) {
	bool check = false;
	if (e.From().convertToMin() <= now.convertToMin() && now.convertToMin() <= e.To().convertToMin()) {
		check = true;
	}
	return check;
}

int minUsed(Time now, std::string historyFile, std::string activeTimeFile) {
	int result = -1;
	std::vector<ActiveTime> listActiveTime;
	readFile(activeTimeFile, listActiveTime);
	std::vector<ActiveTime> listHistoryTime;
	readFile(historyFile, listHistoryTime);
	int usedTime = 0;
	ActiveTime current;

	for (auto e : listActiveTime)
		if (isInThisTime(now, e))current = e;
	for (auto e : listHistoryTime) {
		if (isInThisTime(e.From(), current)) {
			usedTime += e.To().convertToMin() - e.From().convertToMin();
		}
	}

	/*for (auto e : listActiveTime) {
		if (e.From().convertToMin() < now.convertToMin() && now.convertToMin() < e.To().convertToMin()) {
			result = e.Sum() - usedTime;

			if(now.convertToMin() + result > e.To().convertToMin())result = 0;

		}
	}*/

	return usedTime;
}

int timeRemain(Time startCP, Time now, std::string activeTimeFile) {
	std::vector<ActiveTime> listActiveTime;
	readFile(activeTimeFile, listActiveTime);
	int usedFromStartCP = now.convertToMin() - startCP.convertToMin();
	int usedFromStartLine = minUsed(startCP, ".\\Downloads\\history.txt", ".\\Downloads\\activate.txt") + usedFromStartCP;
	int MIN = -1, remainFromT = 0, remainFromD = 0, remainFromS = 0;
	for (auto e : listActiveTime)
		if (isInThisTime(now, e)) {
			if (!e.isDuration && !e.isSum)MIN = e.To().convertToMin() - now.convertToMin();
			else if (!e.isDuration && e.isSum) {
				remainFromT = e.To().convertToMin() - now.convertToMin();
				remainFromS = e.Sum() - usedFromStartLine;
				MIN = remainFromT;
				if (MIN > remainFromS)MIN = remainFromS;
			}
			else if (e.isDuration && !e.isSum) {
				remainFromT = e.To().convertToMin() - now.convertToMin();
				remainFromD = e.Duration() - usedFromStartCP;
				MIN = remainFromT;
				if (MIN > remainFromD)MIN = remainFromD;
			}
			else if (e.isDuration && e.isSum) {
				remainFromT = e.To().convertToMin() - now.convertToMin();
				remainFromD = e.Duration() - usedFromStartCP;
				remainFromS = e.Sum() - usedFromStartLine;
				MIN = remainFromD;
				if (MIN > remainFromT)MIN = remainFromT;
				if (MIN > remainFromS)MIN = remainFromS;
			}
		}
	/*for (auto e : listActiveTime)
		if (isInThisTime(now, e)) {
			remainFromT = e.To().convertToMin() - now.convertToMin();
			remainFromD = startCP.convertToMin() + e.Duration() - usedFromStartCP;
			remainFromS = e.Sum() - usedFromStartLine - usedFromStartCP;
		}
	MIN = remainFromD;
	if (MIN > remainFromT)MIN = remainFromT;
	if (MIN > remainFromS)MIN = remainFromS;*/
	return MIN;
}

//bool checkInterruptTime(Time now) {
//	std::vector<ActiveTime> listActiveTime;
//	readFile(".\\Downloads\\activate.txt", listActiveTime);
//	std::vector<ActiveTime> listHistoryTime;
//	readFile(".\\Downloads\\history.txt", listHistoryTime);
//	ActiveTime lastTime = listHistoryTime[listHistoryTime.size() - 1];
//	ActiveTime current;
//	bool check = false;
//	for (auto e : listActiveTime)
//		if (isInThisTime(now, e))current = e;
//	if (isInThisTime(lastTime.From(), current) && current.Duration() == (lastTime.To().convertToMin() - lastTime.From().convertToMin()))
//		check = true;
//	return check;
//}

int interruptTimeRemain(Time now) {
	std::vector<ActiveTime> listActiveTime;
	readFile(".\\Downloads\\activate.txt", listActiveTime);
	std::vector<ActiveTime> listHistoryTime;
	readFile(".\\Downloads\\history.txt", listHistoryTime);
	ActiveTime lastTime;
	if (listHistoryTime.size() != 0) { lastTime = listHistoryTime[listHistoryTime.size() - 1]; }
	else return 0;
	ActiveTime current;
	bool check = false;
	for (auto e : listActiveTime)
		if (isInThisTime(now, e))current = e;
	if (isInThisTime(lastTime.From(), current) && current.Duration() == (lastTime.To().convertToMin() - lastTime.From().convertToMin()))
		check = true;
	if (!check)return 0;
	else {
		int timeRemain = now.convertToMin() - lastTime.To().convertToMin() - current.InterruptTime();
		return timeRemain;
	}
}

void writeWrongPassFile() {
	Time now = getTime();
	std::ofstream file(".\\Downloads\\wrongpass.txt");

	file << now.Hour() << " " << now.Minute();

	file.close();
}

Time readWrongPassFile() {
	int hour = 0;
	int min = 0;
	std::ifstream file(".\\Downloads\\wrongpass.txt");

	file >> hour;
	file >> min;
	Time newtime(hour, min);

	file.close();
	return newtime;
}

std::string hashFile() {
	std::ifstream file(".\\Downloads\\activate.txt");
	std::stringstream s;
	while (!file.eof()) {
		std::string word;
		file >> word;
		s << word;
	}

	file.close();
	return s.str();
}

int nextTimeToRun(Time now) {
	int result = 0;
	std::vector<ActiveTime> listActiveTime;
	readFile(".\\Downloads\\activate.txt", listActiveTime);
	std::vector<int> timeFrom;
	for (auto e : listActiveTime) {
		timeFrom.push_back(e.From().convertToMin());
	}
	sort(timeFrom.begin(), timeFrom.end());
	for (int i = 0; i < timeFrom.size() - 1; i++) {
		if (timeFrom[i] < now.convertToMin() && now.convertToMin() < timeFrom[i + 1])
			result = timeFrom[i + 1] - now.convertToMin();
	}
	return result;
}

void saveEndTime() {
	Time now = getTime();
	std::ofstream file(".\\Downloads\\endTime.txt");

	file << now.Hour() << " " << now.Minute();

	file.close();
}

Time readEndTime() {
	int hour = 0;
	int min = 0;
	std::ifstream file(".\\Downloads\\endTime.txt");

	file >> hour;
	file >> min;
	Time newtime(hour, min);

	file.close();
	return newtime;
}

void savelineEndTime() {
	std::ofstream file(".\\Downloads\\endTime.txt");

	file << std::endl;

	file.close();
}

std::string getlineEndTime() {
	std::ifstream file(".\\Downloads\\endTime.txt");
	std::string s;
	file >> s;

	file.close();
	return s;
}