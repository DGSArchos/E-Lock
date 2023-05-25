#include "lwip/apps/httpd.h"
#include "pico/cyw43_arch.h"

#define ELECTROAIMANT 16

// CGI handler which is run when a request for /led.cgi is detected
const char * cgi_led_handler(int iIndex, int iNumParams, char *pcParam[], char *pcValue[])
{
    gpio_init(ELECTROAIMANT);
    gpio_set_dir(ELECTROAIMANT, GPIO_OUT);
    
    // Check if an request for LED has been made (/led.cgi?led=x)
    if (strcmp(pcParam[0] , "led") == 0){
        // Look at the argument to check if LED is to be turned on (x=1) or off (x=0)
        if(strcmp(pcValue[0], "0") == 0)
            gpio_put(ELECTROAIMANT, 0);
        else if(strcmp(pcValue[0], "1") == 0)
            gpio_put(ELECTROAIMANT, 1);
    }
    
    // Send the index page back to the user
    return "/index.shtml";
}

// tCGI Struct
// Fill this with all of the CGI requests and their respective handlers
static const tCGI cgi_handlers[] = {
    {
        // Html request for "/led.cgi" triggers cgi_handler
        "/led.cgi", cgi_led_handler
    },
};

void cgi_init(void)
{
    http_set_cgi_handlers(cgi_handlers, 1);
}