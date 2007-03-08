// Sugar Runtime
// ISO C99 Source code
//
// Licensed under the BSD license
// (c) Sebastien Pierre, Ivy, 2007.

#ifndef __SUGAR_RUNTIME__
#define __SUGAR_RUNTIME__

#include <stdarg.h>

#define DECLARE_MODULE(m)            SgModule* m;
#define END_MODULE
#define DECLARE_CLASS(c)             SgClass*  c;
#define END_CLASS
#define DECLARE_ATTRIBUTE(c,a)       
#define DECLARE_CLASS_ATTRIBUTE(c,a) 

#define NEW0(C)                      SgObject_new0(C)
#define NEW1(C,a)                    SgObject_new1(C,a)
#define NEW2(C,a,b,c)                SgObject_new2(C,a,b)
#define NEW3(C,a,b,c,d)              SgObject_new3(C,a,b,c)
#define RESOLVE(O,s)                 SgObject_get(O,#s)
#define $G(O,s)                      SgObject_get(O,#s)

#define LIST(...)                    SgCore_list(0, __VA_ARGS__)
#define INT(v)                       SgCore_int(v)
#define FLOAT(v)                     SgCore_float(v)
#define DOUBLE(v)                    SgCore_double(v)
#define STRING(v)                    SgCore_string(v)

#define MODULE_INIT(M)               void M##_initialize() {
#define END_MODULE_INIT              }

// ===========================================================================
//
// TAGS DEFINITION
//
// ===========================================================================

// Tags are used to disambiguate values.

#define TAG_UNDEFINED                'U'
#define TAG_NULL                     'N'
#define TAG_INT                      'i'
#define TAG_LONG                     'l'
#define TAG_FLOAT                    'f'
#define TAG_DOUBLE                   'd'
#define TAG_CLASS                    'c'
#define TAG_CLOSURE                  'f'
#define TAG_OBJECT                   'o'

// ===========================================================================
//
// BASE TYPE DEFINITIONS
//
// ===========================================================================

typedef struct SgValue_ SgValue;
struct SgValue__struct {
	unsigned char tag;
};

typedef struct SgObject_ SgObject;
struct SgObject_ {
	unsigned char tag;
	unsigned long id;
	void*         slots;
};

typedef struct SgObject SgModule;
typedef struct SgObject SgClass;

void SgClass_declareAttribute(SgClass* self, const char* attribute);
void SgClass_declareClassAttribute(SgClass* self, const char* attribute);

SgObject* SgObject_new0(SgClass* self);
SgObject* SgObject_new1(SgClass* self, SgValue* a);
SgObject* SgObject_new2(SgClass* self, SgValue* a, SgValue* b);
SgObject* SgObject_new3(SgClass* self, SgValue* a, SgValue* b, SgValue* c);
SgValue*  SgObject_get(SgObject* self, char* slotName);

SgValue*  SgCore_list(int length, ...);
SgValue*  SgCore_int(int i);
SgValue*  SgCore_float(float f);
SgValue*  SgCore_double(double g);
SgValue*  SgCore_string(char* g);

#endif
// EOF
