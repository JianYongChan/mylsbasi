#include <iostream>
#include <string>
#include "interpreter.h"

int main() {
    std::cout << "calc> ";
    std::string expr;

    while (std::getline(std::cin, expr)) {
        Interpreter interpreter (expr.c_str());
        int result = interpreter.Expr();
        std::cout << result << std::endl;
        std::cout << "calc> ";
    }
}
