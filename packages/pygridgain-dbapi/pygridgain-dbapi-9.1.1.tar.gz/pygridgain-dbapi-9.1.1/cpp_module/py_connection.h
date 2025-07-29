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

#define PY_CONNECTION_CLASS_NAME "PyConnection"

namespace ignite {
class sql_environment;
class sql_connection;
}

/**
 * Connection Python object.
 */
struct py_connection {
    PyObject_HEAD

    /** Environment. */
    ignite::sql_environment *m_environment;

    /** Connection. */
    ignite::sql_connection *m_connection;
};

/**
 * Connection init function.
 */
int py_connection_init(py_connection *self, PyObject *args, PyObject *kwds);

/**
 * Connection dealloc function.
 */
void py_connection_dealloc(py_connection *self);

/**
 * Create a new instance of py_connection python class.
 *
 * @param env Environment.
 * @param conn Connection.
 * @return A new class instance.
 */
py_connection* make_py_connection(std::unique_ptr<ignite::sql_environment> env,
    std::unique_ptr<ignite::sql_connection> conn);

/**
 * Prepare PyConnection type for registration.
 */
int prepare_py_connection_type();

/**
 * Register PyConnection type within module.
 */
int register_py_connection_type(PyObject* mod);