#include <iostream>
#include <string>

int main() {
    std::string str_1 = "737";
    std::cout << std::stoi(str_1) << std::endl;
    std::string str_2 = "0x37";
    std::cout << std::stoi(str_2, nullptr, 0) << std::endl;
}

