
/**
 * IPyEvalBase.h
 *
 * Copyright 2023 Matthew Ballance and Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may 
 * not use this file except in compliance with the License.  
 * You may obtain a copy of the License at:
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software 
 * distributed under the License is distributed on an "AS IS" BASIS, 
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
 * See the License for the specific language governing permissions and 
 * limitations under the License.
 *
 * Created on:
 *     Author: 
 */
#pragma once
#include <stdint.h>
#include <stdio.h>
#include <stdarg.h>
#include <sys/types.h>

typedef struct _object PyObject;
typedef struct _typeobject PyTypeObject;
typedef ssize_t Py_ssize_t;
typedef wchar_t Py_UNICODE;

namespace pyapi {


class IPyEvalBase {
public:

    virtual ~IPyEvalBase() { }

    virtual int PyAIter_Check(PyObject* p0) = 0;

    virtual int PyArg_VaParse(PyObject* p0, const char* p1, va_list p2) = 0;

    virtual int PyArg_VaParseTupleAndKeywords(PyObject* p0, PyObject* p1, const char* p2, char** p3, va_list p4) = 0;

    virtual int PyArg_ValidateKeywordArguments(PyObject* p0) = 0;

    virtual PyObject* PyBool_FromLong(long p0) = 0;

    virtual char* PyByteArray_AsString(PyObject* p0) = 0;

    virtual PyObject* PyByteArray_Concat(PyObject* p0, PyObject* p1) = 0;

    virtual PyObject* PyByteArray_FromObject(PyObject* p0) = 0;

    virtual PyObject* PyByteArray_FromStringAndSize(const char* p0, Py_ssize_t p1) = 0;

    virtual int PyByteArray_Resize(PyObject* p0, Py_ssize_t p1) = 0;

    virtual Py_ssize_t PyByteArray_Size(PyObject* p0) = 0;

    virtual char* PyBytes_AsString(PyObject* p0) = 0;

    virtual int PyBytes_AsStringAndSize(PyObject* obj, char** s, Py_ssize_t* len) = 0;

    virtual void PyBytes_Concat(PyObject** p0, PyObject* p1) = 0;

    virtual void PyBytes_ConcatAndDel(PyObject** p0, PyObject* p1) = 0;

    virtual PyObject* PyBytes_DecodeEscape(const char* p0, Py_ssize_t p1, const char* p2, Py_ssize_t p3, const char* p4) = 0;

    virtual PyObject* PyBytes_FromFormatV(const char* p0, va_list p1) = 0;

    virtual PyObject* PyBytes_FromObject(PyObject* p0) = 0;

    virtual PyObject* PyBytes_FromString(const char* p0) = 0;

    virtual PyObject* PyBytes_FromStringAndSize(const char* p0, Py_ssize_t p1) = 0;

    virtual PyObject* PyBytes_Repr(PyObject* p0, int p1) = 0;

    virtual Py_ssize_t PyBytes_Size(PyObject* p0) = 0;

    virtual PyObject* PyCallIter_New(PyObject* p0, PyObject* p1) = 0;

    virtual int PyCallable_Check(PyObject* p0) = 0;

    virtual PyObject* PyCell_Get(PyObject* p0) = 0;

    virtual PyObject* PyCell_New(PyObject* p0) = 0;

    virtual int PyCell_Set(PyObject* p0, PyObject* p1) = 0;

    virtual PyObject* PyClassMethod_New(PyObject* p0) = 0;

    virtual PyObject* PyCodec_BackslashReplaceErrors(PyObject* exc) = 0;

    virtual PyObject* PyCodec_Decode(PyObject* object, const char* encoding, const char* errors) = 0;

    virtual PyObject* PyCodec_Decoder(const char* encoding) = 0;

    virtual PyObject* PyCodec_Encode(PyObject* object, const char* encoding, const char* errors) = 0;

    virtual PyObject* PyCodec_Encoder(const char* encoding) = 0;

    virtual PyObject* PyCodec_IgnoreErrors(PyObject* exc) = 0;

    virtual PyObject* PyCodec_IncrementalDecoder(const char* encoding, const char* errors) = 0;

    virtual PyObject* PyCodec_IncrementalEncoder(const char* encoding, const char* errors) = 0;

    virtual int PyCodec_KnownEncoding(const char* encoding) = 0;

    virtual PyObject* PyCodec_LookupError(const char* name) = 0;

    virtual PyObject* PyCodec_NameReplaceErrors(PyObject* exc) = 0;

    virtual int PyCodec_Register(PyObject* search_function) = 0;

    virtual int PyCodec_RegisterError(const char* name, PyObject* error) = 0;

    virtual PyObject* PyCodec_ReplaceErrors(PyObject* exc) = 0;

    virtual PyObject* PyCodec_StreamReader(const char* encoding, PyObject* stream, const char* errors) = 0;

    virtual PyObject* PyCodec_StreamWriter(const char* encoding, PyObject* stream, const char* errors) = 0;

