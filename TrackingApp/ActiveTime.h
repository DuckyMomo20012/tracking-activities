#define _CRT_SECURE_NO_WARNINGS
#pragma once

#include<ctime>
#include<fstream>

#include"Tokenizer.h"

struct Time
{
	int _hour;
	int _minute;
	
	Time();
	
	Time(int hour, int minute);
	
	void mod(int hour, int minute);
	
	int Hour() { return _hour; }
	int Minute() { return _minute; }
	int convertToMin() { return _hour * 60 + _minute; }
	std::string toString();
	Time sub(Time t);
	std::string fileName();
};

struct ActiveTime {
	Time _from;
	Time _to;
	int _duration; //minute
	int _interrupt_time; //minute
	int _sum; //minute
	bool isDuration;
	bool isInterruptTime;
	bool isSum;
	
	ActiveTime();
	
	ActiveTime(Time from, Time to);
	void setFrom(Time x) { _from = x; }
	void setTo(Time x) { _to = x; }
	void setDuration(int x) { _duration = x; }
	void setInterruptTime(int x) { _interrupt_time = x; }
	void setSum(int x) { _sum = x; }
	Time From() { return _from; }
	Time To() { return _to; }
	int Duration() { return _duration; }
	int InterruptTime() { return _interrupt_time; }
	int Sum() { return _sum; }
	
	std::string toString();
	
};

Time getTime();

void readFile(std::string filename, std::vector<ActiveTime>& listActiveTime);

void writeStartTimeToFile(std::string filename, Time activeTime);

void writeEndTimeToFile(std::string filename, Time activeTime);

bool isInUseTime(Time now, std::vector<ActiveTime> listActiveTime);

int minUsed(Time now, std::string historyFile, std::string activeTimeFile);

int timeRemain(Time startCP, Time now, std::string activeTimeFile);

int interruptTimeRemain(Time now);

void writeWrongPassFile();

Time readWrongPassFile();

std::string hashFile();

int nextTimeToRun(Time now);

void saveEndTime();

Time readEndTime();

void savelineEndTime();

std::string getlineEndTime();

std::string encrypt(std::string pass);
