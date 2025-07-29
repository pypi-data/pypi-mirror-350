/*
 *  Copyright (C) GridGain Systems. All Rights Reserved.
 *  _________        _____ __________________        _____
 *  __  ____/___________(_)______  /__  ____/______ ____(_)_______
 *  _  / __  __  ___/__  / _  __  / _  / __  _  __ `/__  / __  __ \
 *  / /_/ /  _  /    _  /  / /_/ /  / /_/ /  / /_/ / _  /  _  / / /
 *  \____/   /_/     /_/   \_,__/   \____/   \__,_/  /_/   /_/ /_/
 */

#pragma once

#include "ignite/odbc/diagnostic/diagnosable.h"

#include <string>

namespace ignite {

/** SSL Mode enum. */
enum class ssl_mode {
    DISABLE = 0,

    REQUIRE = 1,

    UNKNOWN = 100
};

/**
 * Convert mode from string.
 *
 * @param val String value.
 * @param dflt Default value to return on error.
 * @return Corresponding enum value.
 */
[[nodiscard]] ssl_mode ssl_mode_from_string(const std::string &val, ssl_mode dflt = ssl_mode::UNKNOWN);

/**
 * Convert mode to string.
 *
 * @param val Value to convert.
 * @return String value.
 */
[[nodiscard]] std::string to_string(ssl_mode val);

} // namespace ignite
