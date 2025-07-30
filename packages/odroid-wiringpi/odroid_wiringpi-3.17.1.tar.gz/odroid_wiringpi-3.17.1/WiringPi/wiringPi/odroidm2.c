/*----------------------------------------------------------------------------*/
//
//
//	WiringPi ODROID-M2 Board Control file (ROCKCHIP 64Bits Platform)
//
//
/*----------------------------------------------------------------------------*/
/*******************************************************************************
Copyright (C) 2024 Steve Jeong <steve@how2flow.net>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*******************************************************************************/
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <asm/ioctl.h>
#include <sys/mman.h>
#include <sys/stat.h>
/*----------------------------------------------------------------------------*/
#include "softPwm.h"
#include "softTone.h"
/*----------------------------------------------------------------------------*/
#include "wiringPi.h"
#include "odroidm2.h"
/*----------------------------------------------------------------------------*/
// wiringPi gpio map define
/*----------------------------------------------------------------------------*/
static const int pinToGpio[64] = {
	// wiringPi number to native gpio number
	124,106,	//  0 |  1 : GPIO3_D4, GPIO3_B2
	125,139,	//  2 |  3 : GPIO3_D5, GPIO4_B3
	42,  43,	//  4 |  5 : GPIO1_B2, GPIO1_B3
	28,  24,	//  6 |  7 : GPIO0_D4, GPIO0_D0
	135,134,	//  8 |  9 : GPIO4_A7, GPIO4_A6
	29,  44,	// 10 | 11 : GPIO0_D5, GPIO1_B4
	122,121,	// 12 | 13 : GPIO3_D2, GPIO3_D1
	123,112,	// 14 | 15 : GPIO3_D3, GPIO3_C0
	113, -1,	// 16 | 17 : GPIO3_C1
	-1,  -1,	// 18 | 19 :
	-1,  47,	// 20 | 21 : , GPIO1_B7
	46, 120,	// 22 | 23 : GPIO1_B6, GPIO3_D0
	119, -1,	// 24 | 25 : GPIO3_C7,
	140,141,	// 26 | 27 : GPIO4_B4, GPIO4_B5
	-1,  -1,	// 28 | 29 :
	136,137,	// 30 | 31 : GPIO4_B0, GPIO4_B1
	// EXT_PINS:
	116, 117, 118, -1, // 32...35
	// Padding:
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,	-1,// 36...49
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 // 50...63
};

static const int phyToGpio[64] = {
	// physical header pin number to native gpio number
	-1,		//  0
	-1,  -1,	//  1 |  2 : 3.3V, 5.0V
	135, -1,	//  3 |  4 : GPIO4_A7, 5.0V
	134, -1,	//  5 |  6 : GPIO4_A6, GND
	24, 112,	//  7 |  8 : GPIO0_D0, GPIO3_C0
	-1, 113,	//  9 | 10 : GND, GPIO3_C1
	124,106,	// 11 | 12 : GPIO3_D4, GPIO3_B2
	125, -1,	// 13 | 14 : GPIO3_D5, GND
	139, 42,	// 15 | 16 : GPIO4_B3, GPIO1_B2
	-1,  43,	// 17 | 18 : 3.3V, GPIO1_B3
	122, -1,	// 19 | 20 : GPIO3_D2, GND
	121, 28,	// 21 | 22 : GPIO3_D1, GPIO0_D4
	123, 29,	// 23 | 24 : GPIO3_D3, GPIO0_D5
	-1,  44,	// 25 | 26 : GND, GPIO1_B4
	136,137,	// 27 | 28 : GPIO4_B0, GPIO4_B1
	47,  -1,	// 29 | 30 : GPIO1_B7, GND
	46, 140,	// 31 | 32 : GPIO1_B6, GPIO4_B4
	120, -1,	// 33 | 34 : GPIO3_D0, GND
	119,141,	// 35 | 36 : GPIO3_C7, GPIO4_B5
	-1,  -1,	// 37 | 38 : ADC.AIN4, 1.8V REF
	-1,  -1,	// 39 | 40 : GND, ADC.AIN5

	// Not used
	-1, -1, -1, -1, -1, -1, -1, -1,	-1, -1, // 41...50

	// EXT_PINS
	116, 117, 118, // 51...53

	// Not used
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1	// 54...63
};

static const char *pinToPwm[64] = {
	// wiringPi number to pwm group number
		"None", "fd8b0030",	   // GPIO3_D4, GPIO3_B2 (PWM3)
		"None", "febf0030",	   // GPIO3_D5, GPIO4_B3 (PWM15)
		"None", "None",		   // GPIO1_B2, GPIO1_B3
		"None", "febd0030",	   // GPIO0_D4, GPIO0_D0 (PWM7)
		"None", "None",        // GPIO4_A7, GPIO4_A6
		"None", "None",        // GPIO0_D5, GPIO1_B4
		"None", "None",        // GPIO3_D2, GPIO3_D1
		"None", "None",        // GPIO3_D3, GPIO3_C0
		"None", "None",		   // GPIO3_C1
		"None", "None",		   //
		"None", "None",		   // , GPIO1_B7
		"None", "febe0000",	   // GPIO1_B6, GPIO3_D0 (PWM8)
		"None", "None",		   // GPIO3_C7,
		"None", "None",        // GPIO4_B4, GPIO4_B5
		"None", "None",        //
		"None", "None",        // GPIO4_B0, GPIO4_B1
	// Padding:
	"None","None","None","None","None","None","None","None","None","None","None","None","None","None","None","None", // 32...47
	"None","None","None","None","None","None","None","None","None","None","None","None","None","None","None","None"  // 48...63
};

