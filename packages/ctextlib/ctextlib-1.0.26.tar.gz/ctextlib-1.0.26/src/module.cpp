// https://docs.microsoft.com/en-us/visualstudio/python/working-with-c-cpp-python-in-visual-studio?view=vs-2017&viewFallbackFrom=vs-2015//
// https://pybind11.readthedocs.io/en/stable/classes.html

#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <pybind11/numpy.h>
#include <cmath>
#include <string>

#include "CTextA.h"   //ANSI/UTF8 
#include "CTextU.h"   //Unicode-16
 
//PYBIND11_MAKE_OPAQUE(std::vector<std::string>);
//PYBIND11_MAKE_OPAQUE(std::vector<CTextA>);

namespace py = pybind11;

using namespace std;

PYBIND11_MODULE(ctextlib, m)
{
    py::class_<CTextA> (m, "Text")
        // constructors
        .def(py::init<>())
        .def(py::init<const char*>())
        .def(py::init<const std::string &>())
        // operators
        .def(py::self + py::self)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self < py::self)
        .def(py::self > py::self)
        // .def(py::self + char())
        // .def(char() + py::self)
        .def(py::self + std::string())
        .def(std::string() + py::self)
        .def(py::self += py::self)
        .def(py::self += std::string())
        .def("__add__", [](const CTextA& c2, const CTextA& c1) { return c2 + c1; })
        .def("__add__", [](const CTextA& c1, const char* c2) { return c2 + c1; })
        .def("__repr__", [](const CTextA &a) { return a.str() == nullptr? "": a.str(); })
        // functions
        .def("addToFileName", &CTextA::addToFileName, "modifies a filename, adds the provided string to file name but keeps extension and path")
        .def("append", [](CTextA& s, const char* str)->CTextA& { return s.append(str); }, "append string", py::arg("str"))
        .def("append", [](CTextA& s, const char* str, size_t len)->CTextA& { return s.append(*str, len); }, "append characters", py::arg("c"), py::arg("len") = 1)
        .def("append", [](CTextA& s, const vector<string>& list)->CTextA& { return s.append(list); }, "append single character or string list", py::arg("list")) 
        .def("appendRange", [](CTextA& s, const char* begin, const char* end)->CTextA& { return s.appendRange(*begin, *end); }, "append all characters in the range ", py::arg("begin"), py::arg("end"))  
        .def("between", [](CTextA& s, const char* left, const char* right, bool include)->bool { return s.between(left, right, include); }, "keeps the part of the string between the first and last sub-strings sLeft and sRight (by default separattors are not included", py::arg("left"), py::arg("right"), py::arg("include") = false)
        .def("capacity", &CTextA::capacity)
        .def("clear", &CTextA::clear, py::arg("bRelease") = false)
        .def("collectBlocks", [](CTextA& s, const char* sepBegin, const char* sepEnd, bool all)->vector<string> {  vector<string> res;  s.collectBlocks(res, sepBegin, sepEnd, all); return res; }, "collect blocks", py::arg("sepBegin"), py::arg("sepEnd"), py::arg("all") = true)
        .def("collectLines", [](CTextA& s, const char* sep)->vector<string> {  vector<string> res;  s.collectLines(res, false, sep); return res; }, "fills a list with the collected lines", py::arg("sep") = CTextA::SeparatorsLine)
        .def("checkBalance", &CTextA::checkBalance, "checks if the blocks defined with the given separators are balanced")  
        .def("contain", (bool (CTextA::*)(const char* s, bool bCase) const) &CTextA::contain, "returns true if our string contains another string  ", py::arg("str"), py::arg("case") = true)
        .def("contain", [](CTextA& s, const vector<string>& list, bool bCase)->bool { return s.containAny(list, bCase, true); }, "returns true if contains any of the provided strings", py::arg("list"), py::arg("case") = true)
        .def("containAny", (bool (CTextA::*)(const char* s, bool bCase) const) &CTextA::containAny, "returns true if our string contains any of the characters in the list", py::arg("str"), py::arg("case") = true)
        .def("containOnly", (bool (CTextA::*)(const char* s, bool bCase) const) &CTextA::containOnly, "returns true if our string contains only characters in the list", py::arg("str"), py::arg("case") = true)
        .def("count", [](CTextA& s, const char* str, bool bCase)->size_t { return s.count(str, bCase); }, "returns the count of occurences of the given substring", py::arg("str"), py::arg("case") = true)
        .def("countWordFrequencies", [](CTextA& s, bool bCase, const char* sep)->std::vector< std::pair<int, string> > { std::vector< std::pair<int, string> >  res;  s.countWordFrequencies(res, bCase, sep); return res; }, "fill the container with the words frequency counts", py::arg("case") = true, py::arg("sep") = CTextA::SeparatorsWord) 
        .def("cutAfterFirst", [](CTextA& s, const char* str, bool include, bool bCase)->CTextA& { return s.cutAfterFirst(*str, include, bCase); }, "leaves everyting left from c, c is not included, everything after is removed", py::arg("str"), py::arg("include") = false, py::arg("case") = true)
        .def("cutAfterLast", [](CTextA& s, const char* str, bool include, bool bCase)->CTextA& { return s.cutAfterLast(*str, include, bCase); }, "leaves everyting left from the last character, c is not included", py::arg("str"), py::arg("include") = false, py::arg("case") = true)
        .def("cutBeforeFirst", [](CTextA& s, const char* str, bool include, bool bCase)->CTextA& { return s.cutBeforeFirst(*str, include, bCase); }, "cut everything before the first occurence of string str", py::arg("str"), py::arg("include") = false, py::arg("case") = true)
        .def("cutAfterFirstOfAny", [](CTextA& s, const char* str, bool include, bool bCase)->CTextA& { return s.cutAfterFirstOfAny(str, include, bCase); }, "cut after the first occurence of any character from the list", py::arg("str"), py::arg("include") = false, py::arg("case") = true)
        .def("cutBeforeFirstOfAny", [](CTextA& s, const char* str, bool include, bool bCase)->CTextA& { return s.cutBeforeFirstOfAny(str, include, bCase); }, "cut everything before the first occurence of any of the characters from the list or leave intact, include if set, character is included", py::arg("str"), py::arg("include") = false, py::arg("case") = true)
        .def("cutEnds", (CTextA& (CTextA::*)(size_t)) &CTextA::cutEnds, "remove count of characters from left and right", py::arg("count"))
        .def("cutLeft", &CTextA::cutLeft, "removes count characters from left", py::arg("count"))
        .def("cutRight", &CTextA::cutRight, "removes count characters from left", py::arg("count"))
        .def("enclose", [](CTextA& s, const char* str)->CTextA& {return s.enclose(str,str); }, "enclose with same character", py::arg("c"))
        .def("enclose", (CTextA& (CTextA::*)(const char* begin, const char* end, bool checkEnds)) &CTextA::enclose, "enclose with the provided text separators (if not already ends and begins with them)", py::arg("begin"), py::arg("end"), py::arg("checkEnds") = true)          
        .def("endsWith", [](CTextA& s, const char* str, bool bCase)->bool { return s.endsWith(str, 0, bCase); }, "return true if ends with the provided string", py::arg("str"), py::arg("case") = true)
        .def("endsWithAny", [](CTextA& s, const vector<string>& list, bool bCase)->bool { return s.endsWithAny(list, 0, bCase, true); }, "returns true if ends with any of the strings from the list", py::arg("list"), py::arg("case") = true)
        .def("equal", [](CTextA& s, const char* str, size_t len)->CTextA& { return s.equal(*str, len); }, "init witb len number of characters", py::arg("c"), py::arg("len"))
        .def("erase", &CTextA::erase, "delete count characters starting at zero-based index", py::arg("from"), py::arg("count") = 1)
        .def("find", (const char* (CTextA::*)(const char* s, bool bCase) const) &CTextA::find, "return a pointer to the first occurence of the string, or 0 pointer if not found", py::arg("str"), py::arg("case") = true)      
        .def("first", &CTextA::first) 
        .def("fromArray", [](CTextA& s, const vector<int>& list, const char* sep)->void { s.fromArray<int>(list, false, 2, sep); }, "compose a string from array using the given separator", py::arg("list"), py::arg("sep") = CTextA::SPACE)
        .def("fromArray", [](CTextA& s, const vector<float>& list, const char* sep)->void { s.fromArray<float>(list, false, 2, sep); }, "compose a string from array using the given separator", py::arg("list"), py::arg("sep") = CTextA::SPACE)
        .def("fromArray", [](CTextA& s, const vector<string>& list, const char* sep)->void { s.fromArray(list, sep); }, "compose a string from array using the given separator", py::arg("list"), py::arg("sep") = CTextA::SPACE)        
        .def("fromArrayAsHex", [](CTextA& s, const vector<int>& list, int wHex, const char* sep)->void { s.fromArray<int>(list, true, wHex, sep); }, "compose a string from integerrs array in hex format using the given separator", py::arg("list"), py::arg("wHex") = 2, py::arg("sep") = CTextA::SPACE) 
        .def("fromBinary", &CTextA::fromBinary<char>, "create a binary string from the number")
        .def("fromBinary", &CTextA::fromBinary<int>, "create a binary string from the number")
        .def("fromBinary", &CTextA::fromBinary<long long>, "create a binary string from the number")
        .def("fromHex", &CTextA::fromHex, "create a hexadecimal string from the number", py::arg("s"))
        .def("fromHex", &CTextA::fromHexNumber<char>, "create a hexadecimal string from the number", py::arg("i"), py::arg("hasBase") = false, py::arg("upper") = false, py::arg("append") = false)
        .def("fromHex", &CTextA::fromHexNumber<int>, "create a hexadecimal string from the number", py::arg("i"), py::arg("hasBase") = false, py::arg("upper") = false, py::arg("append") = false)
        .def("fromHex", &CTextA::fromHexNumber<long long>, "create a hexadecimal string from the number", py::arg("i"), py::arg("hasBase") = false, py::arg("upper") = false, py::arg("append") = false)
        .def("fromInteger", &CTextA::fromInteger<char>, "convert the decimal nteger to string", py::arg("i"), py::arg("append") = false, py::arg("padd") = 0, py::arg("paddValue") = '0')
        .def("fromInteger", &CTextA::fromInteger<int>, "convert the decimal nteger to string", py::arg("i"), py::arg("append") = false, py::arg("padd") = 0, py::arg("paddValue") = '0')
        .def("fromInteger", &CTextA::fromInteger<long long>, "convert the decimal integer to string", py::arg("i"), py::arg("append") = false, py::arg("padd") = 0, py::arg("paddValue") = '0')
        .def("fromDouble", &CTextA::fromDouble, "convert double to string", py::arg("d"), py::arg("precision") = 6, py::arg("fixed") = true, py::arg("nozeros") = false, py::arg("append") = false)
        .def("fromMatrix", [](CTextA& s, py::array_t<int> m, const char* sep, const char* sepLine)->void {   py::buffer_info buf = m.request();  size_t h = buf.shape[0]; size_t w = buf.shape[1]; int* ptr = (int*)buf.ptr; s.fromMatrix<int>(ptr, w, h, false, 2, sep, sepLine);  }, "//compose string from a 2D numerical matrix", py::arg("list"), py::arg("sep") = CTextA::SPACE, py::arg("sepLine") = CTextA::EOL)
        .def("fromMatrix", [](CTextA& s, py::array_t<double> m, const char* sep, const char* sepLine)->void {   py::buffer_info buf = m.request();  size_t h = buf.shape[0]; size_t w = buf.shape[1]; double* ptr = (double*)buf.ptr; s.fromMatrix<double>(ptr, w, h, false, 2, sep, sepLine);  }, "//compose string from a 2D numerical matrix", py::arg("list"), py::arg("sep") = CTextA::SPACE, py::arg("sepLine") = CTextA::EOL)
        .def("fromMatrixAsHex", [](CTextA& s, py::array_t<int> m, int wHex, const char* sep, const char* sepLine)->void {   py::buffer_info buf = m.request();  size_t h = buf.shape[0]; size_t w = buf.shape[1]; int* ptr = (int*)buf.ptr; s.fromMatrix<int>(ptr, w, h, true, wHex, sep, sepLine);  }, "//compose string from a 2D numerical matrix", py::arg("list"), py::arg("wHex") = 2, py::arg("sep") = CTextA::SPACE, py::arg("sepLine") = CTextA::EOL)      
        .def("getDir", &CTextA::getDir, "get a folder from a full module path")
        .def("getExtension", &CTextA::getExtension, "if our string contains file path, return pointer to the extension")
        .def("getFileName", &CTextA::getFileName, "if our string contains file path, return pointer to the file name")
        .def("hash", &CTextA::hash)
        .def("indexOf", [](CTextA& s, const char* str, size_t from, bool bCase)->size_t { return s.lastIndexOf(str, from, bCase); }, "find the offset of first instance of the string in the list, return index or -1 if not found", py::arg("str"), py::arg("from") = 0, py::arg("case") = true)   
        .def("indexOfAny", [](CTextA& s, const char* cList, bool bCase)->size_t { return s.indexOfAny(cList, 0, bCase); }, "find the offset of the first instance of the characters in the list", py::arg("cList"), py::arg("case") = true)
        .def("indexOfAny", [](CTextA& s, const vector<string>& list, bool bCase)->size_t { return s.indexOfAny(list, 0, bCase, true); }, "find the offset of the first instance of the strings in the list", py::arg("list"), py::arg("case") = true)
        .def("insert", [](CTextA& s, size_t from, const char* c, size_t count)->CTextA& { return s.insert(from, *c, count); }, "insert character at zero-based index, if index is past end of string", py::arg("from"), py::arg("c"), py::arg("count"))  
        .def("insert", [](CTextA& s, size_t from, const char* str)->CTextA& { return s.insert(from, str); }, "insert substring at zero-based index; concatenates, if index is past end of string", py::arg("from"), py::arg("str"))
        .def("insertAtBegin", &CTextA::insertAtBegin, py::arg("str"), py::arg("skip") = 1, py::arg("sep") = CTextA::Separators)
        .def("insertAtEnd", &CTextA::insertAtEnd, py::arg("str"), py::arg("skip") = 1, py::arg("sep") = CTextA::Separators)
        .def("isAlpha", &CTextA::isAlpha, "return true if contains only alphabeta characters")
        .def("isBinary", &CTextA::isBinary, "return true if contains only 0s and 1s")
        .def("isEmpty", &CTextA::isEmpty, "return true if empty")
        .def("isHexNumber", &CTextA::isHexNumber, "return true if contains only hexadecimal digits")
        .def("isLower", &CTextA::isLower, py::arg("strict") = false)
        .def("isNumber", &CTextA::isNumber, "return true if contains only decimal digits", py::arg("allowSign") = true)
        .def("isPalindrome", &CTextA::isPalindrome)
        .def("isUpper", &CTextA::isUpper, py::arg("strict") = false)
        .def("keep", &CTextA::keep, "keeps count characters starting from given position")
        .def("keepEnds", &CTextA::keepEnds, "keeps the characters from both ends, returns number of deleted characters")
        .def("keepLeft", &CTextA::keepLeft, "keeps count characters from left and removes the rest, returns number of deleted characters")
        .def("keepRight", &CTextA::keepRight, "keeps count characters from right and removes the rest, returns number of deleted characters")
        .def("left", &CTextA::left, "return new string containing first count characters")
        .def("length", &CTextA::length, "returns the number of characters in the string")
        .def("last", &CTextA::last)
        .def("lastIndexOf", [](CTextA& s, const char* str, size_t from, bool bCase)->size_t { return s.lastIndexOf(str, from, bCase); }, "find the first character position starting at right, where from is the offset from the end and the returned idx is from the beggining", py::arg("str"), py::arg("from") = 0, py::arg("case") = true)    
        .def("lastIndexOfAny", [](CTextA& s, const char* cList, bool bCase)->size_t { return s.lastIndexOfAny(cList, 0, bCase); }, "find the offset of the first instance of the characters in the list starting from right", py::arg("cList"), py::arg("case") = true)
        .def("lines", [](CTextA& s, const char* sep)->vector<string> { vector<string> res;  s.collectLines(res, false, sep); return res; }, "return list with all found lines", py::arg("sep") = CTextA::SeparatorsLine)
        .def("linesCount", &CTextA::linesCount,"returns the number of the lines in the string", py::arg("sep") = CTextA::EOL)
        .def("linesAppend", [](CTextA& s, const char* str, const char* sep)->size_t { return s.linesInsertAtEnd(str, 1, sep);}, "append text to each line", py::arg("str"), py::arg("sep") = CTextA::SeparatorsLine)  
        .def("linesInsertAtBegin", [](CTextA& s, const char* str, const char* sep)->size_t { return s.linesInsertAtBegin(str, 1, sep); }, "insert text at each line begin", py::arg("str"), py::arg("sep") = CTextA::SeparatorsLine)
        .def("linesPaddRight", [](CTextA& s, const char* str, size_t len, const char* sep, const char* sepNew)->size_t { return s.linesPaddRight(*str, len, sep, sepNew); }, "append text to each line", py::arg("str"), py::arg("len"), py::arg("sep") = CTextA::SeparatorsLine, py::arg("sepNew") = CTextA::EOL)
        .def("linesSort", &CTextA::linesSort, py::arg("sep") = CTextA::SeparatorsLine, py::arg("sepNew") = CTextA::EOL)
        .def("linesRemoveEmpty", &CTextA::linesRemoveEmpty, py::arg("minLen") = 0, py::arg("sep") = CTextA::SeparatorsLine)                
        .def("linesTrim", &CTextA::linesTrim, py::arg("cList"), py::arg("sep") = CTextA::SeparatorsLine, py::arg("sepNew") = CTextA::EOL)
        .def("limit", &CTextA::limit, "limit the the length, if our text length is smaller nothing is done")
        .def("lower", &CTextA::toLower, "conversion to lowercase (in place)")
        .def("makeUnique", (size_t(CTextA::*)()) &CTextA::makeUnique, "make sure that all characters occurs only once")
        .def("mid", &CTextA::mid, "leaves the middle characters, count characters are cut from both ends, returns new string")   
        .def("nextLine", [](CTextA& s, int pos, CTextA& line, bool appendSeparators, const char* sep)->int { size_t _pos = pos;  bool res = s.nextLine(_pos, line, appendSeparators, sep); return res ? (int)_pos : -1; }, py::arg("pos"), py::arg("line"), py::arg("appendSeparators") = false, py::arg("sep") = CTextA::SeparatorsLine)
        .def("nextWord", [](CTextA& s, int pos, CTextA& line, const char* sep)->int { size_t _pos = pos;  bool res = s.nextWord(_pos, line, sep); return res ? (int)_pos : -1; }, py::arg("pos"), py::arg("line"), py::arg("sep") = CTextA::SeparatorsWord)
        .def("paddLeft", &CTextA::paddLeft, "fills from start with the given characters until given lenght")
        .def("paddRight", &CTextA::paddRight, "fills from end with the given characters until given lenght")   
        .def("pathCombine", &CTextA::pathCombine, "combine paths, C:\\Temp\" + \"..\\Folder\\\" = \"C:\\Folder")
        .def("push_back", (CTextA& (CTextA::*)(const char*)) &CTextA::push_back, "append string")
        .def("push_front", (CTextA& (CTextA::*)(const char*)) &CTextA::push_front, "insert string at start")
        .def("quote", &CTextA::quote)
        .def("randomAlpha", &CTextA::randomAlpha, "generate text containing random alpha upper and lower characters ", py::arg("len") = 16)
        .def("random", &CTextA::randomAlphaNumeric, "generate text containing random alphanumeric upper and lower characters ", py::arg("len") = 16)
        .def("randomNumber", &CTextA::randomNumber, "generate text containing a random integer with the given length", py::arg("len") = 10)
        .def("reduceChain", [](CTextA& s, const char* cList, const char* cNew)->CTextA { return s.reduceChain(cList, *cNew); }, "reduce blocks of the separators from the list to a single character", py::arg("cList") = CTextA::SeparatorsWord, py::arg("cNew") = CTextA::SPACE)
        .def("regexLines", [](CTextA& s, const char* regex, const char* sep)->vector<string> { vector<string> res;  s.regexCollectLines(res, regex, sep); return res;  }, "collect all lines matching the given regex condition", py::arg("regex"), py::arg("sep") = CTextA::SeparatorsLine)
        .def("regexWords", [](CTextA& s, const char* regex, const char* sep)->vector<string> { vector<string> res;  s.regexCollectWords(res, regex, sep); return res;  }, "collect all words matching the given regex condition", py::arg("regex"), py::arg("sep") = CTextA::SeparatorsWord)
        .def("regexSearch", [](CTextA& s, const char* regex)->vector<string> { vector<string> res;  s.regexSearch(res, regex); return res;  }, "collect substrings using the provided Regex expression and regex_iterator", py::arg("regex"))
        .def("regexReplace", (CTextA& (CTextA::*)(const char* regexp, const char* fmt)) &CTextA::regexReplace, "replace strings using the provided Regex expression")
        .def("regexMatch", (bool (CTextA::*)(const char*) const) &CTextA::regexMatch)         
        .def("remove", (size_t(CTextA::*)(const char*, bool)) &CTextA::remove, "delete all occurences of the string s", py::arg("str"), py::arg("case") = true)
        .def("removeAny", (size_t(CTextA::*)(const char*, bool)) &CTextA::removeAny, "delete all of provided in the list characters", py::arg("str"), py::arg("case") = true)
        .def("removeAny", &CTextA::removeAny<vector<string>>, "remove any from the provided in the list strings", py::arg("list"), py::arg("case") = true, py::arg("longList") = true)
        .def("removeExtension", &CTextA::removeExtension, "remove the extension from a file path")
        .def("removeFileName", &CTextA::removeFileName, "if string contain file path, remove the file name", py::arg("keepSlash") = true)
        .def("removeLast", &CTextA::removeLast, "removes the last character, return true if not empty and sucessful")
        .def("removeWhileBegins", &CTextA::removeWhileBegins, "remove the characters from str while begins to the characters from our string", py::arg("str"))
        .def("removeWhileEnds", &CTextA::removeWhileEnds, "remove the characters from str while ends to the characters from our string", py::arg("str"))       
        .def("replace", (size_t (CTextA::*)(const char* what, const char* with, bool bCase)) &CTextA::replace, "replace all occurrences of substring \"what\" with substring \"with\"", py::arg("what"), py::arg("with"), py::arg("case") = true)    
        .def("replace", [](CTextA& s, const char* str, size_t len, const char* c)->CTextA& { return s.replace(*str, len, *c); }, "replace range with single character", py::arg("str"), py::arg("len"), py::arg("c"))  
        .def("replace", [](CTextA& s, const vector<string>& what, const char* c, bool bCase)->CTextA& { return s.replaceAny(what, *c, bCase, true); }, "replace all found strings in list 'what' with a single character ", py::arg("what"), py::arg("with"), py::arg("case") = true)
        .def("replaceAny", [](CTextA& s, const vector<string>& what, const vector<string>& with, bool bCase)->CTextA& { return s.replaceAny(what, with, bCase, true); }, "replace found strings in list 'what' with corresponding strings from list 'with' ", py::arg("what"), py::arg("with"), py::arg("case") = true)
        .def("replaceAny", [](CTextA& s, const vector<string>& what, const char* with, bool bCase)->CTextA& { return s.replaceAny(what, with, bCase, true); }, "replace found strings in list 'what' with the string 'with' ", py::arg("what"), py::arg("with"), py::arg("case") = true)
        .def("replaceExtension", &CTextA::replaceExtension, "change the file path extension")
        .def("replaceFileName", &CTextA::replaceFileName, "change the file name")
        .def("replaceLastFolder", &CTextA::replaceLastFolder, "replace last folder name")
        .def("replaceFirst", &CTextA::replaceFirst, "replace first character")
        .def("replaceLast", &CTextA::replaceFirst, "replace last character")     
        .def("readFile", &CTextA::readFile<char>, "reads a text file into the string", py::arg("path"), py::arg("asHex") = false)
        .def("reverse", &CTextA::reverse)
        .def("reverseFind", &CTextA::reverseFind, py::arg("s"), py::arg("case") = true)
        .def("right", &CTextA::right, "return new string with count characters from the end of our string")
        .def("rotateLeft", &CTextA::rotateLeft, "rotate tne string to the left")
        .def("rotateRight", &CTextA::rotateRight, "rotate tne string to the right")
        .def("sentences", [](CTextA& s, const char* sep, const char* sepWords)->vector<string> { vector<string> res;  s.collectSentences(res, sep); return res; }, "return list with all found words", py::arg("sep") = CTextA::SeparatorsWord, py::arg("sepWords") = CTextA::SeparatorsWord)
        .def("shuffle", &CTextA::shuffle)
        .def("sort", &CTextA::sort)
        .def("split",[](CTextA& s, const char* sep = CTextA::Separators)->vector<string> { vector<string> res;  s.split(res, false, sep); return res; }, "fills the STL container with the collected substrings", py::arg("sep") = CTextA::Separators)
        .def("str", (const char* (CTextA::*)(size_t pos) const) &CTextA::str, "return text buffer", py::arg("pos") = 0)
        .def("toBinary", &CTextA::toBinary, "if the string contains a binary number, convert it  ")
        .def("toHex", &CTextA::toHex, "convert string to hex values separated by the given separator", py::arg("sep") = CTextA::SPACE)
        .def("toHexNumber", &CTextA::toHexNumber, "if the string contains a hex number, convert it , 1E --> 30")
        .def("toDouble", &CTextA::toDouble)
        .def("toInteger", &CTextA::toInteger)     
        .def("trim", &CTextA::trim, "trim string from both sides", py::arg("cList") = CTextA::Separators)
        .def("trim", &CTextA::trim, "trim string from both sides", py::arg("cList") = CTextA::Separators)
        .def("trimLeft", (CTextA& (CTextA::*)(const char*)) &CTextA::trimLeft, "trim string from left", py::arg("cList") = CTextA::Separators)
        .def("trimRight", (CTextA& (CTextA::*)(const char*)) &CTextA::trimRight, "trim string from right", py::arg("cList") = CTextA::Separators)
        .def("upper", &CTextA::toUpper, "conversion to uppercase (in place)")
        .def("words", [](CTextA& s, const char* sep)->vector<string> { vector<string> res;  s.collectWords(res, sep); return res; }, "return list with all found words", py::arg("sep") = CTextA::SeparatorsWord)
        .def("wordsCapitalize", &CTextA::wordsCapitalize, "make all words in a text start with upper character", py::arg("sep") = CTextA::SeparatorsWord)
        .def("wordsCount", &CTextA::wordsCount, "return number of the found words divided by seps", py::arg("sep") = CTextA::SeparatorsWord)
        .def("wordsEnclose", (CTextA& (CTextA::*)(const char* sBegin, const char* sEnd, const char* sep)) &CTextA::wordsEnclose, "enclose all words", py::arg("sBegin"), py::arg("sEnd"), py::arg("sep") = CTextA::SeparatorsWord)
        .def("wordsSort", &CTextA::wordsSort, "sort the text words in ascending order", py::arg("sep") = CTextA::SeparatorsWord, py::arg("sepNew") = CTextA::SPACE)
        .def("wordsReplace", [](CTextA& s, const vector<string>& what, const char* with, bool bCase, const char* sep)->CTextA& { return s.wordsReplace(what, with, bCase, sep); }, "replace found strings from the list with the string 'with' ", py::arg("what"), py::arg("with"), py::arg("case") = true, py::arg("sep") = CTextA::SeparatorsWord)
        .def("wordsReplace", [](CTextA& s, const vector<string>& what, const vector<string>& with, bool bCase, const char* sep)->CTextA& { return s.wordsReplace(what, with, bCase, sep); }, "replace found strings from the list with the strings from another list ", py::arg("what"), py::arg("with"), py::arg("case") = true, py::arg("sep") = CTextA::SeparatorsWord)
        .def("wordsReplaceWithChar", [](CTextA& s, const vector<string>& what, const char* c, bool bCase, const char* sep)->CTextA& { return s.wordsReplaceWithChar(what, *c, bCase, sep); }, "replace all found words from the list with a single character ", py::arg("what"), py::arg("with"), py::arg("case") = true, py::arg("sep") = CTextA::SeparatorsWord)
        .def("wordsReverse", &CTextA::wordsReverse, "reverse words inplace", py::arg("sep") = CTextA::SeparatorsWord)
        .def("writeFile", &CTextA::writeFile<char>, "write string to a text file with the given encoding", py::arg("path"), py::arg("encoding") = 1, py::arg("asHex") = false)
        ;
        
    py::class_<CTextU> (m, "TextU")
        // constructors
        .def(py::init<>())
        .def(py::init<const wchar_t*>())
        .def(py::init<const std::wstring &>())
         // operators
        .def(py::self + py::self)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self < py::self)
        .def(py::self > py::self)
        .def(py::self + std::wstring())
        .def(std::wstring() + py::self)
        .def(py::self += py::self)
        .def(py::self += std::wstring())
        .def("__add__", [](const CTextU& c2, const CTextU& c1) { return c2 + c1; })
        .def("__add__", [](const CTextU& c1, const wchar_t* c2) { return c2 + c1; })
        .def("__repr__", [](const CTextU &a) { return a.str() == nullptr? L"": a.str(); })
        // functions
        .def("addToFileName", &CTextU::addToFileName, "modifies a filename, adds the provided string to file name but keeps extension and path")
        .def("append", [](CTextU& s, const wchar_t* str)->CTextU& { return s.append(str); }, "append string", py::arg("str"))
        .def("append", [](CTextU& s, const wchar_t* str, size_t len)->CTextU& { return s.append(*str, len); }, "append characters", py::arg("c"), py::arg("len") = 1)
        .def("append", [](CTextU& s, const vector<wstring>& list)->CTextU& { return s.append(list); }, "append single character or string list", py::arg("list"))
        .def("appendRange", [](CTextU& s, const wchar_t* begin, const wchar_t* end)->CTextU& { return s.appendRange(*begin, *end); }, "append all characters in the range ", py::arg("begin"), py::arg("end"))
        .def("between", [](CTextU& s, const wchar_t* left, const wchar_t* right, bool include)->bool { return s.between(left, right, include); }, "keeps the part of the string between the first and last sub-strings sLeft and sRight (by default separattors are not included", py::arg("left"), py::arg("right"), py::arg("include") = false)
        .def("capacity", &CTextU::capacity)
        .def("clear", &CTextU::clear, py::arg("bRelease") = false)
        .def("collectBlocks", [](CTextU& s, const wchar_t* sepBegin, const wchar_t* sepEnd, bool all)->vector<wstring> {  vector<wstring> res;  s.collectBlocks(res, sepBegin, sepEnd, all); return res; }, "collect blocks", py::arg("sepBegin"), py::arg("sepEnd"), py::arg("all") = true)
        .def("collectLines", [](CTextU& s, const wchar_t* sep)->vector<wstring> {  vector<wstring> res;  s.collectLines(res, false, sep); return res; }, "fills a list with the collected lines", py::arg("sep") = CTextU::SeparatorsLine)
        .def("checkBalance", &CTextU::checkBalance, "checks if the blocks defined with the given separators are balanced")
        .def("contain", (bool (CTextU::*)(const wchar_t* s, bool bCase) const) &CTextU::contain, "returns true if our string contains another string  ", py::arg("str"), py::arg("case") = true)
        .def("contain", [](CTextU& s, const vector<wstring>& list, bool bCase)->bool { return s.containAny(list, bCase, true); }, "returns true if contains any of the provided strings", py::arg("list"), py::arg("case") = true)
        .def("containAny", (bool (CTextU::*)(const wchar_t* s, bool bCase) const) &CTextU::containAny, "returns true if our string contains any of the characters in the list", py::arg("str"), py::arg("case") = true)
        .def("containOnly", (bool (CTextU::*)(const wchar_t* s, bool bCase) const) &CTextU::containOnly, "returns true if our string contains only characters in the list", py::arg("str"), py::arg("case") = true)
        .def("count", [](CTextU& s, const wchar_t* str, bool bCase)->size_t { return s.count(str, bCase); }, "returns the count of occurences of the given substring", py::arg("str"), py::arg("case") = true)
        .def("countWordFrequencies", [](CTextU& s, bool bCase, const wchar_t* sep)->std::vector< std::pair<int, wstring> > { std::vector< std::pair<int, wstring> >  res;  s.countWordFrequencies(res, bCase, sep); return res; }, "fill the container with the words frequency counts", py::arg("case") = true, py::arg("sep") = CTextU::SeparatorsWord)
        .def("cutAfterFirst", [](CTextU& s, const wchar_t* str, bool include, bool bCase)->CTextU& { return s.cutAfterFirst(*str, include, bCase); }, "leaves everyting left from c, c is not included, everything after is removed", py::arg("str"), py::arg("include") = false, py::arg("case") = true)
        .def("cutAfterLast", [](CTextU& s, const wchar_t* str, bool include, bool bCase)->CTextU& { return s.cutAfterLast(*str, include, bCase); }, "leaves everyting left from the last character, c is not included", py::arg("str"), py::arg("include") = false, py::arg("case") = true)
        .def("cutBeforeFirst", [](CTextU& s, const wchar_t* str, bool include, bool bCase)->CTextU& { return s.cutBeforeFirst(*str, include, bCase); }, "cut everything before the first occurence of string str", py::arg("str"), py::arg("include") = false, py::arg("case") = true)
        .def("cutAfterFirstOfAny", [](CTextU& s, const wchar_t* str, bool include, bool bCase)->CTextU& { return s.cutAfterFirstOfAny(str, include, bCase); }, "cut after the first occurence of any character from the list", py::arg("str"), py::arg("include") = false, py::arg("case") = true)
        .def("cutBeforeFirstOfAny", [](CTextU& s, const wchar_t* str, bool include, bool bCase)->CTextU& { return s.cutBeforeFirstOfAny(str, include, bCase); }, "cut everything before the first occurence of any of the characters from the list or leave intact, include if set, character is included", py::arg("str"), py::arg("include") = false, py::arg("case") = true)
        .def("cutEnds", (CTextU& (CTextU::*)(size_t)) &CTextU::cutEnds, "remove count of characters from left and right", py::arg("count"))
        .def("cutLeft", &CTextU::cutLeft, "removes count characters from left", py::arg("count"))
        .def("cutRight", &CTextU::cutRight, "removes count characters from left", py::arg("count"))
        .def("enclose", [](CTextU& s, const wchar_t* str)->CTextU& {return s.enclose(str, str); }, "enclose with same character", py::arg("c"))
        .def("enclose", (CTextU& (CTextU::*)(const wchar_t* begin, const wchar_t* end, bool checkEnds)) &CTextU::enclose, "enclose with the provided text separators (if not already ends and begins with them)", py::arg("begin"), py::arg("end"), py::arg("checkEnds") = true)
        .def("endsWith", [](CTextU& s, const wchar_t* str, bool bCase)->bool { return s.endsWith(str, 0, bCase); }, "return true if ends with the provided string", py::arg("str"), py::arg("case") = true)
        .def("endsWithAny", [](CTextU& s, const vector<wstring>& list, bool bCase)->bool { return s.endsWithAny(list, 0, bCase, true); }, "returns true if ends with any of the strings from the list", py::arg("list"), py::arg("case") = true)
        .def("equal", [](CTextU& s, const wchar_t* str, size_t len)->CTextU& { return s.equal(*str, len); }, "init witb len number of characters", py::arg("c"), py::arg("len"))
        .def("erase", &CTextU::erase, "delete count characters starting at zero-based index", py::arg("from"), py::arg("count") = 1)
        .def("find", (const wchar_t* (CTextU::*)(const wchar_t* s, bool bCase) const) &CTextU::find, "return a pointer to the first occurence of the string, or 0 pointer if not found", py::arg("str"), py::arg("case") = true)
        .def("first", &CTextU::first)
        .def("fromArray", [](CTextU& s, const vector<int>& list, const wchar_t* sep)->void { s.fromArray<int>(list, false, 2, sep); }, "compose a string from array using the given separator", py::arg("list"), py::arg("sep") = CTextU::SPACE)
        .def("fromArray", [](CTextU& s, const vector<float>& list, const wchar_t* sep)->void { s.fromArray<float>(list, false, 2, sep); }, "compose a string from array using the given separator", py::arg("list"), py::arg("sep") = CTextU::SPACE)
        .def("fromArray", [](CTextU& s, const vector<wstring>& list, const wchar_t* sep)->void { s.fromArray(list, sep); }, "compose a string from array using the given separator", py::arg("list"), py::arg("sep") = CTextU::SPACE)
        .def("fromArrayAsHex", [](CTextU& s, const vector<int>& list, int wHex, const wchar_t* sep)->void { s.fromArray<int>(list, true, wHex, sep); }, "compose a string from integerrs array in hex format using the given separator", py::arg("list"), py::arg("wHex") = 2, py::arg("sep") = CTextU::SPACE)
        .def("fromBinary", &CTextU::fromBinary<char>, "create a binary string from the number")
        .def("fromBinary", &CTextU::fromBinary<int>, "create a binary string from the number")
        .def("fromBinary", &CTextU::fromBinary<long long>, "create a binary string from the number")
        .def("fromHex", &CTextU::fromHexNumber<char>, "create a hexadecimal string from the number", py::arg("i"), py::arg("hasBase") = false, py::arg("upper") = false, py::arg("append") = false)
        .def("fromHex", &CTextU::fromHexNumber<int>, "create a hexadecimal string from the number", py::arg("i"), py::arg("hasBase") = false, py::arg("upper") = false, py::arg("append") = false)
        .def("fromHex", &CTextU::fromHexNumber<long long>, "create a hexadecimal string from the number", py::arg("i"), py::arg("hasBase") = false, py::arg("upper") = false, py::arg("append") = false)
        .def("fromInteger", &CTextU::fromInteger<char>, "convert the decimal nteger to string", py::arg("i"), py::arg("append") = false, py::arg("padd") = 0, py::arg("paddValue") = '0')
        .def("fromInteger", &CTextU::fromInteger<int>, "convert the decimal nteger to string", py::arg("i"), py::arg("append") = false, py::arg("padd") = 0, py::arg("paddValue") = '0')
        .def("fromInteger", &CTextU::fromInteger<long long>, "convert the decimal integer to string", py::arg("i"), py::arg("append") = false, py::arg("padd") = 0, py::arg("paddValue") = '0')
        .def("fromDouble", &CTextU::fromDouble, "convert double to string", py::arg("d"), py::arg("precision") = 6, py::arg("fixed") = true, py::arg("nozeros") = false, py::arg("append") = false)
        .def("fromMatrix", [](CTextU& s, py::array_t<int> m, const wchar_t* sep, const wchar_t* sepLine)->void {   py::buffer_info buf = m.request();  size_t h = buf.shape[0]; size_t w = buf.shape[1]; int* ptr = (int*)buf.ptr; s.fromMatrix<int>(ptr, w, h, false, 2, sep, sepLine);  }, "compose string from a 2D numerical matrix", py::arg("list"), py::arg("sep") = CTextU::SPACE, py::arg("sepLine") = CTextU::EOL)
        .def("fromMatrix", [](CTextU& s, py::array_t<double> m, const wchar_t* sep, const wchar_t* sepLine)->void {   py::buffer_info buf = m.request();  size_t h = buf.shape[0]; size_t w = buf.shape[1]; double* ptr = (double*)buf.ptr; s.fromMatrix<double>(ptr, w, h, false, 2, sep, sepLine);  }, "compose string from a 2D numerical matrix", py::arg("list"), py::arg("sep") = CTextU::SPACE, py::arg("sepLine") = CTextU::EOL)
        .def("fromMatrixAsHex", [](CTextU& s, py::array_t<int> m, int wHex, const wchar_t* sep, const wchar_t* sepLine)->void {   py::buffer_info buf = m.request();  size_t h = buf.shape[0]; size_t w = buf.shape[1]; int* ptr = (int*)buf.ptr; s.fromMatrix<int>(ptr, w, h, true, wHex, sep, sepLine);  }, "compose string from a 2D numerical matrix", py::arg("list"), py::arg("wHex") = 2, py::arg("sep") = CTextU::SPACE, py::arg("sepLine") = CTextU::EOL)
        .def("getDir", &CTextU::getDir, "get a folder from a full module path")
        .def("getExtension", &CTextU::getExtension, "if our string contains file path, return the extension")
        .def("getFileName", &CTextU::getFileName, "if our string contains file path, return the file name")
        .def("hash", &CTextU::hash)
        .def("indexOf", [](CTextU& s, const wchar_t* str, size_t from, bool bCase)->size_t { return s.lastIndexOf(str, from, bCase); }, "find the offset of first instance of the string in the list, return index or -1 if not found", py::arg("str"), py::arg("from") = 0, py::arg("case") = true)
        .def("indexOfAny", [](CTextU& s, const wchar_t* cList, bool bCase)->size_t { return s.indexOfAny(cList, 0, bCase); }, "find the offset of the first instance of the characters in the list", py::arg("cList"), py::arg("case") = true)
        .def("indexOfAny", [](CTextU& s, const vector<wstring>& list, bool bCase)->size_t { return s.indexOfAny(list, 0, bCase, true); }, "find the offset of the first instance of the strings in the list", py::arg("list"), py::arg("case") = true)
        .def("insert", [](CTextU& s, size_t from, const wchar_t* c, size_t count)->CTextU& { return s.insert(from, *c, count); }, "insert character at zero-based index, if index is past end of string", py::arg("from"), py::arg("c"), py::arg("count"))
        .def("insert", [](CTextU& s, size_t from, const wchar_t* str)->CTextU& { return s.insert(from, str); }, "insert substring at zero-based index; concatenates, if index is past end of string", py::arg("from"), py::arg("str"))
        .def("insertAtBegin", &CTextU::insertAtBegin, py::arg("str"), py::arg("skip") = 1, py::arg("sep") = CTextU::Separators)
        .def("insertAtEnd", &CTextU::insertAtEnd, py::arg("str"), py::arg("skip") = 1, py::arg("sep") = CTextU::Separators)
        .def("isAlpha", &CTextU::isAlpha, "return true if contains only alphabeta characters")
        .def("isBinary", &CTextU::isBinary, "return true if contains only 0s and 1s")
        .def("isEmpty", &CTextU::isEmpty, "return true if empty")
        .def("isHexNumber", &CTextU::isHexNumber, "return true if contains only hexadecimal digits")
        .def("isLower", &CTextU::isLower, py::arg("strict") = false)
        .def("isNumber", &CTextU::isNumber, "return true if contains only decimal digits", py::arg("allowSign") = true)
        .def("isPalindrome", &CTextU::isPalindrome)
        .def("isUpper", &CTextU::isUpper, py::arg("strict") = false)
        .def("keep", &CTextU::keep, "keeps count characters starting from given position")
        .def("keepEnds", &CTextU::keepEnds, "keeps the characters from both ends, returns number of deleted characters")
        .def("keepLeft", &CTextU::keepLeft, "keeps count characters from left and removes the rest, returns number of deleted characters")
        .def("keepRight", &CTextU::keepRight, "keeps count characters from right and removes the rest, returns number of deleted characters")
        .def("left", &CTextU::left, "return new string containing first count characters")
        .def("length", &CTextU::length, "returns the number of characters in the string")
        .def("last", &CTextU::last)
        .def("lastIndexOf", [](CTextU& s, const wchar_t* str, size_t from, bool bCase)->size_t { return s.lastIndexOf(str, from, bCase); }, "find the first character position starting at right, where from is the offset from the end and the returned idx is from the beggining", py::arg("str"), py::arg("from") = 0, py::arg("case") = true)
        .def("lastIndexOfAny", [](CTextU& s, const wchar_t* cList, bool bCase)->size_t { return s.lastIndexOfAny(cList, 0, bCase); }, "find the offset of the first instance of the characters in the list starting from right", py::arg("cList"), py::arg("case") = true)
        .def("lines", [](CTextU& s, const wchar_t* sep)->vector<wstring> { vector<wstring> res;  s.collectLines(res, false, sep); return res; }, "return list with all found lines", py::arg("sep") = CTextU::SeparatorsLine)
        .def("linesCount", &CTextU::linesCount, "returns the number of the lines in the string", py::arg("sep") = CTextU::EOL)
        .def("linesAppend", [](CTextU& s, const wchar_t* str, const wchar_t* sep)->size_t { return s.linesInsertAtEnd(str, 1, sep); }, "append text to each line", py::arg("str"), py::arg("sep") = CTextU::SeparatorsLine)
        .def("linesInsertAtBegin", [](CTextU& s, const wchar_t* str, const wchar_t* sep)->size_t { return s.linesInsertAtBegin(str, 1, sep); }, "insert text at each line begin", py::arg("str"), py::arg("sep") = CTextU::SeparatorsLine)
        .def("linesPaddRight", [](CTextU& s, const wchar_t* str, size_t len, const wchar_t* sep, const wchar_t* sepNew)->size_t { return s.linesPaddRight(*str, len, sep, sepNew); }, "append text to each line", py::arg("str"), py::arg("len"), py::arg("sep") = CTextU::SeparatorsLine, py::arg("sepNew") = CTextU::EOL)
        .def("linesSort", &CTextU::linesSort, py::arg("sep") = CTextU::SeparatorsLine, py::arg("sepNew") = CTextU::EOL)
        .def("linesRemoveEmpty", &CTextU::linesRemoveEmpty, py::arg("minLen") = 0, py::arg("sep") = CTextU::SeparatorsLine)
        .def("linesTrim", &CTextU::linesTrim, py::arg("cList"), py::arg("sep") = CTextU::SeparatorsLine, py::arg("sepNew") = CTextU::EOL)
        .def("limit", &CTextU::limit, "limit the the length, if our text length is smaller nothing is done")
        .def("lower", &CTextU::toLower, "conversion to lowercase (in place)")
        .def("makeUnique", (size_t(CTextU::*)()) &CTextU::makeUnique, "make sure that all characters occurs only once")
        .def("mid", &CTextU::mid, "leaves the middle characters, count characters are cut from both ends, returns new string")
        .def("nextLine", [](CTextU& s, int pos, CTextU& line, bool appendSeparators, const wchar_t* sep)->int { size_t _pos = pos;  bool res = s.nextLine(_pos, line, appendSeparators, sep); return res ? (int)_pos : -1; }, py::arg("pos"), py::arg("line"), py::arg("appendSeparators") = false, py::arg("sep") = CTextU::SeparatorsLine)
        .def("nextWord", [](CTextU& s, int pos, CTextU& line, const wchar_t* sep)->int { size_t _pos = pos;  bool res = s.nextWord(_pos, line, sep); return res ? (int)_pos : -1; }, py::arg("pos"), py::arg("line"), py::arg("sep") = CTextU::SeparatorsWord)
        .def("paddLeft", &CTextU::paddLeft, "fills from start with the given characters until given lenght")
        .def("paddRight", &CTextU::paddRight, "fills from end with the given characters until given lenght")
        .def("pathCombine", &CTextU::pathCombine, "combine paths, C:\\Temp\" + \"..\\Folder\\\" = \"C:\\Folder")
        .def("push_back", (CTextU& (CTextU::*)(const wchar_t*)) &CTextU::push_back, "append string")
        .def("push_front", (CTextU& (CTextU::*)(const wchar_t*)) &CTextU::push_front, "insert string at start")
        .def("quote", &CTextU::quote)
        .def("randomAlpha", &CTextU::randomAlpha, "generate text containing random alpha upper and lower characters ", py::arg("len") = 16)
        .def("random", &CTextU::randomAlphaNumeric, "generate text containing random alphanumeric upper and lower characters ", py::arg("len") = 16)
        .def("randomNumber", &CTextU::randomNumber, "generate text containing a random integer with the given length", py::arg("len") = 10)
        .def("reduceChain", [](CTextU& s, const wchar_t* cList, const wchar_t* cNew)->CTextU { return s.reduceChain(cList, *cNew); }, "reduce blocks of the separators from the list to a single character", py::arg("cList") = CTextU::SeparatorsWord, py::arg("cNew") = CTextU::SPACE)
        .def("regexLines", [](CTextU& s, const wchar_t* regex, const wchar_t* sep)->vector<wstring> { vector<wstring> res;  s.regexCollectLines(res, regex, sep); return res;  }, "collect all lines matching the given regex condition", py::arg("regex"), py::arg("sep") = CTextU::SeparatorsLine)
        .def("regexWords", [](CTextU& s, const wchar_t* regex, const wchar_t* sep)->vector<wstring> { vector<wstring> res;  s.regexCollectWords(res, regex, sep); return res;  }, "collect all words matching the given regex condition", py::arg("regex"), py::arg("sep") = CTextU::SeparatorsWord)
        .def("regexSearch", [](CTextU& s, const wchar_t* regex)->vector<wstring> { vector<wstring> res;  s.regexSearch(res, regex); return res;  }, "collect substrings using the provided Regex expression and regex_iterator", py::arg("regex"))
        .def("regexReplace", (CTextU& (CTextU::*)(const wchar_t* regexp, const wchar_t* fmt)) &CTextU::regexReplace, "replace strings using the provided Regex expression")
        .def("regexMatch", (bool (CTextU::*)(const wchar_t*) const) &CTextU::regexMatch)
        .def("remove", (size_t(CTextU::*)(const wchar_t*, bool)) &CTextU::remove, "delete all occurences of the string s", py::arg("str"), py::arg("case") = true)
        .def("removeAny", (size_t(CTextU::*)(const wchar_t*, bool)) &CTextU::removeAny, "delete all of provided in the list characters", py::arg("str"), py::arg("case") = true)
        .def("removeAny", &CTextU::removeAny<vector<wstring>>, "remove any from the provided in the list strings", py::arg("list"), py::arg("case") = true, py::arg("longList") = true)
        .def("removeExtension", &CTextU::removeExtension, "remove the extension from a file path")
        .def("removeFileName", &CTextU::removeFileName, "if string contain file path, remove the file name", py::arg("keepSlash") = true)
        .def("removeLast", &CTextU::removeLast, "removes the last character, return true if not empty and sucessful")
        .def("removeWhileBegins", &CTextU::removeWhileBegins, "remove the characters from str while begins to the characters from our string", py::arg("str"))
        .def("removeWhileEnds", &CTextU::removeWhileEnds, "remove the characters from str while ends to the characters from our string", py::arg("str"))
        .def("replace", (size_t(CTextU::*)(const wchar_t* what, const wchar_t* with, bool bCase)) &CTextU::replace, "replace all occurrences of substring \"what\" with substring \"with\"", py::arg("what"), py::arg("with"), py::arg("case") = true)
        .def("replace", [](CTextU& s, const wchar_t* str, size_t len, const wchar_t* c)->CTextU& { return s.replace(*str, len, *c); }, "replace range with single character", py::arg("str"), py::arg("len"), py::arg("c"))
        .def("replace", [](CTextU& s, const vector<wstring>& what, const wchar_t* c, bool bCase)->CTextU& { return s.replaceAny(what, *c, bCase, true); }, "replace all found strings in list 'what' with a single character ", py::arg("what"), py::arg("with"), py::arg("case") = true)
        .def("replaceAny", [](CTextU& s, const vector<wstring>& what, const vector<wstring>& with, bool bCase)->CTextU& { return s.replaceAny(what, with, bCase, true); }, "replace found strings in list 'what' with corresponding strings from list 'with' ", py::arg("what"), py::arg("with"), py::arg("case") = true)
        .def("replaceAny", [](CTextU& s, const vector<wstring>& what, const wchar_t* with, bool bCase)->CTextU& { return s.replaceAny(what, with, bCase, true); }, "replace found strings in list 'what' with the string 'with' ", py::arg("what"), py::arg("with"), py::arg("case") = true)
        .def("replaceExtension", &CTextU::replaceExtension, "change the file path extension")
        .def("replaceFileName", &CTextU::replaceFileName, "change the file name")
        .def("replaceLastFolder", &CTextU::replaceLastFolder, "replace last folder name")
        .def("replaceFirst", &CTextU::replaceFirst, "replace first character")
        .def("replaceLast", &CTextU::replaceFirst, "replace last character")
        .def("readFile", &CTextU::readFile<char>, "read a whole text file into our string", py::arg("path"), py::arg("asHex") = false)
