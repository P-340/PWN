# ELF Format Cheatsheet

## Introduction 

<img width="680" height="1135" alt="image" src="https://github.com/user-attachments/assets/5856ea20-7286-4852-80ae-0a43385c2d69" />
## Compilation 
<img width="690" height="205" alt="image" src="https://github.com/user-attachments/assets/a6fa69c5-ed8d-4ec3-96bc-3ae72ad583aa" />
## Executable Headers(Ehdr)
-đây là phần đầu của têp
-nó sẽ định nghĩa một thông tin cơ bản của file, giống như một file magic number dùng để nhận biết một file ELF hay là một kiểu file khác .
Ngoài ra nó còn xác định loại của ELF, kiến trúc và một số option mà liên kết nó với các phần khác của ELF file.
32-bit struct:
```c
#define EI_NIDENT (16)

typedef struct
{
  unsigned char	e_ident[EI_NIDENT];	/* Magic number và info  */
  Elf32_Half	e_type;			/* Object file type */
  Elf32_Half	e_machine;		/* Architecture */
  Elf32_Word	e_version;		/* Object file version */
  Elf32_Addr	e_entry;		/* Entry point virtual address */
  Elf32_Off	e_phoff;		/* Program header table file offset */
  Elf32_Off	e_shoff;		/* Section header table file offset */
  Elf32_Word	e_flags;		/* Processor-specific flags */
  Elf32_Half	e_ehsize;		/* ELF header size in bytes */
  Elf32_Half	e_phentsize;		/* Program header table entry size */
  Elf32_Half	e_phnum;		/* Program header table entry count */
  Elf32_Half	e_shentsize;		/* Section header table entry size */
  Elf32_Half	e_shnum;		/* Section header table entry count */
  Elf32_Half	e_shstrndx;		/* Section header string table index */
} Elf32_Ehdr;
```
64-bit struct:
```c
typedef struct
{
  unsigned char	e_ident[EI_NIDENT];	/* Magic number and other info */
  Elf64_Half	e_type;			/* Object file type */
  Elf64_Half	e_machine;		/* Architecture */
  Elf64_Word	e_version;		/* Object file version */
  Elf64_Addr	e_entry;		/* Entry point virtual address */
  Elf64_Off	e_phoff;		/* Program header table file offset */
  Elf64_Off	e_shoff;		/* Section header table file offset */
  Elf64_Word	e_flags;		/* Processor-specific flags */
  Elf64_Half	e_ehsize;		/* ELF header size in bytes */
  Elf64_Half	e_phentsize;		/* Program header table entry size */
  Elf64_Half	e_phnum;		/* Program header table entry count */
  Elf64_Half	e_shentsize;		/* Section header table entry size */
  Elf64_Half	e_shnum;		/* Section header table entry count */
  Elf64_Half	e_shstrndx;		/* Section header string table index */
} Elf64_Ehdr;
```
EI_NIDENT  là kích thước trong byte của mục nhập cấu trúc đầu tiên ,e_type
Đây là ELF magic headers va một số thông số kỹ thuật cơ bản của file
Values:
- e_ident: đây là mảng 16 byte xác định đối tượng ELF,nó luôn bắt đầu với "\x7fELF".
- e_type : Chỉ định loại ELF:
   *ET_NONE (Undefined): Một định dạng file ELF không rõ hoặc không được chỉ định
   *ET_EXEC (executable file): Một ELF  thực thi độc lập - khi nạp vào bộ nhớ để chay qua execve,kernel sẽ ánh xạ binary này vào các địa chỉ ảo cố định xác định trước trong Program Header
   *ET_DYN (shared object): một thư viện hoặc một thực thi liên kết động - khi được kernel nạp vào một base address ngẫu nhiên khi ASLR được bật
   *ET_REL (Relocatable file) : một tệp đối tượng(object file - .o) hoặc các thư viện tĩnh (.a tập hợp các file .o) sinh ra sau đoạn complie/assemble nhưng chưa qua linker chứa mã máy,dữ liệu nhị phân nhưng chưa có địa chỉ bộ nhớ tuyệt đối hay cố định
   *ET_CORE (Core dump file) : được kernel tự động ghi ra đĩa khi một tiến trình gặp lỗi như SIGEGV,SIGABRT,SIGBUS...
- e_machine: mã số kiến trúc CPU(0x03-x86 32-bit, 0x3E- AMD64/x86-64, 0x28 EM_ARM ,....)
- e_version: phiên bản của ELF file - luôn mang giá trị 1 (/EV_CURRENT) vì định dạng chuẩn chưa từng lên 2
- e_entry: địa chỉ bộ nhớ ảo thường trỏ vào _start 
- e_phoff(Program Header Table offset):Vị trí tính bằng byte từ đầu file đến Phdr - phần môt tả các segments
- e_shoff(Section header table offset):Vị trí tính bằng byte từ đầu file đến Shdr - phần môt tả các sections
- e_flags (Processor-specific flags): các cờ cấu hình đặc thù của từng CPU
- e_ehsize(ELF Header size): kích thước chính của ELF header tính bằng bytes:
  * ELF 32-bit: 52 bytes(0x34)
  * ELF 64-bit: 64 bytes(0x40)
- e_phentsize:kích thước mỗi bản ghi trong bằng Phdr
- e_phnum: số lượng entry có trong bảng Phdr
- e_shentsize : Kích thước nhập cảnh của Shdr
- e_shnum : số lượng entry có trong bảng Shdr
- e_shstrndx : chỉ index trỏ đến entry của Section .shstrtab trong bảng Shdr, section này chứa các chuỗi tên của tất cả các section(các chuỗi kết thúc bằng null byte như ".text\0",".data\0").Nhờ nó công cj đọc ELF mới giải mã được tên các section
- Note: e_phoff và e_shoff là offsets của ELF file, e_entry thay vào đó là một địa chỉ ảo