    virtual PyObject* PyCodec_StrictErrors(PyObject* exc) = 0;

    virtual int PyCodec_Unregister(PyObject* search_function) = 0;

    virtual PyObject* PyCodec_XMLCharRefReplaceErrors(PyObject* exc) = 0;

    virtual int PyCompile_OpcodeStackEffect(int opcode, int oparg) = 0;

    virtual int PyCompile_OpcodeStackEffectWithJump(int opcode, int oparg, int jump) = 0;

    virtual int PyContextVar_Get(PyObject* var, PyObject* default_value, PyObject** value) = 0;

    virtual PyObject* PyContextVar_New(const char* name, PyObject* default_value) = 0;

    virtual int PyContextVar_Reset(PyObject* var, PyObject* token) = 0;

    virtual PyObject* PyContextVar_Set(PyObject* var, PyObject* value) = 0;

    virtual PyObject* PyContext_Copy(PyObject* p0) = 0;

    virtual PyObject* PyContext_CopyCurrent() = 0;

    virtual int PyContext_Enter(PyObject* p0) = 0;

    virtual int PyContext_Exit(PyObject* p0) = 0;

    virtual PyObject* PyContext_New() = 0;

    virtual PyObject* PyDictProxy_New(PyObject* p0) = 0;

    virtual void PyDict_Clear(PyObject* mp) = 0;

    virtual int PyDict_Contains(PyObject* mp, PyObject* key) = 0;

    virtual PyObject* PyDict_Copy(PyObject* mp) = 0;

    virtual int PyDict_DelItem(PyObject* mp, PyObject* key) = 0;

    virtual int PyDict_DelItemString(PyObject* dp, const char* key) = 0;

    virtual PyObject* PyDict_GetItem(PyObject* mp, PyObject* key) = 0;

    virtual PyObject* PyDict_GetItemString(PyObject* dp, const char* key) = 0;

    virtual PyObject* PyDict_GetItemWithError(PyObject* mp, PyObject* key) = 0;

    virtual PyObject* PyDict_Items(PyObject* mp) = 0;

    virtual PyObject* PyDict_Keys(PyObject* mp) = 0;

    virtual int PyDict_Merge(PyObject* mp, PyObject* other, int override) = 0;

    virtual int PyDict_MergeFromSeq2(PyObject* d, PyObject* seq2, int override) = 0;

    virtual PyObject* PyDict_New() = 0;

    virtual int PyDict_Next(PyObject* mp, Py_ssize_t* pos, PyObject** key, PyObject** value) = 0;

    virtual PyObject* PyDict_SetDefault(PyObject* mp, PyObject* key, PyObject* defaultobj) = 0;

    virtual int PyDict_SetItem(PyObject* mp, PyObject* key, PyObject* item) = 0;

    virtual int PyDict_SetItemString(PyObject* dp, const char* key, PyObject* item) = 0;

    virtual Py_ssize_t PyDict_Size(PyObject* mp) = 0;

    virtual int PyDict_Update(PyObject* mp, PyObject* other) = 0;

    virtual PyObject* PyDict_Values(PyObject* mp) = 0;

    virtual int PyErr_BadArgument() = 0;

    virtual int PyErr_CheckSignals() = 0;

    virtual void PyErr_Clear() = 0;

    virtual void PyErr_Display(PyObject* p0, PyObject* p1, PyObject* p2) = 0;

    virtual int PyErr_ExceptionMatches(PyObject* p0) = 0;

    virtual void PyErr_Fetch(PyObject** p0, PyObject** p1, PyObject** p2) = 0;

    virtual PyObject* PyErr_FormatV(PyObject* exception, const char* format, va_list vargs) = 0;

    virtual void PyErr_GetExcInfo(PyObject** p0, PyObject** p1, PyObject** p2) = 0;

    virtual int PyErr_GivenExceptionMatches(PyObject* p0, PyObject* p1) = 0;

    virtual PyObject* PyErr_NewException(const char* name, PyObject* base, PyObject* dict) = 0;

    virtual PyObject* PyErr_NewExceptionWithDoc(const char* name, const char* doc, PyObject* base, PyObject* dict) = 0;

    virtual PyObject* PyErr_NoMemory() = 0;

    virtual void PyErr_NormalizeException(PyObject** p0, PyObject** p1, PyObject** p2) = 0;

    virtual PyObject* PyErr_Occurred() = 0;

    virtual void PyErr_Print() = 0;

    virtual void PyErr_PrintEx(int p0) = 0;

    virtual PyObject* PyErr_ProgramText(const char* filename, int lineno) = 0;

    virtual PyObject* PyErr_ProgramTextObject(PyObject* filename, int lineno) = 0;

    virtual void PyErr_RangedSyntaxLocationObject(PyObject* filename, int lineno, int col_offset, int end_lineno, int end_col_offset) = 0;

    virtual void PyErr_Restore(PyObject* p0, PyObject* p1, PyObject* p2) = 0;

    virtual void PyErr_SetExcInfo(PyObject* p0, PyObject* p1, PyObject* p2) = 0;

