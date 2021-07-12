#pragma once


#include <msclr\marshal_cppstd.h>
#include<thread>
#include<chrono>
#include<ctime>
#include"ActiveTime.h"
#include<stdlib.h>
#include"screenShot.h"
#include<WinUser.h>





namespace App {

	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;
	using namespace std;
	using namespace System::Threading;


static bool loginFlag;
static bool notLogin=true;

static void waitOneMinute() {
	Sleep(60000);
	if (notLogin == true)
	{
		system("c:\\windows\\system32\\shutdown /s");
	}
}
static void wait15Second() {
		Sleep(15000);
		if (loginFlag ==false)
		{
			system("c:\\windows\\system32\\shutdown /s");
		}
	}
static void shutDownPC() {
	Sleep(10000);
	system("c:\\windows\\system32\\shutdown /s");
}

	public ref class MyForm : public System::Windows::Forms::Form
	{
	public:
		MyForm(void)
		{
			InitializeComponent();
		}
	private: System::Windows::Forms::Label^ label2;

		int wrongPass = 0;
	
	protected:

		~MyForm()
		{
			
			if (components)
			{
				delete components;
			}
		}
	private: System::Windows::Forms::TextBox^ textBox1;
	protected:
	private: System::Windows::Forms::Button^ button1;
	private: System::Windows::Forms::Label^ label1;


	private:
		
		System::ComponentModel::Container^ components;

#pragma region Windows Form Designer generated code
		
		void InitializeComponent(void)
		{
			System::ComponentModel::ComponentResourceManager^ resources = (gcnew System::ComponentModel::ComponentResourceManager(MyForm::typeid));
			this->textBox1 = (gcnew System::Windows::Forms::TextBox());
			this->button1 = (gcnew System::Windows::Forms::Button());
			this->label1 = (gcnew System::Windows::Forms::Label());
			this->label2 = (gcnew System::Windows::Forms::Label());
			this->SuspendLayout();
			// 
			// textBox1
			// 
			resources->ApplyResources(this->textBox1, L"textBox1");
			this->textBox1->Name = L"textBox1";
			// 
			// button1
			// 
			resources->ApplyResources(this->button1, L"button1");
			this->button1->Name = L"button1";
			this->button1->UseVisualStyleBackColor = true;
			this->button1->Click += gcnew System::EventHandler(this, &MyForm::button1_Click);
			// 
			// label1
			// 
			resources->ApplyResources(this->label1, L"label1");
			this->label1->ForeColor = System::Drawing::Color::Black;
			this->label1->Name = L"label1";
			this->label1->UseCompatibleTextRendering = true;
			// 
			// label2
			// 
			resources->ApplyResources(this->label2, L"label2");
			this->label2->Name = L"label2";
			// 
			// MyForm
			// 
			resources->ApplyResources(this, L"$this");
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->BackColor = System::Drawing::SystemColors::ActiveCaption;
			this->ControlBox = false;
			this->Controls->Add(this->label2);
			this->Controls->Add(this->label1);
			this->Controls->Add(this->button1);
			this->Controls->Add(this->textBox1);
			this->Name = L"TrackingApp";
			this->Load += gcnew System::EventHandler(this, &MyForm::MyForm_Load);
			this->ResumeLayout(false);
			this->PerformLayout();

		}
		Thread^ th1;
		Thread^ waitLogin;
		Thread^ shutdown;

		

#pragma endregion
	private: System::Void button1_Click(System::Object^ sender, System::EventArgs^ e) {

		string childPass = "1234";
		string ParentPass = "0000";
		msclr::interop::marshal_context convert;

		if (getlineEndTime() != "") {
			writeEndTimeToFile(".\\Downloads\\history.txt", readEndTime());
			savelineEndTime();
		}

		if (convert.marshal_as<string>(textBox1->Text) == ParentPass) {
			notLogin = false;
			loginFlag = true;
			MessageBox::Show("Phu huynh dang nhap thanh cong\n Vui long tat hop thoai nay ");
			this->Hide();
			///Sleep 1 hour
			chrono::hours oneHour(1);
			this_thread::sleep_for(oneHour);
			this->Show();
			
		}
		else if(convert.marshal_as<string>(textBox1->Text) != ParentPass){
			
			loginFlag = false;
			wrongPass++;

			//Doc file txt xem co o trong thoi gian su dung hay khong
			//Trong 1 phien hd chi can doc 1 lan
			bool stop = false;
			if (stop == false)
			{
				stop = true;
				WinExec("python downloadConfig.py",SW_HIDE);
				//Sleep(5000);
			}
			
			std::vector<ActiveTime> listActiveTime;
			readFile(".\\Downloads\\activate.txt", listActiveTime);
			Time now = Time();
			bool checkInUsed = isInUseTime(now, listActiveTime);
			Time startComputer = now;


			bool accept = checkInUsed;
			
			//Neu khong duoc su dung
			if (!accept)
			{
				notLogin = false;
				// New thread zone and shutdown
				if (th1 == nullptr)
				{				
					th1 = gcnew Thread(gcnew ThreadStart(wait15Second));
					th1->Start();
				}
				String^ msg = "Con " + nextTimeToRun(now) + " phut nua la den gio mo may";
				MessageBox::Show(msg, "Time Left"); //thong bao
			}

			//Nau duoc su dung
			else if (accept==true)
			{
				if (convert.marshal_as<string>(textBox1->Text) == childPass)
				{
					loginFlag = false;
					this->textBox1->Hide();
					this->button1->Hide();
					this->label1->Text = L"Ban da dang nhap thanh cong";
					this->label1->Show();
					

					int interruptTime = interruptTimeRemain(now);
					if (interruptTime < 0) {
						shutdown = gcnew Thread(gcnew ThreadStart(shutDownPC));
						shutdown->Start();
						interruptTime = interruptTime * -1;
						MessageBox::Show("May tinh van dang trong thoi gian nghi\nCon "+interruptTime+ " phut la den gio mo may", "Thong bao");
						this->Close();
						system("c:\\windows\\system32\\shutdown /s");
						System::Environment::Exit(0);
					}
					else{
					writeStartTimeToFile(".\\Downloads\\history.txt", now);

					//Kiem tra con bao lau thi het gio
					int minuteRemain = timeRemain(startComputer, now, ".\\Downloads\\activate.txt");
					
					String^ msg = "Con " + minuteRemain + " phut nua la het gio";
					MessageBox::Show(msg, "Time Left"); //thong bao


					//Thong bao xong thi dong Login page
					Sleep(10);
					
					this->Hide();
					
					std::string hashString = hashFile();

					while (true) {
						//goi 
						WinExec("python downloadConfig.py", SW_HIDE);
						Sleep(30000);
						

						//update
						string newHashString = hashFile();
						if (hashString != newHashString) {
							hashString = newHashString;
							MessageBox::Show("Thoi gian su dung vua duoc update", "Thong bao");
						}


						//chup man hinh
						now = getTime();
						std::string path = ".\\Upload\\"+now.fileName()+".jpg";
						TakeScreenShot(path);
						//Gui anh
						WinExec("python uploadImage.py", SW_HIDE);
						WinExec("python uploadConfig.py", SW_HIDE);

						Sleep(30000);

						saveEndTime();
						//
						int minuteRemain = timeRemain(startComputer, now, ".\\Downloads\\activate.txt");
						if (minuteRemain <= 1) {
							MessageBox::Show("Con 1 phut nua la het gio","Thong bao");
							Sleep(60000);
							now = getTime();
							saveEndTime();
							
							system("c:\\windows\\system32\\shutdown /s");

						}
					}
					
					}
				}
				else {
					if (wrongPass == 3)
					{
						
						writeWrongPassFile();
						MessageBox::Show("Sai mat khau 3 lan, vui long cho 10p sau de tiep tuc", "Thong bao");
						this->Close(); //Close roi moi shutdown
						Application::Exit();
						System::Environment::Exit(0);
						//Shutdown
						system("c:\\windows\\system32\\shutdown /s");
					}
				}

			}
		}

	}
	private: System::Void MyForm_Load(System::Object^ sender, System::EventArgs^ e) {

		Time lastWrongpass = readWrongPassFile();

		Time now = getTime();
		int timeFromLastWrongpass = now.convertToMin() - lastWrongpass.convertToMin();
		if ( timeFromLastWrongpass < 10) {
			shutdown = gcnew Thread(gcnew ThreadStart(shutDownPC));
			shutdown->Start();
			MessageBox::Show("May tinh van dang dong do sai mat khau\nCon " + (10 - timeFromLastWrongpass) + " phut la den gio mo may", "Thong bao");
			
			this->Close();
			system("c:\\windows\\system32\\shutdown /s");
			System::Environment::Exit(0);

		}
		if (waitLogin == nullptr)
		{
			waitLogin = gcnew Thread(gcnew ThreadStart(waitOneMinute));
			waitLogin->Start();
		}
	
		
		this->label1->Hide();
	}
};

}
