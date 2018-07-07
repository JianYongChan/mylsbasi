#include <iostream>
#include <string>
#include "interpreter.h"

int main() {
    std::cout << "calc> ";
    std::string expr;

    while (std::getline(std::cin, expr)) {
        std::cout << expr << std::endl;
        Interpreter interpreter (expr.c_str());
        int result = interpreter.Expr();
        std::cout << "result: " << result << std::endl;
        std::cout << "calc> ";
    }
}
