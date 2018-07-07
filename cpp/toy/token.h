#ifndef TOKEN_H__
#define TOKEN_H__

#include <string>

// Token的类型
enum Type {
    kINTEGER = 0,
    kEOF,
    kPLUS,
    kMINUS,
    kMULTI,
    kDIVID
};

struct Token {
        Token() :
            type_(kEOF), value_("") {  }

        Token(Type type, const std::string& value) :
            type_(type), value_(value) {  }

        Token(const Token &) = default;

        Token& operator=(const Token &) = default;

        char* ToString() const;

        Type type_;
        std::string value_;
};

#endif /* TOKEN_H__ */