- định dạng e_type:
```c
#define ET_NONE		0		/* No file type */
#define ET_REL		1		/* Relocatable file */
#define ET_EXEC		2		/* Executable file */
#define ET_DYN		3		/* Shared object file */
#define ET_CORE		4		/* Core file */
#define	ET_NUM		5		/* Number of defined types */
#define ET_LOOS		0xfe00		/* OS-specific range start */
#define ET_HIOS		0xfeff		/* OS-specific range end */
#define ET_LOPROC	0xff00		/* Processor-specific range start */
#define ET_HIPROC	0xffff		/* Processor-specific range end */
```
- định dạng e_machine:
```c
#define EM_NONE		 0	/* No machine */
#define EM_M32		 1	/* AT&T WE 32100 */
#define EM_SPARC	 2	/* SUN SPARC */
#define EM_386		 3	/* Intel 80386 */
#define EM_68K		 4	/* Motorola m68k family */
#define EM_88K		 5	/* Motorola m88k family */
#define EM_IAMCU	 6	/* Intel MCU */
#define EM_860		 7	/* Intel 80860 */
#define EM_MIPS		 8	/* MIPS R3000 big-endian */
#define EM_S370		 9	/* IBM System/370 */
#define EM_MIPS_RS3_LE	10	/* MIPS R3000 little-endian */
				/* reserved 11-14 */
#define EM_PARISC	15	/* HPPA */
				/* reserved 16 */
#define EM_VPP500	17	/* Fujitsu VPP500 */
#define EM_SPARC32PLUS	18	/* Sun's "v8plus" */
#define EM_960		19	/* Intel 80960 */
#define EM_PPC		20	/* PowerPC */
#define EM_PPC64	21	/* PowerPC 64-bit */
#define EM_S390		22	/* IBM S390 */
#define EM_SPU		23	/* IBM SPU/SPC */
				/* reserved 24-35 */
#define EM_V800		36	/* NEC V800 series */
#define EM_FR20		37	/* Fujitsu FR20 */
#define EM_RH32		38	/* TRW RH-32 */
#define EM_RCE		39	/* Motorola RCE */
#define EM_ARM		40	/* ARM */
#define EM_FAKE_ALPHA	41	/* Digital Alpha */
#define EM_SH		42	/* Hitachi SH */
#define EM_SPARCV9	43	/* SPARC v9 64-bit */
#define EM_TRICORE	44	/* Siemens Tricore */
#define EM_ARC		45	/* Argonaut RISC Core */
#define EM_H8_300	46	/* Hitachi H8/300 */
#define EM_H8_300H	47	/* Hitachi H8/300H */
#define EM_H8S		48	/* Hitachi H8S */
#define EM_H8_500	49	/* Hitachi H8/500 */
#define EM_IA_64	50	/* Intel Merced */
#define EM_MIPS_X	51	/* Stanford MIPS-X */
#define EM_COLDFIRE	52	/* Motorola Coldfire */
#define EM_68HC12	53	/* Motorola M68HC12 */
#define EM_MMA		54	/* Fujitsu MMA Multimedia Accelerator */
#define EM_PCP		55	/* Siemens PCP */
#define EM_NCPU		56	/* Sony nCPU embeeded RISC */
#define EM_NDR1		57	/* Denso NDR1 microprocessor */
#define EM_STARCORE	58	/* Motorola Start*Core processor */
#define EM_ME16		59	/* Toyota ME16 processor */
#define EM_ST100	60	/* STMicroelectronic ST100 processor */
#define EM_TINYJ	61	/* Advanced Logic Corp. Tinyj emb.fam */
#define EM_X86_64	62	/* AMD x86-64 architecture */
#define EM_PDSP		63	/* Sony DSP Processor */
#define EM_PDP10	64	/* Digital PDP-10 */
#define EM_PDP11	65	/* Digital PDP-11 */
#define EM_FX66		66	/* Siemens FX66 microcontroller */
#define EM_ST9PLUS	67	/* STMicroelectronics ST9+ 8/16 mc */
#define EM_ST7		68	/* STmicroelectronics ST7 8 bit mc */
#define EM_68HC16	69	/* Motorola MC68HC16 microcontroller */
#define EM_68HC11	70	/* Motorola MC68HC11 microcontroller */
#define EM_68HC08	71	/* Motorola MC68HC08 microcontroller */
#define EM_68HC05	72	/* Motorola MC68HC05 microcontroller */
#define EM_SVX		73	/* Silicon Graphics SVx */
#define EM_ST19		74	/* STMicroelectronics ST19 8 bit mc */
#define EM_VAX		75	/* Digital VAX */
#define EM_CRIS		76	/* Axis Communications 32-bit emb.proc */
#define EM_JAVELIN	77	/* Infineon Technologies 32-bit emb.proc */
#define EM_FIREPATH	78	/* Element 14 64-bit DSP Processor */
#define EM_ZSP		79	/* LSI Logic 16-bit DSP Processor */
#define EM_MMIX		80	/* Donald Knuth's educational 64-bit proc */
#define EM_HUANY	81	/* Harvard University machine-independent object files */
#define EM_PRISM	82	/* SiTera Prism */
#define EM_AVR		83	/* Atmel AVR 8-bit microcontroller */
#define EM_FR30		84	/* Fujitsu FR30 */
#define EM_D10V		85	/* Mitsubishi D10V */
#define EM_D30V		86	/* Mitsubishi D30V */
#define EM_V850		87	/* NEC v850 */
#define EM_M32R		88	/* Mitsubishi M32R */
#define EM_MN10300	89	/* Matsushita MN10300 */
#define EM_MN10200	90	/* Matsushita MN10200 */
#define EM_PJ		91	/* picoJava */
#define EM_OPENRISC	92	/* OpenRISC 32-bit embedded processor */
#define EM_ARC_COMPACT	93	/* ARC International ARCompact */
#define EM_XTENSA	94	/* Tensilica Xtensa Architecture */
#define EM_VIDEOCORE	95	/* Alphamosaic VideoCore */
#define EM_TMM_GPP	96	/* Thompson Multimedia General Purpose Proc */
#define EM_NS32K	97	/* National Semi. 32000 */
#define EM_TPC		98	/* Tenor Network TPC */
#define EM_SNP1K	99	/* Trebia SNP 1000 */
#define EM_ST200	100	/* STMicroelectronics ST200 */
#define EM_IP2K		101	/* Ubicom IP2xxx */
#define EM_MAX		102	/* MAX processor */
#define EM_CR		103	/* National Semi. CompactRISC */
#define EM_F2MC16	104	/* Fujitsu F2MC16 */
#define EM_MSP430	105	/* Texas Instruments msp430 */
#define EM_BLACKFIN	106	/* Analog Devices Blackfin DSP */
#define EM_SE_C33	107	/* Seiko Epson S1C33 family */
#define EM_SEP		108	/* Sharp embedded microprocessor */
#define EM_ARCA		109	/* Arca RISC */
#define EM_UNICORE	110	/* PKU-Unity & MPRC Peking Uni. mc series */
#define EM_EXCESS	111	/* eXcess configurable cpu */
#define EM_DXP		112	/* Icera Semi. Deep Execution Processor */
#define EM_ALTERA_NIOS2 113	/* Altera Nios II */
#define EM_CRX		114	/* National Semi. CompactRISC CRX */
#define EM_XGATE	115	/* Motorola XGATE */
#define EM_C166		116	/* Infineon C16x/XC16x */
#define EM_M16C		117	/* Renesas M16C */
#define EM_DSPIC30F	118	/* Microchip Technology dsPIC30F */
#define EM_CE		119	/* Freescale Communication Engine RISC */
#define EM_M32C		120	/* Renesas M32C */
				/* reserved 121-130 */
#define EM_TSK3000	131	/* Altium TSK3000 */
#define EM_RS08		132	/* Freescale RS08 */
#define EM_SHARC	133	/* Analog Devices SHARC family */
#define EM_ECOG2	134	/* Cyan Technology eCOG2 */
#define EM_SCORE7	135	/* Sunplus S+core7 RISC */
#define EM_DSP24	136	/* New Japan Radio (NJR) 24-bit DSP */
#define EM_VIDEOCORE3	137	/* Broadcom VideoCore III */
#define EM_LATTICEMICO32 138	/* RISC for Lattice FPGA */
#define EM_SE_C17	139	/* Seiko Epson C17 */
#define EM_TI_C6000	140	/* Texas Instruments TMS320C6000 DSP */
#define EM_TI_C2000	141	/* Texas Instruments TMS320C2000 DSP */
#define EM_TI_C5500	142	/* Texas Instruments TMS320C55x DSP */
#define EM_TI_ARP32	143	/* Texas Instruments App. Specific RISC */
#define EM_TI_PRU	144	/* Texas Instruments Prog. Realtime Unit */
				/* reserved 145-159 */
#define EM_MMDSP_PLUS	160	/* STMicroelectronics 64bit VLIW DSP */
#define EM_CYPRESS_M8C	161	/* Cypress M8C */
#define EM_R32C		162	/* Renesas R32C */
#define EM_TRIMEDIA	163	/* NXP Semi. TriMedia */
#define EM_QDSP6	164	/* QUALCOMM DSP6 */
#define EM_8051		165	/* Intel 8051 and variants */
#define EM_STXP7X	166	/* STMicroelectronics STxP7x */
#define EM_NDS32	167	/* Andes Tech. compact code emb. RISC */
#define EM_ECOG1X	168	/* Cyan Technology eCOG1X */
#define EM_MAXQ30	169	/* Dallas Semi. MAXQ30 mc */
#define EM_XIMO16	170	/* New Japan Radio (NJR) 16-bit DSP */
#define EM_MANIK	171	/* M2000 Reconfigurable RISC */
#define EM_CRAYNV2	172	/* Cray NV2 vector architecture */
#define EM_RX		173	/* Renesas RX */
#define EM_METAG	174	/* Imagination Tech. META */
#define EM_MCST_ELBRUS	175	/* MCST Elbrus */
#define EM_ECOG16	176	/* Cyan Technology eCOG16 */
#define EM_CR16		177	/* National Semi. CompactRISC CR16 */
#define EM_ETPU		178	/* Freescale Extended Time Processing Unit */
#define EM_SLE9X	179	/* Infineon Tech. SLE9X */
#define EM_L10M		180	/* Intel L10M */
#define EM_K10M		181	/* Intel K10M */
				/* reserved 182 */
#define EM_AARCH64	183	/* ARM AARCH64 */
				/* reserved 184 */
#define EM_AVR32	185	/* Amtel 32-bit microprocessor */
#define EM_STM8		186	/* STMicroelectronics STM8 */
#define EM_TILE64	187	/* Tileta TILE64 */
#define EM_TILEPRO	188	/* Tilera TILEPro */
#define EM_MICROBLAZE	189	/* Xilinx MicroBlaze */
#define EM_CUDA		190	/* NVIDIA CUDA */
#define EM_TILEGX	191	/* Tilera TILE-Gx */
#define EM_CLOUDSHIELD	192	/* CloudShield */
#define EM_COREA_1ST	193	/* KIPO-KAIST Core-A 1st gen. */
#define EM_COREA_2ND	194	/* KIPO-KAIST Core-A 2nd gen. */
#define EM_ARC_COMPACT2	195	/* Synopsys ARCompact V2 */
#define EM_OPEN8	196	/* Open8 RISC */
#define EM_RL78		197	/* Renesas RL78 */
#define EM_VIDEOCORE5	198	/* Broadcom VideoCore V */
#define EM_78KOR	199	/* Renesas 78KOR */
#define EM_56800EX	200	/* Freescale 56800EX DSC */
#define EM_BA1		201	/* Beyond BA1 */
#define EM_BA2		202	/* Beyond BA2 */
#define EM_XCORE	203	/* XMOS xCORE */
#define EM_MCHP_PIC	204	/* Microchip 8-bit PIC(r) */
				/* reserved 205-209 */
#define EM_KM32		210	/* KM211 KM32 */
#define EM_KMX32	211	/* KM211 KMX32 */
#define EM_EMX16	212	/* KM211 KMX16 */
#define EM_EMX8		213	/* KM211 KMX8 */
#define EM_KVARC	214	/* KM211 KVARC */
#define EM_CDP		215	/* Paneve CDP */
#define EM_COGE		216	/* Cognitive Smart Memory Processor */
#define EM_COOL		217	/* Bluechip CoolEngine */
#define EM_NORC		218	/* Nanoradio Optimized RISC */
#define EM_CSR_KALIMBA	219	/* CSR Kalimba */
#define EM_Z80		220	/* Zilog Z80 */
#define EM_VISIUM	221	/* Controls and Data Services VISIUMcore */
#define EM_FT32		222	/* FTDI Chip FT32 */
#define EM_MOXIE	223	/* Moxie processor */
#define EM_AMDGPU	224	/* AMD GPU */
				/* reserved 225-242 */
#define EM_RISCV	243	/* RISC-V */

#define EM_BPF		247	/* Linux BPF -- in-kernel virtual machine */
#define EM_CSKY		252     /* C-SKY */

#define EM_NUM		253

/* Old spellings/synonyms.  */

#define EM_ARC_A5	EM_ARC_COMPACT

/* If it is necessary to assign new unofficial EM_* values, please
   pick large random numbers (0x8523, 0xa7f2, etc.) to minimize the
   chances of collision with official or non-GNU unofficial values.  */

#define EM_ALPHA	0x9026
```
e_version denfines:
```c
#define EV_NONE		  0		/* Invalid ELF version */
#define EV_CURRENT	1		/* Current version */
#define EV_NUM		  2
```
## Section Header (Shdr)
Các đoạn code và dữ liệu được chia thành các chunk liên tiếp nhau được gọi là các section
Nó là chỉ là một vùng không gian chứa dữ liệu hoặc code,những thông số kỹ thuật trong một section header đang chỉ định các chi tiết cần thiết như là size và offset
Mọi section đều có một section header mà định nghĩa bản thân nó
32-bit struct:
```c 
typedef struct
{
  Elf32_Word	sh_name;		/* Section name (string tbl index) */
  Elf32_Word	sh_type;		/* Section type */
  Elf32_Word	sh_flags;		/* Section flags */
  Elf32_Addr	sh_addr;		/* Section virtual addr at execution */
  Elf32_Off	sh_offset;		/* Section file offset */
  Elf32_Word	sh_size;		/* Section size in bytes */
  Elf32_Word	sh_link;		/* Link to another section */
  Elf32_Word	sh_info;		/* Additional section information */
  Elf32_Word	sh_addralign;		/* Section alignment */
  Elf32_Word	sh_entsize;		/* Entry size if section holds table */
} Elf32_Shdr;
```
64-bit struct:
```c
typedef struct
{
  Elf64_Word	sh_name;		/* Section name (string tbl index) */
  Elf64_Word	sh_type;		/* Section type */
  Elf64_Xword	sh_flags;		/* Section flags */
  Elf64_Addr	sh_addr;		/* Section virtual addr at execution */
  Elf64_Off	sh_offset;		/* Section file offset */
  Elf64_Xword	sh_size;		/* Section size in bytes */
  Elf64_Word	sh_link;		/* Link to another section */
  Elf64_Word	sh_info;		/* Additional section information */
  Elf64_Xword	sh_addralign;		/* Section alignment */
  Elf64_Xword	sh_entsize;		/* Entry size if section holds table */
} Elf64_Shdr;
```
Các giá trị:
- sh_name : Index chỉ vào bảng chuỗi,nếu bằng không thì nghĩa là không có tên (.shstrtab)
- sh_type:kiểu của section
  * SHT_NULL : mục rỗng không được sử dụng (nằm ở Index 0 của section header
  * SHT_PROGBITS: dữ liệu của chương trình do trình biên dịch tạo ra :
     * .text : chứa mã máy của chương trình
     * .data : Biến toàn cục đã được khởi tạo giá trị
     * .rodata : Các hằng số only read (ví dụ chuỗi string "hello","/bin/sh")
  * Bảng Symbol: dùng lể lưu danh sách các tên hàm như main, win, puts,system 
     * SHT_SYMTAB(.symtab): Bảng symbol dung cho việc debug(sẽ mất nếu người tạo bài dùng lệnh strip để xoá dấu vết)
     * SHT_DYNSYM(.dynsym): Bảng symbol dùng cho liên kết động lúc chương trình chạy
  * SHT_STRTAB:  String table- chữa các chuỗi ký tự kết thúc bằng byte \x00 (như .strtab,.dynstr,.shstrtab) để đặt tên cho các hàm, biến và section
  * SHT_RELA và SHT_REL: chứa các entry phục vụ việc cập nhật địa chỉ hàm/biến lúc chạy(chẳng hạn cơ chế phân giải địa chỉ hàm thư viện trong bảng GOT/PLT).SHT_RETA có thêm trường hằng số bù (addend),còn SHT_REL thì không .
  * SHT_HASH : Bảng băm giúp trình liên kết động tìm kiếm nhanh các symbol mà không cần duyệt tuần tự.
  * SHT_NOTE: Chứa ghi chú
  * SHT_NOBITS: Phân vùng dữ liệu chưa được khởi tạo (.bss,...), không tốn dung lượng lưu trữ trong file trên ổ,nhưng vẫn được cấp phát một vùng nhớ trống
  * SHT_SHLIB: Dự trữ
- sh_flags: Mô tả thông tin bổ sung về một phần
  * SHF_WRITE: Writable trong thời gian chạy(.data,.bss,.got),khi pwn sẽ thường nhắm vào bss
  * SHF_ALLOC: báo cho hệ thống biết section chứa cờ này cần nạp vào RAM khi program run
  * SHF_EXECINSTR: Chứa mã lệnh được phép Thực thi(ví dụ : .text,.plt).khi bật NX,CPU chỉ chấp nhận chạy code nằm trong vùng nhớ có cờ này, ROPgadget hay quét gadget ở đây
- sh_addr: Phần địạ chỉ thực tế trên RAM của section khi chương trình chạy (nếu cờ PIE bật, cái này sẽ là offset so với base, nếu PIE tắt đây sẽ là địa chỉ cố định )
- sh_offset: Vị trí bắt đầu của section tính bằng số byte kể từ đầu ELF
- sh_size: Độ dài(tổng số byte) của section đó
- sh_link: Tạo mối liên kết đến một section khác(VD: SHT_SYMTAB, SHT_DYNSYM, hoặc SHT_DYNAMIC có bảng string liên kết có chứa các tên symbol trong question.Relocation sections (type SHT_REL or SHT_RELA) được liên kết với bảng symbol mô tả các symbol liên quan đến quá trình tái định vị.
- sh_info: Thông tin phần bổ sung, nếu sh_link liên kết với section là relocation thì sh_info trỏ tới section như .got sẽ bị sửa địa chỉ
- sh_addralign: căn chỉnh địa chỉ bộ nhớ(luôn là luỹ thừa của 2) để CPU truy xuất dữ liệu tối ưu
- sh_entsize : một số section bản chất là một cái mảng các struct có kích thước mỗi phần tử cố định (như bảng .dynsym chứa danh sách các Elf64_Sym, hoặc .rela.plt chứa
- danh sách các Elf64_Rela).Trường sh_entsize lưu kích thước (tính bằng byte) của 1 dòng trong bảng đó .Nếu section không phải là bảng (như .text),trường này bằng 0.(Lợi dụng cách tính chỉ số phần tự dựa trên sh_entsize trong .dynsym và .rela.plt chính là cốt lõi của kỹ thuật Ret2diresolve)

Tất cả section header định nghĩa section ,đều được lưu trữ trong section header table
Để cài và thực thi một nhị phân trong một quá trình bạn cần tổ chức khác nhau của mã và dữ liệu trong nhị phân.vì lý do này, các tệp thực thi ELF chỉ định một logic khác ,  đó là segments,được sử dụng tại thời điểm thực thi chương trình, trong khi các section được sử dụng tại link time
Các section là thành phần tuỳ chọn; chúng chủ yếu chứa metadata cho công cụ debuggers.Program header mới là thành phần quyết định cách một ELF binary được nạp vào bộ nhớ
Do đó section header hkoong được nạp vào bộ nhớ
sh_type defines: 
```c
#define SHT_NULL	  0		/* Section header table entry unused */
#define SHT_PROGBITS	  1		/* Program data */
#define SHT_SYMTAB	  2		/* Symbol table */
#define SHT_STRTAB	  3		/* String table */
#define SHT_RELA	  4		/* Relocation entries with addends */
#define SHT_HASH	  5		/* Symbol hash table */
#define SHT_DYNAMIC	  6		/* Dynamic linking information */
#define SHT_NOTE	  7		/* Notes */
#define SHT_NOBITS	  8		/* Program space with no data (bss) */
#define SHT_REL		  9		/* Relocation entries, no addends */
#define SHT_SHLIB	  10		/* Reserved */
#define SHT_DYNSYM	  11		/* Dynamic linker symbol table */
#define SHT_INIT_ARRAY	  14		/* Array of constructors */
#define SHT_FINI_ARRAY	  15		/* Array of destructors */
#define SHT_PREINIT_ARRAY 16		/* Array of pre-constructors */
#define SHT_GROUP	  17		/* Section group */
#define SHT_SYMTAB_SHNDX  18		/* Extended section indeces */
#define	SHT_NUM		  19		/* Number of defined types.  */
#define SHT_LOOS	  0x60000000	/* Start OS-specific.  */
#define SHT_GNU_ATTRIBUTES 0x6ffffff5	/* Object attributes.  */
#define SHT_GNU_HASH	  0x6ffffff6	/* GNU-style hash table.  */
#define SHT_GNU_LIBLIST	  0x6ffffff7	/* Prelink library list */
#define SHT_CHECKSUM	  0x6ffffff8	/* Checksum for DSO content.  */
#define SHT_LOSUNW	  0x6ffffffa	/* Sun-specific low bound.  */
#define SHT_SUNW_move	  0x6ffffffa
#define SHT_SUNW_COMDAT   0x6ffffffb
#define SHT_SUNW_syminfo  0x6ffffffc
#define SHT_GNU_verdef	  0x6ffffffd	/* Version definition section.  */
#define SHT_GNU_verneed	  0x6ffffffe	/* Version needs section.  */
#define SHT_GNU_versym	  0x6fffffff	/* Version symbol table.  */
#define SHT_HISUNW	  0x6fffffff	/* Sun-specific high bound.  */
#define SHT_HIOS	  0x6fffffff	/* End OS-specific type */
#define SHT_LOPROC	  0x70000000	/* Start of processor-specific */
#define SHT_HIPROC	  0x7fffffff	/* End of processor-specific */
#define SHT_LOUSER	  0x80000000	/* Start of application-specific */
#define SHT_HIUSER	  0x8fffffff	/* End of application-specific */
```
sh_flags defines:
```c
#define SHF_WRITE	     (1 << 0)	/* Writable */
#define SHF_ALLOC	     (1 << 1)	/* Occupies memory during execution */
#define SHF_EXECINSTR	     (1 << 2)	/* Executable */
#define SHF_MERGE	     (1 << 4)	/* Might be merged */
#define SHF_STRINGS	     (1 << 5)	/* Contains nul-terminated strings */
#define SHF_INFO_LINK	     (1 << 6)	/* `sh_info' contains SHT index */
#define SHF_LINK_ORDER	     (1 << 7)	/* Preserve order after combining */
#define SHF_OS_NONCONFORMING (1 << 8)	/* Non-standard OS specific handling
					   required */
#define SHF_GROUP	     (1 << 9)	/* Section is member of a group.  */
#define SHF_TLS		     (1 << 10)	/* Section hold thread-local data.  */
#define SHF_COMPRESSED	     (1 << 11)	/* Section with compressed data. */
#define SHF_MASKOS	     0x0ff00000	/* OS-specific.  */
#define SHF_MASKPROC	     0xf0000000	/* Processor-specific */
#define SHF_ORDERED	     (1 << 30)	/* Special ordering requirement
					   (Solaris).  */
#define SHF_EXCLUDE	     (1U << 31)	/* Section is excluded unless
					   referenced or allocated (Solaris).*/
```
## Section
Theo tiêu chuẩn ELF, mục đầu tiên trong bảng tiêu đề section (section header table) của mọi tệp ELF được quy định là một mục NULL.
Kiểu (type) của mục này là SHT_NULL, và tất cả các trường (field) trong section header đều được đặt về giá trị 0.
sections:
    
	.init: Chứa mã máy thực thi thực hiện các tác vụ khởi tạo và cần được chạy trước khi mã khác trong tệp nhị phân được thực thi. Section này có cờ SHF_EXECINSTR, cho biết nó chứa các lệnh có thể thực thi. Hệ thống thực thi mã trong section .init trước khi chuyển quyền điều khiển đến điểm bắt đầu thực thi chính của tệp nhị phân.
	
    .fini: Ngược lại với .init, section này chứa mã thực thi cần chạy sau khi chương trình chính hoàn tất.
    
	.text: Chứa phần mã máy chính của chương trình. Section này có cờ SHF_EXECINSTR, cho biết mã bên trong có thể thực thi. Nó có kiểu SHT_PROGBITS vì chứa dữ liệu mã do người dùng định nghĩa, chẳng hạn như mã được biên dịch từ chương trình C.
    
	.bss: Chứa dữ liệu chưa được khởi tạo (uninitialized data). Section này có kiểu SHT_NOBITS. Nó không chiếm dung lượng tương ứng trong tệp trên đĩa, giúp tránh lãng phí không gian lưu trữ. Khi chương trình chạy, vùng nhớ dành cho dữ liệu này thường được khởi tạo bằng 0. Section này có quyền ghi.
    
	.data: Chứa dữ liệu của chương trình đã được khởi tạo. Section này có quyền ghi và có kiểu SHT_PROGBITS.
    
	.rodata: Chứa dữ liệu chỉ đọc (read-only data), chẳng hạn như các chuỗi được sử dụng trong mã chương trình. Nếu dữ liệu cần có khả năng thay đổi, nó thường được đặt trong .data thay vì .rodata. Ví dụ, các chuỗi được viết trực tiếp trong mã nguồn để truyền cho hàm printf() có thể được lưu tại đây.
    
	.plt: Là viết tắt của Procedure Linkage Table (bảng liên kết thủ tục). Đây là vùng mã phục vụ cho việc liên kết động (dynamic linking), hỗ trợ chương trình gọi các hàm bên ngoài được cung cấp bởi thư viện dùng chung (shared library). Cơ chế này phối hợp với GOT (Global Offset Table).
    
	.got.plt: Là một bảng dùng để lưu trữ hoặc hỗ trợ tra cứu địa chỉ của các hàm bên ngoài phục vụ cho cơ chế liên kết động. Bảng này thường có quyền ghi khi sử dụng cơ chế lazy binding mặc định. Tuy nhiên, quyền ghi có thể được loại bỏ sau khi các địa chỉ đã được giải quyết, chẳng hạn khi sử dụng cơ chế Relocation Read-Only (RELRO). Biến môi trường LD_BIND_NOW cũng có thể được thiết lập để yêu cầu giải quyết các hàm được nhập ngay khi chương trình khởi tạo.
    
	.rel.*: Chứa thông tin về cách các phần của tệp đối tượng ELF hoặc ảnh chương trình trong bộ nhớ cần được điều chỉnh tại thời điểm liên kết hoặc khi chạy chương trình. Các section này có kiểu SHT_REL. Trong định dạng này, thông tin cộng thêm (addend) được lưu riêng tại vị trí cần thực hiện phép tái định vị.
    
	.rela.*: Tương tự .rel.*, section này chứa thông tin về cách điều chỉnh các phần của tệp ELF tại thời điểm liên kết hoặc khi chạy chương trình. Điểm khác biệt là thông tin cộng thêm (addend) được lưu trực tiếp trong mục tái định vị. Các section này có kiểu SHT_RELA.
    
	.dynamic: Chứa các cấu trúc và đối tượng phục vụ cho việc liên kết động. Section này chứa một bảng gồm các cấu trúc ElfN_Dyn. Nó cũng chứa thông tin tham chiếu đến những thành phần quan trọng mà trình liên kết động cần sử dụng, chẳng hạn như bảng chuỗi động, bảng ký hiệu động, section .got.plt và section tái định vị động. Các thành phần này có thể được tham chiếu thông qua những thẻ như DT_STRTAB, DT_SYMTAB, DT_PLTGOT và DT_RELA.
    
	.init_array: Chứa một mảng các con trỏ hàm dùng làm hàm khởi tạo (constructors). Những hàm này được gọi lần lượt trong quá trình khởi tạo chương trình. Trong GCC, bạn có thể đánh dấu một hàm trong mã nguồn C là hàm khởi tạo bằng cách sử dụng thuộc tính __attribute__((constructor)). Theo mặc định, section này có thể chứa một mục dùng để thực thi hàm frame_dummy.
    
	.fini_array: Chứa một mảng các con trỏ hàm dùng làm hàm hủy (destructors). Những hàm này được gọi trong quá trình kết thúc chương trình hoặc khi thư viện được gỡ bỏ, tùy thuộc vào ngữ cảnh.
    
	.shstrtab: Là một mảng các chuỗi kết thúc bằng ký tự NULL (\0), chứa tên của tất cả các section trong tệp ELF.
    
	.symtab: Chứa bảng ký hiệu (symbol table), gồm các cấu trúc ElfN_Sym. Mỗi cấu trúc liên kết một tên ký hiệu với một đối tượng mã hoặc dữ liệu trong tệp ELF, chẳng hạn như một hàm hoặc một biến.
    
	.strtab: Chứa các chuỗi biểu diễn tên ký hiệu. Các cấu trúc trong .symtab tham chiếu đến những chuỗi này để xác định tên tương ứng.
    
	.dynsym: Tương tự .symtab, nhưng chứa các ký hiệu cần thiết cho quá trình liên kết động thay vì chỉ phục vụ cho việc liên kết tĩnh.
    
	.dynstr: Tương tự .strtab, nhưng chứa các chuỗi tên ký hiệu cần thiết cho quá trình liên kết động.
    
	.interp: Chứa chuỗi chỉ định trình thông dịch chương trình (program interpreter) cần sử dụng để nạp và thực thi tệp ELF. Đối với các chương trình Linux liên kết động, chuỗi này thường chỉ đến trình nạp động, chẳng hạn như ld-linux.
    
	.rel.dyn: Chứa các mục tái định vị động, thường liên quan đến việc điều chỉnh địa chỉ của các đối tượng dữ liệu và những tham chiếu khác cần được xử lý khi nạp chương trình hoặc thư viện.
    
	.rel.plt: Chứa các mục tái định vị liên quan đến các hàm được gọi thông qua PLT, phục vụ cho việc giải quyết địa chỉ hàm trong quá trình liên kết động.

Trong các phiên bản gcc cũ hơn :
- .ctors: Tương đương với .init_array
- .dtors: Tương đương với .fini_
##Program Headers (Phdr)
Bảng Program header cung cấp một góc nhìn theo các segment(phân đoạn) của file binary,trái ngước với góc nhìn theo các section được cung cấp bởi bảng section header
Góc nhìn theo section của một tệp ELF chủ yếu phục vụ mục đích liên kết tĩnh, các công cụ phân tích nhị phân như readelf,objdump,IDA Pro... .
Ngược lại, theo segment được hệ điều hành và dynamic linker sử dụng khi nạp một tệp ELF vào tiến trình để thực thi.Góc nhìn này  cho biết các phần của tệp được tổ chức và ánh xạ vào bộ nhớ như thế nào để thực thi.
<img width="764" height="438" alt="image" src="https://github.com/user-attachments/assets/1ae72113-c484-4226-aa35-5bb892d80a54" />
32-bit struct:
```c
  typedef struct
{
  Elf32_Word	p_type;			/* Segment type */
  Elf32_Off	p_offset;		/* Segment file offset */
  Elf32_Addr	p_vaddr;		/* Segment virtual address */
  Elf32_Addr	p_paddr;		/* Segment physical address */
  Elf32_Word	p_filesz;		/* Segment size in file */
  Elf32_Word	p_memsz;		/* Segment size in memory */
  Elf32_Word	p_flags;		/* Segment flags */
  Elf32_Word	p_align;		/* Segment alignment */
} Elf32_Phdr;
```
64-bit struct:
```c
typedef struct
{
  Elf64_Word	p_type;			/* Segment type */
  Elf64_Word	p_flags;		/* Segment flags */
  Elf64_Off	p_offset;		/* Segment file offset */
  Elf64_Addr	p_vaddr;		/* Segment virtual address */
  Elf64_Addr	p_paddr;		/* Segment physical address */
  Elf64_Xword	p_filesz;		/* Segment size in file */
  Elf64_Xword	p_memsz;		/* Segment size in memory */
  Elf64_Xword	p_align;		/* Segment alignment */
} Elf64_Phdr;
```
Giá trị:
- p_type: các loại segment
   *PT_NULL: Mục Program Header không được sử dụng. Nó thường xuất hiện ở đầu bảng Program Header, nhưng tiêu chuẩn ELF không bắt buộc nó phải là mục đầu tiên.
   *PT_LOAD: Segment có thể được nạp vào bộ nhớ. Hệ điều hành sử dụng thông tin này để xác định phần dữ liệu cần ánh xạ vào bộ nhớ ảo khi thực thi chương trình.
   *PT_DYNAMIC: Chứa thông tin phục vụ liên kết động (dynamic linking), liên quan đến section .dynamic.
   *PT_INTERP: Xác định trình thông dịch chương trình (program interpreter) cần sử dụng. Đối với chương trình ELF liên kết động trên Linux, nó thường chỉ đến trình nạp động như ld-linux. Thông tin đường dẫn này được lưu trong section .interp.
   *PT_GNU_EH_FRAME: Mô tả vị trí và kích thước của bảng dữ liệu .eh_frame_hdr, thường được sử dụng để hỗ trợ tìm kiếm thông tin xử lý ngoại lệ và stack unwinding trong các chương trình được biên dịch bằng GCC hoặc các công cụ tương thích. Nó không trực tiếp chứa các hàm xử lý ngoại lệ.
   *PT_GNU_STACK: Dùng để biểu thị các thuộc tính liên quan đến stack của tiến trình, đặc biệt là việc stack có cần quyền thực thi hay không. Hệ điều hành có thể sử dụng thông tin này để thiết lập quyền bộ nhớ cho stack.
-p_flags:
   *PF_X(execute): Segment có quyền thực thi
   *PF_W(write): Segment có quyền viết
   *PF_R(read): Segment có quyền đọc
-p_offset : độ lệch tính bằng byte từ đầu tệp ELF đếm vị trí dữ liệu tương ứng segment
-p_vaddr : địa chỉ ảo mà segment sẽ được ánh xạ vào trong tệp ELF
-p_paddr : địa chỉ vật lý của segment (trong một số hệ thống chuyên dụng,trường này có thể được dùng để chỉ định địa chỉ vật lý mà segment cần được nạp đến,tuy nhiên trên các hệ điều hanh hiện đại sẽ thường dùng địa chỉ ảo)
-p_filesz: Kích thước segment trong tệp được lưu trong tệp ELF,tính bằng byte
-p_memsz: Kích thước bộ nhớ cần cho segment để lưu vào bộ nhớ
-p_align: xác định yêu cầu căn chỉnh của segment, tương tự trường sh_addralign trong Section Header.
p_type defines:
```c
#define	PT_NULL		0		/* Program header table entry unused */
#define PT_LOAD		1		/* Loadable program segment */
#define PT_DYNAMIC	2		/* Dynamic linking information */
#define PT_INTERP	3		/* Program interpreter */
#define PT_NOTE		4		/* Auxiliary information */
#define PT_SHLIB	5		/* Reserved */
#define PT_PHDR		6		/* Entry for header table itself */
#define PT_TLS		7		/* Thread-local storage segment */
#define	PT_NUM		8		/* Number of defined types */
#define PT_LOOS		0x60000000	/* Start of OS-specific */
#define PT_GNU_EH_FRAME	0x6474e550	/* GCC .eh_frame_hdr segment */
#define PT_GNU_STACK	0x6474e551	/* Indicates stack executability */
#define PT_GNU_RELRO	0x6474e552	/* Read-only after relocation */
#define PT_LOSUNW	0x6ffffffa
#define PT_SUNWBSS	0x6ffffffa	/* Sun Specific segment */
#define PT_SUNWSTACK	0x6ffffffb	/* Stack segment */
#define PT_HISUNW	0x6fffffff
#define PT_HIOS		0x6fffffff	/* End of OS-specific */
#define PT_LOPROC	0x70000000	/* Start of processor-specific */
#define PT_HIPROC	0x7fffffff	/* End of processor-specific */
```
p_flags defines:
```c
#define PF_X		(1 << 0)	/* Segment is executable */
#define PF_W		(1 << 1)	/* Segment is writable */
#define PF_R		(1 << 2)	/* Segment is readable */
#define PF_MASKOS	0x0ff00000	/* OS-specific */
#define PF_MASKPROC	0xf0000000	/* Processor-specific */
```
## Segment
Có 2 loại segment :
  -Text Segment:
     *.text
     *.rodata
     *.hash
     *.dynsym
     *.dynstr
     *.plt
     *.rel.got
 -Data Segment:
     *.data
     *.dynamic
     *.got.plt
     *.bss
## Symbols
Symbol (ký hiệu) là một tham chiếu mang tính biểu tượng đến một loại dữ liệu hoặc mã lệnh nào đó, chẳng hạn như một biến toàn cục hoặc một hàm.
32-bit struct:
```c
typedef struct
{
  Elf32_Word	st_name;		/* Symbol name (string tbl index) */
  Elf32_Addr	st_value;		/* Symbol value */
  Elf32_Word	st_size;		/* Symbol size */
  unsigned char	st_info;		/* Symbol type and binding */
  unsigned char	st_other;		/* Symbol visibility */
  Elf32_Section	st_shndx;		/* Section index */
} Elf32_Sym;
```
64-bít struct: 
```c
typedef struct
{
  Elf64_Word	st_name;		/* Symbol name (string tbl index) */
  unsigned char	st_info;		/* Symbol type and binding */
  unsigned char st_other;		/* Symbol visibility */
  Elf64_Section	st_shndx;		/* Section index */
  Elf64_Addr	st_value;		/* Symbol value */
  Elf64_Xword	st_size;		/* Symbol size */
} Elf64_Sym;
```
Giá trị:
-st_name — Tên symbol: Chỉ số dùng để xác định tên symbol trong bảng chuỗi, thường là .strtab hoặc .dynstr. Ví dụ: main, printf, global_var.
-st_info — Loại và phạm vi liên kết của symbol: Chứa thông tin về kiểu symbol (symbol type) và phạm vi liên kết (symbol binding). Giá trị này được giải mã bằng các macro được định nghĩa trong ELF.
-st_other — Khả năng hiển thị của symbol (symbol visibility): Xác định cách symbol có thể được truy cập hoặc nhìn thấy từ những đối tượng khác.

   * STV_DEFAULT: Khả năng hiển thị mặc định. Symbol có thể được truy cập từ các đối tượng khác nếu phạm vi liên kết và những điều kiện liên quan cho phép. Symbol toàn cục có thể bị thay thế (preempted) trong một số tình huống liên kết động.
   * STV_PROTECTED: Symbol có thể được nhìn thấy từ các đối tượng khác, nhưng các tham chiếu bên trong đối tượng định nghĩa symbol đó sẽ gắn với chính định nghĩa này, không bị thay thế bởi định nghĩa khác.
   * STV_HIDDEN: Symbol không được hiển thị để các đối tượng ELF khác truy cập trực tiếp thông qua cơ chế liên kết thông thường.
   * STV_INTERNAL: Mức hiển thị được dành riêng cho các mục đích đặc biệt theo quy định của nền tảng hoặc hệ thống.

-st_shndx — Chỉ số section: Xác định section liên quan đến symbol. Ví dụ, symbol của một hàm có thể thuộc section .text. Một số giá trị đặc biệt biểu thị symbol chưa được định nghĩa hoặc không gắn với section thông thường.
-st_value — Giá trị symbol: Giá trị của symbol. Tùy loại tệp ELF và loại symbol, trường này có thể biểu thị địa chỉ, độ lệch hoặc một giá trị khác theo quy định của ELF.
-st_size — Kích thước symbol: Kích thước của đối tượng mà symbol đại diện, tính bằng byte, nếu kích thước được xác định. Ví dụ, nó có thể biểu thị kích thước của một hàm hoặc biến.

st_info Values:
-st_bind: Xác định phạm vi liên kết của symbol
  * STB_LOCAL : symbol cục bộ không được hienre thị đê các tệp đói tượng khác tham chiếu thông qua cơ ché liên kết thông thường
  * STB_GLOBAL : Symbol toàn cục có thể được các tệp đối tượng khác tham chiếu khi chúng được liên kết với nhau, miễn là điều kiện liên kết phù hợp
  * STB_WEAK : Symbol yếu có cách xử lý tương tự symbol toàn cục,nhưng có độ ưu tiên thấp hơn trong một số quy tắc phân giải symbol
-st_type: kiểu symbol
  *STT_NOTYPE: Symbol kiểu không được định nghĩa
  *STT_FUNC: Symbol đại diện cho một hàm hoặc một đoạn mã thực thi khác
  *STT_OBJECT:Symbol đại dienj cho một đối tượng dữ liệu ví dụ như biến toàn cục
  *STT_SECTION: Symbol đại diện cho một section trong tệp ELF.các symbol này thượng được sử dụng trong các tệp đối tượng phục vụ quá trình liên kết

-Các macro

  *ELFN_ST_BIND(st_info): Lấy giá trị st_bind từ st_info.
  *ELFN_ST_TYPE(st_info): Lấy giá trị st_type từ st_info.
  *ELFN_ST_INFO(st_bind, st_type): Tạo giá trị st_info từ st_bind và st_type.

-Các macro xử lý st_info
```c

#define ELF32_ST_BIND(val)       (((unsigned char) (val)) >> 4)
#define ELF32_ST_TYPE(val)       ((val) & 0xf)
#define ELF32_ST_INFO(bind, type) (((bind) << 4) + ((type) & 0xf))

#define ELF64_ST_BIND(val)       ELF32_ST_BIND (val)
#define ELF64_ST_TYPE(val)       ELF32_ST_TYPE (val)
#define ELF64_ST_INFO(bind, type) ELF32_ST_INFO ((bind), (type))
```
Ý nghĩa:

    ELF32_ST_BIND(val): Lấy 4 bit cao để xác định phạm vi liên kết của symbol.
    ELF32_ST_TYPE(val): Lấy 4 bit thấp để xác định loại symbol.
    ELF32_ST_INFO(bind, type): Kết hợp giá trị binding và type thành một byte st_info.
    Các macro ELF64 sử dụng cùng cách mã hóa này như các macro ELF32.

Các giá trị của st_bind
```c
#define STB_LOCAL	0		/* Local symbol */
#define STB_GLOBAL	1		/* Global symbol */
#define STB_WEAK	2		/* Weak symbol */
#define	STB_NUM		3		/* Number of defined types.  */
#define STB_LOOS	10		/* Start of OS-specific */
#define STB_GNU_UNIQUE	10		/* Unique symbol.  */
#define STB_HIOS	12		/* End of OS-specific */
#define STB_LOPROC	13		/* Start of processor-specific */
#define STB_HIPROC	15		/* End of processor-specific */
```
st_type defines:
```c
#define STT_NOTYPE	0		/* Symbol type is unspecified */
#define STT_OBJECT	1		/* Symbol is a data object */
#define STT_FUNC	2		/* Symbol is a code object */
#define STT_SECTION	3		/* Symbol associated with a section */
#define STT_FILE	4		/* Symbol's name is file name */
#define STT_COMMON	5		/* Symbol is a common data object */
#define STT_TLS		6		/* Symbol is thread-local data object*/
#define	STT_NUM		7		/* Number of defined types.  */
#define STT_LOOS	10		/* Start of OS-specific */
#define STT_GNU_IFUNC	10		/* Symbol is indirect code object */
#define STT_HIOS	12		/* End of OS-specific */
#define STT_LOPROC	13		/* Start of processor-specific */
#define STT_HIPROC	15		/* End of processor-specific */
```
