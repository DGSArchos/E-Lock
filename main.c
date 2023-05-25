#include "lwip/apps/httpd.h"
#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "lwipopts.h"
#include "cgi.h"
#include "ssi.h"

#define ELECTROAIMANT 16

// Wifi Infos
const char WIFI_SSID[] = "Chris";
const char WIFI_PASSWORD[] = "Password";

// main
int main(){
    stdio_init_all();

    gpio_init(ELECTROAIMANT);
    gpio_set_dir(ELECTROAIMANT, GPIO_OUT);
    
    cyw43_arch_init();

    cyw43_arch_enable_sta_mode();

    // Essayer de se connecter au réseaux
    while(cyw43_arch_wifi_connect_timeout_ms(WIFI_SSID, WIFI_PASSWORD, CYW43_AUTH_WPA2_AES_PSK, 5000) != 0){
        printf("En attente de connexion...\n");
    }

    // Afficher un message de succès
    printf("Connexion etablie !\n");

    // initialiser le serveur
    httpd_init();
    printf("Serveur http initialisé !\n");

    // initialiser SSI & CGI
    ssi_init();
    printf("SSI initialisé\n");
    cgi_init();
    printf("CGI initialisé\n");

    // boucle infini
    while(1);
    
}