    virtual PyObject* PyErr_SetFromErrno(PyObject* p0) = 0;

    virtual PyObject* PyErr_SetFromErrnoWithFilename(PyObject* exc, const char* filename) = 0;

    virtual PyObject* PyErr_SetFromErrnoWithFilenameObject(PyObject* p0, PyObject* p1) = 0;

    virtual PyObject* PyErr_SetFromErrnoWithFilenameObjects(PyObject* p0, PyObject* p1, PyObject* p2) = 0;

    virtual PyObject* PyErr_SetImportError(PyObject* p0, PyObject* p1, PyObject* p2) = 0;

    virtual PyObject* PyErr_SetImportErrorSubclass(PyObject* p0, PyObject* p1, PyObject* p2, PyObject* p3) = 0;

    virtual void PyErr_SetInterrupt() = 0;

    virtual int PyErr_SetInterruptEx(int signum) = 0;

    virtual void PyErr_SetNone(PyObject* p0) = 0;

    virtual void PyErr_SetObject(PyObject* p0, PyObject* p1) = 0;

    virtual void PyErr_SetString(PyObject* exception, const char* string) = 0;

    virtual void PyErr_SyntaxLocation(const char* filename, int lineno) = 0;

    virtual void PyErr_SyntaxLocationEx(const char* filename, int lineno, int col_offset) = 0;

    virtual void PyErr_SyntaxLocationObject(PyObject* filename, int lineno, int col_offset) = 0;

    virtual int PyErr_WarnEx(PyObject* category, const char* message, Py_ssize_t stack_level) = 0;

    virtual int PyErr_WarnExplicit(PyObject* category, const char* message, const char* filename, int lineno, const char* module, PyObject* registry) = 0;

    virtual int PyErr_WarnExplicitObject(PyObject* category, PyObject* message, PyObject* filename, int lineno, PyObject* module, PyObject* registry) = 0;

    virtual void PyErr_WriteUnraisable(PyObject* p0) = 0;

    virtual PyObject* PyEval_EvalCode(PyObject* p0, PyObject* p1, PyObject* p2) = 0;

    virtual PyObject* PyEval_EvalCodeEx(PyObject* co, PyObject* globals, PyObject* locals, PyObject* const* args, int argc, PyObject* const* kwds, int kwdc, PyObject* const* defs, int defc, PyObject* kwdefs, PyObject* closure) = 0;

    virtual PyObject* PyEval_GetBuiltins() = 0;

    virtual const char* PyEval_GetFuncDesc(PyObject* p0) = 0;

    virtual const char* PyEval_GetFuncName(PyObject* p0) = 0;

    virtual PyObject* PyEval_GetGlobals() = 0;

    virtual PyObject* PyEval_GetLocals() = 0;

    virtual PyObject* PyException_GetCause(PyObject* p0) = 0;

    virtual PyObject* PyException_GetContext(PyObject* p0) = 0;

    virtual PyObject* PyException_GetTraceback(PyObject* p0) = 0;

    virtual void PyException_SetCause(PyObject* p0, PyObject* p1) = 0;

    virtual void PyException_SetContext(PyObject* p0, PyObject* p1) = 0;

    virtual int PyException_SetTraceback(PyObject* p0, PyObject* p1) = 0;

    virtual double PyFloat_AsDouble(PyObject* p0) = 0;

    virtual PyObject* PyFloat_FromDouble(double p0) = 0;

    virtual PyObject* PyFloat_FromString(PyObject* p0) = 0;

    virtual PyObject* PyFloat_GetInfo() = 0;

    virtual double PyFloat_GetMax() = 0;

    virtual double PyFloat_GetMin() = 0;

    virtual PyObject* PyFrozenSet_New(PyObject* p0) = 0;

    virtual Py_ssize_t PyGC_Collect() = 0;

    virtual int PyGC_Disable() = 0;

    virtual int PyGC_Enable() = 0;

    virtual int PyGC_IsEnabled() = 0;

    virtual PyObject* PyImport_AddModule(const char* name) = 0;

    virtual PyObject* PyImport_AddModuleObject(PyObject* name) = 0;

    virtual PyObject* PyImport_ExecCodeModule(const char* name, PyObject* co) = 0;

    virtual PyObject* PyImport_ExecCodeModuleEx(const char* name, PyObject* co, const char* pathname) = 0;

    virtual PyObject* PyImport_ExecCodeModuleObject(PyObject* name, PyObject* co, PyObject* pathname, PyObject* cpathname) = 0;

    virtual PyObject* PyImport_ExecCodeModuleWithPathnames(const char* name, PyObject* co, const char* pathname, const char* cpathname) = 0;

    virtual PyObject* PyImport_GetImporter(PyObject* path) = 0;

    virtual long PyImport_GetMagicNumber() = 0;

    virtual const char* PyImport_GetMagicTag() = 0;

    virtual PyObject* PyImport_GetModule(PyObject* name) = 0;

