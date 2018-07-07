#include <string>
#include "interpreter.h"

// 对表达式求值
int Interpreter::Expr() {
    // 将现下的token设置为第一个token
    current_token_ = GetNextToken();

    // 第一个token应该是一个数字
    Token left = current_token_;
    Eat(kINTEGER);
    int result = std::stoi(left.value_);
    std::cout << "now result = " << result << std::endl;

    while (current_char_ != '\0') {
        Token op = current_token_;
        std::cout << "op: " << op.value_ << std::endl;
        if (op.value_ == "+") {
            std::cout << "KPLUS" << std::endl;
            Eat(kPLUS);
        } else if (op.value_ == "-") {
            Eat(kMINUS);
        } else if (op.value_ == "*") {
            Eat(kMULTI);
        } else if (op.value_ == "/") {
            Eat(kDIVID);
        }

        Token right = current_token_;
        Eat(kINTEGER);
        int right_val = std::stoi(right.value_);

        if (op.type_ == kPLUS) {
            result += right_val;
            std::cout << "kplus" << std::endl;
            std::cout << "result: " << result << std::endl;
        } else if (op.type_ == kMINUS) {
            result -= right_val;
        } else if (op.type_ == kMULTI) {
            result *= right_val;
        } else if (op.type_ == kDIVID) {
            result /= right_val;
        }
    }

    return  result;
}

// 跳过空格
void Interpreter::SkipWhitespace() {
    while (current_char_ == ' ') {
        Advance();
    }
}

// 验证当前的Token是否为所需要的类型
void Interpreter::Eat(Type type) {
    if (current_token_.type_ != type) {
        Error();
    } else {
        current_token_ = GetNextToken();
    }
}

void Interpreter::Advance() {
    pos += 1;
    if (pos >= strlen(text_)) {
        // '\0'表示结束了
        current_char_ = '\0';
    } else {
        current_char_ = text_[pos];
    }
}

void Interpreter::Error() const {
    perror("Parsing Error\n");
}

void Interpreter::ParseInteger(std::string *pstr) {
    std::string result = "";
    while (isdigit(current_char_)) {
        result += current_char_;
        Advance();
    }

    *pstr = result;
}

Token Interpreter::GetNextToken() {
    while (current_char_ != '\0') {
        if (isspace(current_char_)) {
            SkipWhitespace();
            continue;
        }

        if (isdigit(current_char_)) {
            std::string intstr;
            ParseInteger(&intstr);
            return Token(kINTEGER, intstr.c_str());
        }

        if (current_char_ == '+') {
            Advance();
            return Token(kPLUS, "+");
        }

        if (current_char_ == '-') {
            Advance();
            return Token(kMINUS, "-");
        }

        if (current_char_ == '*') {
            Advance();
            return Token(kMULTI, "*");
        }

        if (current_char_ == '/') {
            Advance();
            return Token(kMULTI, "/");
        }

        Error();
    }

        return Token();
}
