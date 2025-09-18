#include "STC15F2K60S2.H" //±?????
#include "sys.H"		  //±?????
#include "displayer.H"
#include "beep.H"
#include "music.H"
#include "key.H"
#include "stepmotor.H"
#include "vib.H"
#include "hall.H"
#include "adc.H"
#include "uart1.h"
#include "uart2.h"
#include "IR.h"
#include "DS1302.h"
#include "M24C02.h"
#include "FM_Radio.h"
#include "EXT.h"
#include "stepmotor.h"

code unsigned long SysClock = 11059200; // ±??????¨???????¤×÷?±??????(Hz)?????§±????????????????¤×÷?????¨?????±????????????
#ifdef _displayer_H_					// ???????é?????±±??????¨??????????????±í????‘?????????????????
code char decode_table[] = {
	// 数字 0-9
	0x3F, // 0: 00111111 (a,b,c,d,e,f亮)
	0x06, // 1: 00000110 (b,c亮)
	0x5B, // 2: 01011011 (a,b,g,e,d亮)
	0x4F, // 3: 01001111 (a,b,g,c,d亮)
	0x66, // 4: 01100110 (f,g,b,c亮)
	0x6D, // 5: 01101101 (a,f,g,c,d亮)
	0x7D, // 6: 01111101 (a,f,g,c,d,e亮)
	0x07, // 7: 00000111 (a,b,c亮)
	0x7F, // 8: 01111111 (全亮)
	0x6F, // 9: 01101111 (a,b,c,d,f,g亮)

	// 大写字母 A-Z（常用可显示的字母）
	0x77, // A (10): 01110111 (a,b,c,f,g亮)
	0x7C, // B (11): 01111100 (f,g,c,d,e亮，类似8少a)
	0x39, // C (12): 00111001 (a,f,e,d亮)
	0x5E, // D (13): 01011110 (b,c,d,e,g亮)
	0x79, // E (14): 01111001 (a,f,e,d,g亮)
	0x71, // F (15): 01110001 (a,f,e,g亮)
	0x3D, // G (16): 00111101 (a,f,g,c,d,e亮，6多g)
	0x76, // H (17): 01110110 (f,g,b,c,e亮)
	0x06, // I (18): 00000110 (同1)
	0x1E, // J (19): 00011110 (b,c,d,e亮)
	0x75, // K (20): 01110101 (f,g,b,c,e亮，类似H但e段不同)
	0x38, // L (21): 00111000 (f,e,d亮)
	0x15, // M (22): 00010101 (a,b,c,f,e亮，自定义简化版)
	0x54, // N (23): 01010100 (a,b,c,f,g亮，简化版)
	0x5C, // O (24): 01011100 (a,b,c,d,e亮，类似0少g)
	0x73, // P (25): 01110011 (a,b,f,g,e亮)
	0x6B, // Q (26): 01100111 (a,b,c,d,f,g亮，9多e)
	0x50, // R (27): 01010000 (a,b,f,g亮，简化版)
	0x6D, // S (28): 01101101 (同5)
	0x78, // T (29): 01111000 (f,g,e亮)
	0x3E, // U (30): 00111110 (b,c,d,e,f亮，类似0少a)
	0x1C, // V (31): 00011100 (b,c,d,e亮，简化版)
	0x2A, // W (32): 00101010 (自定义简化版，显示为双V)
	0x76, // X (33): 01110110 (同H)
	0x6E, // Y (34): 01101110 (b,c,d,f,g亮)
	0x5B, // Z (35): 01011011 (同2)

	// 小写字母（常用）
	0x5F, // a (36): 01011111 (类似9少b)
	0x7C, // b (37): 01111100 (同大写B)
	0x58, // c (38): 01011000 (f,e,d,g亮)
	0x5E, // d (39): 01011110 (同大写D)
	0x7B, // e (40): 01111011 (a,f,g,e,d亮，E多g)
	0x71, // f (41): 01110001 (同大写F)

	// 符号
	0x40, // - (42): 01000000 (g亮)
	0x80, // . (43): 10000000 (小数点亮)
	0x00, // 空格 (44): 00000000 (全灭)
	0x63  // = (45): 01100011 (g和d段亮)
};
#endif
code char pokemon_get_DAZE[] = {
	0x00, 0x08, 0x25, 0x04, 0x27, 0x04, 0x31, 0x04, 0x27, 0x04, 0x31, 0x04, 0x32, 0x04, 0x33, 0x20,
	0x00, 0x08, 0x26, 0x08, 0x31, 0x08, 0x33, 0x08, 0x32, 0x08, 0x31, 0x08, 0x27, 0x08, 0x25, 0x08,
	0x00, 0x08, 0x26, 0x04, 0x27, 0x04, 0x31, 0x04, 0x27, 0x04, 0x31, 0x04, 0x32, 0x04, 0x33, 0x20,
	0x00, 0x08, 0x26, 0x08, 0x31, 0x04, 0x33, 0x08, 0x35, 0x04, 0x00, 0x10, 0x00, 0x08, 0x26, 0x08,

	0x31, 0x04, 0x26, 0x04, 0x31, 0x04, 0x26, 0x04, 0x31, 0x04, 0x26, 0x04, 0x31, 0x04, 0x26, 0x04,
	0x26, 0x08, 0x31, 0x08, 0x31, 0x04, 0x32, 0x08, 0x27, 0x14, 0x00, 0x08, 0x26, 0x04, 0x26, 0x04,
	0x31, 0x04, 0x26, 0x04, 0x31, 0x04, 0x26, 0x04, 0x31, 0x04, 0x26, 0x04, 0x26, 0x04, 0x26, 0x04,
	0x33, 0x08, 0x33, 0x08, 0x32, 0x04, 0x31, 0x08, 0x27, 0x24,

	0x00, 0x10};