#if defined(_WIN32) 
        .def("readFile", &CTextU::readFile<wchar_t>, "read a whole text file into our string", py::arg("path"), py::arg("asHex") = false)
#endif
        .def("reverse", &CTextU::reverse)
        .def("reverseFind", &CTextU::reverseFind, py::arg("s"), py::arg("case") = true)
        .def("right", &CTextU::right, "return new string with count characters from the end of our string")
        .def("rotateLeft", &CTextU::rotateLeft, "rotate tne string to the left")
        .def("rotateRight", &CTextU::rotateRight, "rotate tne string to the right")
        .def("sentences", [](CTextU& s, const wchar_t* sep, const wchar_t* sepWords)->vector<wstring> { vector<wstring> res;  s.collectSentences(res, sep); return res; }, "return list with all found words", py::arg("sep") = CTextU::SeparatorsWord, py::arg("sepWords") = CTextU::SeparatorsWord)
        .def("shuffle", &CTextU::shuffle)
        .def("sort", &CTextU::sort)
        .def("split", [](CTextU& s, const wchar_t* sep = CTextU::Separators)->vector<wstring> { vector<wstring> res;  s.split(res, false, sep); return res; }, "fills the STL container with the collected substrings", py::arg("sep") = CTextU::Separators)
        .def("str", (const wchar_t* (CTextU::*)(size_t pos) const) &CTextU::str, "return text buffer", py::arg("pos") = 0)
        .def("toBinary", &CTextU::toBinary, "if the string contains a binary number, convert it  ")
        .def("toHex", &CTextU::toHex, "convert string to hex values separated by the given separator", py::arg("sep") = CTextU::SPACE)
        .def("toHexNumber", &CTextU::toHexNumber, "if the string contains a hex number, convert it , 1E --> 30")
        .def("toDouble", &CTextU::toDouble)
        .def("toInteger", &CTextU::toInteger)
        .def("trim", &CTextU::trim, "trim string from both sides", py::arg("cList") = CTextU::Separators)
        .def("trim", &CTextU::trim, "trim string from both sides", py::arg("cList") = CTextU::Separators)
        .def("trimLeft", (CTextU& (CTextU::*)(const wchar_t*)) &CTextU::trimLeft, "trim string from left", py::arg("cList") = CTextU::Separators)
        .def("trimRight", (CTextU& (CTextU::*)(const wchar_t*)) &CTextU::trimRight, "trim string from right", py::arg("cList") = CTextU::Separators)
        .def("upper", &CTextU::toUpper, "conversion to uppercase (in place)")
        .def("words", [](CTextU& s, const wchar_t* sep)->vector<wstring> { vector<wstring> res;  s.collectWords(res, sep); return res; }, "return list with all found words", py::arg("sep") = CTextU::SeparatorsWord)
        .def("wordsCapitalize", &CTextU::wordsCapitalize, "make all words in a text start with upper character", py::arg("sep") = CTextU::SeparatorsWord)
        .def("wordsCount", &CTextU::wordsCount, "return number of the found words divided by seps", py::arg("sep") = CTextU::SeparatorsWord)
        .def("wordsEnclose", (CTextU& (CTextU::*)(const wchar_t* sBegin, const wchar_t* sEnd, const wchar_t* sep)) &CTextU::wordsEnclose, "enclose all words", py::arg("sBegin"), py::arg("sEnd"), py::arg("sep") = CTextU::SeparatorsWord)
        .def("wordsSort", &CTextU::wordsSort, "sort the text words in ascending order", py::arg("sep") = CTextU::SeparatorsWord, py::arg("sepNew") = CTextU::SPACE)
        .def("wordsReplace", [](CTextU& s, const vector<wstring>& what, const wchar_t* with, bool bCase, const wchar_t* sep)->CTextU& { return s.wordsReplace(what, with, bCase, sep); }, "replace found strings from the list with the string 'with' ", py::arg("what"), py::arg("with"), py::arg("case") = true, py::arg("sep") = CTextU::SeparatorsWord)
        .def("wordsReplace", [](CTextU& s, const vector<wstring>& what, const vector<wstring>& with, bool bCase, const wchar_t* sep)->CTextU& { return s.wordsReplace(what, with, bCase, sep); }, "replace found strings from the list with the strings from another list ", py::arg("what"), py::arg("with"), py::arg("case") = true, py::arg("sep") = CTextU::SeparatorsWord)
        .def("wordsReplaceWithChar", [](CTextU& s, const vector<wstring>& what, const wchar_t* c, bool bCase, const wchar_t* sep)->CTextU& { return s.wordsReplaceWithChar(what, *c, bCase, sep); }, "replace all found words from the list with a single character ", py::arg("what"), py::arg("with"), py::arg("case") = true, py::arg("sep") = CTextU::SeparatorsWord)
        .def("wordsReverse", &CTextU::wordsReverse, "reverse words inplace", py::arg("sep") = CTextU::SeparatorsWord)
        .def("writeFile", &CTextU::writeFile<char>, "write string to a text file with the given encoding", py::arg("path"), py::arg("encoding") = 1, py::arg("asHex") = false)
