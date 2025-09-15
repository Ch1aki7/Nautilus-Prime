#include "STC15F2K60S2.H" //必须。
#include "sys.H"		  //必须。
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

code unsigned long SysClock = 11059200; // 必须。定义系统工作时钟频率(Hz)，用户必须修改成与实际工作频率（下载时选择的）一致
#ifdef _displayer_H_					// 显示模块选用时必须。（数码管显示译码表，用戶可修改、增加等）
code char decode_table[] = {
	0x3F, // 0
	0x06, // 1
	0x5B, // 2
	0x4F, // 3
	0x66, // 4
	0x6D, // 5
	0x7D, // 6
	0x07, // 7
	0x7F, // 8
	0x6F, // 9
	0x76, // H (10)
	0x38, // L (11)
	0x40, // - (12)
	0x00, // 空 (13)
	0x1C};
#endif


void main()
{

	MySTC_Init();
	while (1)
	{
		MySTC_OS();
	}
}