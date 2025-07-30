/*----------------------------------------------------------------------------*/
/*

	WiringPi ODROID-M1 Board Header file

 */
/*----------------------------------------------------------------------------*/
/*******************************************************************************
Copyright (C) 2021-2023 Steve Jeong <steve@how2flow.net>

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

#ifndef	__ODROID_M1_H__
#define	__ODROID_M1_H__

/*----------------------------------------------------------------------------*/
// Common mmap block size for ODROID-M1 GRF register
#define M1_GPIO_PIN_BASE	0
//setClkState mode
#define M1_CLK_ENABLE	0
#define M1_CLK_DISABLE	1

#define M1_GRF_BLOCK_SIZE 0xFFFF
#define GPIO_SIZE	32

#define M1_FUNC_GPIO 0
#define M1_FUNC_PWM 1

// GPIO[0]
#define M1_GPIO_0_BASE	0xFDD60000
// to control clock (PMU_CRU)
#define M1_PMU_CRU_BASE	0xFDD00000
#define M1_PMU_CRU_GPIO_CLK_OFFSET	(0x184 >> 2)
#define M1_PMU_CRU_GPIO_PCLK_BIT	9
// to control IOMUX
#define M1_PMU_GRF_BASE	0xFDC20000
#define M1_PMU_GRF_IOMUX_OFFSET	0x00
#define M1_PMU_GRF_PUPD_OFFSET	(0x20 >> 2)
#define M1_PMU_GRF_DS_OFFSET	(0x70 >> 2)

// GPIO[1:4]
#define M1_GPIO_1_BASE	0xFE740000
#define M1_GPIO_2_BASE	0xFE750000
#define M1_GPIO_3_BASE	0xFE760000
#define M1_GPIO_4_BASE	0xFE770000
// to control clock (SYS_CRU)
#define M1_CRU_BASE	0xFDD20000
#define M1_CRU_GPIO_CLK_OFFSET	(0x37c >> 2)
#define M1_CRU_GPIO_PCLK_BIT	2
// to control IOMUX
#define M1_SYS_GRF_BASE	0xFDC60000
#define M1_SYS_GRF_IOMUX_OFFSET	0x00
#define M1_SYS_GRF_PUPD_OFFSET	(0x80 >> 2)
#define M1_SYS_GRF_DS_OFFSET	(0x200 >> 2)

// Common offset for GPIO registers from each GPIO bank's base address
#define M1_GPIO_DIR_OFFSET	(0x8 >> 2)
#define M1_GPIO_SET_OFFSET	0x00
#define M1_GPIO_GET_OFFSET	(0x70 >> 2)

// GPIO DS LEVELS
#define M1_DS_LEVEL_0	0x01 //0b000001
#define M1_DS_LEVEL_1	0x03 //0b000011
#define M1_DS_LEVEL_2	0x07 //0b000111
#define M1_DS_LEVEL_3	0x0f //0b001111
#define M1_DS_LEVEL_4	0x1f //0b011111
#define M1_DS_LEVEL_5	0x3f //0b111111

// GPIO write mask for WriteByte
#define M1_WRITE_BYTE_MASK_GPIO0_H	0x00070000
#define M1_WRITE_BYTE_MASK_GPIO0_L	0x40000000
#define M1_WRITE_BYTE_MASK_GPIO2_L	0x61100000
#define M1_WRITE_BYTE_MASK_GPIO3_H	0x03C00000
#define M1_WRITE_BYTE_MASK_GPIO3_L	0x04000000

#define CONSUMER "consumer"

#define M1_PWM_INTERNAL_CLK			24000000 // 24MHz

#ifdef __cplusplus
extern "C" {
#endif

extern void init_odroidm1 (struct libodroid *libwiring);
extern void init_odroidm1s (struct libodroid *libwiring);

#ifdef __cplusplus
}
#endif
/*----------------------------------------------------------------------------*/
#endif	/* __ODROID_M1_H__ */
/*----------------------------------------------------------------------------*/

