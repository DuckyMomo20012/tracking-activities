
#include <iostream>
//#include<Windows.h>
#include<vector>
#include<fstream>
#include<atlimage.h>
//#include<afxdialogex.h>
#include<unordered_map>
#include"wintoastlib.h"
#include<string>
#define _AFXDLL

using namespace std;
using namespace WinToastLib;

class WinToastHandler : public WinToastLib::IWinToastHandler
{
public:
    WinToastHandler() {}
    
    // Public interfaces
    void toastActivated() const override {}
    void toastActivated(int actionIndex) const override {
        wchar_t buf[250];
        swprintf_s(buf, L"Button clicked: %d", actionIndex);
        
    }
    void toastDismissed(WinToastDismissalReason state) const override {}
    void toastFailed() const override {}

};

void TakeScreenShot(const std::string& path)
{
    //setting to the screen shot
    keybd_event(VK_SNAPSHOT, 0x45, KEYEVENTF_EXTENDEDKEY, 0);
    keybd_event(VK_SNAPSHOT, 0x45, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0);

    //handler of the bitmap that save the screen shot
    HBITMAP hBitmap;

    //I have to give for it time to make it work
    Sleep(100);

    //take the screen shot
    OpenClipboard(NULL);

    //save the screen shot in the bitmap handler 
    hBitmap = (HBITMAP)GetClipboardData(CF_BITMAP);

    //relese the screen shot
    CloseClipboard();

    std::vector<BYTE> buf;
    IStream* stream = NULL;
    HRESULT hr = CreateStreamOnHGlobal(0, TRUE, &stream);
    CImage image;
    ULARGE_INTEGER liSize;

    // screenshot to jpg and save to stream
    image.Attach(hBitmap);
    image.Save(stream, Gdiplus::ImageFormatJPEG);
    IStream_Size(stream, &liSize);
    DWORD len = liSize.LowPart;
    IStream_Reset(stream);
    buf.resize(len);
    IStream_Read(stream, &buf[0], len);
    stream->Release();

    // put the imapge in the file
    std::fstream fi;
    fi.open(path, std::fstream::binary | std::fstream::out);
    fi.write(reinterpret_cast<const char*>(&buf[0]), buf.size() * sizeof(BYTE));
    fi.close();
}

string encrypted(string pass)
{
    string str;
    for (int i = 0; i < pass.length(); i++)
    {
        str+=(pass[i] + 12);
    }
    return str;
}

void notification() {
    if (!WinToast::isCompatible()) {
        std::wcout << L"Error, your system in not supported!" << std::endl;
    }

    WinToast::instance()->setAppName(L"WinToastExample");
    const auto aumi = WinToast::configureAUMI(L"mohabouje", L"wintoast", L"wintoastexample", L"20161006");
    WinToast::instance()->setAppUserModelId(aumi);
    
    if (!WinToast::instance()->initialize()) {
        std::wcout << L"Error, could not initialize the lib!" << std::endl;
    }

    WinToastHandler* handler = new WinToastHandler();
    WinToastTemplate templ = WinToastTemplate(WinToastTemplate::Text01);
    //templ.setImagePath(L"C:/example.png");
    templ.setTextField(L"Con 10 phut la het gio ", WinToastTemplate::FirstLine);
    //templ.setTextField(L"subtitle", WinToastTemplate::SecondLine);
    
    //templ.setDuration(WinToastTemplate::Short);

    if (!WinToast::instance()->showToast(templ,handler)) {
        std::wcout << L"Error: Could not launch your toast notification!" << std::endl;
    }

}
int main()
{
    cout << "Hello World!\n";
    cout << "Are you sure" << endl;

    string str;
    cin >> str;

    string pass = "vuquanghop";
    string hash = encrypted(pass);
    cout << hash;
    
    if (encrypted(str) == hash)
    {
        cout << "Login"<<endl;
    }

    TakeScreenShot("image.jpg");

    notification();
    Sleep(1);
    return 0;
}