    virtual PyObject* PyImport_GetModuleDict() = 0;

    virtual PyObject* PyImport_Import(PyObject* name) = 0;

    virtual int PyImport_ImportFrozenModule(const char* name) = 0;

    virtual int PyImport_ImportFrozenModuleObject(PyObject* name) = 0;

    virtual PyObject* PyImport_ImportModule(const char* name) = 0;

    virtual PyObject* PyImport_ImportModuleLevel(const char* name, PyObject* globals, PyObject* locals, PyObject* fromlist, int level) = 0;

    virtual PyObject* PyImport_ImportModuleLevelObject(PyObject* name, PyObject* globals, PyObject* locals, PyObject* fromlist, int level) = 0;

    virtual PyObject* PyImport_ImportModuleNoBlock(const char* name) = 0;

    virtual PyObject* PyImport_ReloadModule(PyObject* m) = 0;

    virtual PyObject* PyInstanceMethod_Function(PyObject* p0) = 0;

    virtual PyObject* PyInstanceMethod_New(PyObject* p0) = 0;

    virtual PyObject* PyIter_Next(PyObject* p0) = 0;

    virtual int PyList_Append(PyObject* p0, PyObject* p1) = 0;

    virtual PyObject* PyList_AsTuple(PyObject* p0) = 0;

    virtual PyObject* PyList_GetItem(PyObject* p0, Py_ssize_t p1) = 0;

    virtual PyObject* PyList_GetSlice(PyObject* p0, Py_ssize_t p1, Py_ssize_t p2) = 0;

    virtual int PyList_Insert(PyObject* p0, Py_ssize_t p1, PyObject* p2) = 0;

    virtual PyObject* PyList_New(Py_ssize_t size) = 0;

    virtual int PyList_Reverse(PyObject* p0) = 0;

    virtual int PyList_SetItem(PyObject* p0, Py_ssize_t p1, PyObject* p2) = 0;

    virtual int PyList_SetSlice(PyObject* p0, Py_ssize_t p1, Py_ssize_t p2, PyObject* p3) = 0;

    virtual Py_ssize_t PyList_Size(PyObject* p0) = 0;

    virtual int PyList_Sort(PyObject* p0) = 0;

    virtual double PyLong_AsDouble(PyObject* p0) = 0;

    virtual long PyLong_AsLong(PyObject* p0) = 0;

    virtual long PyLong_AsLongAndOverflow(PyObject* p0, int* p1) = 0;

    virtual long long PyLong_AsLongLong(PyObject* p0) = 0;

    virtual long long PyLong_AsLongLongAndOverflow(PyObject* p0, int* p1) = 0;

    virtual size_t PyLong_AsSize_t(PyObject* p0) = 0;

    virtual Py_ssize_t PyLong_AsSsize_t(PyObject* p0) = 0;

    virtual unsigned long PyLong_AsUnsignedLong(PyObject* p0) = 0;

    virtual unsigned long long PyLong_AsUnsignedLongLong(PyObject* p0) = 0;

    virtual unsigned long long PyLong_AsUnsignedLongLongMask(PyObject* p0) = 0;

    virtual unsigned long PyLong_AsUnsignedLongMask(PyObject* p0) = 0;

    virtual void* PyLong_AsVoidPtr(PyObject* p0) = 0;

    virtual PyObject* PyLong_FromDouble(double p0) = 0;

    virtual PyObject* PyLong_FromLong(long p0) = 0;

    virtual PyObject* PyLong_FromLongLong(long long p0) = 0;

    virtual PyObject* PyLong_FromSize_t(size_t p0) = 0;

    virtual PyObject* PyLong_FromSsize_t(Py_ssize_t p0) = 0;

    virtual PyObject* PyLong_FromString(const char* p0, char** p1, int p2) = 0;

    virtual PyObject* PyLong_FromUnicodeObject(PyObject* u, int base) = 0;

    virtual PyObject* PyLong_FromUnsignedLong(unsigned long p0) = 0;

    virtual PyObject* PyLong_FromUnsignedLongLong(unsigned long long p0) = 0;

    virtual PyObject* PyLong_FromVoidPtr(void* p0) = 0;

    virtual PyObject* PyLong_GetInfo() = 0;

    virtual int PyMapping_Check(PyObject* o) = 0;

    virtual PyObject* PyMapping_GetItemString(PyObject* o, const char* key) = 0;

    virtual int PyMapping_HasKey(PyObject* o, PyObject* key) = 0;

    virtual int PyMapping_HasKeyString(PyObject* o, const char* key) = 0;

    virtual PyObject* PyMapping_Items(PyObject* o) = 0;

    virtual PyObject* PyMapping_Keys(PyObject* o) = 0;

    virtual int PyMapping_SetItemString(PyObject* o, const char* key, PyObject* value) = 0;

    virtual Py_ssize_t PyMapping_Size(PyObject* o) = 0;

    virtual PyObject* PyMapping_Values(PyObject* o) = 0;

