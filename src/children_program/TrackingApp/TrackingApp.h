#pragma once
#include <msclr\marshal_cppstd.h>
#include<thread>
#include<chrono>
#include<ctime>
#include"ActiveTime.h"
#include<stdlib.h>
#include"screenShot.h"
#include<WinUser.h>
namespace TrackingApp {

	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;
	using namespace std;
	using namespace System::Threading;


static bool loginFlag;
static bool notLogin = true;
static void outTime() {
	Sleep(60000);
	system("c:\\windows\\system32\\shutdown /s");
}
static void waitOneMinute() {
		Sleep(60000);
		if (notLogin == true)
		{
			system("c:\\windows\\system32\\shutdown /s");
		}
	}
static void wait15Second() {
		Sleep(15000);
		if (loginFlag == false)
		{
			system("c:\\windows\\system32\\shutdown /s");
		}
	}
static void shutDownPC() {
		Sleep(10000);
		system("c:\\windows\\system32\\shutdown /s");
	}
	/// <summary>
	/// Summary for TrackingApp
	/// </summary>
	public ref class TrackingApp : public System::Windows::Forms::Form
	{
	public:
		TrackingApp(void)
		{
			InitializeComponent();
			//
			//TODO: Add the constructor code here
			//
		}
		int wrongPass = 0;

	protected:
		/// <summary>
		/// Clean up any resources being used.
		/// </summary>
		~TrackingApp()
		{
			if (components)
			{
				delete components;
			}
		}
	private: System::Windows::Forms::TextBox^ textBox1;
	private: System::Windows::Forms::Button^ button1;
	private: System::Windows::Forms::Label^ label1;
	private: System::Windows::Forms::Label^ label2;
	protected:

	private:
		/// <summary>
		/// Required designer variable.
		/// </summary>
		System::ComponentModel::Container ^components;

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
			this->label2 = (gcnew System::Windows::Forms::Label());
			this->SuspendLayout();
			// 
			// textBox1
			// 
			this->textBox1->Location = System::Drawing::Point(24, 109);
			this->textBox1->Name = L"textBox1";
			this->textBox1->Size = System::Drawing::Size(160, 22);
			this->textBox1->TabIndex = 0;
			// 
			// button1
			// 
			this->button1->Location = System::Drawing::Point(190, 100);
			this->button1->Name = L"button1";
			this->button1->Size = System::Drawing::Size(80, 41);
			this->button1->TabIndex = 1;
			this->button1->Text = L"Login";
			this->button1->UseVisualStyleBackColor = true;
			this->button1->Click += gcnew System::EventHandler(this, &TrackingApp::button1_Click);
			// 
			// label1
			// 
			this->label1->AutoSize = true;
			this->label1->Font = (gcnew System::Drawing::Font(L"Microsoft Sans Serif", 12, System::Drawing::FontStyle::Regular, System::Drawing::GraphicsUnit::Point,
				static_cast<System::Byte>(0)));
			this->label1->Location = System::Drawing::Point(12, 106);
			this->label1->Name = L"label1";
			this->label1->Size = System::Drawing::Size(274, 25);
			this->label1->TabIndex = 2;
			this->label1->Text = L"Bạn đã đăng nhập thành công";
			this->label1->TextAlign = System::Drawing::ContentAlignment::MiddleCenter;
			// 
			// label2
			// 
			this->label2->AutoSize = true;
			this->label2->Font = (gcnew System::Drawing::Font(L"Microsoft Sans Serif", 16.2F, System::Drawing::FontStyle::Regular, System::Drawing::GraphicsUnit::Point,
				static_cast<System::Byte>(0)));
			this->label2->Location = System::Drawing::Point(66, 49);
			this->label2->Name = L"label2";
			this->label2->Size = System::Drawing::Size(154, 32);
			this->label2->TabIndex = 3;
			this->label2->Text = L"Đăng nhập";
			this->label2->TextAlign = System::Drawing::ContentAlignment::MiddleCenter;
			// 
			// TrackingApp
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(8, 16);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(308, 253);
			this->ControlBox = false;
			this->Controls->Add(this->label2);
			this->Controls->Add(this->label1);
			this->Controls->Add(this->button1);
			this->Controls->Add(this->textBox1);
			this->Name = L"TrackingApp";
			this->ShowInTaskbar = false;
			this->Text = L"TrackingApp";
			this->Load += gcnew System::EventHandler(this, &TrackingApp::TrackingApp_Load);
			this->ResumeLayout(false);
			this->PerformLayout();

		}
		Thread^ th1;
		Thread^ waitLogin;
		Thread^ shutdown;
		Thread^ shutdownThread;
#pragma endregion
	private: System::Void button1_Click(System::Object^ sender, System::EventArgs^ e) {

		//Đây là mật khẩu đã được mã hoá
		//Mật khẩu của con là 4321
		string childPass = "@?>=";
		//Mật khẩu của cha là 1234
		string ParentPass = "=>?@";
		msclr::interop::marshal_context convert;

		//Mã hoá mật khẩu người dùng nhập vào
		std::string encrypted = encrypt(convert.marshal_as<string>(textBox1->Text));

		//Chép thời gian user sử dụng lần cuối vào file history.txt
		if (getlineEndTime() != "") {
			writeEndTimeToFile(".\\Downloads\\history.txt", readEndTime());
			savelineEndTime();
		}

		//Nếu mật khẩu nhập là mật khẩu cha
		if (encrypted == ParentPass) {

			notLogin = false;
			loginFlag = true;
			MessageBox::Show("Phu huynh dang nhap thanh cong\n Vui long tat hop thoai nay ");
			this->Hide();
			///Sleep 1 hour
			chrono::hours oneHour(1);
			this_thread::sleep_for(oneHour);
			this->Show();

		}
		//Nếu mật khẩu khác mật khẩu cha
		else if (encrypted != ParentPass) {

			loginFlag = false;
			wrongPass++;

			
			// <Cập nhật file từ Cloud>
			bool stop = false;
			if (stop == false)
			{
				stop = true;
				WinExec("python downloadConfig.py", SW_HIDE);
				//Sleep(5000);
			}
			//<Cập nhật file từ Cloud/>

			//Đọc file activate.txt
			std::vector<ActiveTime> listActiveTime;
			readFile(".\\Downloads\\activate.txt", listActiveTime);

			Time now = Time();
			
			if (listActiveTime.size() == 0) {
				system("c:\\windows\\system32\\shutdown /s");
				MessageBox::Show("Hom nay phu huynh chua cap nhat thoi gian su dung","Thong bao");
				this->Close();
				
			}

			//Tạo 1 biến kiểm tra xem có được sử dụng hay không

			bool checkInUsed = isInUseTime(now, listActiveTime);
			Time startComputer = now;


			bool accept = checkInUsed;

			//Nếu không được sử dụng
			if (!accept)
			{
				notLogin = false;
				// Tạo một luồng mới và tắt máy
				if (th1 == nullptr)
				{
					th1 = gcnew Thread(gcnew ThreadStart(wait15Second));
					th1->Start();
				}
				String^ msg = "Con " + nextTimeToRun(now) + " phut nua la den gio mo may";
				MessageBox::Show(msg, "Time Left"); //thong bao
			}

			//Nếu được sử dụng
			else if (accept == true)
			{
				//Kiểm tra xem có phải mật khẩu của trẻ hay không
				if (encrypted == childPass)
				{
					notLogin = false;
					this->textBox1->Hide();
					this->button1->Hide();
					this->label1->Text = L"Ban da dang nhap thanh cong";
					this->label1->Show();

					//Kiểm tra có phải đang trong thời gian Interrupt hay không
					int interruptTime = interruptTimeRemain(now);
					if (interruptTime < 0) {
						shutdown = gcnew Thread(gcnew ThreadStart(shutDownPC));
						shutdown->Start();
						interruptTime = interruptTime * -1;
						MessageBox::Show("May tinh van dang trong thoi gian nghi\nCon " + interruptTime + " phut la den gio mo may", "Thong bao");
						this->Close();
						system("c:\\windows\\system32\\shutdown /s");
						System::Environment::Exit(0);
					}
					//Nếu không
					else {
						writeStartTimeToFile(".\\Downloads\\history.txt", now);

						//Kiểm tra còn bao lâu thì hết giờ
						int minuteRemain = timeRemain(startComputer, now, ".\\Downloads\\activate.txt");

						//Thông báo ra người dùng
						String^ msg = "Con " + minuteRemain + " phut nua la het gio";
						MessageBox::Show(msg, "Time Left"); //thong bao


						//Thông báo xong thì đóng Login page và vào chế độ chạy ẩn
						Sleep(10);
						this->Hide();

						std::string hashString = hashFile();
						//Gọi chương trình theo dõi bàn phím
						WinExec("python keyLogger.py", SW_HIDE);

						// Cứ mỗi 1 phút 
						while (true) {
							//Sẽ gọi chương trình cập nhật lại dữ liệu
							WinExec("python downloadConfig.py", SW_HIDE);
							Sleep(30000);


							//Nếu dữ liệu được cập nhật
							string newHashString = hashFile();
							if (hashString != newHashString) {
								hashString = newHashString;
								
								MessageBox::Show("Thoi gian su dung vua duoc update", "Thong bao");
								Sleep(2000);
								readFile(".\\Downloads\\activate.txt", listActiveTime);
								Time now = Time();
								if (listActiveTime.size() == 0) {
									system("c:\\windows\\system32\\shutdown /s");
									MessageBox::Show("Hom nay phu huynh chua cap nhat thoi gian su dung", "Thong bao");
									this->Close();

								}
							}

							//Nếu không được cập nhật
							//Chụp màn hình hiện tạ
							now = getTime();
							std::string path = ".\\Upload\\" + now.fileName() + ".jpg";
							TakeScreenShot(path);
							//Gọi chương trình gửi ảnh và đưa ảnh, các file dữ liệu lên Cloud
							WinExec("python uploadImage.py", SW_HIDE);
							WinExec("python uploadConfig.py", SW_HIDE);

							Sleep(30000);

							//Lưu sự kiện người dùng dùng lần cuối,
							saveEndTime();
							

							//Nếu thời gian dưới 1phút thì thông báo ra màn hình và chạy luồng tắt máy
							int minuteRemain = timeRemain(startComputer, now, ".\\Downloads\\activate.txt");
							if (minuteRemain <= 1) {
								now = getTime();
								saveEndTime();
								
								shutdownThread = gcnew Thread(gcnew ThreadStart(outTime));
								shutdownThread->Start();
								MessageBox::Show("Con 1 phut nua la het gio", "Thong bao");
								

							}
						}

					}
				}
				else {
					//Nếu sai mật khẩu 3 lần thì tắt máy
					if (wrongPass == 3)
					{

						writeWrongPassFile();
						
						system("c:\\windows\\system32\\shutdown /s");
						MessageBox::Show("Sai mat khau 3 lan, vui long cho 10p sau de tiep tuc", "Thong bao");
						this->Close(); //Close roi moi shutdown
						Application::Exit();
						System::Environment::Exit(0);
						
						
					}
				}

			}
		}
	}
private: System::Void TrackingApp_Load(System::Object^ sender, System::EventArgs^ e) {
	
	//Hàm này sẽ được gọi đầu tiên

	//<wrongPass>
	
	Time lastWrongpass = readWrongPassFile();

	Time now = getTime();
	int timeFromLastWrongpass = now.convertToMin() - lastWrongpass.convertToMin();
	//Nếu trẻ nhấp ai 3 lần thì lần mở máy tiếp theo, đoạn code này sẽ được chạy
	if (timeFromLastWrongpass < 10) {
		//Tạo một luồng tắt máy 
		shutdown = gcnew Thread(gcnew ThreadStart(shutDownPC));
		shutdown->Start();
		MessageBox::Show("May tinh van dang dong do sai mat khau\nCon " + (10 - timeFromLastWrongpass) + " phut la den gio mo may", "Thong bao");

		this->Close();
		system("c:\\windows\\system32\\shutdown /s");
		System::Environment::Exit(0);

	}
	//</wrongPass


	//<handle waitLogin>
	//Nếu người dùng không đăng nhập trong vòng 1 phút, máy tính sẽ tắt
	if (waitLogin == nullptr)
	{
		//Tạo một luồng chờ 10 phút
		waitLogin = gcnew Thread(gcnew ThreadStart(waitOneMinute));
		waitLogin->Start();
	}
	//<handle waitLogin/>


	this->label1->Hide();
}
};
}