static const int pinToPwmNum[64] = {
	// wiringPi number to pwm pin number
	 -1,  3,	//  0 |  1 : GPIO3_D4, GPIO3_B2 (PWM3)
	 -1,  2,	//  2 |  3 : GPIO3_D5, GPIO4_B3 (PWM15)
	 -1, -1,	//  4 |  5 : GPIO1_B2, GPIO1_B3
	 -1,  1,	//  6 |  7 : GPIO0_D4, GPIO0_D0 (PWM7)
	 -1, -1,	//  8 |  9 : GPIO4_A7, GPIO4_A6
	 -1, -1,	// 10 | 11 : GPIO0_D5, GPIO1_B4
	 -1, -1,	// 12 | 13 : GPIO3_D2, GPIO3_D1
	 -1, -1,	// 14 | 15 : GPIO3_D3, GPIO3_C0
	 -1, -1,	// 16 | 17 : GPIO3_C1
	 -1, -1,	// 18 | 19 :
	 -1, -1,	// 20 | 21 : , GPIO1_B7
	 -1,  0,	// 22 | 23 : GPIO1_B6, GPIO3_D0 (PWM8)
	 -1, -1,	// 24 | 25 : GPIO3_C7,
	 -1, -1,	// 26 | 27 : GPIO4_B4, GPIO4_B5
	 -1, -1,	// 28 | 29 :
	 -1, -1,	// 30 | 31 : GPIO4_B0, GPIO4_B1
	// Padding:
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,	// 32...47
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1	// 48...63
};

static char pwmPinPath[10][(BLOCK_SIZE)] = {
	"","",
	"","",
	// Padding:
	"None","None","None",
	"None","None","None"
};

static char setupedPwmPinPath[10][BLOCK_SIZE] = {
	"None","None",
	"None","None",
	"None","None",
	"None","None",
	"None","None"
};
/*----------------------------------------------------------------------------*/
//
// Global variable define
//
/*----------------------------------------------------------------------------*/
/* ADC file descriptor */
static int adcFds[2];

/* GPIO mmap control. Actual GPIO bank number. */
static volatile uint32_t *gpio[5];

/* GRF(General Register Files) base addresses to control GPIO modes */
static volatile uint32_t *grf[2];

/* CRU(Clock & Reset Unit) base addresses to control CLK mode */
static volatile uint32_t *cru[2];

/* wiringPi Global library */
static struct libodroid	*lib = NULL;

/* pwm sysnode */
static DIR *pwm;
static struct dirent *pwmchip;
/* pwm params */
static char sysPwmPath[(BLOCK_SIZE / 4)];
static char pwmExport[(BLOCK_SIZE / 16)];
static char pwmUnexport[(BLOCK_SIZE / 16)];
static char pwmPeriod[(BLOCK_SIZE / 16)];
static char pwmDuty[(BLOCK_SIZE / 16)];
static unsigned int pwmClock;
static unsigned int pwmRange;
/*----------------------------------------------------------------------------*/
// Function prototype define
/*----------------------------------------------------------------------------*/
static int	gpioToShiftRegBy32	(int pin);
static int	gpioToShiftRegBy16	(int pin);
static void	setClkState	(int bank, int state);
static int	setIomuxMode 	(int pin, int mode);
/*----------------------------------------------------------------------------*/
// Function of pwm define
/*----------------------------------------------------------------------------*/
static int	pinToSysPwmPath	(int pin);
static int	pwmSetup (int pin);
static int	pwmRelease (int pin);
/*----------------------------------------------------------------------------*/
// wiringPi core function
/*----------------------------------------------------------------------------*/
static int		_getModeToGpio		(int mode, int pin);
static int		_pinMode		(int pin, int mode);
static int		_getDrive		(int pin);
static int		_setDrive		(int pin, int value);
static int		_getAlt			(int pin);
static int		_getPUPD		(int pin);
static int		_pullUpDnControl	(int pin, int pud);
static int		_digitalRead		(int pin);
static int		_digitalWrite		(int pin, int value);
static int		_pwmWrite		(int pin, int value);
static int		_analogRead		(int pin);
static int		_digitalWriteByte	(const unsigned int value);
static unsigned int	_digitalReadByte	(void);
static void		_pwmSetRange	(unsigned int range);
static void		_pwmSetClock	(int divisor);
/*----------------------------------------------------------------------------*/
// board init function
/*----------------------------------------------------------------------------*/
static 	void init_gpio_mmap	(void);
static 	void init_adc_fds	(void);
void init_odroidm2 	(struct libodroid *libwiring);
/*----------------------------------------------------------------------------*/
//
// for the offset to the GPIO bit
//
/*----------------------------------------------------------------------------*/
static int gpioToShiftRegBy32 (int pin)
{
	return pin % 32;
}
/*----------------------------------------------------------------------------*/
//
// for the offset to the GPIO bit
//
/*----------------------------------------------------------------------------*/
static int gpioToShiftRegBy16 (int pin)
{
	return pin % 16;
}
/*----------------------------------------------------------------------------*/
//
// config pwm sys path. "/sys/class/pwm/pwmchip?"
//
/*----------------------------------------------------------------------------*/
static int pinToSysPwmPath (int pin)
{
	const char *pwmGroup;
	char pwmLinkSrc[(BLOCK_SIZE / 8)];
	char pwmPath[(BLOCK_SIZE / 8)];
	int sz_link;

	memset(pwmLinkSrc, 0, sizeof(pwmLinkSrc));
	memset(pwmPath, 0, sizeof(pwmPath));

	pwmGroup = pinToPwm[pin];
	pwm = opendir("/sys/class/pwm");
	if (pwm == NULL) {
		printf("need to set device: pwm\n");
		return -1;
	}

	while (1) {
		pwmchip = readdir(pwm);

		if (pwmchip == NULL) {
			break;
		}

		if (strlen(pwmchip->d_name) <= 2)
			continue;

		sprintf(pwmPath, "%s/%s", "/sys/class/pwm", pwmchip->d_name);
		sz_link = readlink(pwmPath, pwmLinkSrc, sizeof(pwmLinkSrc));
		if (sz_link < 0) {
			perror("Read symbolic link fail");
			return sz_link;
		}

		if (strstr(pwmLinkSrc, pwmGroup) != NULL) {
			strncpy(sysPwmPath, pwmPath, (sizeof(sysPwmPath) - 1));
			break;
		}
	}
	closedir(pwm);

	return 0;
}

