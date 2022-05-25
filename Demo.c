#include <stdio.h>
#include <stdbool.h>
#if defined(D_NEXYS_A7)                 //Check to see if platform was defined
   #include <bsp_printf.h>
   #include <bsp_mem_map.h>
   #include <bsp_version.h>
#else                       
   PRE_COMPILED_MSG("no platform was defined")
#endif
#include <psp_api.h>

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//System Defines
//Scope: Global
//System controller addresses for GPIO Switches and LEDS
#define GPIO_SWs    0x80001400
#define GPIO_LEDs   0x80001404
#define GPIO_INOUT  0x80001408

#define GPIO2_BTNs  0x80001800  //Buttuon BTNC
#define GPIO2_INOUT 0x80001808

#define SegEn_ADDR    0x80001038
#define SegDig_ADDR   0x8000103C

#define GPIO3_BTNs  0x8000101C  //Button BTNU/L/R/D 0x02/4/8/10

#define secDelay    10000000

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//GPIO Helper Functions
#define READ_GPIO(dir) (*(volatile unsigned *)dir)
#define WRITE_GPIO(dir, value) { (*(volatile unsigned *)dir) = (value); }
#define WRITE_7Seg(dir, value) { (*(volatile unsigned *)dir) = (value); } 
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

int main(void)
{
//Scope: main Function

//Variable Definitions
int En_Value=0xFFFF, count = 0, mode = 1; 
int i, switches_value, buttons2_value, buttons3_value, buttons4_value, buttons5_value, buttons6_value; 

char char_Val;
//Initialization of Modules
uartInit();             //initialization of the UART
WRITE_GPIO(GPIO_INOUT, En_Value);       //Initialization of SW and LED GPIO Ports
WRITE_GPIO(GPIO2_INOUT, 0x0);           //Initializaiton of Push Buttons

WRITE_7Seg(SegEn_ADDR, 0xFFFFFFFF);
WRITE_7Seg(SegDig_ADDR, 0xFFFFFFFF);

//Test for connection
printfNexys("SweRV EH1 processor Connected");       //test String to see that the uart is communicating properly
printfNexys("UART connected to Serial Terminal");
printfNexys("Check the LEDs to see progress of Program uploading");

for(int m = 1; m < 0xFFFF; m = m*2)
{
    WRITE_GPIO(GPIO_LEDs, m);
    for(int j =0; j < 0.5* secDelay; j++){}          //Delay to see test values

}
    
    printfNexys("Program Ready.");
    printfNexys("Link Start");
//for(int j =0; j < secDelay; j++){}          //Delay to see test values

    while(1) //Scope: Infinite Loop
    {  

        if(mode == 1)
        {
            buttons3_value = READ_GPIO(GPIO3_BTNs);
            buttons3_value = buttons3_value & 0x2;
            if (buttons3_value==0x2)   
                {
                count = 0;
                printfNexys("Restarting");
                }

            buttons4_value = READ_GPIO(GPIO3_BTNs);
            buttons4_value = buttons4_value & 0x4;
            if (buttons4_value==0x4) 
                {
                    count += 60;
                    printfNexys("Minute Skip.");
                }
            buttons5_value = READ_GPIO(GPIO3_BTNs);
            buttons5_value = buttons5_value & 0x8;
            if (buttons5_value==0x8) 
                {
                    count *= 2;
                    printfNexys("Double Time!!");
                }
            else count++;

            buttons6_value = READ_GPIO(GPIO3_BTNs);
            buttons6_value = buttons6_value & 0x10;
            if (buttons6_value==0x10) 
                {
                    count = 0xFFFF;
                    printfNexys("OVERLOAD INCOMING!");
                }
            WRITE_GPIO(GPIO_LEDs, count);

            for (i=0; i<secDelay; i++);

            buttons2_value = READ_GPIO(GPIO2_BTNs);
            if (buttons2_value==0x1) mode = 2;

            
        }

        else if (mode == 2)
        {
            switches_value = READ_GPIO(GPIO_SWs);
            switches_value = switches_value >> 16;
            WRITE_GPIO(GPIO_LEDs, switches_value);

            buttons3_value = READ_GPIO(GPIO3_BTNs);
            buttons3_value = buttons3_value & 0x2;
            if (buttons3_value==0x2)   
                {
                char_Val = switches_value + '0';
                printfNexys("%c",char_Val);
                } 
            buttons4_value = READ_GPIO(GPIO3_BTNs);
            buttons4_value = buttons4_value & 0x4;
            if (buttons4_value==0x4) 
                {
                    printfNexys("Printing Message");
                    WRITE_7Seg(SegEn_ADDR, 0x30717101);
                    WRITE_7Seg(SegDig_ADDR, 0xFFFFFF48);
                }
            
            
            
            for (int l =0; l < secDelay; l++){};
            
            buttons2_value = READ_GPIO(GPIO2_BTNs);
            if (buttons2_value==0x1) mode = 1;
        }

    }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//User Functions

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////