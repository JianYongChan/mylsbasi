#ifndef INTERPRETER_H__
#define INTERPRETER_H__

#include <string.h>
#include <iostream>
#include "token.h"


class Interpreter {
    public:
        Interpreter(const char* text) :
            text_(text), current_token_() { }

        int Expr();

        void Eat(Type type);

    private:
        const char* text_;
        int pos = 0;
        Token current_token_;
        char current_char_ = text_[0];

        // 跳过空格
        void SkipWhitespace();

        // 前进到下一个token
        void Advance();

        // 遇到异常输出错误信息
        // 比如输入的表达式不符合要求
        void Error() const;

        // 将字符串解析为数字
        void ParseInteger(std::string *pstr);

        // 这个方法将一条算术表达式分解为多个token
        Token GetNextToken();
};

#endif /* INTERPRETER_H__ */
