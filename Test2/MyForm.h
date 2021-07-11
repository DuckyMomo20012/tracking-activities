#pragma once
#include"mainPage.h"
#include<iostream>
#include <msclr\marshal_cppstd.h>
#include<thread>
#include<chrono>
#include<ctime>
#include"ActiveTime.h"




namespace Test2 {

	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;
	using namespace std;
	using namespace System::Threading;

static bool login1;
static void wait15Second() {
		Sleep(15000);
		if (login1==false)
		{
			MessageBox::Show("Done");
		}
	}

	/// <summary>
	/// Summary for MyForm
	/// </summary>
	public ref class MyForm : public System::Windows::Forms::Form
	{
	public:
		MyForm(void)
		{
			InitializeComponent();
			//
			//TODO: Add the constructor code here
			// 
			//

		}
	public:
		int wrongPass = 0;
		//bool login1;
	protected:
		/// <summary>
		/// Clean up any resources being used.
		/// </summary>
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

	protected:

	protected:

	private:
		/// <summary>
		/// Required designer variable.
		/// </summary>
		System::ComponentModel::Container^ components;

#pragma region Windows Form Designer generated code
		/// <summary>
		/// Required method for Designer support - do not modify
		/// the contents of this method with the code editor.
		/// </summary>
		void InitializeComponent(void)
		{

			this->textBox1 = (gcnew System::Windows::Forms::TextBox());
			this->button1 = (gcnew System::Windows::Forms::Button());
			this->label1 = (gcnew System::Windows::Forms::Label());
			this->SuspendLayout();
			// 
			// textBox1
			// 
			this->textBox1->Location = System::Drawing::Point(40, 88);
			this->textBox1->Name = L"textBox1";
			this->textBox1->Size = System::Drawing::Size(131, 22);
			this->textBox1->TabIndex = 0;
			// 
			// button1
			// 
			this->button1->Location = System::Drawing::Point(198, 86);
			this->button1->Name = L"button1";
			this->button1->Size = System::Drawing::Size(75, 23);
			this->button1->TabIndex = 1;
			this->button1->Text = L"Login";
			this->button1->UseVisualStyleBackColor = true;
			this->button1->Click += gcnew System::EventHandler(this, &MyForm::button1_Click);
			// 
			// label1
			// 
			this->label1->AutoSize = true;
			this->label1->Location = System::Drawing::Point( 109, 160);
			this->label1->Name = L"label1";
			this->label1->Size = System::Drawing::Size(46, 17);
			this->label1->TabIndex = 2;
			this->label1->Text = L"label1";
			// 
			// MyForm
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(8, 16);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(282, 253);
			this->Controls->Add(this->label1);
			this->Controls->Add(this->button1);
			this->Controls->Add(this->textBox1);
			this->ControlBox = false;
			this->Name = L"MyForm";
			this->Text = L"MyForm";
			this->Load += gcnew System::EventHandler(this, &MyForm::MyForm_Load);
			this->ResumeLayout(false);
			this->PerformLayout();

		}
		Thread^ th1;

#pragma endregion
	private: System::Void button1_Click(System::Object^ sender, System::EventArgs^ e) {

		string childPass = "1234";
		string ParentPass = "0000";
		msclr::interop::marshal_context convert;


		if (convert.marshal_as<string>(textBox1->Text) == ParentPass) {
			//this->Hide();
			//May be work
			/*chrono::seconds oneHour(30);
			this_thread::sleep_for(oneHour);
			this->Show();*/
			mainPage^ m1 = gcnew mainPage();
			login1 = true;
			m1->ShowDialog();


		}
		else {
			login1 = false;
			wrongPass++;
			int getHour = 23;
			int getMinute = 30;
			time_t timer = time(0);
			tm* now = localtime(&timer);
			Time currentTime = Time(now->tm_hour, now->tm_min);
			if (th1 == nullptr)
			{
				th1 = gcnew Thread(gcnew ThreadStart(wait15Second));
				th1->Start();
				
			}



			if (currentTime._hour < getHour)
			{

				// New thread zone and shutdown


				//Cont
				


			}
			else if (currentTime._hour >= getHour) {
				if (convert.marshal_as<string>(textBox1->Text) == childPass)
				{
					MessageBox::Show("Con 10 p nhua la het gio", "Time Left");
					Sleep(10);
					this->Hide();
					mainPage^ main = gcnew mainPage;
					main->ShowDialog();

					Sleep(10);

					this->Close();

				}
				else {
					if (wrongPass == 3)
					{
						this->Close();
						//
						// Time ten;
						// Plus 10 to ten
						//ActiveTime t;
						// t._from=ten
						//Shutdown
					}
				}

			}
		}

	}
	private: System::Void MyForm_Load(System::Object^ sender, System::EventArgs^ e) {

	}

		  
	};


}
