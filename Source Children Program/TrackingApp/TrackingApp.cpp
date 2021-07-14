#include "TrackingApp.h"

using namespace System;
using namespace System::Windows::Forms;
[STAThread]
void main(array<String^>^ args) {
	Application::EnableVisualStyles();
	Application::SetCompatibleTextRenderingDefault(false);
	TrackingApp::TrackingApp app;
	Application::Run(% app);

	System::Environment::Exit(0);


}