    virtual PyObject* PyMethod_Function(PyObject* p0) = 0;

    virtual PyObject* PyMethod_New(PyObject* p0, PyObject* p1) = 0;

    virtual PyObject* PyMethod_Self(PyObject* p0) = 0;

    virtual PyObject* PyNumber_Absolute(PyObject* o) = 0;

    virtual PyObject* PyNumber_Add(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_And(PyObject* o1, PyObject* o2) = 0;

    virtual Py_ssize_t PyNumber_AsSsize_t(PyObject* o, PyObject* exc) = 0;

    virtual int PyNumber_Check(PyObject* o) = 0;

    virtual PyObject* PyNumber_Divmod(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_Float(PyObject* o) = 0;

    virtual PyObject* PyNumber_FloorDivide(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_InPlaceAdd(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_InPlaceAnd(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_InPlaceFloorDivide(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_InPlaceLshift(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_InPlaceMatrixMultiply(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_InPlaceMultiply(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_InPlaceOr(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_InPlacePower(PyObject* o1, PyObject* o2, PyObject* o3) = 0;

    virtual PyObject* PyNumber_InPlaceRemainder(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_InPlaceRshift(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_InPlaceSubtract(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_InPlaceTrueDivide(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_InPlaceXor(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_Index(PyObject* o) = 0;

    virtual PyObject* PyNumber_Invert(PyObject* o) = 0;

    virtual PyObject* PyNumber_Long(PyObject* o) = 0;

    virtual PyObject* PyNumber_Lshift(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_MatrixMultiply(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_Multiply(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_Negative(PyObject* o) = 0;

    virtual PyObject* PyNumber_Or(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_Positive(PyObject* o) = 0;

    virtual PyObject* PyNumber_Power(PyObject* o1, PyObject* o2, PyObject* o3) = 0;

    virtual PyObject* PyNumber_Remainder(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_Rshift(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_Subtract(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_ToBase(PyObject* n, int base) = 0;

    virtual PyObject* PyNumber_TrueDivide(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PyNumber_Xor(PyObject* o1, PyObject* o2) = 0;

    virtual int PyODict_DelItem(PyObject* od, PyObject* key) = 0;

    virtual PyObject* PyODict_New() = 0;

    virtual int PyODict_SetItem(PyObject* od, PyObject* key, PyObject* item) = 0;

    virtual void PyOS_AfterFork_Child() = 0;

    virtual void PyOS_AfterFork_Parent() = 0;

    virtual void PyOS_BeforeFork() = 0;

    virtual PyObject* PyOS_FSPath(PyObject* path) = 0;

    virtual int PyOS_InterruptOccurred() = 0;

    virtual char* PyOS_Readline(FILE* p0, FILE* p1, const char* p2) = 0;

    virtual char* PyOS_double_to_string(double val, char format_code, int precision, int flags, int* type) = 0;

    virtual int PyOS_mystricmp(const char* p0, const char* p1) = 0;

    virtual int PyOS_mystrnicmp(const char* p0, const char* p1, Py_ssize_t p2) = 0;

    virtual double PyOS_string_to_double(const char* str, char** endptr, PyObject* overflow_exception) = 0;

    virtual long PyOS_strtol(const char* p0, char** p1, int p2) = 0;

    virtual unsigned long PyOS_strtoul(const char* p0, char** p1, int p2) = 0;

    virtual int PyOS_vsnprintf(char* str, size_t size, const char* format, va_list va) = 0;

    virtual PyObject* PyObject_ASCII(PyObject* p0) = 0;

    virtual int PyObject_AsFileDescriptor(PyObject* p0) = 0;

    virtual PyObject* PyObject_Bytes(PyObject* p0) = 0;

    virtual PyObject* PyObject_Call(PyObject* callable, PyObject* args, PyObject* kwargs) = 0;

    virtual void PyObject_CallFinalizer(PyObject* p0) = 0;

    virtual int PyObject_CallFinalizerFromDealloc(PyObject* p0) = 0;

    virtual PyObject* PyObject_CallMethodNoArgs(PyObject* self, PyObject* name) = 0;

    virtual PyObject* PyObject_CallMethodOneArg(PyObject* self, PyObject* name, PyObject* arg) = 0;

    virtual PyObject* PyObject_CallNoArgs(PyObject* func) = 0;

    virtual PyObject* PyObject_CallObject(PyObject* callable, PyObject* args) = 0;

    virtual PyObject* PyObject_CallOneArg(PyObject* func, PyObject* arg) = 0;

    virtual void* PyObject_Calloc(size_t nelem, size_t elsize) = 0;

    virtual int PyObject_CheckBuffer(PyObject* obj) = 0;

    virtual void PyObject_ClearWeakRefs(PyObject* p0) = 0;

    virtual int PyObject_CopyData(PyObject* dest, PyObject* src) = 0;

    virtual int PyObject_DelItem(PyObject* o, PyObject* key) = 0;

    virtual int PyObject_DelItemString(PyObject* o, const char* key) = 0;

    virtual PyObject* PyObject_Dir(PyObject* p0) = 0;

    virtual PyObject* PyObject_Format(PyObject* obj, PyObject* format_spec) = 0;

    virtual void PyObject_Free(void* ptr) = 0;

    virtual void PyObject_GC_Del(void* p0) = 0;

    virtual int PyObject_GC_IsFinalized(PyObject* p0) = 0;

    virtual int PyObject_GC_IsTracked(PyObject* p0) = 0;

    virtual void PyObject_GC_Track(void* p0) = 0;

    virtual void PyObject_GC_UnTrack(void* p0) = 0;

    virtual PyObject** PyObject_GET_WEAKREFS_LISTPTR(PyObject* op) = 0;

    virtual PyObject* PyObject_GenericGetAttr(PyObject* p0, PyObject* p1) = 0;

    virtual PyObject* PyObject_GenericGetDict(PyObject* p0, void* p1) = 0;

    virtual int PyObject_GenericSetAttr(PyObject* p0, PyObject* p1, PyObject* p2) = 0;

    virtual int PyObject_GenericSetDict(PyObject* p0, PyObject* p1, void* p2) = 0;

    virtual PyObject* PyObject_GetAIter(PyObject* p0) = 0;

    virtual PyObject* PyObject_GetAttr(PyObject* p0, PyObject* p1) = 0;

    virtual PyObject* PyObject_GetAttrString(PyObject* p0, const char* p1) = 0;

    virtual PyObject* PyObject_GetItem(PyObject* o, PyObject* key) = 0;

    virtual PyObject* PyObject_GetIter(PyObject* p0) = 0;

    virtual int PyObject_HasAttr(PyObject* p0, PyObject* p1) = 0;

    virtual int PyObject_HasAttrString(PyObject* p0, const char* p1) = 0;

    virtual int PyObject_IS_GC(PyObject* obj) = 0;

    virtual PyObject* PyObject_Init(PyObject* p0, PyTypeObject* p1) = 0;

    virtual int PyObject_IsInstance(PyObject* object, PyObject* typeorclass) = 0;

    virtual int PyObject_IsSubclass(PyObject* object, PyObject* typeorclass) = 0;

    virtual int PyObject_IsTrue(PyObject* p0) = 0;

    virtual Py_ssize_t PyObject_LengthHint(PyObject* o, Py_ssize_t p1) = 0;

    virtual void* PyObject_Malloc(size_t size) = 0;

    virtual int PyObject_Not(PyObject* p0) = 0;

    virtual int PyObject_Print(PyObject* p0, FILE* p1, int p2) = 0;

    virtual void* PyObject_Realloc(void* ptr, size_t new_size) = 0;

    virtual PyObject* PyObject_Repr(PyObject* p0) = 0;

    virtual PyObject* PyObject_RichCompare(PyObject* p0, PyObject* p1, int p2) = 0;

    virtual int PyObject_RichCompareBool(PyObject* p0, PyObject* p1, int p2) = 0;

    virtual PyObject* PyObject_SelfIter(PyObject* p0) = 0;

    virtual int PyObject_SetAttr(PyObject* p0, PyObject* p1, PyObject* p2) = 0;

    virtual int PyObject_SetAttrString(PyObject* p0, const char* p1, PyObject* p2) = 0;

    virtual int PyObject_SetItem(PyObject* o, PyObject* key, PyObject* v) = 0;

    virtual Py_ssize_t PyObject_Size(PyObject* o) = 0;

    virtual PyObject* PyObject_Str(PyObject* p0) = 0;

    virtual PyObject* PyObject_Type(PyObject* o) = 0;

    virtual PyObject* PyObject_Vectorcall(PyObject* callable, PyObject* const* args, size_t nargsf, PyObject* kwnames) = 0;

    virtual PyObject* PyObject_VectorcallDict(PyObject* callable, PyObject* const* args, size_t nargsf, PyObject* kwargs) = 0;

    virtual PyObject* PyObject_VectorcallMethod(PyObject* name, PyObject* const* args, size_t nargsf, PyObject* kwnames) = 0;

    virtual PyObject* PySeqIter_New(PyObject* p0) = 0;

    virtual int PySequence_Check(PyObject* o) = 0;

    virtual PyObject* PySequence_Concat(PyObject* o1, PyObject* o2) = 0;

    virtual int PySequence_Contains(PyObject* seq, PyObject* ob) = 0;

    virtual Py_ssize_t PySequence_Count(PyObject* o, PyObject* value) = 0;

    virtual int PySequence_DelItem(PyObject* o, Py_ssize_t i) = 0;

    virtual int PySequence_DelSlice(PyObject* o, Py_ssize_t i1, Py_ssize_t i2) = 0;

    virtual PyObject* PySequence_Fast(PyObject* o, const char* m) = 0;

    virtual PyObject* PySequence_GetItem(PyObject* o, Py_ssize_t i) = 0;

    virtual PyObject* PySequence_GetSlice(PyObject* o, Py_ssize_t i1, Py_ssize_t i2) = 0;

    virtual PyObject* PySequence_InPlaceConcat(PyObject* o1, PyObject* o2) = 0;

    virtual PyObject* PySequence_InPlaceRepeat(PyObject* o, Py_ssize_t count) = 0;

    virtual Py_ssize_t PySequence_Index(PyObject* o, PyObject* value) = 0;

    virtual PyObject* PySequence_List(PyObject* o) = 0;

    virtual PyObject* PySequence_Repeat(PyObject* o, Py_ssize_t count) = 0;

    virtual int PySequence_SetItem(PyObject* o, Py_ssize_t i, PyObject* v) = 0;

    virtual int PySequence_SetSlice(PyObject* o, Py_ssize_t i1, Py_ssize_t i2, PyObject* v) = 0;

    virtual Py_ssize_t PySequence_Size(PyObject* o) = 0;

    virtual PyObject* PySequence_Tuple(PyObject* o) = 0;

    virtual int PySet_Add(PyObject* set, PyObject* key) = 0;

    virtual int PySet_Clear(PyObject* set) = 0;

    virtual int PySet_Contains(PyObject* anyset, PyObject* key) = 0;

    virtual int PySet_Discard(PyObject* set, PyObject* key) = 0;

    virtual PyObject* PySet_New(PyObject* p0) = 0;

    virtual PyObject* PySet_Pop(PyObject* set) = 0;

    virtual Py_ssize_t PySet_Size(PyObject* anyset) = 0;

    virtual Py_ssize_t PySlice_AdjustIndices(Py_ssize_t length, Py_ssize_t* start, Py_ssize_t* stop, Py_ssize_t step) = 0;

    virtual int PySlice_GetIndices(PyObject* r, Py_ssize_t length, Py_ssize_t* start, Py_ssize_t* stop, Py_ssize_t* step) = 0;

    virtual PyObject* PySlice_New(PyObject* start, PyObject* stop, PyObject* step) = 0;

    virtual int PySlice_Unpack(PyObject* slice, Py_ssize_t* start, Py_ssize_t* stop, Py_ssize_t* step) = 0;

    virtual PyObject* PyStaticMethod_New(PyObject* p0) = 0;

    virtual PyObject* PyTuple_GetItem(PyObject* p0, Py_ssize_t p1) = 0;

    virtual PyObject* PyTuple_GetSlice(PyObject* p0, Py_ssize_t p1, Py_ssize_t p2) = 0;

    virtual PyObject* PyTuple_New(Py_ssize_t size) = 0;

    virtual int PyTuple_SetItem(PyObject* p0, Py_ssize_t p1, PyObject* p2) = 0;

    virtual Py_ssize_t PyTuple_Size(PyObject* p0) = 0;

    virtual unsigned int PyType_ClearCache() = 0;

    virtual PyObject* PyType_GenericAlloc(PyTypeObject* p0, Py_ssize_t p1) = 0;

    virtual PyObject* PyType_GenericNew(PyTypeObject* p0, PyObject* p1, PyObject* p2) = 0;

    virtual unsigned long PyType_GetFlags(PyTypeObject* p0) = 0;

    virtual PyObject* PyType_GetModule(struct _typeobject* p0) = 0;

    virtual void* PyType_GetModuleState(struct _typeobject* p0) = 0;

    virtual void* PyType_GetSlot(PyTypeObject* p0, int p1) = 0;

    virtual int PyType_HasFeature(PyTypeObject* type, unsigned long feature) = 0;

    virtual int PyType_IsSubtype(PyTypeObject* p0, PyTypeObject* p1) = 0;

    virtual void PyType_Modified(PyTypeObject* p0) = 0;

    virtual int PyType_Ready(PyTypeObject* p0) = 0;

    virtual PyObject* PyUnicodeDecodeError_Create(const char* encoding, const char* object, Py_ssize_t length, Py_ssize_t start, Py_ssize_t end, const char* reason) = 0;

    virtual PyObject* PyUnicodeDecodeError_GetEncoding(PyObject* p0) = 0;

    virtual int PyUnicodeDecodeError_GetEnd(PyObject* p0, Py_ssize_t* p1) = 0;

    virtual PyObject* PyUnicodeDecodeError_GetObject(PyObject* p0) = 0;

    virtual PyObject* PyUnicodeDecodeError_GetReason(PyObject* p0) = 0;

    virtual int PyUnicodeDecodeError_GetStart(PyObject* p0, Py_ssize_t* p1) = 0;

    virtual int PyUnicodeDecodeError_SetEnd(PyObject* p0, Py_ssize_t p1) = 0;

    virtual int PyUnicodeDecodeError_SetReason(PyObject* exc, const char* reason) = 0;

    virtual int PyUnicodeDecodeError_SetStart(PyObject* p0, Py_ssize_t p1) = 0;

    virtual PyObject* PyUnicodeEncodeError_Create(const char* encoding, const Py_UNICODE* object, Py_ssize_t length, Py_ssize_t start, Py_ssize_t end, const char* reason) = 0;

    virtual PyObject* PyUnicodeEncodeError_GetEncoding(PyObject* p0) = 0;

    virtual int PyUnicodeEncodeError_GetEnd(PyObject* p0, Py_ssize_t* p1) = 0;

    virtual PyObject* PyUnicodeEncodeError_GetObject(PyObject* p0) = 0;

    virtual PyObject* PyUnicodeEncodeError_GetReason(PyObject* p0) = 0;

    virtual int PyUnicodeEncodeError_GetStart(PyObject* p0, Py_ssize_t* p1) = 0;

    virtual int PyUnicodeEncodeError_SetEnd(PyObject* p0, Py_ssize_t p1) = 0;

    virtual int PyUnicodeEncodeError_SetReason(PyObject* exc, const char* reason) = 0;

    virtual int PyUnicodeEncodeError_SetStart(PyObject* p0, Py_ssize_t p1) = 0;

    virtual PyObject* PyUnicodeTranslateError_Create(const Py_UNICODE* object, Py_ssize_t length, Py_ssize_t start, Py_ssize_t end, const char* reason) = 0;

    virtual int PyUnicodeTranslateError_GetEnd(PyObject* p0, Py_ssize_t* p1) = 0;

    virtual PyObject* PyUnicodeTranslateError_GetObject(PyObject* p0) = 0;

    virtual PyObject* PyUnicodeTranslateError_GetReason(PyObject* p0) = 0;

    virtual int PyUnicodeTranslateError_GetStart(PyObject* p0, Py_ssize_t* p1) = 0;

    virtual int PyUnicodeTranslateError_SetEnd(PyObject* p0, Py_ssize_t p1) = 0;

    virtual int PyUnicodeTranslateError_SetReason(PyObject* exc, const char* reason) = 0;

    virtual int PyUnicodeTranslateError_SetStart(PyObject* p0, Py_ssize_t p1) = 0;

    virtual PyObject* PyVectorcall_Call(PyObject* callable, PyObject* tuple, PyObject* dict) = 0;

    virtual PyObject* PyWrapper_New(PyObject* p0, PyObject* p1) = 0;

    virtual int Py_BytesMain(int argc, char** argv) = 0;

    virtual void Py_DecRef(PyObject* p0) = 0;

    virtual wchar_t* Py_DecodeLocale(const char* arg, size_t* size) = 0;

    virtual char* Py_EncodeLocale(const wchar_t* text, size_t* error_pos) = 0;

    virtual int Py_EnterRecursiveCall(const char* where) = 0;

    virtual int Py_FdIsInteractive(FILE* p0, const char* p1) = 0;

    virtual void Py_Finalize() = 0;

    virtual int Py_FinalizeEx() = 0;

    virtual PyObject* Py_GenericAlias(PyObject* p0, PyObject* p1) = 0;

    virtual const char* Py_GetBuildInfo() = 0;

    virtual const char* Py_GetCompiler() = 0;

    virtual const char* Py_GetCopyright() = 0;

    virtual wchar_t* Py_GetExecPrefix() = 0;

    virtual wchar_t* Py_GetPath() = 0;

    virtual const char* Py_GetPlatform() = 0;

    virtual wchar_t* Py_GetPrefix() = 0;

    virtual wchar_t* Py_GetProgramFullPath() = 0;

    virtual wchar_t* Py_GetProgramName() = 0;

    virtual wchar_t* Py_GetPythonHome() = 0;

    virtual int Py_GetRecursionLimit() = 0;

    virtual const char* Py_GetVersion() = 0;

    virtual void Py_IncRef(PyObject* p0) = 0;

    virtual void Py_Initialize() = 0;

    virtual void Py_InitializeEx(int p0) = 0;

    virtual int Py_IsInitialized() = 0;

    virtual void Py_LeaveRecursiveCall() = 0;

    virtual int Py_MakePendingCalls() = 0;

    virtual int Py_ReprEnter(PyObject* p0) = 0;

    virtual void Py_ReprLeave(PyObject* p0) = 0;

    virtual int Py_RunMain() = 0;

    virtual void Py_SetRecursionLimit(int p0) = 0;

    virtual void Py_UNICODE_COPY(Py_UNICODE* target, const Py_UNICODE* source, Py_ssize_t length) = 0;

    virtual void Py_UNICODE_FILL(Py_UNICODE* target, Py_UNICODE value, Py_ssize_t length) = 0;

    virtual char* Py_UniversalNewlineFgets(char* p0, int p1, FILE* p2, PyObject* p3) = 0;

    virtual PyObject* Py_VaBuildValue(const char* p0, va_list p1) = 0;

    virtual double fmod(double p0, double p1) = 0;

    virtual double frexp(double p0, int* p1) = 0;

    virtual double ldexp(double p0, int p1) = 0;

    virtual double modf(double p0, double* p1) = 0;

    virtual double pow(double p0, double p1) = 0;
};

}
