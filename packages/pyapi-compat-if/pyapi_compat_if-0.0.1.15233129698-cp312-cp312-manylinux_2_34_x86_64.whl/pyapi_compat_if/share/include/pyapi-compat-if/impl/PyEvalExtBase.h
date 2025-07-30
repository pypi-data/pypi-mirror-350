
/**
 * PyEvalExtBase.h
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
#include "pyapi-compat-if/IPyEvalBase.h"
#include "Python.h"

namespace pyapi {

class PyEvalExtBase : public virtual IPyEvalBase {
public:
    PyEvalExtBase() { }

    virtual ~PyEvalExtBase() { }
    virtual int PyAIter_Check(PyObject* p0) override {
    return ::PyAIter_Check(p0);
}

virtual int PyArg_VaParse(PyObject* p0, const char* p1, va_list p2) override {
return ::PyArg_VaParse(p0, p1, p2);
}

virtual int PyArg_VaParseTupleAndKeywords(PyObject* p0, PyObject* p1, const char* p2, char** p3, va_list p4) override {
return ::PyArg_VaParseTupleAndKeywords(p0, p1, p2, p3, p4);
}

virtual int PyArg_ValidateKeywordArguments(PyObject* p0) override {
return ::PyArg_ValidateKeywordArguments(p0);
}

virtual PyObject* PyBool_FromLong(long p0) override {
return ::PyBool_FromLong(p0);
}

virtual char* PyByteArray_AsString(PyObject* p0) override {
return ::PyByteArray_AsString(p0);
}

virtual PyObject* PyByteArray_Concat(PyObject* p0, PyObject* p1) override {
return ::PyByteArray_Concat(p0, p1);
}

virtual PyObject* PyByteArray_FromObject(PyObject* p0) override {
return ::PyByteArray_FromObject(p0);
}

virtual PyObject* PyByteArray_FromStringAndSize(const char* p0, Py_ssize_t p1) override {
return ::PyByteArray_FromStringAndSize(p0, p1);
}

virtual int PyByteArray_Resize(PyObject* p0, Py_ssize_t p1) override {
return ::PyByteArray_Resize(p0, p1);
}

virtual Py_ssize_t PyByteArray_Size(PyObject* p0) override {
return ::PyByteArray_Size(p0);
}

virtual char* PyBytes_AsString(PyObject* p0) override {
return ::PyBytes_AsString(p0);
}

virtual int PyBytes_AsStringAndSize(PyObject* obj, char** s, Py_ssize_t* len) override {
return ::PyBytes_AsStringAndSize(obj, s, len);
}

virtual void PyBytes_Concat(PyObject** p0, PyObject* p1) override {
return ::PyBytes_Concat(p0, p1);
}

virtual void PyBytes_ConcatAndDel(PyObject** p0, PyObject* p1) override {
return ::PyBytes_ConcatAndDel(p0, p1);
}

virtual PyObject* PyBytes_DecodeEscape(const char* p0, Py_ssize_t p1, const char* p2, Py_ssize_t p3, const char* p4) override {
return ::PyBytes_DecodeEscape(p0, p1, p2, p3, p4);
}

virtual PyObject* PyBytes_FromFormatV(const char* p0, va_list p1) override {
return ::PyBytes_FromFormatV(p0, p1);
}

virtual PyObject* PyBytes_FromObject(PyObject* p0) override {
return ::PyBytes_FromObject(p0);
}

virtual PyObject* PyBytes_FromString(const char* p0) override {
return ::PyBytes_FromString(p0);
}

virtual PyObject* PyBytes_FromStringAndSize(const char* p0, Py_ssize_t p1) override {
return ::PyBytes_FromStringAndSize(p0, p1);
}

virtual PyObject* PyBytes_Repr(PyObject* p0, int p1) override {
return ::PyBytes_Repr(p0, p1);
}

virtual Py_ssize_t PyBytes_Size(PyObject* p0) override {
return ::PyBytes_Size(p0);
}

virtual PyObject* PyCallIter_New(PyObject* p0, PyObject* p1) override {
return ::PyCallIter_New(p0, p1);
}

virtual int PyCallable_Check(PyObject* p0) override {
return ::PyCallable_Check(p0);
}

virtual PyObject* PyCell_Get(PyObject* p0) override {
return ::PyCell_Get(p0);
}

virtual PyObject* PyCell_New(PyObject* p0) override {
return ::PyCell_New(p0);
}

virtual int PyCell_Set(PyObject* p0, PyObject* p1) override {
return ::PyCell_Set(p0, p1);
}

virtual PyObject* PyClassMethod_New(PyObject* p0) override {
return ::PyClassMethod_New(p0);
}

virtual PyObject* PyCodec_BackslashReplaceErrors(PyObject* exc) override {
return ::PyCodec_BackslashReplaceErrors(exc);
}

virtual PyObject* PyCodec_Decode(PyObject* object, const char* encoding, const char* errors) override {
return ::PyCodec_Decode(object, encoding, errors);
}

virtual PyObject* PyCodec_Decoder(const char* encoding) override {
return ::PyCodec_Decoder(encoding);
}

virtual PyObject* PyCodec_Encode(PyObject* object, const char* encoding, const char* errors) override {
return ::PyCodec_Encode(object, encoding, errors);
}

virtual PyObject* PyCodec_Encoder(const char* encoding) override {
return ::PyCodec_Encoder(encoding);
}

virtual PyObject* PyCodec_IgnoreErrors(PyObject* exc) override {
return ::PyCodec_IgnoreErrors(exc);
}

virtual PyObject* PyCodec_IncrementalDecoder(const char* encoding, const char* errors) override {
return ::PyCodec_IncrementalDecoder(encoding, errors);
}

virtual PyObject* PyCodec_IncrementalEncoder(const char* encoding, const char* errors) override {
return ::PyCodec_IncrementalEncoder(encoding, errors);
}

virtual int PyCodec_KnownEncoding(const char* encoding) override {
return ::PyCodec_KnownEncoding(encoding);
}

virtual PyObject* PyCodec_LookupError(const char* name) override {
return ::PyCodec_LookupError(name);
}

virtual PyObject* PyCodec_NameReplaceErrors(PyObject* exc) override {
return ::PyCodec_NameReplaceErrors(exc);
}

virtual int PyCodec_Register(PyObject* search_function) override {
return ::PyCodec_Register(search_function);
}

virtual int PyCodec_RegisterError(const char* name, PyObject* error) override {
return ::PyCodec_RegisterError(name, error);
}

virtual PyObject* PyCodec_ReplaceErrors(PyObject* exc) override {
return ::PyCodec_ReplaceErrors(exc);
}

virtual PyObject* PyCodec_StreamReader(const char* encoding, PyObject* stream, const char* errors) override {
return ::PyCodec_StreamReader(encoding, stream, errors);
}

virtual PyObject* PyCodec_StreamWriter(const char* encoding, PyObject* stream, const char* errors) override {
return ::PyCodec_StreamWriter(encoding, stream, errors);
}

virtual PyObject* PyCodec_StrictErrors(PyObject* exc) override {
return ::PyCodec_StrictErrors(exc);
}

virtual int PyCodec_Unregister(PyObject* search_function) override {
return ::PyCodec_Unregister(search_function);
}

virtual PyObject* PyCodec_XMLCharRefReplaceErrors(PyObject* exc) override {
return ::PyCodec_XMLCharRefReplaceErrors(exc);
}

virtual int PyCompile_OpcodeStackEffect(int opcode, int oparg) override {
return ::PyCompile_OpcodeStackEffect(opcode, oparg);
}

virtual int PyCompile_OpcodeStackEffectWithJump(int opcode, int oparg, int jump) override {
return ::PyCompile_OpcodeStackEffectWithJump(opcode, oparg, jump);
}

virtual int PyContextVar_Get(PyObject* var, PyObject* default_value, PyObject** value) override {
return ::PyContextVar_Get(var, default_value, value);
}

virtual PyObject* PyContextVar_New(const char* name, PyObject* default_value) override {
return ::PyContextVar_New(name, default_value);
}

virtual int PyContextVar_Reset(PyObject* var, PyObject* token) override {
return ::PyContextVar_Reset(var, token);
}

virtual PyObject* PyContextVar_Set(PyObject* var, PyObject* value) override {
return ::PyContextVar_Set(var, value);
}

virtual PyObject* PyContext_Copy(PyObject* p0) override {
return ::PyContext_Copy(p0);
}

virtual PyObject* PyContext_CopyCurrent() override {
return ::PyContext_CopyCurrent();
}

virtual int PyContext_Enter(PyObject* p0) override {
return ::PyContext_Enter(p0);
}

virtual int PyContext_Exit(PyObject* p0) override {
return ::PyContext_Exit(p0);
}

virtual PyObject* PyContext_New() override {
return ::PyContext_New();
}

virtual PyObject* PyDictProxy_New(PyObject* p0) override {
return ::PyDictProxy_New(p0);
}

virtual void PyDict_Clear(PyObject* mp) override {
return ::PyDict_Clear(mp);
}

virtual int PyDict_ClearWatcher(int watcher_id) override {
return ::PyDict_ClearWatcher(watcher_id);
}

virtual int PyDict_Contains(PyObject* mp, PyObject* key) override {
return ::PyDict_Contains(mp, key);
}

virtual PyObject* PyDict_Copy(PyObject* mp) override {
return ::PyDict_Copy(mp);
}

virtual int PyDict_DelItem(PyObject* mp, PyObject* key) override {
return ::PyDict_DelItem(mp, key);
}

virtual int PyDict_DelItemString(PyObject* dp, const char* key) override {
return ::PyDict_DelItemString(dp, key);
}

virtual PyObject* PyDict_GetItem(PyObject* mp, PyObject* key) override {
return ::PyDict_GetItem(mp, key);
}

virtual PyObject* PyDict_GetItemString(PyObject* dp, const char* key) override {
return ::PyDict_GetItemString(dp, key);
}

virtual PyObject* PyDict_GetItemWithError(PyObject* mp, PyObject* key) override {
return ::PyDict_GetItemWithError(mp, key);
}

virtual PyObject* PyDict_Items(PyObject* mp) override {
return ::PyDict_Items(mp);
}

virtual PyObject* PyDict_Keys(PyObject* mp) override {
return ::PyDict_Keys(mp);
}

virtual int PyDict_Merge(PyObject* mp, PyObject* other, int override) override {
return ::PyDict_Merge(mp, other, override);
}

virtual int PyDict_MergeFromSeq2(PyObject* d, PyObject* seq2, int override) override {
return ::PyDict_MergeFromSeq2(d, seq2, override);
}

virtual PyObject* PyDict_New() override {
return ::PyDict_New();
}

virtual int PyDict_Next(PyObject* mp, Py_ssize_t* pos, PyObject** key, PyObject** value) override {
return ::PyDict_Next(mp, pos, key, value);
}

virtual PyObject* PyDict_SetDefault(PyObject* mp, PyObject* key, PyObject* defaultobj) override {
return ::PyDict_SetDefault(mp, key, defaultobj);
}

virtual int PyDict_SetItem(PyObject* mp, PyObject* key, PyObject* item) override {
return ::PyDict_SetItem(mp, key, item);
}

virtual int PyDict_SetItemString(PyObject* dp, const char* key, PyObject* item) override {
return ::PyDict_SetItemString(dp, key, item);
}

virtual Py_ssize_t PyDict_Size(PyObject* mp) override {
return ::PyDict_Size(mp);
}

virtual int PyDict_Unwatch(int watcher_id, PyObject* dict) override {
return ::PyDict_Unwatch(watcher_id, dict);
}

virtual int PyDict_Update(PyObject* mp, PyObject* other) override {
return ::PyDict_Update(mp, other);
}

virtual PyObject* PyDict_Values(PyObject* mp) override {
return ::PyDict_Values(mp);
}

virtual int PyDict_Watch(int watcher_id, PyObject* dict) override {
return ::PyDict_Watch(watcher_id, dict);
}

virtual int PyErr_BadArgument() override {
return ::PyErr_BadArgument();
}

virtual int PyErr_CheckSignals() override {
return ::PyErr_CheckSignals();
}

virtual void PyErr_Clear() override {
return ::PyErr_Clear();
}

virtual void PyErr_Display(PyObject* p0, PyObject* p1, PyObject* p2) override {
return ::PyErr_Display(p0, p1, p2);
}

virtual void PyErr_DisplayException(PyObject* p0) override {
return ::PyErr_DisplayException(p0);
}

virtual int PyErr_ExceptionMatches(PyObject* p0) override {
return ::PyErr_ExceptionMatches(p0);
}

virtual void PyErr_Fetch(PyObject** p0, PyObject** p1, PyObject** p2) override {
return ::PyErr_Fetch(p0, p1, p2);
}

virtual PyObject* PyErr_FormatV(PyObject* exception, const char* format, va_list vargs) override {
return ::PyErr_FormatV(exception, format, vargs);
}

virtual void PyErr_GetExcInfo(PyObject** p0, PyObject** p1, PyObject** p2) override {
return ::PyErr_GetExcInfo(p0, p1, p2);
}

virtual PyObject* PyErr_GetHandledException() override {
return ::PyErr_GetHandledException();
}

virtual PyObject* PyErr_GetRaisedException() override {
return ::PyErr_GetRaisedException();
}

virtual int PyErr_GivenExceptionMatches(PyObject* p0, PyObject* p1) override {
return ::PyErr_GivenExceptionMatches(p0, p1);
}

virtual PyObject* PyErr_NewException(const char* name, PyObject* base, PyObject* dict) override {
return ::PyErr_NewException(name, base, dict);
}

virtual PyObject* PyErr_NewExceptionWithDoc(const char* name, const char* doc, PyObject* base, PyObject* dict) override {
return ::PyErr_NewExceptionWithDoc(name, doc, base, dict);
}

virtual PyObject* PyErr_NoMemory() override {
return ::PyErr_NoMemory();
}

virtual void PyErr_NormalizeException(PyObject** p0, PyObject** p1, PyObject** p2) override {
return ::PyErr_NormalizeException(p0, p1, p2);
}

virtual PyObject* PyErr_Occurred() override {
return ::PyErr_Occurred();
}

virtual void PyErr_Print() override {
return ::PyErr_Print();
}

virtual void PyErr_PrintEx(int p0) override {
return ::PyErr_PrintEx(p0);
}

virtual PyObject* PyErr_ProgramText(const char* filename, int lineno) override {
return ::PyErr_ProgramText(filename, lineno);
}

virtual PyObject* PyErr_ProgramTextObject(PyObject* filename, int lineno) override {
return ::PyErr_ProgramTextObject(filename, lineno);
}

virtual void PyErr_RangedSyntaxLocationObject(PyObject* filename, int lineno, int col_offset, int end_lineno, int end_col_offset) override {
return ::PyErr_RangedSyntaxLocationObject(filename, lineno, col_offset, end_lineno, end_col_offset);
}

virtual void PyErr_Restore(PyObject* p0, PyObject* p1, PyObject* p2) override {
return ::PyErr_Restore(p0, p1, p2);
}

virtual void PyErr_SetExcInfo(PyObject* p0, PyObject* p1, PyObject* p2) override {
return ::PyErr_SetExcInfo(p0, p1, p2);
}

virtual PyObject* PyErr_SetFromErrno(PyObject* p0) override {
return ::PyErr_SetFromErrno(p0);
}

virtual PyObject* PyErr_SetFromErrnoWithFilename(PyObject* exc, const char* filename) override {
return ::PyErr_SetFromErrnoWithFilename(exc, filename);
}

virtual PyObject* PyErr_SetFromErrnoWithFilenameObject(PyObject* p0, PyObject* p1) override {
return ::PyErr_SetFromErrnoWithFilenameObject(p0, p1);
}

virtual PyObject* PyErr_SetFromErrnoWithFilenameObjects(PyObject* p0, PyObject* p1, PyObject* p2) override {
return ::PyErr_SetFromErrnoWithFilenameObjects(p0, p1, p2);
}

virtual void PyErr_SetHandledException(PyObject* p0) override {
return ::PyErr_SetHandledException(p0);
}

virtual PyObject* PyErr_SetImportError(PyObject* p0, PyObject* p1, PyObject* p2) override {
return ::PyErr_SetImportError(p0, p1, p2);
}

virtual PyObject* PyErr_SetImportErrorSubclass(PyObject* p0, PyObject* p1, PyObject* p2, PyObject* p3) override {
return ::PyErr_SetImportErrorSubclass(p0, p1, p2, p3);
}

virtual void PyErr_SetInterrupt() override {
return ::PyErr_SetInterrupt();
}

virtual int PyErr_SetInterruptEx(int signum) override {
return ::PyErr_SetInterruptEx(signum);
}

virtual void PyErr_SetNone(PyObject* p0) override {
return ::PyErr_SetNone(p0);
}

virtual void PyErr_SetObject(PyObject* p0, PyObject* p1) override {
return ::PyErr_SetObject(p0, p1);
}

virtual void PyErr_SetRaisedException(PyObject* p0) override {
return ::PyErr_SetRaisedException(p0);
}

virtual void PyErr_SetString(PyObject* exception, const char* string) override {
return ::PyErr_SetString(exception, string);
}

virtual void PyErr_SyntaxLocation(const char* filename, int lineno) override {
return ::PyErr_SyntaxLocation(filename, lineno);
}

virtual void PyErr_SyntaxLocationEx(const char* filename, int lineno, int col_offset) override {
return ::PyErr_SyntaxLocationEx(filename, lineno, col_offset);
}

virtual void PyErr_SyntaxLocationObject(PyObject* filename, int lineno, int col_offset) override {
return ::PyErr_SyntaxLocationObject(filename, lineno, col_offset);
}

virtual int PyErr_WarnEx(PyObject* category, const char* message, Py_ssize_t stack_level) override {
return ::PyErr_WarnEx(category, message, stack_level);
}

virtual int PyErr_WarnExplicit(PyObject* category, const char* message, const char* filename, int lineno, const char* module, PyObject* registry) override {
return ::PyErr_WarnExplicit(category, message, filename, lineno, module, registry);
}

virtual int PyErr_WarnExplicitObject(PyObject* category, PyObject* message, PyObject* filename, int lineno, PyObject* module, PyObject* registry) override {
return ::PyErr_WarnExplicitObject(category, message, filename, lineno, module, registry);
}

virtual void PyErr_WriteUnraisable(PyObject* p0) override {
return ::PyErr_WriteUnraisable(p0);
}

virtual PyObject* PyEval_EvalCode(PyObject* p0, PyObject* p1, PyObject* p2) override {
return ::PyEval_EvalCode(p0, p1, p2);
}

virtual PyObject* PyEval_EvalCodeEx(PyObject* co, PyObject* globals, PyObject* locals, PyObject* const* args, int argc, PyObject* const* kwds, int kwdc, PyObject* const* defs, int defc, PyObject* kwdefs, PyObject* closure) override {
return ::PyEval_EvalCodeEx(co, globals, locals, args, argc, kwds, kwdc, defs, defc, kwdefs, closure);
}

virtual PyObject* PyEval_GetBuiltins() override {
return ::PyEval_GetBuiltins();
}

virtual const char* PyEval_GetFuncDesc(PyObject* p0) override {
return ::PyEval_GetFuncDesc(p0);
}

virtual const char* PyEval_GetFuncName(PyObject* p0) override {
return ::PyEval_GetFuncName(p0);
}

virtual PyObject* PyEval_GetGlobals() override {
return ::PyEval_GetGlobals();
}

virtual PyObject* PyEval_GetLocals() override {
return ::PyEval_GetLocals();
}

virtual PyObject* PyException_GetArgs(PyObject* p0) override {
return ::PyException_GetArgs(p0);
}

virtual PyObject* PyException_GetCause(PyObject* p0) override {
return ::PyException_GetCause(p0);
}

virtual PyObject* PyException_GetContext(PyObject* p0) override {
return ::PyException_GetContext(p0);
}

virtual PyObject* PyException_GetTraceback(PyObject* p0) override {
return ::PyException_GetTraceback(p0);
}

virtual void PyException_SetArgs(PyObject* p0, PyObject* p1) override {
return ::PyException_SetArgs(p0, p1);
}

virtual void PyException_SetCause(PyObject* p0, PyObject* p1) override {
return ::PyException_SetCause(p0, p1);
}

virtual void PyException_SetContext(PyObject* p0, PyObject* p1) override {
return ::PyException_SetContext(p0, p1);
}

virtual int PyException_SetTraceback(PyObject* p0, PyObject* p1) override {
return ::PyException_SetTraceback(p0, p1);
}

virtual double PyFloat_AsDouble(PyObject* p0) override {
return ::PyFloat_AsDouble(p0);
}

virtual PyObject* PyFloat_FromDouble(double p0) override {
return ::PyFloat_FromDouble(p0);
}

virtual PyObject* PyFloat_FromString(PyObject* p0) override {
return ::PyFloat_FromString(p0);
}

virtual PyObject* PyFloat_GetInfo() override {
return ::PyFloat_GetInfo();
}

virtual double PyFloat_GetMax() override {
return ::PyFloat_GetMax();
}

virtual double PyFloat_GetMin() override {
return ::PyFloat_GetMin();
}

virtual int PyFloat_Pack2(double x, char* p, int le) override {
return ::PyFloat_Pack2(x, p, le);
}

virtual int PyFloat_Pack4(double x, char* p, int le) override {
return ::PyFloat_Pack4(x, p, le);
}

virtual int PyFloat_Pack8(double x, char* p, int le) override {
return ::PyFloat_Pack8(x, p, le);
}

virtual double PyFloat_Unpack2(const char* p, int le) override {
return ::PyFloat_Unpack2(p, le);
}

virtual double PyFloat_Unpack4(const char* p, int le) override {
return ::PyFloat_Unpack4(p, le);
}

virtual double PyFloat_Unpack8(const char* p, int le) override {
return ::PyFloat_Unpack8(p, le);
}

virtual PyObject* PyFrozenSet_New(PyObject* p0) override {
return ::PyFrozenSet_New(p0);
}

virtual Py_ssize_t PyGC_Collect() override {
return ::PyGC_Collect();
}

virtual int PyGC_Disable() override {
return ::PyGC_Disable();
}

virtual int PyGC_Enable() override {
return ::PyGC_Enable();
}

virtual int PyGC_IsEnabled() override {
return ::PyGC_IsEnabled();
}

virtual PyObject* PyImport_AddModule(const char* name) override {
return ::PyImport_AddModule(name);
}

virtual PyObject* PyImport_AddModuleObject(PyObject* name) override {
return ::PyImport_AddModuleObject(name);
}

virtual PyObject* PyImport_ExecCodeModule(const char* name, PyObject* co) override {
return ::PyImport_ExecCodeModule(name, co);
}

virtual PyObject* PyImport_ExecCodeModuleEx(const char* name, PyObject* co, const char* pathname) override {
return ::PyImport_ExecCodeModuleEx(name, co, pathname);
}

virtual PyObject* PyImport_ExecCodeModuleObject(PyObject* name, PyObject* co, PyObject* pathname, PyObject* cpathname) override {
return ::PyImport_ExecCodeModuleObject(name, co, pathname, cpathname);
}

virtual PyObject* PyImport_ExecCodeModuleWithPathnames(const char* name, PyObject* co, const char* pathname, const char* cpathname) override {
return ::PyImport_ExecCodeModuleWithPathnames(name, co, pathname, cpathname);
}

virtual PyObject* PyImport_GetImporter(PyObject* path) override {
return ::PyImport_GetImporter(path);
}

virtual long PyImport_GetMagicNumber() override {
return ::PyImport_GetMagicNumber();
}

virtual const char* PyImport_GetMagicTag() override {
return ::PyImport_GetMagicTag();
}

virtual PyObject* PyImport_GetModule(PyObject* name) override {
return ::PyImport_GetModule(name);
}

virtual PyObject* PyImport_GetModuleDict() override {
return ::PyImport_GetModuleDict();
}

virtual PyObject* PyImport_Import(PyObject* name) override {
return ::PyImport_Import(name);
}

virtual int PyImport_ImportFrozenModule(const char* name) override {
return ::PyImport_ImportFrozenModule(name);
}

virtual int PyImport_ImportFrozenModuleObject(PyObject* name) override {
return ::PyImport_ImportFrozenModuleObject(name);
}

virtual PyObject* PyImport_ImportModule(const char* name) override {
return ::PyImport_ImportModule(name);
}

virtual PyObject* PyImport_ImportModuleLevel(const char* name, PyObject* globals, PyObject* locals, PyObject* fromlist, int level) override {
return ::PyImport_ImportModuleLevel(name, globals, locals, fromlist, level);
}

virtual PyObject* PyImport_ImportModuleLevelObject(PyObject* name, PyObject* globals, PyObject* locals, PyObject* fromlist, int level) override {
return ::PyImport_ImportModuleLevelObject(name, globals, locals, fromlist, level);
}

virtual PyObject* PyImport_ImportModuleNoBlock(const char* name) override {
return ::PyImport_ImportModuleNoBlock(name);
}

virtual PyObject* PyImport_ReloadModule(PyObject* m) override {
return ::PyImport_ReloadModule(m);
}

virtual PyObject* PyInstanceMethod_Function(PyObject* p0) override {
return ::PyInstanceMethod_Function(p0);
}

virtual PyObject* PyInstanceMethod_New(PyObject* p0) override {
return ::PyInstanceMethod_New(p0);
}

virtual PyObject* PyIter_Next(PyObject* p0) override {
return ::PyIter_Next(p0);
}

virtual int PyList_Append(PyObject* p0, PyObject* p1) override {
return ::PyList_Append(p0, p1);
}

virtual PyObject* PyList_AsTuple(PyObject* p0) override {
return ::PyList_AsTuple(p0);
}

virtual PyObject* PyList_GetItem(PyObject* p0, Py_ssize_t p1) override {
return ::PyList_GetItem(p0, p1);
}

virtual PyObject* PyList_GetSlice(PyObject* p0, Py_ssize_t p1, Py_ssize_t p2) override {
return ::PyList_GetSlice(p0, p1, p2);
}

virtual int PyList_Insert(PyObject* p0, Py_ssize_t p1, PyObject* p2) override {
return ::PyList_Insert(p0, p1, p2);
}

virtual PyObject* PyList_New(Py_ssize_t size) override {
return ::PyList_New(size);
}

virtual int PyList_Reverse(PyObject* p0) override {
return ::PyList_Reverse(p0);
}

virtual int PyList_SetItem(PyObject* p0, Py_ssize_t p1, PyObject* p2) override {
return ::PyList_SetItem(p0, p1, p2);
}

virtual int PyList_SetSlice(PyObject* p0, Py_ssize_t p1, Py_ssize_t p2, PyObject* p3) override {
return ::PyList_SetSlice(p0, p1, p2, p3);
}

virtual Py_ssize_t PyList_Size(PyObject* p0) override {
return ::PyList_Size(p0);
}

virtual int PyList_Sort(PyObject* p0) override {
return ::PyList_Sort(p0);
}

virtual double PyLong_AsDouble(PyObject* p0) override {
return ::PyLong_AsDouble(p0);
}

virtual long PyLong_AsLong(PyObject* p0) override {
return ::PyLong_AsLong(p0);
}

virtual long PyLong_AsLongAndOverflow(PyObject* p0, int* p1) override {
return ::PyLong_AsLongAndOverflow(p0, p1);
}

virtual long long PyLong_AsLongLong(PyObject* p0) override {
return ::PyLong_AsLongLong(p0);
}

virtual long long PyLong_AsLongLongAndOverflow(PyObject* p0, int* p1) override {
return ::PyLong_AsLongLongAndOverflow(p0, p1);
}

virtual size_t PyLong_AsSize_t(PyObject* p0) override {
return ::PyLong_AsSize_t(p0);
}

virtual Py_ssize_t PyLong_AsSsize_t(PyObject* p0) override {
return ::PyLong_AsSsize_t(p0);
}

virtual unsigned long PyLong_AsUnsignedLong(PyObject* p0) override {
return ::PyLong_AsUnsignedLong(p0);
}

virtual unsigned long long PyLong_AsUnsignedLongLong(PyObject* p0) override {
return ::PyLong_AsUnsignedLongLong(p0);
}

virtual unsigned long long PyLong_AsUnsignedLongLongMask(PyObject* p0) override {
return ::PyLong_AsUnsignedLongLongMask(p0);
}

virtual unsigned long PyLong_AsUnsignedLongMask(PyObject* p0) override {
return ::PyLong_AsUnsignedLongMask(p0);
}

virtual void* PyLong_AsVoidPtr(PyObject* p0) override {
return ::PyLong_AsVoidPtr(p0);
}

virtual PyObject* PyLong_FromDouble(double p0) override {
return ::PyLong_FromDouble(p0);
}

virtual PyObject* PyLong_FromLong(long p0) override {
return ::PyLong_FromLong(p0);
}

virtual PyObject* PyLong_FromLongLong(long long p0) override {
return ::PyLong_FromLongLong(p0);
}

virtual PyObject* PyLong_FromSize_t(size_t p0) override {
return ::PyLong_FromSize_t(p0);
}

virtual PyObject* PyLong_FromSsize_t(Py_ssize_t p0) override {
return ::PyLong_FromSsize_t(p0);
}

virtual PyObject* PyLong_FromString(const char* p0, char** p1, int p2) override {
return ::PyLong_FromString(p0, p1, p2);
}

virtual PyObject* PyLong_FromUnicodeObject(PyObject* u, int base) override {
return ::PyLong_FromUnicodeObject(u, base);
}

virtual PyObject* PyLong_FromUnsignedLong(unsigned long p0) override {
return ::PyLong_FromUnsignedLong(p0);
}

virtual PyObject* PyLong_FromUnsignedLongLong(unsigned long long p0) override {
return ::PyLong_FromUnsignedLongLong(p0);
}

virtual PyObject* PyLong_FromVoidPtr(void* p0) override {
return ::PyLong_FromVoidPtr(p0);
}

virtual PyObject* PyLong_GetInfo() override {
return ::PyLong_GetInfo();
}

virtual int PyMapping_Check(PyObject* o) override {
return ::PyMapping_Check(o);
}

virtual PyObject* PyMapping_GetItemString(PyObject* o, const char* key) override {
return ::PyMapping_GetItemString(o, key);
}

virtual int PyMapping_HasKey(PyObject* o, PyObject* key) override {
return ::PyMapping_HasKey(o, key);
}

virtual int PyMapping_HasKeyString(PyObject* o, const char* key) override {
return ::PyMapping_HasKeyString(o, key);
}

virtual PyObject* PyMapping_Items(PyObject* o) override {
return ::PyMapping_Items(o);
}

virtual PyObject* PyMapping_Keys(PyObject* o) override {
return ::PyMapping_Keys(o);
}

virtual int PyMapping_SetItemString(PyObject* o, const char* key, PyObject* value) override {
return ::PyMapping_SetItemString(o, key, value);
}

virtual Py_ssize_t PyMapping_Size(PyObject* o) override {
return ::PyMapping_Size(o);
}

virtual PyObject* PyMapping_Values(PyObject* o) override {
return ::PyMapping_Values(o);
}

virtual PyObject* PyMethod_Function(PyObject* p0) override {
return ::PyMethod_Function(p0);
}

virtual PyObject* PyMethod_New(PyObject* p0, PyObject* p1) override {
return ::PyMethod_New(p0, p1);
}

virtual PyObject* PyMethod_Self(PyObject* p0) override {
return ::PyMethod_Self(p0);
}

virtual PyObject* PyNumber_Absolute(PyObject* o) override {
return ::PyNumber_Absolute(o);
}

virtual PyObject* PyNumber_Add(PyObject* o1, PyObject* o2) override {
return ::PyNumber_Add(o1, o2);
}

virtual PyObject* PyNumber_And(PyObject* o1, PyObject* o2) override {
return ::PyNumber_And(o1, o2);
}

virtual Py_ssize_t PyNumber_AsSsize_t(PyObject* o, PyObject* exc) override {
return ::PyNumber_AsSsize_t(o, exc);
}

virtual int PyNumber_Check(PyObject* o) override {
return ::PyNumber_Check(o);
}

virtual PyObject* PyNumber_Divmod(PyObject* o1, PyObject* o2) override {
return ::PyNumber_Divmod(o1, o2);
}

virtual PyObject* PyNumber_Float(PyObject* o) override {
return ::PyNumber_Float(o);
}

virtual PyObject* PyNumber_FloorDivide(PyObject* o1, PyObject* o2) override {
return ::PyNumber_FloorDivide(o1, o2);
}

virtual PyObject* PyNumber_InPlaceAdd(PyObject* o1, PyObject* o2) override {
return ::PyNumber_InPlaceAdd(o1, o2);
}

virtual PyObject* PyNumber_InPlaceAnd(PyObject* o1, PyObject* o2) override {
return ::PyNumber_InPlaceAnd(o1, o2);
}

virtual PyObject* PyNumber_InPlaceFloorDivide(PyObject* o1, PyObject* o2) override {
return ::PyNumber_InPlaceFloorDivide(o1, o2);
}

virtual PyObject* PyNumber_InPlaceLshift(PyObject* o1, PyObject* o2) override {
return ::PyNumber_InPlaceLshift(o1, o2);
}

virtual PyObject* PyNumber_InPlaceMatrixMultiply(PyObject* o1, PyObject* o2) override {
return ::PyNumber_InPlaceMatrixMultiply(o1, o2);
}

virtual PyObject* PyNumber_InPlaceMultiply(PyObject* o1, PyObject* o2) override {
return ::PyNumber_InPlaceMultiply(o1, o2);
}

virtual PyObject* PyNumber_InPlaceOr(PyObject* o1, PyObject* o2) override {
return ::PyNumber_InPlaceOr(o1, o2);
}

virtual PyObject* PyNumber_InPlacePower(PyObject* o1, PyObject* o2, PyObject* o3) override {
return ::PyNumber_InPlacePower(o1, o2, o3);
}

virtual PyObject* PyNumber_InPlaceRemainder(PyObject* o1, PyObject* o2) override {
return ::PyNumber_InPlaceRemainder(o1, o2);
}

virtual PyObject* PyNumber_InPlaceRshift(PyObject* o1, PyObject* o2) override {
return ::PyNumber_InPlaceRshift(o1, o2);
}

virtual PyObject* PyNumber_InPlaceSubtract(PyObject* o1, PyObject* o2) override {
return ::PyNumber_InPlaceSubtract(o1, o2);
}

virtual PyObject* PyNumber_InPlaceTrueDivide(PyObject* o1, PyObject* o2) override {
return ::PyNumber_InPlaceTrueDivide(o1, o2);
}

virtual PyObject* PyNumber_InPlaceXor(PyObject* o1, PyObject* o2) override {
return ::PyNumber_InPlaceXor(o1, o2);
}

virtual PyObject* PyNumber_Index(PyObject* o) override {
return ::PyNumber_Index(o);
}

virtual PyObject* PyNumber_Invert(PyObject* o) override {
return ::PyNumber_Invert(o);
}

virtual PyObject* PyNumber_Long(PyObject* o) override {
return ::PyNumber_Long(o);
}

virtual PyObject* PyNumber_Lshift(PyObject* o1, PyObject* o2) override {
return ::PyNumber_Lshift(o1, o2);
}

virtual PyObject* PyNumber_MatrixMultiply(PyObject* o1, PyObject* o2) override {
return ::PyNumber_MatrixMultiply(o1, o2);
}

virtual PyObject* PyNumber_Multiply(PyObject* o1, PyObject* o2) override {
return ::PyNumber_Multiply(o1, o2);
}

virtual PyObject* PyNumber_Negative(PyObject* o) override {
return ::PyNumber_Negative(o);
}

virtual PyObject* PyNumber_Or(PyObject* o1, PyObject* o2) override {
return ::PyNumber_Or(o1, o2);
}

virtual PyObject* PyNumber_Positive(PyObject* o) override {
return ::PyNumber_Positive(o);
}

virtual PyObject* PyNumber_Power(PyObject* o1, PyObject* o2, PyObject* o3) override {
return ::PyNumber_Power(o1, o2, o3);
}

virtual PyObject* PyNumber_Remainder(PyObject* o1, PyObject* o2) override {
return ::PyNumber_Remainder(o1, o2);
}

virtual PyObject* PyNumber_Rshift(PyObject* o1, PyObject* o2) override {
return ::PyNumber_Rshift(o1, o2);
}

virtual PyObject* PyNumber_Subtract(PyObject* o1, PyObject* o2) override {
return ::PyNumber_Subtract(o1, o2);
}

virtual PyObject* PyNumber_ToBase(PyObject* n, int base) override {
return ::PyNumber_ToBase(n, base);
}

virtual PyObject* PyNumber_TrueDivide(PyObject* o1, PyObject* o2) override {
return ::PyNumber_TrueDivide(o1, o2);
}

virtual PyObject* PyNumber_Xor(PyObject* o1, PyObject* o2) override {
return ::PyNumber_Xor(o1, o2);
}

virtual int PyODict_DelItem(PyObject* od, PyObject* key) override {
return ::PyODict_DelItem(od, key);
}

virtual PyObject* PyODict_New() override {
return ::PyODict_New();
}

virtual int PyODict_SetItem(PyObject* od, PyObject* key, PyObject* item) override {
return ::PyODict_SetItem(od, key, item);
}

virtual void PyOS_AfterFork_Child() override {
return ::PyOS_AfterFork_Child();
}

virtual void PyOS_AfterFork_Parent() override {
return ::PyOS_AfterFork_Parent();
}

virtual void PyOS_BeforeFork() override {
return ::PyOS_BeforeFork();
}

virtual PyObject* PyOS_FSPath(PyObject* path) override {
return ::PyOS_FSPath(path);
}

virtual int PyOS_InterruptOccurred() override {
return ::PyOS_InterruptOccurred();
}

virtual char* PyOS_Readline(FILE* p0, FILE* p1, const char* p2) override {
return ::PyOS_Readline(p0, p1, p2);
}

virtual char* PyOS_double_to_string(double val, char format_code, int precision, int flags, int* type) override {
return ::PyOS_double_to_string(val, format_code, precision, flags, type);
}

virtual int PyOS_mystricmp(const char* p0, const char* p1) override {
return ::PyOS_mystricmp(p0, p1);
}

virtual int PyOS_mystrnicmp(const char* p0, const char* p1, Py_ssize_t p2) override {
return ::PyOS_mystrnicmp(p0, p1, p2);
}

virtual double PyOS_string_to_double(const char* str, char** endptr, PyObject* overflow_exception) override {
return ::PyOS_string_to_double(str, endptr, overflow_exception);
}

virtual long PyOS_strtol(const char* p0, char** p1, int p2) override {
return ::PyOS_strtol(p0, p1, p2);
}

virtual unsigned long PyOS_strtoul(const char* p0, char** p1, int p2) override {
return ::PyOS_strtoul(p0, p1, p2);
}

virtual int PyOS_vsnprintf(char* str, size_t size, const char* format, va_list va) override {
return ::PyOS_vsnprintf(str, size, format, va);
}

virtual PyObject* PyObject_ASCII(PyObject* p0) override {
return ::PyObject_ASCII(p0);
}

virtual int PyObject_AsFileDescriptor(PyObject* p0) override {
return ::PyObject_AsFileDescriptor(p0);
}

virtual PyObject* PyObject_Bytes(PyObject* p0) override {
return ::PyObject_Bytes(p0);
}

virtual PyObject* PyObject_Call(PyObject* callable, PyObject* args, PyObject* kwargs) override {
return ::PyObject_Call(callable, args, kwargs);
}

virtual void PyObject_CallFinalizer(PyObject* p0) override {
return ::PyObject_CallFinalizer(p0);
}

virtual int PyObject_CallFinalizerFromDealloc(PyObject* p0) override {
return ::PyObject_CallFinalizerFromDealloc(p0);
}

virtual PyObject* PyObject_CallMethodNoArgs(PyObject* self, PyObject* name) override {
return ::PyObject_CallMethodNoArgs(self, name);
}

virtual PyObject* PyObject_CallMethodOneArg(PyObject* self, PyObject* name, PyObject* arg) override {
return ::PyObject_CallMethodOneArg(self, name, arg);
}

virtual PyObject* PyObject_CallNoArgs(PyObject* func) override {
return ::PyObject_CallNoArgs(func);
}

virtual PyObject* PyObject_CallObject(PyObject* callable, PyObject* args) override {
return ::PyObject_CallObject(callable, args);
}

virtual PyObject* PyObject_CallOneArg(PyObject* func, PyObject* arg) override {
return ::PyObject_CallOneArg(func, arg);
}

virtual void* PyObject_Calloc(size_t nelem, size_t elsize) override {
return ::PyObject_Calloc(nelem, elsize);
}

virtual int PyObject_CheckBuffer(PyObject* obj) override {
return ::PyObject_CheckBuffer(obj);
}

virtual void PyObject_ClearWeakRefs(PyObject* p0) override {
return ::PyObject_ClearWeakRefs(p0);
}

virtual int PyObject_CopyData(PyObject* dest, PyObject* src) override {
return ::PyObject_CopyData(dest, src);
}

virtual int PyObject_DelItem(PyObject* o, PyObject* key) override {
return ::PyObject_DelItem(o, key);
}

virtual int PyObject_DelItemString(PyObject* o, const char* key) override {
return ::PyObject_DelItemString(o, key);
}

virtual PyObject* PyObject_Dir(PyObject* p0) override {
return ::PyObject_Dir(p0);
}

virtual PyObject* PyObject_Format(PyObject* obj, PyObject* format_spec) override {
return ::PyObject_Format(obj, format_spec);
}

virtual void PyObject_Free(void* ptr) override {
return ::PyObject_Free(ptr);
}

virtual void PyObject_GC_Del(void* p0) override {
return ::PyObject_GC_Del(p0);
}

virtual int PyObject_GC_IsFinalized(PyObject* p0) override {
return ::PyObject_GC_IsFinalized(p0);
}

virtual int PyObject_GC_IsTracked(PyObject* p0) override {
return ::PyObject_GC_IsTracked(p0);
}

virtual void PyObject_GC_Track(void* p0) override {
return ::PyObject_GC_Track(p0);
}

virtual void PyObject_GC_UnTrack(void* p0) override {
return ::PyObject_GC_UnTrack(p0);
}

virtual PyObject** PyObject_GET_WEAKREFS_LISTPTR(PyObject* op) override {
return ::PyObject_GET_WEAKREFS_LISTPTR(op);
}

virtual PyObject* PyObject_GenericGetAttr(PyObject* p0, PyObject* p1) override {
return ::PyObject_GenericGetAttr(p0, p1);
}

virtual PyObject* PyObject_GenericGetDict(PyObject* p0, void* p1) override {
return ::PyObject_GenericGetDict(p0, p1);
}

virtual int PyObject_GenericSetAttr(PyObject* p0, PyObject* p1, PyObject* p2) override {
return ::PyObject_GenericSetAttr(p0, p1, p2);
}

virtual int PyObject_GenericSetDict(PyObject* p0, PyObject* p1, void* p2) override {
return ::PyObject_GenericSetDict(p0, p1, p2);
}

virtual PyObject* PyObject_GetAIter(PyObject* p0) override {
return ::PyObject_GetAIter(p0);
}

virtual PyObject* PyObject_GetAttr(PyObject* p0, PyObject* p1) override {
return ::PyObject_GetAttr(p0, p1);
}

virtual PyObject* PyObject_GetAttrString(PyObject* p0, const char* p1) override {
return ::PyObject_GetAttrString(p0, p1);
}

virtual PyObject* PyObject_GetItem(PyObject* o, PyObject* key) override {
return ::PyObject_GetItem(o, key);
}

virtual void* PyObject_GetItemData(PyObject* obj) override {
return ::PyObject_GetItemData(obj);
}

virtual PyObject* PyObject_GetIter(PyObject* p0) override {
return ::PyObject_GetIter(p0);
}

virtual void* PyObject_GetTypeData(PyObject* obj, PyTypeObject* cls) override {
return ::PyObject_GetTypeData(obj, cls);
}

virtual int PyObject_HasAttr(PyObject* p0, PyObject* p1) override {
return ::PyObject_HasAttr(p0, p1);
}

virtual int PyObject_HasAttrString(PyObject* p0, const char* p1) override {
return ::PyObject_HasAttrString(p0, p1);
}

virtual int PyObject_IS_GC(PyObject* obj) override {
return ::PyObject_IS_GC(obj);
}

virtual PyObject* PyObject_Init(PyObject* p0, PyTypeObject* p1) override {
return ::PyObject_Init(p0, p1);
}

virtual int PyObject_IsInstance(PyObject* object, PyObject* typeorclass) override {
return ::PyObject_IsInstance(object, typeorclass);
}

virtual int PyObject_IsSubclass(PyObject* object, PyObject* typeorclass) override {
return ::PyObject_IsSubclass(object, typeorclass);
}

virtual int PyObject_IsTrue(PyObject* p0) override {
return ::PyObject_IsTrue(p0);
}

virtual Py_ssize_t PyObject_LengthHint(PyObject* o, Py_ssize_t p1) override {
return ::PyObject_LengthHint(o, p1);
}

virtual void* PyObject_Malloc(size_t size) override {
return ::PyObject_Malloc(size);
}

virtual int PyObject_Not(PyObject* p0) override {
return ::PyObject_Not(p0);
}

virtual int PyObject_Print(PyObject* p0, FILE* p1, int p2) override {
return ::PyObject_Print(p0, p1, p2);
}

virtual void* PyObject_Realloc(void* ptr, size_t new_size) override {
return ::PyObject_Realloc(ptr, new_size);
}

virtual PyObject* PyObject_Repr(PyObject* p0) override {
return ::PyObject_Repr(p0);
}

virtual PyObject* PyObject_RichCompare(PyObject* p0, PyObject* p1, int p2) override {
return ::PyObject_RichCompare(p0, p1, p2);
}

virtual int PyObject_RichCompareBool(PyObject* p0, PyObject* p1, int p2) override {
return ::PyObject_RichCompareBool(p0, p1, p2);
}

virtual PyObject* PyObject_SelfIter(PyObject* p0) override {
return ::PyObject_SelfIter(p0);
}

virtual int PyObject_SetAttr(PyObject* p0, PyObject* p1, PyObject* p2) override {
return ::PyObject_SetAttr(p0, p1, p2);
}

virtual int PyObject_SetAttrString(PyObject* p0, const char* p1, PyObject* p2) override {
return ::PyObject_SetAttrString(p0, p1, p2);
}

virtual int PyObject_SetItem(PyObject* o, PyObject* key, PyObject* v) override {
return ::PyObject_SetItem(o, key, v);
}

virtual Py_ssize_t PyObject_Size(PyObject* o) override {
return ::PyObject_Size(o);
}

virtual PyObject* PyObject_Str(PyObject* p0) override {
return ::PyObject_Str(p0);
}

virtual PyObject* PyObject_Type(PyObject* o) override {
return ::PyObject_Type(o);
}

virtual PyObject* PyObject_Vectorcall(PyObject* callable, PyObject* const* args, size_t nargsf, PyObject* kwnames) override {
return ::PyObject_Vectorcall(callable, args, nargsf, kwnames);
}

virtual PyObject* PyObject_VectorcallDict(PyObject* callable, PyObject* const* args, size_t nargsf, PyObject* kwargs) override {
return ::PyObject_VectorcallDict(callable, args, nargsf, kwargs);
}

virtual PyObject* PyObject_VectorcallMethod(PyObject* name, PyObject* const* args, size_t nargsf, PyObject* kwnames) override {
return ::PyObject_VectorcallMethod(name, args, nargsf, kwnames);
}

virtual PyObject* PySeqIter_New(PyObject* p0) override {
return ::PySeqIter_New(p0);
}

virtual int PySequence_Check(PyObject* o) override {
return ::PySequence_Check(o);
}

virtual PyObject* PySequence_Concat(PyObject* o1, PyObject* o2) override {
return ::PySequence_Concat(o1, o2);
}

virtual int PySequence_Contains(PyObject* seq, PyObject* ob) override {
return ::PySequence_Contains(seq, ob);
}

virtual Py_ssize_t PySequence_Count(PyObject* o, PyObject* value) override {
return ::PySequence_Count(o, value);
}

virtual int PySequence_DelItem(PyObject* o, Py_ssize_t i) override {
return ::PySequence_DelItem(o, i);
}

virtual int PySequence_DelSlice(PyObject* o, Py_ssize_t i1, Py_ssize_t i2) override {
return ::PySequence_DelSlice(o, i1, i2);
}

virtual PyObject* PySequence_Fast(PyObject* o, const char* m) override {
return ::PySequence_Fast(o, m);
}

virtual PyObject* PySequence_GetItem(PyObject* o, Py_ssize_t i) override {
return ::PySequence_GetItem(o, i);
}

virtual PyObject* PySequence_GetSlice(PyObject* o, Py_ssize_t i1, Py_ssize_t i2) override {
return ::PySequence_GetSlice(o, i1, i2);
}

virtual PyObject* PySequence_InPlaceConcat(PyObject* o1, PyObject* o2) override {
return ::PySequence_InPlaceConcat(o1, o2);
}

virtual PyObject* PySequence_InPlaceRepeat(PyObject* o, Py_ssize_t count) override {
return ::PySequence_InPlaceRepeat(o, count);
}

virtual Py_ssize_t PySequence_Index(PyObject* o, PyObject* value) override {
return ::PySequence_Index(o, value);
}

virtual PyObject* PySequence_List(PyObject* o) override {
return ::PySequence_List(o);
}

virtual PyObject* PySequence_Repeat(PyObject* o, Py_ssize_t count) override {
return ::PySequence_Repeat(o, count);
}

virtual int PySequence_SetItem(PyObject* o, Py_ssize_t i, PyObject* v) override {
return ::PySequence_SetItem(o, i, v);
}

virtual int PySequence_SetSlice(PyObject* o, Py_ssize_t i1, Py_ssize_t i2, PyObject* v) override {
return ::PySequence_SetSlice(o, i1, i2, v);
}

virtual Py_ssize_t PySequence_Size(PyObject* o) override {
return ::PySequence_Size(o);
}

virtual PyObject* PySequence_Tuple(PyObject* o) override {
return ::PySequence_Tuple(o);
}

virtual int PySet_Add(PyObject* set, PyObject* key) override {
return ::PySet_Add(set, key);
}

virtual int PySet_Clear(PyObject* set) override {
return ::PySet_Clear(set);
}

virtual int PySet_Contains(PyObject* anyset, PyObject* key) override {
return ::PySet_Contains(anyset, key);
}

virtual int PySet_Discard(PyObject* set, PyObject* key) override {
return ::PySet_Discard(set, key);
}

virtual PyObject* PySet_New(PyObject* p0) override {
return ::PySet_New(p0);
}

virtual PyObject* PySet_Pop(PyObject* set) override {
return ::PySet_Pop(set);
}

virtual Py_ssize_t PySet_Size(PyObject* anyset) override {
return ::PySet_Size(anyset);
}

virtual Py_ssize_t PySlice_AdjustIndices(Py_ssize_t length, Py_ssize_t* start, Py_ssize_t* stop, Py_ssize_t step) override {
return ::PySlice_AdjustIndices(length, start, stop, step);
}

virtual int PySlice_GetIndices(PyObject* r, Py_ssize_t length, Py_ssize_t* start, Py_ssize_t* stop, Py_ssize_t* step) override {
return ::PySlice_GetIndices(r, length, start, stop, step);
}

virtual PyObject* PySlice_New(PyObject* start, PyObject* stop, PyObject* step) override {
return ::PySlice_New(start, stop, step);
}

virtual int PySlice_Unpack(PyObject* slice, Py_ssize_t* start, Py_ssize_t* stop, Py_ssize_t* step) override {
return ::PySlice_Unpack(slice, start, stop, step);
}

virtual PyObject* PyStaticMethod_New(PyObject* p0) override {
return ::PyStaticMethod_New(p0);
}

virtual PyObject* PyTuple_GetItem(PyObject* p0, Py_ssize_t p1) override {
return ::PyTuple_GetItem(p0, p1);
}

virtual PyObject* PyTuple_GetSlice(PyObject* p0, Py_ssize_t p1, Py_ssize_t p2) override {
return ::PyTuple_GetSlice(p0, p1, p2);
}

virtual PyObject* PyTuple_New(Py_ssize_t size) override {
return ::PyTuple_New(size);
}

virtual int PyTuple_SetItem(PyObject* p0, Py_ssize_t p1, PyObject* p2) override {
return ::PyTuple_SetItem(p0, p1, p2);
}

virtual Py_ssize_t PyTuple_Size(PyObject* p0) override {
return ::PyTuple_Size(p0);
}

virtual unsigned int PyType_ClearCache() override {
return ::PyType_ClearCache();
}

virtual int PyType_ClearWatcher(int watcher_id) override {
return ::PyType_ClearWatcher(watcher_id);
}

virtual PyObject* PyType_GenericAlloc(PyTypeObject* p0, Py_ssize_t p1) override {
return ::PyType_GenericAlloc(p0, p1);
}

virtual PyObject* PyType_GenericNew(PyTypeObject* p0, PyObject* p1, PyObject* p2) override {
return ::PyType_GenericNew(p0, p1, p2);
}

virtual PyObject* PyType_GetDict(PyTypeObject* p0) override {
return ::PyType_GetDict(p0);
}

virtual unsigned long PyType_GetFlags(PyTypeObject* p0) override {
return ::PyType_GetFlags(p0);
}

virtual PyObject* PyType_GetModule(PyTypeObject* p0) override {
return ::PyType_GetModule(p0);
}

virtual void* PyType_GetModuleState(PyTypeObject* p0) override {
return ::PyType_GetModuleState(p0);
}

virtual PyObject* PyType_GetName(PyTypeObject* p0) override {
return ::PyType_GetName(p0);
}

virtual PyObject* PyType_GetQualName(PyTypeObject* p0) override {
return ::PyType_GetQualName(p0);
}

virtual void* PyType_GetSlot(PyTypeObject* p0, int p1) override {
return ::PyType_GetSlot(p0, p1);
}

virtual Py_ssize_t PyType_GetTypeDataSize(PyTypeObject* cls) override {
return ::PyType_GetTypeDataSize(cls);
}

virtual int PyType_HasFeature(PyTypeObject* type, unsigned long feature) override {
return ::PyType_HasFeature(type, feature);
}

virtual int PyType_IsSubtype(PyTypeObject* p0, PyTypeObject* p1) override {
return ::PyType_IsSubtype(p0, p1);
}

virtual void PyType_Modified(PyTypeObject* p0) override {
return ::PyType_Modified(p0);
}

virtual int PyType_Ready(PyTypeObject* p0) override {
return ::PyType_Ready(p0);
}

virtual int PyType_SUPPORTS_WEAKREFS(PyTypeObject* type) override {
return ::PyType_SUPPORTS_WEAKREFS(type);
}

virtual int PyType_Unwatch(int watcher_id, PyObject* type) override {
return ::PyType_Unwatch(watcher_id, type);
}

virtual int PyType_Watch(int watcher_id, PyObject* type) override {
return ::PyType_Watch(watcher_id, type);
}

virtual PyObject* PyUnicodeDecodeError_Create(const char* encoding, const char* object, Py_ssize_t length, Py_ssize_t start, Py_ssize_t end, const char* reason) override {
return ::PyUnicodeDecodeError_Create(encoding, object, length, start, end, reason);
}

virtual PyObject* PyUnicodeDecodeError_GetEncoding(PyObject* p0) override {
return ::PyUnicodeDecodeError_GetEncoding(p0);
}

virtual int PyUnicodeDecodeError_GetEnd(PyObject* p0, Py_ssize_t* p1) override {
return ::PyUnicodeDecodeError_GetEnd(p0, p1);
}

virtual PyObject* PyUnicodeDecodeError_GetObject(PyObject* p0) override {
return ::PyUnicodeDecodeError_GetObject(p0);
}

virtual PyObject* PyUnicodeDecodeError_GetReason(PyObject* p0) override {
return ::PyUnicodeDecodeError_GetReason(p0);
}

virtual int PyUnicodeDecodeError_GetStart(PyObject* p0, Py_ssize_t* p1) override {
return ::PyUnicodeDecodeError_GetStart(p0, p1);
}

virtual int PyUnicodeDecodeError_SetEnd(PyObject* p0, Py_ssize_t p1) override {
return ::PyUnicodeDecodeError_SetEnd(p0, p1);
}

virtual int PyUnicodeDecodeError_SetReason(PyObject* exc, const char* reason) override {
return ::PyUnicodeDecodeError_SetReason(exc, reason);
}

virtual int PyUnicodeDecodeError_SetStart(PyObject* p0, Py_ssize_t p1) override {
return ::PyUnicodeDecodeError_SetStart(p0, p1);
}

virtual PyObject* PyUnicodeEncodeError_GetEncoding(PyObject* p0) override {
return ::PyUnicodeEncodeError_GetEncoding(p0);
}

virtual int PyUnicodeEncodeError_GetEnd(PyObject* p0, Py_ssize_t* p1) override {
return ::PyUnicodeEncodeError_GetEnd(p0, p1);
}

virtual PyObject* PyUnicodeEncodeError_GetObject(PyObject* p0) override {
return ::PyUnicodeEncodeError_GetObject(p0);
}

virtual PyObject* PyUnicodeEncodeError_GetReason(PyObject* p0) override {
return ::PyUnicodeEncodeError_GetReason(p0);
}

virtual int PyUnicodeEncodeError_GetStart(PyObject* p0, Py_ssize_t* p1) override {
return ::PyUnicodeEncodeError_GetStart(p0, p1);
}

virtual int PyUnicodeEncodeError_SetEnd(PyObject* p0, Py_ssize_t p1) override {
return ::PyUnicodeEncodeError_SetEnd(p0, p1);
}

virtual int PyUnicodeEncodeError_SetReason(PyObject* exc, const char* reason) override {
return ::PyUnicodeEncodeError_SetReason(exc, reason);
}

virtual int PyUnicodeEncodeError_SetStart(PyObject* p0, Py_ssize_t p1) override {
return ::PyUnicodeEncodeError_SetStart(p0, p1);
}

virtual int PyUnicodeTranslateError_GetEnd(PyObject* p0, Py_ssize_t* p1) override {
return ::PyUnicodeTranslateError_GetEnd(p0, p1);
}

virtual PyObject* PyUnicodeTranslateError_GetObject(PyObject* p0) override {
return ::PyUnicodeTranslateError_GetObject(p0);
}

virtual PyObject* PyUnicodeTranslateError_GetReason(PyObject* p0) override {
return ::PyUnicodeTranslateError_GetReason(p0);
}

virtual int PyUnicodeTranslateError_GetStart(PyObject* p0, Py_ssize_t* p1) override {
return ::PyUnicodeTranslateError_GetStart(p0, p1);
}

virtual int PyUnicodeTranslateError_SetEnd(PyObject* p0, Py_ssize_t p1) override {
return ::PyUnicodeTranslateError_SetEnd(p0, p1);
}

virtual int PyUnicodeTranslateError_SetReason(PyObject* exc, const char* reason) override {
return ::PyUnicodeTranslateError_SetReason(exc, reason);
}

virtual int PyUnicodeTranslateError_SetStart(PyObject* p0, Py_ssize_t p1) override {
return ::PyUnicodeTranslateError_SetStart(p0, p1);
}

virtual PyObject* PyVectorcall_Call(PyObject* callable, PyObject* tuple, PyObject* dict) override {
return ::PyVectorcall_Call(callable, tuple, dict);
}

virtual PyObject* PyWrapper_New(PyObject* p0, PyObject* p1) override {
return ::PyWrapper_New(p0, p1);
}

virtual int Py_BytesMain(int argc, char** argv) override {
return ::Py_BytesMain(argc, argv);
}

virtual void Py_DecRef(PyObject* p0) override {
return ::Py_DecRef(p0);
}

virtual wchar_t* Py_DecodeLocale(const char* arg, size_t* size) override {
return ::Py_DecodeLocale(arg, size);
}

virtual char* Py_EncodeLocale(const wchar_t* text, size_t* error_pos) override {
return ::Py_EncodeLocale(text, error_pos);
}

virtual int Py_EnterRecursiveCall(const char* where) override {
return ::Py_EnterRecursiveCall(where);
}

virtual int Py_FdIsInteractive(FILE* p0, const char* p1) override {
return ::Py_FdIsInteractive(p0, p1);
}

virtual void Py_Finalize() override {
return ::Py_Finalize();
}

virtual int Py_FinalizeEx() override {
return ::Py_FinalizeEx();
}

virtual char* Py_GETENV(const char* name) override {
return ::Py_GETENV(name);
}

virtual PyObject* Py_GenericAlias(PyObject* p0, PyObject* p1) override {
return ::Py_GenericAlias(p0, p1);
}

virtual const char* Py_GetBuildInfo() override {
return ::Py_GetBuildInfo();
}

virtual const char* Py_GetCompiler() override {
return ::Py_GetCompiler();
}

virtual const char* Py_GetCopyright() override {
return ::Py_GetCopyright();
}

virtual wchar_t* Py_GetExecPrefix() override {
return ::Py_GetExecPrefix();
}

virtual wchar_t* Py_GetPath() override {
return ::Py_GetPath();
}

virtual const char* Py_GetPlatform() override {
return ::Py_GetPlatform();
}

virtual wchar_t* Py_GetPrefix() override {
return ::Py_GetPrefix();
}

virtual wchar_t* Py_GetProgramFullPath() override {
return ::Py_GetProgramFullPath();
}

virtual wchar_t* Py_GetProgramName() override {
return ::Py_GetProgramName();
}

virtual wchar_t* Py_GetPythonHome() override {
return ::Py_GetPythonHome();
}

virtual int Py_GetRecursionLimit() override {
return ::Py_GetRecursionLimit();
}

virtual const char* Py_GetVersion() override {
return ::Py_GetVersion();
}

virtual void Py_IncRef(PyObject* p0) override {
return ::Py_IncRef(p0);
}

virtual void Py_Initialize() override {
return ::Py_Initialize();
}

virtual void Py_InitializeEx(int p0) override {
return ::Py_InitializeEx(p0);
}

virtual int Py_IsInitialized() override {
return ::Py_IsInitialized();
}

virtual void Py_LeaveRecursiveCall() override {
return ::Py_LeaveRecursiveCall();
}

virtual int Py_MakePendingCalls() override {
return ::Py_MakePendingCalls();
}

virtual int Py_ReprEnter(PyObject* p0) override {
return ::Py_ReprEnter(p0);
}

virtual void Py_ReprLeave(PyObject* p0) override {
return ::Py_ReprLeave(p0);
}

virtual int Py_RunMain() override {
return ::Py_RunMain();
}

virtual void Py_SetRecursionLimit(int p0) override {
return ::Py_SetRecursionLimit(p0);
}

virtual char* Py_UniversalNewlineFgets(char* p0, int p1, FILE* p2, PyObject* p3) override {
return ::Py_UniversalNewlineFgets(p0, p1, p2, p3);
}

virtual PyObject* Py_VaBuildValue(const char* p0, va_list p1) override {
return ::Py_VaBuildValue(p0, p1);
}
};

} // namespace pyapi
