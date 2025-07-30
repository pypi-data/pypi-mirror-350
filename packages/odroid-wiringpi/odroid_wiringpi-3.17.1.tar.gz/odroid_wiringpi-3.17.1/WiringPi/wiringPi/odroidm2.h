/*----------------------------------------------------------------------------*/
/*

	WiringPi ODROID-M2 Board Header file

 */
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

#ifndef	__ODROID_M2_H__
#define	__ODROID_M2_H__
// flag of Using "/dev/gpiomem" or "libgpiod"
#define DEVMEM

/*----------------------------------------------------------------------------*/
/* Common mmap block size for ODROID-M2 GRF register */
#define M2_GPIO_PIN_BASE	0
#define M2_GRF_BLOCK_SIZE 0xFFFF
#define GPIO_SIZE	32

/* setClkState mode */
#define M2_CLK_ENABLE	0
#define M2_CLK_DISABLE	1

#define M2_FUNC_GPIO 0
#define M2_FUNC_PWM 1

/* CLK (Used for pmu system) */
#define M2_PMU1CRU_BASE 0xFD7F0000
#define M2_PMU1CRU_GPIO_CLK_OFFSET (0x814 >> 2)
#define M2_PMU1CRU_GPIO_PCLK_BIT 5
/* CLK (Used for always on system) */
#define M2_CRU_BASE	0xFD7C0000
#define M2_CRU_GPIO1_CLK_OFFSET (0x840 >> 2)
#define M2_CRU_GPIO1_PCLK_BIT 14
#define M2_CRU_GPIO_CLK_OFFSET (M2_CRU_GPIO1_CLK_OFFSET + 0x1)

/* IOMUX GPIO0_A0:GPIO0_B7 PMU1: A0 ~ B3 PMU2(+0x4000): B4~D7 */
#define M2_PMU_IOC_BASE 0xFD5F0000
#define M2_PMU1_IOC_OFFSET 0x0
#define M2_PMU2_IOC_OFFSET (0x3FF4 >> 2) // (0x4000 - 0xC)
#define M2_PMU1_IOC_PUPD_OFFSET	(0x20 >> 2)
#define M2_PMU1_IOC_DS_OFFSET	(0x10 >> 2)
#define M2_PMU2_IOC_PUPD_OFFSET	(0x4024 >> 2) // 0x28 -> 0x24 to unify the operations
#define M2_PMU2_IOC_DS_OFFSET	(0x4008 >> 2) // 0x14 -> 0x08 to unify the operations
/* IOMUX GPIO1_A0:GPIO4_D7 (GPIO) */
#define M2_BUS_IOC_BASE 0xFD5F8000
#define M2_BUS_IOC_OFFSET 0x0
/* GPIO1_A0:GPIO1_D7 (PUPD/DS) */
#define M2_VCCIO1_4_IOC_PUPD_OFFSET (0x1100 >> 2) // 0x110 -> 0x100 to unify the operations
#define M2_VCCIO1_4_IOC_DS_OFFSET (0x1000 >> 2) // 0x20 -> 0x00 to unify the operations
/* GPIO2_A4:GPIO3_D7, GPIO4_C2:GPIO4_C6 (PUPD/DS) */
#define M2_VCCIO3_5_IOC_PUPD_OFFSET (0x2100 >> 2) // 0x120 -> 0x100
#define M2_VCCIO3_5_IOC_DS_OFFSET (0x2000 >> 2) // 0x44 -> 0x00 to unify the operations
/* GPIO4_D0:GPIO4_D7 (PUPD/DS) */
#define M2_VCCIO2_IOC_PUPD_OFFSET (0x3100 >> 2) // 0x14c -> 0x140 to unify the operations
#define M2_VCCIO2_IOC_DS_OFFSET (0x3018 >> 2) // 0x98 -> 0x18 to unify the operations
/* GPIO4_A0:GPIO4_C1 (PUPD/DS) */
#define M2_VCCIO6_IOC_PUPD_OFFSET (0x4130 >> 2) // 0x140 -> 0x130
#define M2_VCCIO6_IOC_DS_OFFSET (0x4000 >> 2) // 0x80 -> 0x00 to unify the operations

/* GPIO[0] */
#define M2_GPIO_0_BASE	0xFD8A0000
/* GPIO[1:4] */
#define M2_GPIO_1_BASE	0xFEC20000
#define M2_GPIO_2_BASE	0xFEC30000
#define M2_GPIO_3_BASE	0xFEC40000
#define M2_GPIO_4_BASE	0xFEC50000

/* GPIO Port Data common offset ([L]:A0~B7, [H]:C0~D7) */
#define M2_GPIO_DIR_OFFSET (0x8 >> 2)
#define M2_GPIO_SET_OFFSET 0x0
#define M2_GPIO_GET_OFFSET (0x70 >> 2)

/* GPIO DS LEVELS */
#define M2_DS_LEVEL_0	0b000
#define M2_DS_LEVEL_1	0b100
#define M2_DS_LEVEL_2	0b010
#define M2_DS_LEVEL_3	0b110
#define M2_DS_LEVEL_4	0b001
#define M2_DS_LEVEL_5	0b101

/* GPIO write mask for WriteByte */
#define M2_WRITE_BYTE_MASK_GPIO0_H 0x11000000
#define M2_WRITE_BYTE_MASK_GPIO1_L 0x0C000000
#define M2_WRITE_BYTE_MASK_GPIO3_H 0x30000000
#define M2_WRITE_BYTE_MASK_GPIO3_L 0x04000000
#define M2_WRITE_BYTE_MASK_GPIO4_L 0x08000000

#define CONSUMER "consumer"

#define M2_PWM_INTERNAL_CLK			24000000 // 24MHz

#ifdef __cplusplus
extern "C" {
#endif

extern void init_odroidm2 (struct libodroid *libwiring);

#ifdef __cplusplus
}
#endif
/*----------------------------------------------------------------------------*/
#endif	/* __ODROID_M2_H__ */
/*----------------------------------------------------------------------------*/

