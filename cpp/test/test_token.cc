#include <iostream>
#include "../toy/token.h"

int main() {
    Token t1 (kPLUS, "XiBei");
    Token t2 = t1;
    std::cout << t2.value_ << std::endl;
    Token t3 (kPLUS, "TangMou");
    std::cout << t3.value_ << std::endl;
    t3 = t1;
    std::cout << t3.value_ << std::endl;
}
