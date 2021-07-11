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

static bool loginFlag;
static void wait15Second() {
		Sleep(15000);
		if (loginFlag ==false)
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
		}
	public:
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

	protected:

	protected:

	private:
		
		System::ComponentModel::Container^ components;

#pragma region Windows Form Designer generated code
		
		void InitializeComponent(void)
		{
			System::ComponentModel::ComponentResourceManager^ resources = (gcnew System::ComponentModel::ComponentResourceManager(MyForm::typeid));
			this->textBox1 = (gcnew System::Windows::Forms::TextBox());
			this->button1 = (gcnew System::Windows::Forms::Button());
			this->label1 = (gcnew System::Windows::Forms::Label());
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
			// MyForm
			// 
			resources->ApplyResources(this, L"$this");
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->BackColor = System::Drawing::SystemColors::ActiveCaption;
			this->ControlBox = false;
			this->Controls->Add(this->label1);
			this->Controls->Add(this->button1);
			this->Controls->Add(this->textBox1);
			this->Name = L"MyForm";
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
			this->Hide();
			///May be work
			chrono::hours oneHour(1);
			this_thread::sleep_for(oneHour);
			this->Show();
			
			loginFlag = true;



		}
		else if(convert.marshal_as<string>(textBox1->Text) != ParentPass){
			
			loginFlag = false;
			wrongPass++;


			int getHour = 23;
			int getMinute = 30;
			time_t timer = time(0);
			tm* now = localtime(&timer);
			Time currentTime = Time(now->tm_hour, now->tm_min);

			//Doc file txt xem co o trong thoi gian su dung hay khong
			//Trong 1 phien hd chi can doc 1 lan

			bool accept=true;
			// gia su ko cho phep dung
			//Neu khong duoc su dung
			if (!accept)
			{

				// New thread zone and shutdown
				if (th1 == nullptr)
				{
					th1 = gcnew Thread(gcnew ThreadStart(wait15Second));
					th1->Start();

				}

				//Cont
				


			}
			//gia su cho dung
			//Nau duoc su dung
			else if (accept==true)
			{
				if (convert.marshal_as<string>(textBox1->Text) == childPass)
				{
					this->textBox1->Hide();
					this->button1->Hide();
					this->label1->Text = L"Ban da dang nhap thanh cong";
					this->label1->Show();
					//Kiem tra con bao lau thi het gio
					String^ msg;
					MessageBox::Show(msg, "Time Left"); //thong bao


					//Thong bao xong thi dong Login page
					Sleep(10);
					//this->Hide(); //Chay ngam


					//while(moi 5 phut){
					// 
					// Sleep(5phut)
					// Goi ham lay file txt tu Drive, vi wifi co the lag nen moi nguoi cho Sleep() mot luc, tuy tinh hinh
					// Sleep()
					// 
					// 
					//chup man hinh va ghi vo thu muc Upload, chua co thi tao
					// Upload len, nho upload xong phai tu tat script vua chay
					// 
					// 
					//Doc file txt xem co thay doi hay khong, co thi cap nhat
					//if(co thay doi){
					// cap nhat;
					// Thong bao; 
					//}
					//

					//}

					//this->Close();

				}
				else {
					if (wrongPass == 3)
					{
						//C2.1.2.1
						//Neu sai 3 lan se chay vo day
						//Lay thoi gian hien tai cong them 10p roi ghi vo txt 
						

						this->Close(); //Close roi moi shutdown
						//Shutdown
						


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
		this->label1->Hide();
	}

		  
	
};


}