static int pwmSetup (int pin) {
	char cmd[(BLOCK_SIZE * 2)];
	int pwmPin, ret;

	memset(cmd, 0, sizeof(cmd));
	memset(pwmExport, 0, sizeof(pwmExport));

	if ((ret = pinToSysPwmPath(pin)) < 0) {
		perror("set pwm dtb overlays");
		return ret;
	}

	if (strstr(sysPwmPath, "pwmchip") == NULL) {
		printf("config pwm dtb overlays\n");
		return -1;
	}

	pwmPin = pinToPwmNum[pin];
	pwmClock = (M2_PWM_INTERNAL_CLK / 2);
	sprintf(pwmExport, "%d", 0);
	sprintf(pwmPinPath[pwmPin], "%s/pwm%d", sysPwmPath, 0);
	strncpy(setupedPwmPinPath[pwmPin], pwmPinPath[pwmPin], (BLOCK_SIZE - 1));
#ifdef ANDROID
	sprintf(cmd, "su -s sh -c %s %s", SYS_ACCESS_SCRIPT, pwmPinPath[pwmPin]);
#else
	sprintf(cmd, "sudo sh %s %s", SYS_ACCESS_SCRIPT, pwmPinPath[pwmPin]);
#endif
	inputToSysNode(sysPwmPath, "export", pwmExport);
	system(cmd);
	printf("PWM/pin%d: Don't change to gpio mode with overlay registered.\n", pin);

	return 0;
}