#if defined(_WIN32) 
        .def("writeFile", &CTextU::writeFile<wchar_t>, "write string to a text file with the given encoding", py::arg("path"), py::arg("encoding") = 1, py::arg("asHex") = false)
#endif
        ;

    // static methods
    m.def("CollectWords", [](const char* str)->std::vector<std::string>
    { 
        CTextA text(str);
        std::vector<std::string> list;
        text.collectWords(list);

        return list;
           
    }, "return list with all words from a string", py::arg("str"));
    m.def("Contain", [](const char* text, const char* str, bool bCase)->bool
    { 
        return CTextA::Contain(text, str, bCase);
           
    }, "return true if str is contained in the text", py::arg("text"), py::arg("str"), py::arg("case") = true);
    m.def("EndsWith", [](const char* text, const char* str, bool bCase)->bool
    { 
        return CTextA::EndsWith(text, str, bCase);
           
    }, "if the string contains file path return pointer to its extension", py::arg("text"), py::arg("str"), py::arg("case") = true);
    m.def("Find", [](const char* text, const char* str, bool bCase)->std::string
    { 
        return CTextA::StrFind(text, str, bCase);
           
    }, "finds the first occurence of str in the text", py::arg("text"), py::arg("str"), py::arg("case") = true);
    m.def("GetExtension", [](const char* filepath)->std::string
    { 
        std::string res (CTextA::GetExtension(filepath));

        return res;
           
    }, "if the string contains file path return pointer to its extension", py::arg("filepath"));
    m.def("GetFileName", [](const char* filepath)->std::string
    { 
        std::string res (CTextA::GetFileName(filepath));

        return res;
           
    }, "if the string contains file path return pointer to the file or last folder name", py::arg("filepath"));
    m.def("HammingDistance", [](const char* s1, const char* s2)->int
    { 
        return (int)(CTextA::Levenshtein(s1, s2));
           
    }, "return the Hamming distance between the strings", py::arg("s1"), py::arg("s2"));
    m.def("IsBinary", [](const char* str)->bool
    { 
        return (CTextA::IsBinary(str));
           
    }, "return true if the string contain binary number", py::arg("str"));
    m.def("IsDouble", [](const char* str)->bool
    { 
        return (CTextA::IsDouble(str));
           
    }, "return true if the string contains double number", py::arg("str"));
    m.def("IsHexNumber", [](const char* str)->bool
    { 
        return (CTextA::IsHexNumber(str));
           
    }, "return true if the string contains hexadecimal number", py::arg("str"));
    m.def("IsLower", [](const char* str)->bool
    { 
        return (CTextA::IsLower(str));
           
    }, "return true if the string is lower case", py::arg("str"));
    m.def("IsNumber", [](const char* str)->bool
    { 
        return (CTextA::IsNumber(str));
           
    }, "return true if the string contain only digits", py::arg("str"));
    m.def("IsUpper", [](const char* str)->bool
    { 
        return (CTextA::IsUpper(str));
           
    }, "return true if the string is upper case", py::arg("str"));
    m.def("Levenshtein", [](const char* s1, const char* s2)->int
    { 
        return (int)(CTextA::Levenshtein(s1, s2));
           
    }, "return Levenstein distance between the strings", py::arg("s1"), py::arg("s2"));
    m.def("ReadLines", [](const char* filepath)->std::vector<std::string>
    { 
        std::vector<std::string> res;

        CTextA::ReadLinesFromFile(filepath, res);

        return res;
           
    }, "read lines form a text file", py::arg("filepath"));
    m.def("Reverse", [](char* str)->std::string
    { 
        return std::string (CTextA::Strrev(str));
           
    }, "if the string contains file path return pointer to the file or last folder name", py::arg("str"));
    m.def("StartsWith", [](const char* text, const char* str, bool bCase)->bool
    { 
        return CTextA::StartsWith(text, str, bCase);
           
    }, "if the string contains file path return pointer to its extension", py::arg("text"), py::arg("str"), py::arg("bCase") = true);
    m.def("WriteFile", [](const char* filepath, const char* str)->bool
    { 
        return CTextT<char>::WriteFile<char, void>(filepath, str, CTextA::ENCODING_UTF8);
           
    }, "save the string in a text file", py::arg("filepath"), py::arg("str"));
    m.def("ReadFile", [](const char* filepath)->std::string
    { 
        CTextA s;

        s.readFile(filepath);

        return s.str();
           
    }, "reads a string from a text file", py::arg("filepath"));
    m.def("ReadWords", [](const char* filepath)->std::vector<std::string>
    { 
        CTextA text;
        text.readFile(filepath);
        std::vector<std::string> list;
        text.collectWords(list);

        return list;
           
    }, "return list with all words from a text file", py::arg("filepath"));

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}