#define RECEIVE_LEN 5
int count = 0;
// Beep控制
int interp = 1;
int a = 0;
// LED控制
int LEDmode = 1;
int LEDchange = 1;
unsigned char led_val = 0x02;
int led_flow_reverse = 1;
// 串口控制
char data_recieved[RECEIVE_LEN];
char matched_data[] = {0xaa, 0x55};
char uart_data[3];
void myUart2_callback()
{
	char flag = data_recieved[2];
	char menu_select = data_recieved[3];
	char function = data_recieved[3];

	if (flag == 0x01 || flag == 0x02)
		LEDmode = 2;
	else if (flag == 0x00)
		LEDmode = 1;
	else if (flag == 0x03)
	{
		LEDmode = 3;
	}

	if (flag == 0x03)
	{
		interp = 0;
	}
}
void myDisplay_callback()
{
	char flag = data_recieved[2];
	char menu_select = data_recieved[3];
	if (flag == 0x00)
	{
		if (menu_select == 0x00)
			Seg7Print(23, 10, 30, 29, 18, 21, 30, 28);
		else if (menu_select == 0x01)
			Seg7Print(42, 13, 40, 29, 40, 38, 29, 42);
		else if (menu_select == 0x02)
			Seg7Print(42, 11, 27, 24, 32, 28, 40, 42);
		else if (menu_select == 0x03)
			Seg7Print(28, 17, 40, 18, 20, 36, 17, 42);
		else if (menu_select == 0x04)
			Seg7Print(42, 14, 36, 27, 29, 17, 42, 42);
	}
	else if (flag == 0x01)
		Seg7Print(23, 10, 30, 29, 18, 21, 30, 28);
	else if (flag == 0x03)
		Seg7Print(16, 14, 29, 42, 13, 10, 35, 14);
}
void myKey_callback()
{
	if (GetKeyAct(enumKey1) == enumKeyPress)
	{
		SetPlayerMode(enumModePlay);
	}
	if (GetKeyAct(enumKey2) == enumKeyPress)
	{
		SetPlayerMode(enumModePause);
	}
}
void beep_check()
{
	if (GetBeepStatus() == enumBeepFree && interp == 0)
	{
		a += 1;
	}

	if (a > 4)
	{
		a = 0;
	}

	if (interp == 0 && a == 1)
	{
		SetBeep(523, 25);
	}
	else if (interp == 0 && a == 2)
	{
		SetBeep(587, 25);
	}
	else if (interp == 0 && a == 3)
	{
		SetBeep(659, 25);
	}
	else if (interp == 0 && a == 4)
	{
		SetBeep(784, 80);
		interp = 1;
	}
}
void myLED_callback()
{
	// 初始界面
	if (LEDmode == 1 && LEDchange == 1)
	{
		LedPrint(0x55);
	}
	else if (LEDmode == 1 && LEDchange == -1)
	{
		LedPrint(0xaa);
	}
	else if (LEDmode == 2)
	{
		LedPrint(led_val);
	}
	else if (LEDmode == 3 && LEDchange == 1)
	{
		LedPrint(0xFF);
	}
	else if (LEDmode == 3 && LEDchange == -1)
	{
		LedPrint(0x00);
	}
	LEDchange *= -1;

	// 流水灯
	if (led_val < 0x80 && led_flow_reverse == 1)
	{
		led_val = led_val << 1;
	}
	else if (led_val > 0x01 && led_flow_reverse == -1)
	{
		led_val = led_val >> 1;
	}
	else if (led_val == 0x80 || led_val == 0x01)
	{
		led_flow_reverse *= -1;
	}
}
void my10mS_callback()
{
	// Beep轮询
	beep_check();
}
void myVib_callback()
{
	char k = GetVibAct();
	if (k == enumVibQuake)
	{
		uart_data[0] = 0xaa;
		uart_data[1] = 0x55;
		uart_data[2] = 0x01;
		Uart2Print(uart_data, 3);
	}
}
void myHall_callback()
{
	char k = GetHallAct();
	if (k == enumHallGetClose)
	{
		uart_data[0] = 0xaa;
		uart_data[1] = 0x55;
		uart_data[2] = 0x02;
		Uart2Print(uart_data, 3);
		// Beep
		interp = 0;
	}
	else if (k == enumHallGetAway)
	{
		uart_data[0] = 0xaa;
		uart_data[1] = 0x55;
		uart_data[2] = 0x03;
		Uart2Print(uart_data, 3);
	}
}

void main()
{
	Uart2Init(115200, Uart2UsedforEXT);
	displayerInit();
	keyInit();
	VibInit();
	MusicPlayerInit();
	BeepInit();
	HallInit();
	SetDisplayerArea(0, 7);

	SetUart2Rxd(data_recieved, RECEIVE_LEN, matched_data, 2);

	SetMusic(110, 0xFA, pokemon_get_DAZE, sizeof(pokemon_get_DAZE), enumMscDrvLed);

	SetEventCallBack(enumEventHall, myHall_callback);
	SetEventCallBack(enumEventVib, myVib_callback);
	SetEventCallBack(enumEventKey, myKey_callback);
	SetEventCallBack(enumEventUart2Rxd, myUart2_callback);
	SetEventCallBack(enumEventSys1S, myDisplay_callback);
	SetEventCallBack(enumEventSys100mS, myLED_callback);
	SetEventCallBack(enumEventSys10mS, my10mS_callback);

	MySTC_Init();
	while (1)
	{
		MySTC_OS();
	}
}