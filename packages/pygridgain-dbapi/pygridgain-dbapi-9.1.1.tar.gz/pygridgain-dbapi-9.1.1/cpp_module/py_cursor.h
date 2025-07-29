/*
 * Copyright (C) GridGain Systems. All Rights Reserved.
 *  _________        _____ __________________        _____
 *  __  ____/___________(_)______  /__  ____/______ ____(_)_______
 *  _  / __  __  ___/__  / _  __  / _  / __  _  __ `/__  / __  __ \
 *  / /_/ /  _  /    _  /  / /_/ /  / /_/ /  / /_/ / _  /  _  / / /
 *  \____/   /_/     /_/   \_,__/   \____/   \__,_/  /_/   /_/ /_/
 */


#pragma once

#include <memory>

#include <Python.h>

#define PY_CURSOR_CLASS_NAME "PyCursor"

namespace ignite {
class sql_statement;
}

/**
 * Cursor Python object.
 */
struct py_cursor {
    PyObject_HEAD

    /** Statement. */
    ignite::sql_statement *m_statement;
};

/**
 * Connection init function.
 */
int py_cursor_init(py_cursor *self, PyObject *args, PyObject *kwds);

/**
 * Connection dealloc function.
 */
void py_cursor_dealloc(py_cursor *self);

/**
 * Create a new instance of py_cursor python class.
 *
 * @param stmt Statement.
 * @return A new class instance.
 */
py_cursor* make_py_cursor(std::unique_ptr<ignite::sql_statement> stmt);

/**
 * Prepare PyCursor type for registration.
 */
int prepare_py_cursor_type();

/**
 * Register PyCursor type within module.
 */
int register_py_cursor_type(PyObject* mod);
