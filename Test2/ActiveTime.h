#pragma once
#include<iostream>

struct Time
{
	int _hour;
	int _minute;
	Time()
	{

	}
	Time(int hour, int minute) {
		_hour = hour;
		_minute = minute;
	}

};

struct ActiveTime {
	Time _from;
	Time _to;
	int _duration; //minute
	int _interrupt_time; //minute
	int _Sum; //minute
	ActiveTime(Time from, Time to)
	{
		_from = from;
		_to = to;
	}
};