static int pwmRelease (int pin) {
	int pwmPin, ret;

	if ((ret = pinToSysPwmPath(pin)) < 0) {
		return ret;
	}

	if (strstr(sysPwmPath, "pwmchip") == NULL) {
		return -1;
	}

	pwmPin = pinToPwmNum[pin];
	sprintf(pwmUnexport, "%d", (pwmPin % 2));
	sprintf(pwmPinPath[pwmPin], "%s/pwm%d", sysPwmPath, (pwmPin % 2));
	if ((pwm = opendir(pwmPinPath[pwmPin])) != NULL) {
		inputToSysNode(pwmPinPath[pwmPin], "enable", "0");
		inputToSysNode(sysPwmPath, "unexport", pwmUnexport);
		closedir(pwm);
	}

	return 0;
}
/*----------------------------------------------------------------------------*/
static int _getModeToGpio (int mode, int pin)
{
	if (pin > 255)
		return msg(MSG_ERR, "%s : Invalid pin number %d\n", __func__, pin);

	switch (mode) {
	/* Native gpio number */
	case	MODE_GPIO:
		return	pin;
	/* Native gpio number for sysfs */
	case	MODE_GPIO_SYS:
		return	lib->sysFds[pin] != -1 ? pin : -1;
	/* wiringPi number */
	case	MODE_PINS:
		return	pin < 64 ? pinToGpio[pin] : -1;
	/* header pin number */
	case	MODE_PHYS:
		return	pin < 64 ? phyToGpio[pin] : -1;
	default	:
		msg(MSG_WARN, "%s : Unknown Mode %d\n", __func__, mode);
		return	-1;
	}
}
/*----------------------------------------------------------------------------*/
//
// set GPIO clock state
//
/*----------------------------------------------------------------------------*/
static void setClkState (int bank, int state)
{
	uint32_t data, regOffset;
	uint8_t gpioPclkShift;

	regOffset = 0;

	switch (bank) {
		case 0:
			regOffset = M2_PMU1CRU_GPIO_CLK_OFFSET;
			gpioPclkShift = M2_PMU1CRU_GPIO_PCLK_BIT;
			break;
		case 1:
			regOffset = M2_CRU_GPIO1_CLK_OFFSET;
			gpioPclkShift = M2_CRU_GPIO1_PCLK_BIT;
			break;
		default:
			regOffset = M2_CRU_GPIO_CLK_OFFSET;
			gpioPclkShift = ((bank - 2) * 2);
			break;
	}

	data = *(cru[(bank != 0)] + regOffset);
	data &= ~(1 << gpioPclkShift);

	if (state)
		data |= (1 << gpioPclkShift);
	data |= (1 << (gpioPclkShift + 16)); // write_mask

	*(cru[(bank != 0)] + regOffset) = data;

}
/*----------------------------------------------------------------------------*/
//
// set IOMUX mode
//
/*----------------------------------------------------------------------------*/
static int setIomuxMode (int pin, int mode)
{
	uint32_t data, regOffset;
	uint8_t	bank, group, bankOffset, groupOffset;

	if (lib->mode == MODE_GPIO_SYS)
		return -1;
	if ((pin = _getModeToGpio(lib->mode, pin)) < 0)
		return -1;

	bank = (pin / GPIO_SIZE);
	bankOffset = (pin - (bank * GPIO_SIZE));
	group = (bankOffset / 8); // A or B or C or D
	groupOffset = (pin % 8);
	regOffset = 0;

	switch (bank) {
		case 0:
			regOffset = (pin < 12 ? M2_PMU1_IOC_OFFSET : M2_PMU2_IOC_OFFSET);
			break;
		default:
			regOffset = M2_BUS_IOC_OFFSET;
			break;
	}

	if (mode == M2_FUNC_PWM) {
		bank = 1;
		regOffset = M2_BUS_IOC_OFFSET;
	}

	regOffset += (bank * 0x8) + (group * 0x2);
	regOffset += (groupOffset / 4 == 0) ? 0x0 : 0x1;
	data = *(grf[(bank != 0)] + regOffset);

	// Common IOMUX Funtion 1 : GPIO (4'h0)
	switch (mode) {
	case M2_FUNC_GPIO: // Common IOMUX Function 1_GPIO (4'h0)
		data &= ~(0xf << ((groupOffset % 4) * 4)); // ~0x0f = 4'h0
		data |= (0xf << ((groupOffset % 4) * 4 + 16)); // write_mask
		*(grf[bank != 0] + regOffset) = data;
		break;
	case M2_FUNC_PWM: // gpio0_D0, gpio3_B2/D0, gpio4_B3: 4'h1011
		data |= (0xb << ((groupOffset % 4) * 4));
		data &= ~(0x4 << ((groupOffset % 4) * 4));
		data |= (0xf << ((groupOffset % 4) * 4 + 16)); // write_mask
		*(grf[bank] + regOffset) = data;
		break;
	default:
		break;
	}

	return 0;
}
/*----------------------------------------------------------------------------*/
static int _pinMode (int pin, int mode)
{
	uint32_t data, regOffset;
	uint8_t bank, bankOffset;
	int origPin;

	origPin = pin;

	if (lib->mode == MODE_GPIO_SYS)
		return -1;

	if ((pin = _getModeToGpio(lib->mode, pin)) < 0)
		return -1;

	bank = (pin / GPIO_SIZE);
	bankOffset = (pin - (bank * GPIO_SIZE));
	regOffset = (bankOffset / 16 == 0 ? M2_GPIO_DIR_OFFSET : M2_GPIO_DIR_OFFSET + 0x1);

	pwmRelease(origPin);
	softPwmStop(origPin);
	softToneStop(origPin);
	setClkState(bank, M2_CLK_ENABLE);

	data = *(gpio[bank] + regOffset);

	switch (mode) {
		case INPUT:
		case INPUT_PULLUP:
		case INPUT_PULLDOWN:
			_pullUpDnControl(origPin, mode);
			__attribute__((fallthrough));
		case OUTPUT:
			setIomuxMode(origPin, M2_FUNC_GPIO);
			mode = (mode == OUTPUT);
			data &= ~(1 << gpioToShiftRegBy16(pin));
			data |=(mode << gpioToShiftRegBy16(pin));
			data |= (1 << (gpioToShiftRegBy16(pin) + 16)); // write_mask
			*(gpio[bank] + regOffset) = data;
			break;
		case SOFT_PWM_OUTPUT:
			softPwmCreate(origPin, 0, 100);
			break;
		case SOFT_TONE_OUTPUT:
			softToneCreate(origPin);
			break;
		case PWM_OUTPUT:
			setIomuxMode(origPin, M2_FUNC_PWM);
			pwmSetup(origPin);
			break;
		default:
			msg(MSG_WARN, "%s : Unknown Mode %d\n", __func__, mode);
			break;
	}

	return 0;
}
/*----------------------------------------------------------------------------*/
static int _getDrive(int pin)
{
	uint32_t data, regOffset;
	uint8_t bank, group, bankOffset, groupOffset;
	int value = 0;

	if (lib->mode == MODE_GPIO_SYS)
		return	-1;

	if ((pin = _getModeToGpio(lib->mode, pin)) < 0)
		return	-1;

	bank = (pin / GPIO_SIZE);
	bankOffset = (pin - (bank * GPIO_SIZE));
	group = (bankOffset / 8);
	groupOffset = (pin % 8);
	regOffset = 0;

	switch (bank) {
		case 0:
			regOffset = M2_PMU1_IOC_DS_OFFSET;
			if (pin >=12) {
				regOffset = M2_PMU2_IOC_DS_OFFSET;
			}
			break;
		case 1:
			regOffset = M2_VCCIO1_4_IOC_DS_OFFSET;
			break;
		case 2:
			regOffset = M2_VCCIO3_5_IOC_DS_OFFSET;
			__attribute__((fallthrough));
		case 3:
			break;
		case 4:
			if (group < 3) {
				regOffset = M2_VCCIO6_IOC_DS_OFFSET;
				if (pin >= 146 && pin <= 150) {
					regOffset = M2_VCCIO3_5_IOC_DS_OFFSET;
				}
			}
			else {
				regOffset = M2_VCCIO2_IOC_DS_OFFSET;
			}
			break;
		default:
			msg(MSG_WARN, "%s : Out of bank %d\n", __func__, bank);
			break;
	}

	regOffset += (bank * 0x8) + (group * 0x2);
	regOffset += (groupOffset / 4 == 0) ? 0x0 : 0x1;

	data = *(grf[(bank != 0)] + regOffset);
	data = (data >> ((groupOffset % 4) * 4)) & 0x7;

	switch (data) {
		case M2_DS_LEVEL_0:
			value = 0;
			break;
		case M2_DS_LEVEL_1:
			value = 1;
			break;
		case M2_DS_LEVEL_2:
			value = 2;
			break;
		case M2_DS_LEVEL_3:
			value = 3;
			break;
		case M2_DS_LEVEL_4:
			value = 4;
			break;
		case M2_DS_LEVEL_5:
			value = 5;
			break;
		default:
			value = -1;
			break;
	}

	return value;
}
/*----------------------------------------------------------------------------*/
static int _setDrive(int pin, int value)
{
	uint32_t data, regOffset;
	uint8_t bank, group, bankOffset, groupOffset;

	if (lib->mode == MODE_GPIO_SYS)
		return	-1;

	if ((pin = _getModeToGpio(lib->mode, pin)) < 0)
		return	-1;

	bank = (pin / GPIO_SIZE);
	bankOffset = (pin - (bank * GPIO_SIZE));
	group = (bankOffset / 8);
	groupOffset = (pin % 8);
	regOffset = 0;

	switch (bank) {
		case 0:
			regOffset = M2_PMU1_IOC_DS_OFFSET;
			if (pin >=12) {
				regOffset = M2_PMU2_IOC_DS_OFFSET;
			}
			break;
		case 1:
			regOffset = M2_VCCIO1_4_IOC_DS_OFFSET;
			break;
		case 2:
			regOffset = M2_VCCIO3_5_IOC_DS_OFFSET;
			__attribute__((fallthrough));
		case 3:
			break;
		case 4:
			if (group < 3) {
				regOffset = M2_VCCIO6_IOC_DS_OFFSET;
				if (pin >= 146 && pin <= 150) {
					regOffset = M2_VCCIO3_5_IOC_DS_OFFSET;
				}
			}
			else {
				regOffset = M2_VCCIO2_IOC_DS_OFFSET;
			}
			break;
		default:
			msg(MSG_WARN, "%s : Out of bank %d\n", __func__, bank);
			break;
	}

	regOffset += (bank * 0x8) + (group * 0x2);
	regOffset += (groupOffset / 4 == 0) ? 0x0 : 0x1;

	data = *(grf[(bank != 0)] + regOffset);
	data |= (0x7777 << 16);
	data = (data >> ((groupOffset % 4) * 4)) & 0x7;

	switch (value) {
		case 0:
			data |= (M2_DS_LEVEL_0 << ((groupOffset % 4) * 4));
			break;
		case 1:
			data |= (M2_DS_LEVEL_1 << ((groupOffset % 4) * 4));
			break;
		case 2:
			data |= (M2_DS_LEVEL_2 << ((groupOffset % 4) * 4));
			break;
		case 3:
			data |= (M2_DS_LEVEL_3 << ((groupOffset % 4) * 4));
			break;
		case 4:
			data |= (M2_DS_LEVEL_4 << ((groupOffset % 4) * 4));
			break;
		case 5:
			data |= (M2_DS_LEVEL_5 << ((groupOffset % 4) * 4));
			break;
		default:
			break;
	}

	*(grf[(bank != 0)] + regOffset) = data;

	return 0;
}
/*----------------------------------------------------------------------------*/
static int _getAlt (int pin)
{
	// TODO: Working confirmed
	uint32_t regOffset;
	uint16_t ret = 0;
	uint8_t	bank, group, bankOffset, groupOffset, shift;

	if (lib->mode == MODE_GPIO_SYS)
		return	-1;

	if ((pin = _getModeToGpio(lib->mode, pin)) < 0)
		return	-1;

	bank = (pin / GPIO_SIZE); // GPIO0, GPIO1, ...
	bankOffset = (pin - (bank * GPIO_SIZE));
	group = (bankOffset / 8); // GPIO0_A, GPIO0_B, ...
	groupOffset = (pin % 8);
	// The shift to move to the target pin at the register
	shift = groupOffset % 4 * 4;
	regOffset = 0;

	switch (bank) {
		case 0:
			regOffset = (pin < 12 ? M2_PMU1_IOC_OFFSET : M2_PMU2_IOC_OFFSET);
			break;
		default:
			regOffset = M2_BUS_IOC_OFFSET;
			break;
	}

	regOffset += (bank * 0x8) + (group * 0x2);
	regOffset += (groupOffset / 4 == 0) ? 0x0 : 0x1;

	ret = (*(grf[(bank != 0)] + regOffset) >> shift) & 0xf;

	// If it is ALT0 (GPIO mode), check it's direction
	// Add regOffset 0x4 to go to H register
	// when the bit group is in the high two-bytes of the word size
	if (ret == 0) {
		if (bankOffset / 16 == 0)
			regOffset = M2_GPIO_DIR_OFFSET;
		else
			regOffset = (M2_GPIO_DIR_OFFSET + 0x1);
		ret = !!(*(gpio[bank] + regOffset) & (1 << gpioToShiftRegBy16(bankOffset)));
	}
	else {
		// If it is alternative mode, add number 2 to fit into
		// the alts[] array for "gpio readall" command
		// Because the read number directly indicates the number of alt function
		ret += 2;
	}

	return ret;
}
/*----------------------------------------------------------------------------*/
static int _getPUPD (int pin)
{
	uint32_t regOffset, pupd;
	uint8_t bank, group, bankOffset, groupOffset;

	if (lib->mode == MODE_GPIO_SYS)
		return -1;

	if ((pin = _getModeToGpio(lib->mode,pin)) < 0)
		return -1;

	bank = (pin / GPIO_SIZE);
	bankOffset = (pin - (bank * GPIO_SIZE));
	group = (bankOffset / 8);
	groupOffset = (pin % 8);
	regOffset = 0;
	pupd = (0x3 << (groupOffset * 2));

	switch (bank) {
		case 0:
			regOffset = (pin < 12 ? M2_PMU1_IOC_PUPD_OFFSET : M2_PMU2_IOC_PUPD_OFFSET);
			break;
		case 1:
			regOffset = M2_VCCIO1_4_IOC_PUPD_OFFSET;
			break;
		case 2:
			regOffset = 0;
			__attribute__((fallthrough));
		case 3:
			regOffset = M2_VCCIO3_5_IOC_PUPD_OFFSET;
			break;
		case 4:
			if (group < 3) {
				regOffset = M2_VCCIO6_IOC_PUPD_OFFSET;
				if (pin >= 146 && pin <= 150) {
					regOffset = M2_VCCIO3_5_IOC_PUPD_OFFSET;
				}
			}
			else {
				regOffset = M2_VCCIO2_IOC_PUPD_OFFSET;
			}
			break;
		default:
			msg(MSG_WARN, "%s : Out of bank %d\n", __func__, bank);
			break;
	}

	regOffset += (bank * 0x4) + group; // (group * 0x1)

	pupd &= *(grf[(bank != 0)] + regOffset);
	pupd = (pupd >> groupOffset * 2);

	if (pupd & 1) {
		pupd = (pupd & 2) ? 1 : 2;
	}
	else {
		pupd = 0;
	}

	return pupd;
}
/*----------------------------------------------------------------------------*/
static int _pullUpDnControl (int pin, int pud)
{
	uint32_t data, regOffset;
	uint8_t	bank, group, bankOffset, groupOffset;

	if (lib->mode == MODE_GPIO_SYS)
		return	-1;

	if ((pin = _getModeToGpio(lib->mode, pin)) < 0) //exit
		return	-1;

	bank = (pin / GPIO_SIZE);
	bankOffset = (pin - (bank * GPIO_SIZE));
	group = (bankOffset / 8); // A or B or C or D
	groupOffset = (pin % 8);
	regOffset = 0;

	switch (bank) {
		case 0:
			regOffset = M2_PMU1_IOC_PUPD_OFFSET;
			if (pin >=12) {
				regOffset = M2_PMU2_IOC_PUPD_OFFSET;
			}
			break;
		case 1:
			regOffset = M2_VCCIO1_4_IOC_PUPD_OFFSET;
			break;
		case 2:
			regOffset = 0;
			__attribute__((fallthrough));
		case 3:
			regOffset = M2_VCCIO3_5_IOC_PUPD_OFFSET;
			break;
		case 4:
			if (group < 3) {
				regOffset = M2_VCCIO6_IOC_PUPD_OFFSET;
				if (pin >= 146 && pin <= 150) {
					regOffset = M2_VCCIO3_5_IOC_PUPD_OFFSET;
				}
			}
			else {
				regOffset = M2_VCCIO2_IOC_PUPD_OFFSET;
			}
			break;
		default:
			msg(MSG_WARN, "%s : Out of bank %d\n", __func__, bank);
			break;
	}

	regOffset += (bank * 0x4) + group; // (group * 0x1)

	data = *(grf[(bank != 0)] + regOffset);
	data &= ~(0x3 << (groupOffset * 2));

	switch (pud) {
	case PUD_UP:
		data |= (0x3 << (groupOffset * 2));
		break;
	case PUD_DOWN:
		data |= (0x1 << (groupOffset * 2));
		break;
	case PUD_OFF:
		break;
	default:
		/* No message */
		break;
	}

	data |= (0x3 << ((groupOffset * 2) + 16)); // write_mask
	*(grf[(bank != 0)] + regOffset) = data;

	return 0;
}
/*----------------------------------------------------------------------------*/
static int _digitalRead (int pin)
{
	uint8_t bank;
	int ret;
	char c;

	if (lib->mode == MODE_GPIO_SYS) {
		if (lib->sysFds[pin] == -1)
			return -1;

		lseek(lib->sysFds[pin], 0L, SEEK_SET);
		if (read(lib->sysFds[pin], &c, 1) < 0) {
			msg(MSG_WARN, "%s: Failed with reading from sysfs GPIO node. \n", __func__);
			return -1;
		}

		return (c == '0') ? LOW : HIGH;
	}

	if ((pin = _getModeToGpio(lib->mode, pin)) < 0)
		return	-1;

	bank = (pin / GPIO_SIZE);

	ret = *(gpio[bank] + M2_GPIO_GET_OFFSET) & (1 << gpioToShiftRegBy32(pin)) ? HIGH : LOW;

	return ret;
}
/*----------------------------------------------------------------------------*/
static int _digitalWrite (int pin, int value)
{
	uint32_t data, regOffset;
	uint8_t bank, bankOffset;

	if (lib->mode == MODE_GPIO_SYS) {
		if (lib->sysFds[pin] != -1) {
			if (value == LOW) {
				if (write (lib->sysFds[pin], "0\n", 2) < 0)
					msg(MSG_ERR,
					"%s : %s\nEdit direction file to output mode for\n\t/sys/class/gpio/gpio%d/direction\n",
					__func__, strerror(errno), pin + M2_GPIO_PIN_BASE);
			} else {
				if (write (lib->sysFds[pin], "1\n", 2) < 0)
					msg(MSG_ERR,
					"%s : %s\nEdit direction file to output mode for\n\t/sys/class/gpio/gpio%d/direction\n",
					__func__, strerror(errno), pin + M2_GPIO_PIN_BASE);
			}
		}
		return -1;
	}

	if ((pin = _getModeToGpio(lib->mode, pin)) < 0)
		return -1;

	bank = (pin / GPIO_SIZE);
	bankOffset = (pin - (bank * GPIO_SIZE));
	regOffset = (bankOffset / 16 == 0 ? M2_GPIO_SET_OFFSET : M2_GPIO_SET_OFFSET + 0x01);

	data = *(gpio[bank] + regOffset);
	data &= ~(1 << gpioToShiftRegBy16(pin));
	data |= (value << gpioToShiftRegBy16(pin));
	data |= (1 << (gpioToShiftRegBy16(pin) + 16)); // write_mask
	*(gpio[bank] + regOffset) = data;

	return 0;
}
/*----------------------------------------------------------------------------*/
static int _pwmWrite (int pin, int value)
{
	unsigned int duty;
	int pwmPin;

	memset(pwmDuty, 0, sizeof(pwmDuty));

	if (lib->mode == MODE_GPIO_SYS)
		return -1;

	if (((unsigned int)value > pwmRange) || (pwmRange <= 0)) {
		printf("warn : pwm range value is greater than or equal pwmWrite's\n");
		return -1;
	}

	pwmPin = pinToPwmNum[pin];
	duty = ((value * 100) / pwmRange);
	sprintf(pwmDuty, "%d", ((atoi(pwmPeriod) * duty) / 100));

	inputToSysNode(pwmPinPath[pwmPin], "duty_cycle", pwmDuty);

	return 0;
}
/*----------------------------------------------------------------------------*/
static int _analogRead (int pin)
{
	char value[5] = {0, };

	if (lib->mode == MODE_GPIO_SYS)
		return	-1;

	/* wiringPi ADC number = pin 25, pin 29 */
	switch (pin) {
#if defined(ARDUINO)
	/* To work with physical analog channel numbering */
	case	1:	case	25:
		pin = 0;
	break;
	case	0:	case	29:
		pin = 1;
	break;
#else
	case	0:	case	25:
		pin = 0;
	break;
	case	1:	case	29:
		pin = 1;
	break;
#endif
	default:
		return	0;
	}
	if (adcFds [pin] == -1)
		return 0;

	lseek(adcFds [pin], 0L, SEEK_SET);
	if (read(adcFds [pin], &value[0], 4) < 0) {
		msg(MSG_WARN, "%s: Error occurs when it reads from ADC file descriptor. \n", __func__);
		return -1;
	}

	return	atoi(value);
}
/*----------------------------------------------------------------------------*/
static int _digitalWriteByte (const unsigned int value)
{
	union reg_bitfield gpio0, gpio1, gpio3, gpio4;

	if (lib->mode == MODE_GPIO_SYS) {
		return -1;
	}

	setClkState(GPIO_SIZE * 0, M2_CLK_ENABLE);
	setClkState(GPIO_SIZE * 1, M2_CLK_ENABLE);
	setClkState(GPIO_SIZE * 3, M2_CLK_ENABLE);
	setClkState(GPIO_SIZE * 4, M2_CLK_ENABLE);

	/* Read data register */
	gpio0.wvalue = *(gpio[0] + M2_GPIO_GET_OFFSET);
	gpio1.wvalue = *(gpio[1] + M2_GPIO_GET_OFFSET);
	gpio3.wvalue = *(gpio[3] + M2_GPIO_GET_OFFSET);
	gpio4.wvalue = *(gpio[4] + M2_GPIO_GET_OFFSET);

	/* Wiring PI GPIO0 = M2 GPIO3_D.4 */
	gpio3.bits.bit28 = ((value & 0x01) >> 0);
	/* Wiring PI GPIO1 = M2 GPIO3_B.2 */
	gpio3.bits.bit10 = ((value & 0x02) >> 1);
	/* Wiring PI GPIO2 = M2 GPIO3_D.5 */
	gpio3.bits.bit29 = ((value & 0x04) >> 2);
	/* Wiring PI GPIO3 = M2 GPIO4_B.3 */
	gpio4.bits.bit11 = ((value & 0x08) >> 3);
	/* Wiring PI GPIO4 = M2 GPIO1_B.2 */
	gpio1.bits.bit10 = ((value & 0x10) >> 4);
	/* Wiring PI GPIO5 = M2 GPIO1_B.3 */
	gpio1.bits.bit11 = ((value & 0x20) >> 5);
	/* Wiring PI GPIO6 = M1 GPIO0_D.4 */
	gpio0.bits.bit28 = ((value & 0x40) >> 6);
	/* Wiring PI GPIO7 = M1 GPIO0_D.0 */
	gpio0.bits.bit24 = ((value & 0x80) >> 7);

	/* Update data register */
	*(gpio[0] + (M2_GPIO_SET_OFFSET + 0x1)) = (M2_WRITE_BYTE_MASK_GPIO0_H | (gpio0.wvalue >> 16));
	*(gpio[1] + M2_GPIO_SET_OFFSET) = (M2_WRITE_BYTE_MASK_GPIO1_L | (gpio1.wvalue & 0xffff));
	*(gpio[3] + (M2_GPIO_SET_OFFSET + 0x1)) = (M2_WRITE_BYTE_MASK_GPIO3_H | (gpio3.wvalue >> 16));
	*(gpio[3] + M2_GPIO_SET_OFFSET) = (M2_WRITE_BYTE_MASK_GPIO3_L | (gpio3.wvalue & 0xffff));
	*(gpio[4] + M2_GPIO_SET_OFFSET) = (M2_WRITE_BYTE_MASK_GPIO4_L | (gpio4.wvalue & 0xffff));

	return 0;
}
/*----------------------------------------------------------------------------*/
static unsigned int _digitalReadByte (void)
{
	union reg_bitfield gpio0, gpio1, gpio3, gpio4;

	unsigned int value = 0;

	if (lib->mode == MODE_GPIO_SYS) {
		return	-1;
	}

	setClkState(GPIO_SIZE * 0, M2_CLK_ENABLE);
	setClkState(GPIO_SIZE * 1, M2_CLK_ENABLE);
	setClkState(GPIO_SIZE * 3, M2_CLK_ENABLE);
	setClkState(GPIO_SIZE * 4, M2_CLK_ENABLE);

	/* Read data register */
	gpio0.wvalue = *(gpio[0] + M2_GPIO_GET_OFFSET);
	gpio1.wvalue = *(gpio[1] + M2_GPIO_GET_OFFSET);
	gpio3.wvalue = *(gpio[3] + M2_GPIO_GET_OFFSET);
	gpio4.wvalue = *(gpio[4] + M2_GPIO_GET_OFFSET);

	/* Wiring PI GPIO0 = M2 GPIO3_D.4 */
	if (gpio3.bits.bit28)
		value |= 0x01;
	/* Wiring PI GPIO1 = M2 GPIO3_B.2 */
	if (gpio3.bits.bit10)
		value |= 0x02;
	/* Wiring PI GPIO2 = M2 GPIO3_D.5 */
	if (gpio3.bits.bit29)
		value |= 0x04;
	/* Wiring PI GPIO3 = M2 GPIO4_B.3 */
	if (gpio4.bits.bit11)
		value |= 0x08;
	/* Wiring PI GPIO4 = M2 GPIO1_B.2 */
	if (gpio1.bits.bit10)
		value |= 0x10;
	/* Wiring PI GPIO5 = M2 GPIO1_B.3 */
	if (gpio1.bits.bit11)
		value |= 0x20;
	/* Wiring PI GPIO6 = M1 GPIO0_D.4 */
	if (gpio0.bits.bit28)
		value |= 0x40;
	/* Wiring PI GPIO7 = M1 GPIO0_D.0 */
	if (gpio0.bits.bit24)
		value |= 0x80;

	return value;
}
/*----------------------------------------------------------------------------*/
// PWM signal ___-----------___________---------------_______-----_
//               <--value-->           <----value---->
//               <-------range--------><-------range-------->
// PWM frequency == (PWM clock) / range
/*----------------------------------------------------------------------------*/
static void _pwmSetRange (unsigned int range)
{
	unsigned int freq, period;

	memset(pwmPeriod, 0, sizeof(pwmPeriod));

	if (lib->mode == MODE_GPIO_SYS)
		return;

	if (pwmClock < 2) {
		printf("error : pwm freq: %dMHz / (pwmSetClock's value) >= 2\n",
				(M2_PWM_INTERNAL_CLK / 2000000));
		return;
	}

	pwmRange = range;
	if ((pwmRange < 1) || (pwmRange >= pwmClock)) {
		printf("error : invalid value. ( < pwm freq)\n");
		return;
	}

	freq = (pwmClock / pwmRange);
	period = (1000000000 / freq); // period: s to ns.
	sprintf(pwmPeriod, "%d", period);

	for (int i = 0; i < 10; i++) {
		if (strstr(setupedPwmPinPath[i], "None") != NULL)
			continue;
		inputToSysNode(setupedPwmPinPath[i], "period", pwmPeriod);
		inputToSysNode(setupedPwmPinPath[i], "polarity", "normal");
		inputToSysNode(setupedPwmPinPath[i], "enable", "1");
	}
}
/*----------------------------------------------------------------------------*/
// Internal clock: 12MHz
// PWM clock == (Internal clock) / divisor
// PWM frequency == (PWM clock) / range
/*----------------------------------------------------------------------------*/
static void _pwmSetClock (int divisor)
{
	if (pwmClock > 0)
		pwmClock = (pwmClock / divisor);
	else {
		printf("error : pwm mode error\n");
		return;
	}
}
/*----------------------------------------------------------------------------*/
static void init_gpio_mmap (void)
{
	int fd = -1;
	void *mapped_cru[2], *mapped_grf[2], *mapped_gpio[5];

	/* GPIO mmap setup */
	if (!getuid()) {
		if ((fd = open ("/dev/mem", O_RDWR | O_SYNC | O_CLOEXEC) ) < 0)
			msg (MSG_ERR,
				"wiringPiSetup: Unable to open /dev/mem: %s\n",
				strerror (errno));
	} else {
		if (access("/dev/gpiomem",0) == 0) {
			if ((fd = open ("/dev/gpiomem", O_RDWR | O_SYNC | O_CLOEXEC) ) < 0)
				msg (MSG_ERR,
					"wiringPiSetup: Unable to open /dev/gpiomem: %s\n",
					strerror (errno));
			setUsingGpiomem(TRUE);
		} else
			msg (MSG_ERR,
				"wiringPiSetup: /dev/gpiomem doesn't exist. Please try again with sudo.\n");
	}

	if (fd < 0) {
		msg(MSG_ERR, "wiringPiSetup: Cannot open memory area for GPIO use. \n");
	} else {
		mapped_cru[0] = mmap(0, BLOCK_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, M2_PMU1CRU_BASE);
		mapped_cru[1] = mmap(0, BLOCK_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, M2_CRU_BASE);

		mapped_grf[0] = mmap(0, M2_GRF_BLOCK_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, M2_PMU_IOC_BASE);
		mapped_grf[1] = mmap(0, M2_GRF_BLOCK_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, M2_BUS_IOC_BASE);

		mapped_gpio[0] = mmap(0, BLOCK_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, M2_GPIO_0_BASE);
		mapped_gpio[1] = mmap(0, BLOCK_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, M2_GPIO_1_BASE);
		mapped_gpio[2] = mmap(0, BLOCK_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, M2_GPIO_2_BASE);
		mapped_gpio[3] = mmap(0, BLOCK_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, M2_GPIO_3_BASE);
		mapped_gpio[4] = mmap(0, BLOCK_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, M2_GPIO_4_BASE);

		if ((mapped_cru[0] == MAP_FAILED) || (mapped_cru[1] == MAP_FAILED)) {
			msg (MSG_ERR,"wiringPiSetup: mmap (CRU) failed: %s\n",strerror (errno));
		} else {
			cru[0] = (uint32_t *) mapped_cru[0];
			cru[1] = (uint32_t *) mapped_cru[1];
		}

		if ((mapped_grf[0] == MAP_FAILED) || (mapped_grf[1] == MAP_FAILED)) {
			msg (MSG_ERR,"wiringPiSetup: mmap (GRF) failed: %s\n",strerror (errno));
		} else {
			grf[0] = (uint32_t *) mapped_grf[0];
			grf[1] = (uint32_t *) mapped_grf[1];
		}

		if ((mapped_gpio[0] == MAP_FAILED) ||
			(mapped_gpio[1] == MAP_FAILED) ||
			(mapped_gpio[2] == MAP_FAILED) ||
			(mapped_gpio[3] == MAP_FAILED) ||
			(mapped_gpio[4] == MAP_FAILED)) {
			msg (MSG_ERR,
				"wiringPiSetup: mmap (GPIO) failed: %s\n",
				strerror (errno));
		} else {
			gpio[0] = (uint32_t *) mapped_gpio[0];
			gpio[1] = (uint32_t *) mapped_gpio[1];
			gpio[2] = (uint32_t *) mapped_gpio[2];
			gpio[3] = (uint32_t *) mapped_gpio[3];
			gpio[4] = (uint32_t *) mapped_gpio[4];
		}
	}
}
/*----------------------------------------------------------------------------*/
static void init_adc_fds (void)
{
	const char *AIN0_NODE, *AIN1_NODE;

	AIN0_NODE = "/sys/devices/platform/fec10000.saradc/iio:device0/in_voltage5_raw";
	AIN1_NODE = "/sys/devices/platform/fec10000.saradc/iio:device0/in_voltage4_raw";

	adcFds[0] = open(AIN0_NODE, O_RDONLY);
	adcFds[1] = open(AIN1_NODE, O_RDONLY);
}
/*----------------------------------------------------------------------------*/
void init_odroidm2 (struct libodroid *libwiring)
{
	init_gpio_mmap();

	init_adc_fds();

	/* wiringPi Core function initialize */
	libwiring->getModeToGpio	= _getModeToGpio;
	libwiring->pinMode		= _pinMode;
	libwiring->getAlt		= _getAlt;
	libwiring->getPUPD		= _getPUPD;
	libwiring->pullUpDnControl	= _pullUpDnControl;
	libwiring->getDrive			= _getDrive;
	libwiring->setDrive			= _setDrive;
	libwiring->digitalRead		= _digitalRead;
	libwiring->digitalWrite		= _digitalWrite;
	libwiring->analogRead		= _analogRead;
	libwiring->digitalWriteByte	= _digitalWriteByte;
	libwiring->digitalReadByte	= _digitalReadByte;
	libwiring->pwmWrite			= _pwmWrite;
	libwiring->pwmSetRange		= _pwmSetRange;
	libwiring->pwmSetClock		= _pwmSetClock;

	/* specify pin base number */
	libwiring->pinBase		= M2_GPIO_PIN_BASE;

	/* global variable setup */
	lib = libwiring;
}
/*----------------------------------------------------------------------------*/
